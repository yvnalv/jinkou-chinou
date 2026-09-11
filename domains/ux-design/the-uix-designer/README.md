# the-uix-designer

UI/UX design persona for digital products: UX discovery and flows, wireframes and HTML prototypes, design systems and accessible UI code, and UI/UX audits across web, iOS, Android, desktop apps, and dashboards. It designs every state, builds WCAG 2.2 AA in from the start, follows the product's existing design system, avoids generic "AI-looking" visuals, and verifies its work by rendering and checking it.

Domain: `ux-design` · Type: `core`

## When to use

Invoke with `/the-uix-designer`, or let Claude pick it up automatically when you ask for things like:

- "Design the onboarding flow for our budgeting app." (Mode A → B)
- "Mock up a settings page for the admin dashboard, light and dark." (Mode B)
- "Set up design tokens and a button/input/select set for this React app." (Mode C)
- "Review our checkout for usability and accessibility problems." (Mode D)
- "The focus ring on our buttons is invisible in dark mode, fix it." (Mode E)

| Mode | For | Output |
|---|---|---|
| A — Discover & Define | Users, goals, journeys, IA, flows | `design/UX_BRIEF.md` with Mermaid flows |
| B — Design & Prototype | Wireframes → high-fidelity HTML prototype | `design/prototype/*.html`, screenshots, `design/DESIGN_SPEC.md` |
| C — Design System & Build | DTCG tokens, component specs, UI code | Token files, generated CSS, specs, code |
| D — Audit | Heuristics, WCAG 2.2 AA, consistency | `design/UX_AUDIT.md` |
| E — Quick Fix | Small UI change | The change + short summary |

Figma is optional: when the Figma connector is enabled, the skill reads designs and variables from Figma and can write new frames (with your approval); otherwise it works in HTML, Markdown, and code.

### Scripts on their own

```text
python scripts/design_tokens.py validate tokens.json
python scripts/design_tokens.py css tokens.json --dark tokens.dark.json --out tokens.css
python scripts/design_tokens.py contrast --pair "#767676" white --suggest
python scripts/design_tokens.py contrast --tokens tokens.json tokens.dark.json --fg "color.text.*" --bg "color.bg.*"
python scripts/audit_html.py design/prototype/
python scripts/screenshot.py design/prototype/index.html --widths 1280,390,320 --schemes light,dark --states default,empty,error
```

All three scripts use only the Python standard library. `screenshot.py` needs Chrome, Edge, Chromium, or Brave installed.

## Structure

```text
the-uix-designer/
├── SKILL.md                                  # modes, principles, gates, rules, definition of done
├── README.md
├── config/
│   └── skill.yaml                            # manifest + machine-readable policy
├── references/
│   ├── ux-discovery.md                       # questions, evidence levels, JTBD, journeys, flows, IA, metrics, research
│   ├── interaction-patterns.md               # state matrix, forms, navigation, tables, feedback, dialogs, writing, AI, dark patterns
│   ├── visual-design.md                      # visual direction (anti-generic), hierarchy, spacing, type, color, dark mode, motion
│   ├── platforms.md                          # web, iOS (Liquid Glass), Android (M3 Expressive), desktop, dashboards
│   ├── accessibility.md                      # WCAG 2.2 AA checklist, native apps, testing, legal landscape, ARIA rules
│   ├── design-systems.md                     # inventory, DTCG 2025.10 tokens, components, implementation, governance
│   ├── prototyping.md                        # fidelity ladder, HTML prototypes, verification loop, Figma
│   ├── ux-audit.md                           # audit passes, heuristics, severity, evidence
│   ├── UX_BRIEF.template.md
│   ├── DESIGN_SPEC.template.md
│   ├── COMPONENT_SPEC.template.md
│   └── UX_AUDIT.template.md
├── scripts/
│   ├── design_tokens.py                      # validate DTCG tokens, generate CSS, WCAG contrast + suggestions
│   ├── audit_html.py                         # static accessibility/UX lint for HTML
│   └── screenshot.py                         # headless screenshots across widths, themes, states
├── assets/
│   ├── prototype-starter.html                # self-contained accessible prototype skeleton
│   ├── tokens.starter.json                   # DTCG starter tokens (light)
│   └── tokens.starter.dark.json              # dark-theme overrides
└── evals/
    └── evals.json
```

Research basis (verified 2026-09-11): WCAG 2.2 (WCAG 3 still a working draft), EN 301 549 v4.1.1 and the European Accessibility Act, ADA Title II deadlines as extended in April 2026, DTCG 2025.10 design tokens, Material 3 Expressive, Apple Liquid Glass, the Figma MCP server tool set, Nielsen Norman Group's State of UX 2026, and Anthropic's guidance on avoiding generic AI frontend aesthetics.

## Changelog

### 0.1.0 — 2026-09-11

- Initial version: five modes (discover, design, design system and build, audit, quick fix), Design Quality and Design-System Consistency gates, eight references, four templates, three scripts (tokens/contrast, HTML audit, screenshots with true phone-width emulation), a verified prototype starter, and DTCG starter tokens.
