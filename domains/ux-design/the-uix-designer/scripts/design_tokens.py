#!/usr/bin/env python3
"""Validate design tokens, convert them to CSS, and check color contrast.

Works with the W3C Design Tokens Community Group format (DTCG 2025.10):
tokens are objects with "$value"; groups are objects without it; "$type"
is inherited from the closest group; aliases use "{group.token}" and
property-level JSON Pointer references use {"$ref": "#/path"}. Older
string values ("#0066cc", "16px", "200ms") are accepted too.

Several token files can be given; later files override earlier ones (for
example base.tokens.json then brand.tokens.json). A dark theme is passed as
separate override files with --dark.

Commands:
  validate  FILES...                      report structural problems
  css       FILES... [--dark FILES...]    emit CSS custom properties
  contrast  [--tokens FILES...] --pair FG BG [...] | --fg PATTERN --bg PATTERN
            WCAG 2.x contrast ratios, with --suggest for passing alternatives

Examples:
  python design_tokens.py validate tokens.json
  python design_tokens.py css tokens.json --dark tokens.dark.json --out tokens.css
  python design_tokens.py contrast --pair "#767676" "#ffffff" --suggest
  python design_tokens.py contrast --tokens tokens.json --fg "color.text.*" --bg "color.bg.*"
  python design_tokens.py contrast --pair "oklch(0.62 0.19 255)" white --target 4.5 --suggest

Standard library only.
"""

from __future__ import annotations

import argparse
import copy
import fnmatch
import json
import math
import re
import sys
from pathlib import Path

WCAG_THRESHOLDS = {
    "AA normal text": 4.5,
    "AA large text / UI components": 3.0,
    "AAA normal text": 7.0,
    "AAA large text": 4.5,
}
NAMED_COLORS = {
    "white": "#ffffff", "black": "#000000", "red": "#ff0000", "green": "#008000", "blue": "#0000ff",
    "gray": "#808080", "grey": "#808080", "silver": "#c0c0c0", "yellow": "#ffff00", "orange": "#ffa500",
    "purple": "#800080", "navy": "#000080", "teal": "#008080", "maroon": "#800000", "transparent": "#00000000",
}
ALIAS_RE = re.compile(r"^\{([^{}]+)\}$")
EMBEDDED_ALIAS_RE = re.compile(r"\{([^{}]+)\}")


class TokenError(Exception):
    pass


# ---------------------------------------------------------------------------
# Color math (sRGB, HSL, OKLCH) and WCAG contrast
# ---------------------------------------------------------------------------

