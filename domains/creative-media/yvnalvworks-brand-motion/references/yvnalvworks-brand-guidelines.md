# yvnalvworks Brand Guidelines

## 1. Visual Identity Principles
`yvnalvworks` is the personal engineering studio brand of Yovan Alvianto.
The visual identity is modeled on high-performance developer tools, terminal elegance, and modern technical documentation (inspired by Lucide, Linear, and Vercel): dark matte grain surface, big confident Poppins type, one lime punchline.

### Strictly Prohibited Visual Elements:
- **No generic AI aesthetics**: No purple/pink/blue nebula gradients, glowing neon orbs, or floating magic sparkle emojis (`✨` is reserved only for Notion status).
- **No stock illustrations**: No cartoon robots, isometric floating islands, 3D clay icons, or generic 3D human figures.
- **No third-party logos** as decoration on covers.
- **No heavy shadows or skeuomorphic bevels**: Everything is matte and razor-sharp, with 1px subtle borders.

---

## 2. Background

Every slide and every video frame sits on the brand grain background: `assets/brand-kit/backgrounds/yvnalvworks-grain-bg.png` (a `#121212` base with fine speckle grain and soft lighter haze top-left and bottom-right), scaled with `cover`.

- Never use a flat solid fill as the visible background. `#121212` is only the fallback color behind the image.
- Do not tint, blur, or recolor the texture. Cards and code blocks may sit on top of it in `#18181b`.

---

## 3. Color Palette

| Token Name | Hex Code | Usage |
|---|---|---|
| **Canvas** | `#121212` | Base tone of the grain background, fallback fill only |
| **Card Dark** | `#18181b` | Background of dark containers and code blocks |
| **Card Border** | `#27272a` | 1px subtle border for dark cards |
| **Electric Lime** | `#C1FF72` | Signature accent: one punchline phrase per slide, solid framework cards |
| **Text Headline** | `#FFFFFF` | Headlines and the lockup name |
| **Warm Ivory** | `#F0ECE2` | Lockup handle, body copy on dark |
| **Text Secondary**| `#8E8E93` | Explanatory sentences and captions |
| **Text Muted**    | `#71717A` | Slide indicators (`01 / 05`), domain watermarks, tags |
| **Danger**        | `#EF4444` | Anti-pattern warnings and error states |

---

## 4. Typography Rules

1. **Primary typeface (headlines, lockup, body)**: `Poppins` (Google Fonts)
   - Headlines: 700 Bold, tracking `-0.04em`, line height `1.02`. Cover headline is 96px.
   - Subheadings: 600 SemiBold. Body: 400 Regular.
   - Lockup: name 600 / 24px white, handle 400 / 21px Warm Ivory.
2. **Code & Telemetry**: `JetBrains Mono` or `Geist Mono`
   - Weight 500 (Medium).
   - Used for slide numbers, schema keys, terminal outputs, and system metrics.

The full cover layout is in `references/cover-slide-spec.md`.

---

## 5. Lucide Monoline SVG Standard
All visual icons, diagrams, and cards MUST follow Lucide design guidelines (`https://lucide.dev`):
- `viewBox="0 0 24 24"`
- `fill="none"`
- `stroke="currentColor"` or `stroke="#C1FF72"`
- `stroke-width="2"`
- `stroke-linecap="round"`
- `stroke-linejoin="round"`
- Minimal visual density, 24px grid base.
