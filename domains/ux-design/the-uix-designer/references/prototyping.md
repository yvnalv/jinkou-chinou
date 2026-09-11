# Prototyping and Figma

How to go from flows to wireframes to high-fidelity interactive prototypes, how to verify them, and how to work with Figma when the Figma connector is available (Mode B).

## Contents

1. Fidelity ladder
2. Wireframes
3. High-fidelity HTML prototypes
4. The verification loop
5. Presenting designs
6. Figma (optional)

---

## 1. Fidelity ladder

| Fidelity | Purpose | Form |
|---|---|---|
| Sketch | Explore many layout ideas in minutes | ASCII or Mermaid block diagrams in chat |
| Wireframe | Agree on structure, content priority, and flow | Grayscale HTML, real headings and labels, no styling decisions |
| High-fidelity prototype | Validate visual direction, states, and interaction | Single-file HTML from `assets/prototype-starter.html`, with tokens |
| Production UI | Ship | Code in the project's stack (Mode C) |

Move up only when the level below is agreed. Explore two or three alternatives at the sketch or wireframe level when the direction is open; converge before high fidelity.

## 2. Wireframes

* Grayscale, one neutral typeface, boxes for images, but **real content**: actual headings, labels, button text, and realistic data lengths. Lorem ipsum hides content problems.
* Show the content priority of each screen and the primary action.
* Include annotations for behavior ("sorts by due date", "opens detail sheet on mobile").
* Cover the key states from the state matrix in `references/interaction-patterns.md`, at least default, empty, and error.

## 3. High-fidelity HTML prototypes

Start from `assets/prototype-starter.html`:

1. Copy it into the project's design folder (for example `design/prototype/<flow>.html`).
2. Put the product's tokens between the `@tokens:start` and `@tokens:end` markers, generated with `python <skill-dir>/scripts/design_tokens.py css <tokens> --dark <dark tokens>` (start from `assets/tokens.starter.json` when there are none yet).
3. Replace the sample screen. Keep the prototype-only state switcher, and add one `data-view` block per state; the URL hash (`#state=empty&theme=dark`) preselects them.
4. Multi-screen flows: one file per screen linked with real `<a href>`, or one file with sections, whichever keeps it simplest to review.

Rules:

* **Self-contained:** inline CSS and JavaScript, no build step, no external requests except web fonts, which need a fallback stack. It must open from disk and upload as a claude.ai artifact.
* **Semantic HTML first:** real buttons, links, labels, headings, and landmarks, so the prototype is also an accessibility reference for developers.
* **Realistic fake data:** plausible names, amounts, dates, and long values; never real personal data.
* **Values from tokens only:** no hard-coded colors or sizes in components.
* **Responsive:** check 1280, 768, 390, and 320 px widths.
* **Both themes** when the product supports dark mode.

## 4. The verification loop

A prototype is not done because the file was written. Verify it and fix what you find:

```text
python <skill-dir>/scripts/audit_html.py design/prototype/
python <skill-dir>/scripts/design_tokens.py contrast --tokens <tokens> --fg "color.text.*" --bg "color.bg.*"
python <skill-dir>/scripts/screenshot.py design/prototype/orders.html --widths 1280,768,390,320 --schemes light,dark --states default,loading,empty,error
```

Then **look at every screenshot** (read the PNG files). Static checks cannot see overlapping elements, clipped text, horizontal overflow, two states visible at once, or poor hierarchy; screenshots can. `screenshot.py` emulates true phone widths even though Chromium windows cannot be narrower than 500px.

If no Chromium-based browser is available (for example on claude.ai), say so and ask the user to open the file and check the widths and themes; list the rendering as unverified.

Finally, do a keyboard pass in a real browser when possible: Tab through every control and confirm focus is visible, ordered, and never hidden.

## 5. Presenting designs

* Lead with the problem and the user goal, then the design, then the rationale tied to requirements (`UX-xxx`), heuristics, research, or constraints.
* Show states and edge cases, not only the ideal screen.
* Name the trade-offs and the open questions explicitly.
* Ask for specific feedback ("Does the review step give enough confidence before paying?"), not "Thoughts?".
* Hand-off to developers with `references/DESIGN_SPEC.template.md`.

## 6. Figma (optional)

Everything in this skill works without Figma. When the Figma connector (Figma MCP server) is available in the session, use it as an additional source and target. Tool availability verified 2026-09-11; check the connector's tool list in the session, because it changes.

**Reading designs (design to code, audits):**

| Tool | Use |
|---|---|
| `get_design_context` | Structured design context for a frame or selection (defaults to React + Tailwind; ask for the project's stack) |
| `get_screenshot` | Visual reference of a frame |
| `get_metadata` | Lightweight outline of layers to find the right node |
| `get_variable_defs` | Variables and styles in use: map them to tokens |
| `search_design_system`, `get_libraries` | Find existing components and variables before creating new ones |
| `get_code_connect_map` | Existing mappings from Figma components to code components |

**Writing designs (code to design):** `use_figma` (general create and edit, beta), `generate_figma_design` (layers from a web UI), `create_new_file`, `generate_diagram` (FigJam diagrams from Mermaid flows), `upload_assets`. Write access requires a paid Figma seat, and some tools are in beta.

Rules for Figma:

* If the session provides Figma-specific skills (for example a `figma-use` skill that must be loaded before `use_figma`), follow them.
* **Read before writing,** reuse the file's existing components and variables, and put new work on a new page or frame; never overwrite or delete existing designs without explicit approval.
* Keep tokens in sync: Figma variables and the repository's DTCG files must agree; the repository is the source of truth unless the user says otherwise.
* Screenshots and designs from Figma may contain confidential or personal data; do not paste them into public places.