def _srgb_to_linear(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _linear_to_srgb(c: float) -> float:
    return 12.92 * c if c <= 0.0031308 else 1.055 * (c ** (1 / 2.4)) - 0.055


def oklch_to_srgb(l: float, c: float, h: float) -> tuple[tuple[float, float, float], bool]:
    """Return gamma-encoded sRGB (0..1, clipped) and whether it was in gamut."""
    a, b = c * math.cos(math.radians(h)), c * math.sin(math.radians(h))
    l_ = (l + 0.3963377774 * a + 0.2158037573 * b) ** 3
    m_ = (l - 0.1055613458 * a - 0.0638541728 * b) ** 3
    s_ = (l - 0.0894841775 * a - 1.2914855480 * b) ** 3
    lin = (
        4.0767416621 * l_ - 3.3077115913 * m_ + 0.2309699292 * s_,
        -1.2684380046 * l_ + 2.6097574011 * m_ - 0.3413193965 * s_,
        -0.0041960863 * l_ - 0.7034186147 * m_ + 1.7076147010 * s_,
    )
    in_gamut = all(-2e-3 <= v <= 1 + 2e-3 for v in lin)
    rgb = tuple(min(1.0, max(0.0, _linear_to_srgb(min(1.0, max(0.0, v))))) for v in lin)
    return rgb, in_gamut


def srgb_to_oklch(rgb: tuple[float, float, float]) -> tuple[float, float, float]:
    r, g, b = (_srgb_to_linear(v) for v in rgb)
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l_, m_, s_ = (math.copysign(abs(v) ** (1 / 3), v) for v in (l, m, s))
    L = 0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_
    A = 1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_
    B = 0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_
    return L, math.hypot(A, B), math.degrees(math.atan2(B, A)) % 360


def hsl_to_srgb(h: float, s: float, l: float) -> tuple[float, float, float]:
    s, l = s / 100, l / 100

    def f(n: float) -> float:
        k = (n + h / 30) % 12
        return l - s * min(l, 1 - l) * max(-1, min(k - 3, 9 - k, 1))

    return f(0), f(8), f(4)


def _num(text: str, percent_scale: float = 1.0) -> float:
    text = text.strip()
    if text == "none":
        return 0.0
    if text.endswith("%"):
        return float(text[:-1]) / 100 * percent_scale
    if text.endswith("deg"):
        return float(text[:-3])
    return float(text)


class Color:
    """An sRGB color with alpha; remembers its source text for reporting."""

    def __init__(self, rgb: tuple[float, float, float], alpha: float = 1.0, source: str = "", in_gamut: bool = True):
        self.rgb = rgb
        self.alpha = alpha
        self.source = source
        self.in_gamut = in_gamut

    @property
    def hex(self) -> str:
        body = "".join(f"{round(v * 255):02x}" for v in self.rgb)
        return f"#{body}" + (f"{round(self.alpha * 255):02x}" if self.alpha < 1 else "")

    @property
    def oklch(self) -> str:
        l, c, h = srgb_to_oklch(self.rgb)
        if c < 0.0005:  # achromatic: hue is meaningless
            c, h = 0.0, 0.0
        return f"oklch({l:.3f} {c:.3f} {h:.1f}" + (f" / {self.alpha:g})" if self.alpha < 1 else ")")

    def luminance(self) -> float:
        r, g, b = (_srgb_to_linear(v) for v in self.rgb)
        return 0.2126 * r + 0.7152 * g + 0.0722 * b

    def over(self, background: "Color") -> "Color":
        """Composite this color over an opaque background."""
        a = self.alpha
        rgb = tuple(a * f + (1 - a) * b for f, b in zip(self.rgb, background.rgb))
        return Color(rgb, 1.0, self.source)


def parse_css_color(text: str) -> Color:
    raw = text.strip()
    value = NAMED_COLORS.get(raw.lower(), raw)
    m = re.fullmatch(r"#([0-9a-fA-F]{3,8})", value)
    if m:
        h = m.group(1)
        if len(h) in (3, 4):
            h = "".join(ch * 2 for ch in h)
        if len(h) not in (6, 8):
            raise TokenError(f"invalid hex color '{raw}'")
        rgb = tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
        alpha = int(h[6:8], 16) / 255 if len(h) == 8 else 1.0
        return Color(rgb, alpha, raw)
    m = re.fullmatch(r"(rgba?|hsla?|oklch)\((.*)\)", value.strip(), re.I)
    if not m:
        raise TokenError(f"unsupported color '{raw}' (use hex, rgb(), hsl(), oklch(), or a basic name)")
    fn, body = m.group(1).lower(), m.group(2)
    alpha = 1.0
    if "/" in body:
        body, alpha_text = body.split("/", 1)
        alpha = _num(alpha_text)
    parts = [p for p in re.split(r"[\s,]+", body.strip()) if p]
    if fn in ("rgb", "rgba", "hsl", "hsla") and len(parts) == 4:
        alpha = _num(parts.pop())
    if len(parts) != 3:
        raise TokenError(f"color '{raw}' needs three components")
    if fn.startswith("rgb"):
        rgb = tuple(_num(p, 255) / 255 for p in parts)
        return Color(tuple(min(1, max(0, v)) for v in rgb), alpha, raw)
    if fn.startswith("hsl"):
        h, s, l = _num(parts[0]), _num(parts[1], 100), _num(parts[2], 100)
        return Color(hsl_to_srgb(h, s, l), alpha, raw)
    l, c, h = _num(parts[0]), _num(parts[1], 0.4), _num(parts[2])
    rgb, in_gamut = oklch_to_srgb(l, c, h)
    return Color(rgb, alpha, raw, in_gamut)


def color_from_value(value) -> Color:
    """Accept a CSS color string or a DTCG color object."""
    if isinstance(value, str):
        return parse_css_color(value)
    if not isinstance(value, dict):
        raise TokenError(f"invalid color value {value!r}")
    space = value.get("colorSpace")
    comps = value.get("components")
    alpha = float(value.get("alpha", 1))
    comps = [0.0 if c == "none" else float(c) for c in comps] if isinstance(comps, list) else None
    if space == "srgb" and comps and len(comps) == 3:
        return Color(tuple(min(1, max(0, c)) for c in comps), alpha, json.dumps(value))
    if space == "hsl" and comps and len(comps) == 3:
        return Color(hsl_to_srgb(*comps), alpha, json.dumps(value))
    if space == "oklch" and comps and len(comps) == 3:
        rgb, in_gamut = oklch_to_srgb(*comps)
        return Color(rgb, alpha, json.dumps(value), in_gamut)
    if value.get("hex"):
        color = parse_css_color(value["hex"])
        color.alpha = alpha
        return color
    raise TokenError(f"color space '{space}' needs a 'hex' fallback for these tools")


def contrast_ratio(fg: Color, bg: Color) -> float:
    if bg.alpha < 1:
        bg = bg.over(Color((1.0, 1.0, 1.0)))
    if fg.alpha < 1:
        fg = fg.over(bg)
    l1, l2 = sorted((fg.luminance(), bg.luminance()), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


def suggest_foreground(fg: Color, bg: Color, target: float) -> Color | None:
    """Closest color to fg (same OKLCH hue, chroma reduced if needed) that meets target on bg."""
    l0, c0, h0 = srgb_to_oklch(fg.rgb)
    darker_first = bg.luminance() > 0.18
    best = None
    for direction in ((0.0,) if darker_first else (1.0,)) + ((1.0,) if darker_first else (0.0,)):
        lo, hi = (direction, l0) if direction == 0.0 else (l0, direction)
        end_rgb, _ = oklch_to_srgb(direction, c0, h0)
        if contrast_ratio(Color(end_rgb, fg.alpha), bg) < target:
            continue
        for _ in range(40):  # binary search for the lightness closest to the original
            mid = (lo + hi) / 2
            rgb, _ = oklch_to_srgb(mid, c0, h0)
            ok = contrast_ratio(Color(rgb, fg.alpha), bg) >= target
            if direction == 0.0:
                lo, hi = (mid, hi) if ok else (lo, mid)
            else:
                lo, hi = (lo, mid) if ok else (mid, hi)
        final_l = lo if direction == 0.0 else hi
        step = -0.002 if direction == 0.0 else 0.002
        for _ in range(200):  # the hex the user will copy must pass too, not only the exact value
            rgb, _ = oklch_to_srgb(final_l, c0, h0)
            candidate = parse_css_color(Color(rgb).hex)
            candidate.alpha = fg.alpha
            if contrast_ratio(candidate, bg) >= target:
                return candidate
            final_l = min(1.0, max(0.0, final_l + step))
    return best


# ---------------------------------------------------------------------------
# DTCG loading, merging, and alias resolution
# ---------------------------------------------------------------------------

def deep_merge(base: dict, override: dict) -> dict:
    result = copy.deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict) and "$value" not in value:
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = copy.deepcopy(value)
    return result


def load_documents(paths: list[str]) -> dict:
    merged: dict = {}
    for path in paths:
        try:
            doc = json.loads(Path(path).read_text(encoding="utf-8-sig"))
        except FileNotFoundError:
            raise TokenError(f"file not found: {path}")
        except json.JSONDecodeError as exc:
            raise TokenError(f"{path}: invalid JSON ({exc})")
        if not isinstance(doc, dict):
            raise TokenError(f"{path}: the top level must be a JSON object")
        merged = deep_merge(merged, doc)
    return merged


def resolve_pointer(doc: dict, pointer: str, seen: tuple = ()):
    if pointer in seen:
        raise TokenError(f"circular $ref: {' -> '.join(seen + (pointer,))}")
    if not pointer.startswith("#/"):
        raise TokenError(f"only local JSON Pointer references are supported: {pointer}")
    node = doc
    for part in pointer[2:].split("/"):
        part = part.replace("~1", "/").replace("~0", "~")
        if isinstance(node, list) and part.isdigit() and int(part) < len(node):
            node = node[int(part)]
        elif isinstance(node, dict) and part in node:
            node = node[part]
        else:
            raise TokenError(f"$ref target not found: {pointer}")
    return expand_refs(doc, node, seen + (pointer,))


def expand_refs(doc: dict, node, seen: tuple = ()):
    """Replace {"$ref": "#/..."} objects with the referenced content."""
    if isinstance(node, list):
        return [expand_refs(doc, item, seen) for item in node]
    if not isinstance(node, dict):
        return node
    if isinstance(node.get("$ref"), str):
        target = resolve_pointer(doc, node["$ref"], seen)
        extra = {k: v for k, v in node.items() if k != "$ref"}
        if extra and "$value" not in node and any(k.startswith("$") for k in extra):
            return {"$value": target, **{k: expand_refs(doc, v, seen) for k, v in extra.items()}}
        return target
    return {k: expand_refs(doc, v, seen) for k, v in node.items()}


class Token:
    def __init__(self, path: str, raw: dict, inherited_type: str | None):
        self.path = path
        self.raw_value = raw.get("$value")
        self.type = raw.get("$type") or inherited_type
        self.description = raw.get("$description", "")
        self.deprecated = raw.get("$deprecated", False)
        self.value = None  # resolved value (aliases replaced)

    @property
    def css_name(self) -> str:
        return "--" + re.sub(r"[^a-zA-Z0-9-]+", "-", self.path.replace(".", "-")).strip("-").lower()


def collect_tokens(doc: dict) -> tuple[dict[str, Token], list[str]]:
    tokens: dict[str, Token] = {}
    problems: list[str] = []

    def walk(node: dict, prefix: list[str], group_type: str | None) -> None:
        current_type = node.get("$type", group_type)
        for key, child in node.items():
            if key.startswith("$"):
                continue
            path = prefix + [key]
            dotted = ".".join(path)
            if any(ch in key for ch in "{}."):
                problems.append(f"{dotted}: names must not contain '{{', '}}' or '.'")
            if not isinstance(child, dict):
                problems.append(f"{dotted}: expected an object (token or group), got {type(child).__name__}")
                continue
            if "$value" in child:
                name = ".".join(prefix) if key == "$root" else dotted
                tokens[name] = Token(name, child, current_type)
            else:
                walk(child, path, current_type)

    walk(doc, [], None)
    return tokens, problems


def resolve_tokens(tokens: dict[str, Token]) -> list[str]:
    problems: list[str] = []

    def resolve_value(value, chain: tuple):
        if isinstance(value, str):
            m = ALIAS_RE.match(value)
            if m:
                return resolve_alias(m.group(1), chain)
            return value
        if isinstance(value, list):
            return [resolve_value(v, chain) for v in value]
        if isinstance(value, dict):
            return {k: resolve_value(v, chain) for k, v in value.items()}
        return value

    def resolve_alias(target: str, chain: tuple):
        if target in chain:
            raise TokenError(f"circular alias: {' -> '.join(chain + (target,))}")
        if target not in tokens:
            raise TokenError(f"alias {{{target}}} does not match any token")
        token = tokens[target]
        return resolve_value(token.raw_value, chain + (target,))

    for token in tokens.values():
        try:
            token.value = resolve_value(token.raw_value, (token.path,))
            alias = ALIAS_RE.match(token.raw_value) if isinstance(token.raw_value, str) else None
            if token.type is None and alias and alias.group(1) in tokens:
                token.type = tokens[alias.group(1)].type
        except TokenError as exc:
            problems.append(f"{token.path}: {exc}")
    for token in tokens.values():
        if token.type is None:
            problems.append(f"{token.path}: no $type (set it on the token or a parent group)")
    return problems


def load(paths: list[str]) -> tuple[dict[str, Token], list[str]]:
    doc = load_documents(paths)
    doc = expand_refs(doc, doc)
    tokens, problems = collect_tokens(doc)
    problems += resolve_tokens(tokens)
    return tokens, problems


# ---------------------------------------------------------------------------
# Type validation and CSS conversion
# ---------------------------------------------------------------------------

def dimension_css(value) -> str:
    if isinstance(value, str) and re.fullmatch(r"-?\d*\.?\d+(px|rem|em|%)?", value.strip()):
        return value.strip()
    if isinstance(value, dict) and "value" in value:
        unit = value.get("unit", "px")
        if unit not in ("px", "rem"):
            raise TokenError(f"dimension unit must be px or rem, got '{unit}'")
        return f"{value['value']:g}{unit}" if isinstance(value["value"], (int, float)) else f"{value['value']}{unit}"
    if value == 0:
        return "0"
    raise TokenError(f"invalid dimension {value!r}")


def duration_css(value) -> str:
    if isinstance(value, str) and re.fullmatch(r"\d*\.?\d+(ms|s)", value.strip()):
        return value.strip()
    if isinstance(value, dict) and "value" in value and value.get("unit", "ms") in ("ms", "s"):
        return f"{value['value']:g}{value.get('unit', 'ms')}"
    raise TokenError(f"invalid duration {value!r}")


def color_css(value) -> str:
    if isinstance(value, str):
        parse_css_color(value)  # validate
        return value
    if isinstance(value, dict):
        space, comps, alpha = value.get("colorSpace"), value.get("components"), value.get("alpha", 1)
        suffix = f" / {alpha:g}" if alpha != 1 else ""
        if space == "oklch" and isinstance(comps, list) and len(comps) == 3:
            l, c, h = comps
            return f"oklch({l:g} {c:g} {h:g}{suffix})"
        if space == "display-p3" and isinstance(comps, list) and len(comps) == 3:
            return f"color(display-p3 {' '.join(f'{c:g}' for c in comps)}{suffix})"
        color = color_from_value(value)
        return color.hex
    raise TokenError(f"invalid color {value!r}")


FONT_WEIGHTS = {
    "thin": 100, "hairline": 100, "extra-light": 200, "ultra-light": 200, "light": 300, "normal": 400,
    "regular": 400, "book": 400, "medium": 500, "semi-bold": 600, "demi-bold": 600, "bold": 700,
    "extra-bold": 800, "ultra-bold": 800, "black": 900, "heavy": 900, "extra-black": 950, "ultra-black": 950,
}


def font_family_css(value) -> str:
    families = value if isinstance(value, list) else [value]
    generic = {"serif", "sans-serif", "monospace", "cursive", "fantasy", "system-ui", "ui-serif",
               "ui-sans-serif", "ui-monospace", "ui-rounded", "emoji", "math", "-apple-system",
               "BlinkMacSystemFont"}  # keywords must stay unquoted
    return ", ".join(f if f in generic or f.startswith("var(") else f'"{f}"' for f in families)


def to_css(token_type: str, value) -> str | dict[str, str]:
    """Convert a resolved value to CSS; composite types return {suffix: css}."""
    if token_type == "color":
        return color_css(value)
    if token_type == "dimension":
        return dimension_css(value)
    if token_type == "duration":
        return duration_css(value)
    if token_type == "number":
        if not isinstance(value, (int, float)):
            raise TokenError(f"invalid number {value!r}")
        return f"{value:g}"
    if token_type == "fontFamily":
        return font_family_css(value)
    if token_type == "fontWeight":
        if isinstance(value, (int, float)) and 1 <= value <= 1000:
            return f"{value:g}"
        if isinstance(value, str) and value in FONT_WEIGHTS:
            return str(FONT_WEIGHTS[value])
        raise TokenError(f"invalid fontWeight {value!r}")
    if token_type == "cubicBezier":
        if isinstance(value, list) and len(value) == 4 and 0 <= value[0] <= 1 and 0 <= value[2] <= 1:
            return "cubic-bezier(" + ", ".join(f"{v:g}" for v in value) + ")"
        raise TokenError(f"invalid cubicBezier {value!r}")
    if token_type == "strokeStyle":
        return value if isinstance(value, str) else "dashed"
    if token_type == "border":
        return f"{dimension_css(value['width'])} {value.get('style', 'solid') if isinstance(value.get('style'), str) else 'dashed'} {color_css(value['color'])}"
    if token_type == "transition":
        timing = to_css("cubicBezier", value["timingFunction"])
        return f"{duration_css(value['duration'])} {timing} {duration_css(value.get('delay', {'value': 0, 'unit': 'ms'}))}"
    if token_type == "shadow":
        layers = value if isinstance(value, list) else [value]
        parts = []
        for layer in layers:
            inset = "inset " if layer.get("inset") else ""
            parts.append(
                f"{inset}{dimension_css(layer['offsetX'])} {dimension_css(layer['offsetY'])} "
                f"{dimension_css(layer['blur'])} {dimension_css(layer.get('spread', 0))} {color_css(layer['color'])}"
            )
        return ", ".join(parts)
    if token_type == "gradient":
        stops = ", ".join(f"{color_css(s['color'])} {s['position'] * 100:g}%" for s in value)
        return f"linear-gradient(90deg, {stops})"
    if token_type == "typography":
        out = {}
        if "fontFamily" in value:
            out["font-family"] = font_family_css(value["fontFamily"])
        if "fontSize" in value:
            out["font-size"] = dimension_css(value["fontSize"])
        if "fontWeight" in value:
            out["font-weight"] = to_css("fontWeight", value["fontWeight"])
        if "lineHeight" in value:
            lh = value["lineHeight"]
            out["line-height"] = f"{lh:g}" if isinstance(lh, (int, float)) else dimension_css(lh)
        if "letterSpacing" in value:
            out["letter-spacing"] = dimension_css(value["letterSpacing"])
        return out
    raise TokenError(f"unsupported $type '{token_type}'")


def css_value_with_aliases(token: Token, tokens: dict[str, Token]) -> str | dict[str, str]:
    """Keep simple aliases as var() references so semantic tokens stay linked."""
    raw = token.raw_value
    if isinstance(raw, str):
        m = ALIAS_RE.match(raw)
        if m and m.group(1) in tokens and tokens[m.group(1)].type == token.type and token.type != "typography":
            return f"var({tokens[m.group(1)].css_name})"
    return to_css(token.type, token.value)


def validate_types(tokens: dict[str, Token]) -> list[str]:
    problems = []
    for token in tokens.values():
        if token.type is None or token.value is None:
            continue
        try:
            to_css(token.type, token.value)
        except (TokenError, KeyError, TypeError, ValueError) as exc:
            problems.append(f"{token.path}: {exc}")
    return problems


def render_block(selector: str, lines: list[str], indent: str = "") -> list[str]:
    return [f"{indent}{selector} {{"] + [f"{indent}  {line}" for line in lines] + [f"{indent}}}"]


def css_lines(tokens: dict[str, Token], only: set[str] | None = None, resolve: bool = False) -> list[str]:
    lines = []
    for token in tokens.values():
        if only is not None and token.path not in only:
            continue
        value = to_css(token.type, token.value) if resolve else css_value_with_aliases(token, tokens)
        if token.deprecated:
            lines.append(f"/* deprecated: {token.path} */")
        if isinstance(value, dict):
            for prop, v in value.items():
                lines.append(f"{token.css_name}-{prop}: {v};")
        else:
            lines.append(f"{token.css_name}: {value};")
    return lines


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_validate(args) -> int:
    tokens, problems = load(args.files)
    problems += validate_types(tokens)
    by_type: dict[str, int] = {}
    for token in tokens.values():
        by_type[token.type or "?"] = by_type.get(token.type or "?", 0) + 1
    report = {"files": args.files, "tokens": len(tokens), "by_type": by_type, "problems": problems}
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"{len(tokens)} tokens: " + ", ".join(f"{k} {v}" for k, v in sorted(by_type.items())))
        for problem in problems:
            print(f"  ERROR {problem}")
        print("OK" if not problems else f"{len(problems)} problem(s)")
    return 1 if problems else 0


