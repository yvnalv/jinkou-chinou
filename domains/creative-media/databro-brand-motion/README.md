# databro-brand-motion

Specialized brand motion skill for **Databro Studio (`@databroid` — "Belajar Data Science")**, extending `the-motion-designer`.

## Quick Facts

| Field | Value |
| --- | --- |
| Domain | `creative-media` |
| Type | `specialized` (`extends: the-motion-designer`) |
| Version | `0.1.0` |
| Owner | `@yvnalv` |
| Tags | `databro`, `remotion`, `motion-graphics`, `brand-guidelines`, `tiktok`, `reels`, `data-science` |

## When to use

- Creating TikTok, Instagram Reels, or YouTube Shorts motion videos for **Databro Studio (`@databroid`)**.
- Applying Databro's isolated visual identity (`#111111` matte charcoal canvas, `#BFFF72` lime green, `#F2EBE1` warm cream circle badges, `#D92D20` red UI/terminal callouts, fixed top-left `Databro / Belajar Data Science` avatar lockup, and cardless 2–4 word ALL-CAPS Closed Captions).

## Structure

```text
databro-brand-motion/
├── SKILL.md                                  # Databro visual identity & scene archetype rules
├── README.md                                 # Human overview & changelog
├── config/
│   └── skill.yaml                            # Metadata (type: specialized, extends: the-motion-designer)
├── references/
│   └── databro-brand-guidelines.md           # Sampled @databroid hex palette, typography, & choreography
├── assets/
│   ├── databro-avatar.jpg                    # Official Databro Studio circular creator avatar
│   ├── databro.brand.starter.ts              # Isolated DATABRO_BRAND TypeScript token module
│   ├── DatabroLogoLockup.starter.tsx         # Fixed top-left avatar + Databro / Belajar Data Science lockup
│   └── DatabroCaptions.starter.tsx           # Cardless 2-to-4 word ALL-CAPS ExtraBold white CC component
└── evals/
    └── evals.json                            # Trigger & non-trigger evaluation suite
```

## Changelog

### 0.1.0 — 2026-11-09

- Initial release of `databro-brand-motion` extending `the-motion-designer`.
- Extracted Databro Studio (`@databroid`) brand tokens (`#111111`, `#BFFF72`, `#F2EBE1`, `#D92D20`), top-left avatar lockup (`databro-avatar.jpg` + `Databro / Belajar Data Science`), centered Emblem Circle and Command Prompt Callout scene archetypes, and cardless 2–4 word uppercase Closed Captions.
