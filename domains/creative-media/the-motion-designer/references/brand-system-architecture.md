# Brand System Architecture & Multi-Brand Isolation

This reference explains how `the-motion-designer` isolates brand identities (such as **GLM**, **Databro**, or custom client brands) so that colors, typography, logos, and motion styles **never** leak or mix between brands.

---

## 1. Two Ways to Use Brand Guidelines

When `the-motion-designer` runs its **Pre-Generation Option Wizard (Step 1)**, it supports two clean patterns for brand isolation:

### Pattern A: Dedicated Brand Specialized Skills (`domains/creative-media/<brand>-brand-motion/`)
Inside the `creative-media` domain, each major recurring brand can have its own **specialized skill** that declares `extends: the-motion-designer` in its `config/skill.yaml`:

```text
domains/creative-media/
├── the-motion-designer/          # CORE SKILL — Engine, wizard, safe zones, Remotion rules
├── glm-brand-motion/             # SPECIALIZED — GLM colors, fonts, logos, lower-thirds, motion style
└── databro-brand-motion/         # SPECIALIZED — Databro colors, fonts, logos, lower-thirds, motion style
```

* **Zero Cross-Contamination**:
  * `glm-brand-motion` stores only GLM's `brand-guidelines.md`, `glm.brand.ts`, and `assets/logos/` inside its own folder.
  * `databro-brand-motion` stores only Databro's `brand-guidelines.md`, `databro.brand.ts`, and `assets/logos/` inside its own folder.
  * Neither skill ever reads or references the other brand's folder.

### Pattern B: Project-Local Brand Token Packs (`src/brands/<brand>.brand.ts`)
Inside a user's Remotion repository, each brand lives in its own isolated TypeScript token module implementing the `BrandTheme` interface (`assets/brand-tokens.starter.ts`):

```text
my-remotion-video/
├── public/
│   └── brands/
│       ├── glm/                  # Isolated static assets for GLM (logo.svg, fonts/)
│       └── databro/              # Isolated static assets for Databro (logo.svg, fonts/)
└── src/
    └── brands/
        ├── types.ts              # Shared BrandTheme interface (from assets/brand-tokens.starter.ts)
        ├── glm.brand.ts          # Exports GLM_BRAND: BrandTheme
        └── databro.brand.ts      # Exports DATABRO_BRAND: BrandTheme
```

---

## 2. What Belongs in a `BrandTheme` Token Pack

Every isolated brand profile defines:
1. **Identity Metadata**: `id` (`'glm'`, `'databro'`), `displayName`, `tagline`, and `website`.
2. **Color Palette**:
   * `backgroundPrimary`, `backgroundSecondary`, `surfaceCard`, `surfaceBorder`
   * `textPrimary`, `textSecondary`, `textMuted`
   * `accentPrimary`, `accentSecondary`, `accentGradient`
   * `statusSuccess`, `statusWarning`, `statusDanger`
3. **Typography**:
   * `headingFontFamily`, `bodyFontFamily`, `monoFontFamily`
   * `headingWeight`, `letterSpacingHeading`
4. **Asset Paths** (resolved via `staticFile()`):
   * `logoLightPath`, `logoDarkPath`, `iconMarkPath`, `watermarkPath`
5. **Motion Personality**:
   * Default `springPreset` (`'snappy'` | `'smooth'` | `'bouncy'` | `'heavy'`)
   * Default `transitionType` (`'slide'` | `'fade'` | `'wipe'`)
   * `cardBorderRadius` (e.g., `8px` sharp enterprise vs. `24px` rounded modern SaaS)
6. **Subtitle / Closed Caption (CC) Styling**:
   * `ccBackgroundColor`, `ccTextColor`, `ccHighlightWordColor`, `ccBorderRadius`

---

## 3. How to Onboard a New Brand Specialized Skill (Mode D)

When the user provides a brand guidelines folder or document (e.g., for **GLM** or **Databro**) and asks to create a dedicated brand skill:

1. Extract verified facts only from the user's brand guidelines (exact hex codes, font names, logo files, brand voice, and visual dos/don'ts). **If any color, font, or logo variant is missing, ask the user before proceeding.**
2. Scaffold the specialized skill in `domains/creative-media/<brand>-brand-motion/`:
   ```bash
   python tools/skills.py new creative-media/<brand>-brand-motion \
     --type specialized \
     --extends the-motion-designer \
     --with references,assets \
     --summary "<Brand> motion graphics and video production skill with official brand colors, typography, logos, and Remotion templates." \
     --description "Creates programmatic Remotion videos and motion graphics strictly following <Brand> brand guidelines..."
   ```
3. Populate `<brand>-brand-motion/references/brand-guidelines.md` and `<brand>-brand-motion/assets/<brand>.brand.ts`.
4. Copy the core anti-hallucination and safe-zone rules into the specialized skill's `SKILL.md` so it remains 100% self-contained per `SKILL_STANDARD.md`.