def cmd_css(args) -> int:
    tokens, problems = load(args.files)
    problems += validate_types(tokens)
    dark_tokens = None
    if args.dark:
        dark_tokens, dark_problems = load(args.files + args.dark)
        problems += [p for p in dark_problems + validate_types(dark_tokens) if p not in problems]
    if problems:
        for problem in problems:
            print(f"error: {problem}", file=sys.stderr)
        return 1
    out = [f"/* Generated by design_tokens.py from {', '.join(Path(f).name for f in args.files)}. Do not edit by hand. */"]
    out += render_block(args.selector, css_lines(tokens, resolve=args.resolve))
    if dark_tokens is not None:
        changed = {
            path for path, t in dark_tokens.items()
            if path not in tokens or css_value_with_aliases(t, dark_tokens) != css_value_with_aliases(tokens[path], tokens)
        }
        dark = css_lines(dark_tokens, only=changed, resolve=args.resolve)
        if dark:
            out.append("")
            if args.dark_strategy in ("media", "both"):
                guard = f'{args.selector}:not([data-theme="light"])' if args.dark_strategy == "both" else args.selector
                out.append("@media (prefers-color-scheme: dark) {")
                out += render_block(guard, dark, "  ")
                out.append("}")
            if args.dark_strategy in ("attribute", "both"):
                out += render_block(f'{args.selector}[data-theme="dark"]', dark)
    text = "\n".join(out) + "\n"
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(text, encoding="utf-8")
        print(f"wrote {args.out} ({len(tokens)} tokens)")
    else:
        sys.stdout.write(text)
    return 0


