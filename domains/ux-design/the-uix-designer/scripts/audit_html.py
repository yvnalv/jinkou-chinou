#!/usr/bin/env python3
"""Static accessibility and UX lint for HTML files (prototypes, templates, built pages).

Checks what can be decided from markup and inline CSS alone, mapped to WCAG 2.2
where applicable: document language and title, zoom blocking, image
alternatives, form labels and autocomplete, accessible names of buttons and
links, vague link text, duplicate IDs and broken ID references, focusability
of custom controls, aria-hidden on focusable content, heading structure,
landmarks, iframe titles, autoplaying media, data-table headers, removed focus
outlines, reduced-motion support, tiny text, and submit-by-default buttons.

It cannot judge colour contrast through the cascade, visual focus order,
target sizes, reflow, or real screen-reader output; do those checks in a
browser (and with design_tokens.py contrast for token pairs).

Examples:
  python audit_html.py design/prototype/index.html
  python audit_html.py design/prototype/ --json --out design/audit.json
  python audit_html.py page.html --fail-on warn

Exit code: 1 when findings at or above --fail-on (default: error) exist.
Standard library only.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
NON_LABELLED_INPUTS = {"hidden", "submit", "reset", "button", "image"}
INTERACTIVE_ROLES = {"button", "link", "checkbox", "radio", "switch", "tab", "menuitem", "menuitemcheckbox",
                     "menuitemradio", "option", "slider", "spinbutton", "textbox", "combobox", "treeitem"}
NATIVE_FOCUSABLE = {"button", "select", "textarea", "summary", "iframe"}
VAGUE_LINK_TEXT = {"click here", "here", "read more", "more", "learn more", "link", "this link", "details",
                   "continue", "go", "click", "this", "info"}
GENERIC_ALT = {"image", "img", "photo", "picture", "graphic", "icon", "pic", "spacer", "untitled"}
AUTOCOMPLETE_HINTS = re.compile(r"(e-?mail|phone|tel|mobile|first.?name|last.?name|full.?name|given|family|"
                                r"address|street|city|postal|zip|country|username|password|cc-?|card)", re.I)
SEVERITY_RANK = {"error": 0, "warn": 1}


class Node:
    def __init__(self, tag: str, attrs: dict[str, str], line: int, parent: "Node | None"):
        self.tag = tag
        self.attrs = attrs
        self.line = line
        self.parent = parent
        self.children: list["Node | str"] = []

    def get(self, name: str, default: str | None = None) -> str | None:
        return self.attrs.get(name, default)

    def iter(self):
        yield self
        for child in self.children:
            if isinstance(child, Node):
                yield from child.iter()

    def ancestors(self):
        node = self.parent
        while node is not None:
            yield node
            node = node.parent


class TreeBuilder(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.root = Node("#document", {}, 1, None)
        self.stack = [self.root]
        self.styles: list[tuple[int, str]] = []

    def handle_starttag(self, tag, attrs):
        node = Node(tag, {k: (v if v is not None else "") for k, v in attrs}, self.getpos()[0], self.stack[-1])
        self.stack[-1].children.append(node)
        if tag not in VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        node = Node(tag, {k: (v if v is not None else "") for k, v in attrs}, self.getpos()[0], self.stack[-1])
        self.stack[-1].children.append(node)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                break

    def handle_data(self, data):
        current = self.stack[-1]
        current.children.append(data)
        if current.tag == "style":
            self.styles.append((current.line, data))


# ---------------------------------------------------------------------------
# Accessible-name helpers
# ---------------------------------------------------------------------------

def is_hidden(node: Node) -> bool:
    return any(n.get("aria-hidden") == "true" or "hidden" in n.attrs for n in [node, *node.ancestors()])


def text_content(node: Node) -> str:
    parts = []
    for child in node.children:
        if isinstance(child, str):
            parts.append(child)
        elif child.tag in ("script", "style", "template") or child.get("aria-hidden") == "true":
            continue
        elif child.tag == "img":
            parts.append(child.get("alt", "") or "")
        elif child.tag == "svg":
            titles = [t for t in child.iter() if t.tag == "title"]
            parts.append(child.get("aria-label", "") or (text_content(titles[0]) if titles else ""))
        else:
            parts.append(text_content(child))
    return re.sub(r"\s+", " ", " ".join(parts)).strip()


def accessible_name(node: Node, ids: dict[str, Node]) -> str:
    labelledby = node.get("aria-labelledby")
    if labelledby:
        name = " ".join(text_content(ids[i]) for i in labelledby.split() if i in ids).strip()
        if name:
            return name
    if (node.get("aria-label") or "").strip():
        return node.get("aria-label").strip()
    if node.tag == "img":
        return (node.get("alt") or "").strip()
    if node.tag == "input" and node.get("type", "text").lower() in ("submit", "reset", "button"):
        value = (node.get("value") or "").strip()
        return value or ({"submit": "Submit", "reset": "Reset"}.get(node.get("type", "").lower(), ""))
    if node.tag == "input" and node.get("type", "").lower() == "image":
        return (node.get("alt") or "").strip()
    content = text_content(node)
    return content or (node.get("title") or "").strip()


def control_label(node: Node, ids: dict[str, Node], labels_for: dict[str, list[Node]]) -> str:
    for attr in ("aria-labelledby",):
        if node.get(attr):
            name = " ".join(text_content(ids[i]) for i in node.get(attr).split() if i in ids).strip()
            if name:
                return name
    if (node.get("aria-label") or "").strip():
        return node.get("aria-label").strip()
    node_id = node.get("id")
    if node_id and node_id in labels_for:
        name = " ".join(text_content(label) for label in labels_for[node_id]).strip()
        if name:
            return name
    for ancestor in node.ancestors():
        if ancestor.tag == "label":
            return text_content(ancestor)
    return (node.get("title") or "").strip()


def is_focusable(node: Node) -> bool:
    if "disabled" in node.attrs:
        return False
    tabindex = node.get("tabindex")
    if tabindex is not None:
        try:
            return int(tabindex) >= 0
        except ValueError:
            return False
    if node.tag == "a":
        return "href" in node.attrs
    if node.tag == "input":
        return node.get("type", "text").lower() != "hidden"
    return node.tag in NATIVE_FOCUSABLE or "contenteditable" in node.attrs


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

class Audit:
    def __init__(self, path: Path):
        self.path = path
        builder = TreeBuilder()
        builder.feed(path.read_text(encoding="utf-8", errors="replace"))
        builder.close()
        self.root = builder.root
        self.styles = builder.styles
        self.nodes = [n for n in self.root.iter() if n is not self.root]
        self.findings: list[dict] = []
        self.ids: dict[str, Node] = {}
        self.labels_for: dict[str, list[Node]] = {}
        for node in self.nodes:
            if node.tag == "label" and node.get("for"):
                self.labels_for.setdefault(node.get("for"), []).append(node)
        self.is_document = any(n.tag in ("html", "body", "head") for n in self.nodes)

    def add(self, severity: str, rule: str, wcag: str | None, message: str, node: Node | None = None) -> None:
        snippet = None
        if node is not None:
            attrs = " ".join(f'{k}="{v}"' if v else k for k, v in list(node.attrs.items())[:4])
            snippet = f"<{node.tag}{(' ' + attrs) if attrs else ''}>"[:120]
        self.findings.append({
            "severity": severity, "rule": rule, "wcag": wcag, "message": message,
            "line": node.line if node is not None else None, "element": snippet,
        })

    def run(self) -> list[dict]:
        self.check_document()
        self.check_ids()
        self.check_images()
        self.check_controls()
        self.check_buttons_and_links()
        self.check_keyboard()
        self.check_structure()
        self.check_media_and_frames()
        self.check_css()
        self.findings.sort(key=lambda f: (SEVERITY_RANK[f["severity"]], f["line"] or 0))
        return self.findings

    def check_document(self) -> None:
        if not self.is_document:
            return
        html = next((n for n in self.nodes if n.tag == "html"), None)
        if html is None or not (html.get("lang") or "").strip():
            self.add("error", "html-lang", "3.1.1", "<html> needs a lang attribute (e.g. lang=\"en\")", html)
        title = next((n for n in self.nodes if n.tag == "title"), None)
        if title is None or not text_content(title):
            self.add("error", "document-title", "2.4.2", "the page needs a non-empty <title>", title)
        viewport = next((n for n in self.nodes if n.tag == "meta" and (n.get("name") or "").lower() == "viewport"), None)
        if viewport is None:
            self.add("warn", "viewport-missing", "1.4.10", "no <meta name=\"viewport\">; the page will not adapt to small screens")
        else:
            content = (viewport.get("content") or "").replace(" ", "").lower()
            max_scale = re.search(r"maximum-scale=([\d.]+)", content)
            if "user-scalable=no" in content or "user-scalable=0" in content or (max_scale and float(max_scale.group(1)) < 2):
                self.add("error", "viewport-zoom", "1.4.4", "viewport blocks zooming (user-scalable=no or maximum-scale < 2)", viewport)

    def check_ids(self) -> None:
        seen: dict[str, Node] = {}
        for node in self.nodes:
            node_id = node.get("id")
            if node_id is None:
                continue
            if node_id in seen:
                self.add("error", "duplicate-id", "1.3.1", f"id \"{node_id}\" is used more than once; labels and ARIA references break", node)
            seen.setdefault(node_id, node)
        self.ids = seen
        for node in self.nodes:
            refs = []
            if node.tag == "label" and node.get("for"):
                refs.append(("for", node.get("for")))
            for attr in ("aria-labelledby", "aria-describedby", "aria-controls", "aria-owns", "aria-activedescendant"):
                if node.get(attr):
                    refs += [(attr, ref) for ref in node.get(attr).split()]
            for attr, ref in refs:
                if ref not in seen:
                    self.add("error", "broken-idref", "1.3.1", f"{attr}=\"{ref}\" points to no element", node)

    def check_images(self) -> None:
        for node in self.nodes:
            decorative = node.get("role") in ("presentation", "none") or node.get("aria-hidden") == "true"
            if node.tag == "img" and not decorative:
                if "alt" not in node.attrs:
                    self.add("error", "img-alt", "1.1.1", "image has no alt attribute (use alt=\"\" if decorative)", node)
                else:
                    alt = (node.get("alt") or "").strip().lower()
                    src_name = Path((node.get("src") or "").split("?")[0]).name.lower()
                    if alt in GENERIC_ALT or re.search(r"\.(png|jpe?g|gif|svg|webp)$", alt) or (alt and alt == src_name):
                        self.add("warn", "img-alt-quality", "1.1.1", f"alt=\"{node.get('alt')}\" does not describe the image", node)
            if node.tag == "input" and node.get("type", "").lower() == "image" and not (node.get("alt") or "").strip():
                self.add("error", "input-image-alt", "1.1.1", "image button needs alt text", node)
            if node.tag == "svg" and node.get("role") == "img" and not is_hidden(node) and not accessible_name(node, self.ids):
                has_title = any(t.tag == "title" and text_content(t) for t in node.iter())
                if not has_title:
                    self.add("warn", "svg-img-name", "1.1.1", "svg with role=\"img\" needs aria-label or <title>", node)

    def check_controls(self) -> None:
        for node in self.nodes:
            if node.tag not in ("input", "select", "textarea") or is_hidden(node):
                continue
            input_type = node.get("type", "text").lower()
            if node.tag == "input" and input_type in NON_LABELLED_INPUTS:
                continue
            if not control_label(node, self.ids, self.labels_for):
                extra = " (placeholder is not a label)" if node.get("placeholder") else ""
                self.add("error", "control-label", "1.3.1, 4.1.2", f"form control has no label{extra}", node)
            hint = " ".join(filter(None, [node.get("name"), node.get("id"), input_type if input_type in ("email", "tel") else ""]))
            if node.tag == "input" and "autocomplete" not in node.attrs and AUTOCOMPLETE_HINTS.search(hint or ""):
                self.add("warn", "autocomplete", "1.3.5", "personal-data field without an autocomplete attribute", node)
        for node in self.nodes:
            if node.tag == "button" and "type" not in node.attrs and any(a.tag == "form" for a in node.ancestors()):
                self.add("warn", "button-type", None, "<button> inside a form defaults to type=\"submit\"; set type explicitly", node)

    def check_buttons_and_links(self) -> None:
        for node in self.nodes:
            if is_hidden(node):
                continue
            is_button = node.tag == "button" or node.get("role") == "button" or (
                node.tag == "input" and node.get("type", "").lower() == "button")
            if is_button and not accessible_name(node, self.ids):
                self.add("error", "button-name", "4.1.2", "button has no accessible name (text, aria-label, or labelled icon)", node)
            if node.tag == "a":
                if "href" in node.attrs:
                    name = accessible_name(node, self.ids)
                    if not name:
                        self.add("error", "link-name", "2.4.4, 4.1.2", "link has no accessible name", node)
                    elif name.lower().strip(" .!?›»→") in VAGUE_LINK_TEXT and not node.get("aria-describedby"):
                        self.add("warn", "link-vague", "2.4.4", f"link text \"{name}\" does not say where it goes", node)
                elif node.get("onclick") or node.get("role") == "button":
                    self.add("warn", "link-as-button", "2.1.1, 4.1.2", "<a> without href acting as a button; use <button>", node)

    def check_keyboard(self) -> None:
        for node in self.nodes:
            tabindex = node.get("tabindex")
            if tabindex and tabindex.lstrip("-").isdigit() and int(tabindex) > 0:
                self.add("warn", "tabindex-positive", "2.4.3", f"tabindex=\"{tabindex}\" overrides the natural focus order", node)
            if node.get("aria-hidden") == "true":
                focusable = [n for n in node.iter() if is_focusable(n)]
                if focusable:
                    self.add("error", "aria-hidden-focusable", "4.1.2", "aria-hidden content contains focusable elements", focusable[0])
            role = node.get("role")
            native = node.tag in ("a", "button", "input", "select", "textarea", "summary")
            if role in INTERACTIVE_ROLES and not native and node.get("tabindex") is None:
                self.add("error", "role-not-focusable", "2.1.1", f"role=\"{role}\" element is not keyboard focusable (add tabindex=\"0\" and key handlers, or use a native element)", node)
            if node.get("onclick") is not None and not native and role not in INTERACTIVE_ROLES and node.tag not in ("body", "html", "label"):
                self.add("error", "click-non-interactive", "2.1.1", f"click handler on <{node.tag}> is not reachable by keyboard; use <button> or <a href>", node)

    def check_structure(self) -> None:
        headings = [n for n in self.nodes if re.fullmatch(r"h[1-6]", n.tag) and not is_hidden(n)]
        for heading in headings:
            if not text_content(heading):
                self.add("error", "heading-empty", "1.3.1, 2.4.6", "empty heading", heading)
        previous = 0
        for heading in headings:
            level = int(heading.tag[1])
            if previous and level > previous + 1:
                self.add("warn", "heading-order", "1.3.1", f"heading jumps from h{previous} to h{level}", heading)
            previous = level
        if self.is_document:
            h1s = [h for h in headings if h.tag == "h1"]
            if not h1s:
                self.add("warn", "heading-h1", "2.4.6", "page has no <h1>")
            elif len(h1s) > 1:
                self.add("warn", "heading-h1-multiple", "2.4.6", f"page has {len(h1s)} <h1> elements; usually one names the page", h1s[1])
            if not any(n.tag == "main" or n.get("role") == "main" for n in self.nodes):
                self.add("warn", "landmark-main", "1.3.1, 2.4.1", "no <main> landmark")
        for table in (n for n in self.nodes if n.tag == "table" and n.get("role") not in ("presentation", "none")):
            rows = [n for n in table.iter() if n.tag == "tr"]
            if len(rows) > 1 and not any(n.tag == "th" for n in table.iter()):
                self.add("warn", "table-headers", "1.3.1", "data table has no <th> header cells", table)

    def check_media_and_frames(self) -> None:
        for node in self.nodes:
            if node.tag == "iframe" and not (node.get("title") or "").strip() and not is_hidden(node):
                self.add("error", "iframe-title", "4.1.2", "iframe needs a title describing its content", node)
            if node.tag in ("video", "audio") and "autoplay" in node.attrs and "muted" not in node.attrs:
                self.add("warn", "media-autoplay", "1.4.2", "media autoplays with sound; provide muted or a pause control", node)

    def check_css(self) -> None:
        css = "\n".join(text for _, text in self.styles)
        inline = " ".join(n.get("style", "") for n in self.nodes if n.get("style"))
        all_css = css + "\n" + inline
        blocks = re.findall(r"([^{}]+)\{([^{}]*)\}", css)
        removes = bool(re.search(r"outline\s*:\s*(none|0)\b", all_css))
        replaced = any(
            ":focus" in selector and (
                re.search(r"outline\s*:\s*(?!none\b|0\b)\S", body) or re.search(r"box-shadow\s*:|border(-color)?\s*:", body))
            for selector, body in blocks
        )
        if removes and not replaced:
            self.add("warn", "focus-outline-removed", "2.4.7",
                     "CSS removes outlines and no :focus/:focus-visible rule draws a visible replacement")
        if re.search(r"(@keyframes|animation\s*:|transition\s*:)", all_css) and "prefers-reduced-motion" not in css:
            self.add("warn", "reduced-motion", "2.3.3", "CSS animates but has no prefers-reduced-motion rule")
        for size in re.findall(r"font-size\s*:\s*(\d+(?:\.\d+)?)px", all_css):
            if float(size) < 12:
                self.add("warn", "small-text", "1.4.4", f"font-size {size}px is hard to read; use at least 12px (body text 16px)")
                break


def audit_paths(paths: list[str]) -> dict[str, list[dict]]:
    files: list[Path] = []
    for raw in paths:
        p = Path(raw)
        if p.is_dir():
            files += sorted(p.rglob("*.html")) + sorted(p.rglob("*.htm"))
        elif p.is_file():
            files.append(p)
        else:
            sys.exit(f"error: not found: {raw}")
    if not files:
        sys.exit("error: no HTML files found")
    return {str(f): Audit(f).run() for f in files}


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog="See the module docstring for scope and examples.")
    parser.add_argument("paths", nargs="+", help="HTML files or directories (searched recursively)")
    parser.add_argument("--json", action="store_true", help="print JSON")
    parser.add_argument("--out", help="write JSON to this file and print a summary")
    parser.add_argument("--fail-on", choices=("error", "warn"), default="error")
    args = parser.parse_args(argv)

    results = audit_paths(args.paths)
    totals = {"error": 0, "warn": 0}
    for findings in results.values():
        for f in findings:
            totals[f["severity"]] += 1
    report = {
        "files": results,
        "totals": totals,
        "not_covered": ["colour contrast through CSS", "visual focus order and visibility", "target size",
                        "reflow at 320px and 400% zoom", "screen-reader announcements", "motion and timing behaviour"],
    }
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(json.dumps(report, indent=2), encoding="utf-8")
    if args.json and not args.out:
        print(json.dumps(report, indent=2))
    else:
        for path, findings in results.items():
            print(f"{path}: {len(findings)} finding(s)")
            for f in findings:
                where = f"line {f['line']}" if f["line"] else "document"
                wcag = f" [WCAG {f['wcag']}]" if f["wcag"] else ""
                print(f"  {f['severity'].upper():5} {f['rule']}{wcag} ({where}): {f['message']}")
        print(f"\nTotal: {totals['error']} error(s), {totals['warn']} warning(s). "
              "Not covered statically: " + ", ".join(report["not_covered"]) + ".")
        if args.out:
            print(f"JSON written to {args.out}")
    threshold = SEVERITY_RANK[args.fail_on]
    return 1 if any(SEVERITY_RANK[s] <= threshold and n for s, n in totals.items()) else 0


if __name__ == "__main__":
    sys.exit(main())