def lookup_color(ref: str, tokens: dict[str, Token]) -> tuple[str, Color]:
    key = ref[1:-1] if ALIAS_RE.match(ref) else ref
    if key in tokens:
        token = tokens[key]
        if token.type != "color":
            raise TokenError(f"{key} is a {token.type} token, not a color")
        return key, color_from_value(token.value)
    if tokens and re.fullmatch(r"[\w-]+(\.[\w-]+)+", key):
        raise TokenError(f"no color token named '{key}'")
    return ref, parse_css_color(ref)


def cmd_contrast(args) -> int:
    tokens: dict[str, Token] = {}
    if args.tokens:
        tokens, problems = load(args.tokens)
        for problem in problems:  # keep going: a work-in-progress set can still be checked
            print(f"warning: {problem}", file=sys.stderr)
        tokens = {p: t for p, t in tokens.items() if t.value is not None}
    pairs: list[tuple[str, str]] = [tuple(p) for p in (args.pair or [])]
    if args.fg or args.bg:
        if not (args.fg and args.bg and tokens):
            print("error: --fg and --bg need each other and --tokens", file=sys.stderr)
            return 2
        colors = [p for p, t in tokens.items() if t.type == "color"]
        fgs = [p for p in colors if fnmatch.fnmatch(p, args.fg)]
        bgs = [p for p in colors if fnmatch.fnmatch(p, args.bg)]
        if not fgs or not bgs:
            print(f"error: patterns matched {len(fgs)} foreground and {len(bgs)} background tokens", file=sys.stderr)
            return 2
        pairs += [(f, b) for f in fgs for b in bgs]
    if not pairs:
        print("error: give --pair FG BG, or --tokens with --fg and --bg patterns", file=sys.stderr)
        return 2

    results = []
    failures = 0
    for fg_ref, bg_ref in pairs:
        try:
            fg_name, fg = lookup_color(fg_ref, tokens)
            bg_name, bg = lookup_color(bg_ref, tokens)
        except TokenError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2
        ratio = contrast_ratio(fg, bg)
        passes = {label: ratio >= threshold for label, threshold in WCAG_THRESHOLDS.items()}
        ok = ratio >= args.target
        failures += 0 if ok else 1
        row = {
            "foreground": fg_name, "background": bg_name, "fg_hex": fg.hex, "bg_hex": bg.hex,
            "ratio": round(ratio, 2), "target": args.target, "meets_target": ok, "wcag": passes,
        }
        if not fg.in_gamut or not bg.in_gamut:
            row["note"] = "a color is outside sRGB and was clipped; results are for the sRGB fallback"
        if args.suggest and not ok:
            suggestion = suggest_foreground(fg, bg, args.target)
            row["suggested_foreground"] = (
                {"hex": suggestion.hex, "oklch": suggestion.oklch, "ratio": round(contrast_ratio(suggestion, bg), 2)}
                if suggestion else None
            )
        results.append(row)

    if args.json:
        print(json.dumps({"results": results, "failures": failures}, indent=2))
    else:
        for r in results:
            status = "PASS" if r["meets_target"] else "FAIL"
            print(f"[{status}] {r['ratio']:>5}:1  {r['foreground']} ({r['fg_hex']}) on {r['background']} ({r['bg_hex']})")
            if r.get("note"):
                print(f"         note: {r['note']}")
            if "suggested_foreground" in r:
                s = r["suggested_foreground"]
                print(f"         suggest: {s['hex']} / {s['oklch']} -> {s['ratio']}:1" if s
                      else "         suggest: none at this hue/opacity (raise the alpha or change the background)")
        print(f"\n{len(results) - failures}/{len(results)} pair(s) meet {args.target}:1 "
              "(WCAG 2.2: 4.5 normal text, 3 large text >= 24px or 18.66px bold, 3 UI components and graphics)")
    return 1 if failures else 0


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog="See the module docstring for examples.")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("validate", help="report structural and type problems in token files")
    p.add_argument("files", nargs="+")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_validate)

    p = sub.add_parser("css", help="emit CSS custom properties")
    p.add_argument("files", nargs="+", help="token files, merged in order")
    p.add_argument("--dark", nargs="+", help="override files for the dark theme")
    p.add_argument("--dark-strategy", choices=("media", "attribute", "both"), default="both",
                   help="media: prefers-color-scheme; attribute: [data-theme=dark]; both (default)")
    p.add_argument("--selector", default=":root")
    p.add_argument("--resolve", action="store_true", help="write literal values instead of var() aliases")
    p.add_argument("--out", help="write to this file instead of stdout")
    p.set_defaults(func=cmd_css)

    p = sub.add_parser("contrast", help="WCAG 2.x contrast ratios")
    p.add_argument("--tokens", nargs="+", help="token files, so pairs can name tokens (color.text.default)")
    p.add_argument("--pair", nargs=2, action="append", metavar=("FG", "BG"),
                   help="foreground and background: token path or CSS color (hex, rgb(), hsl(), oklch())")
    p.add_argument("--fg", help="glob of foreground token paths, e.g. 'color.text.*'")
    p.add_argument("--bg", help="glob of background token paths, e.g. 'color.bg.*'")
    p.add_argument("--target", type=float, default=4.5, help="required ratio (default 4.5)")
    p.add_argument("--suggest", action="store_true", help="suggest the closest passing foreground")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_contrast)

    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except TokenError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
