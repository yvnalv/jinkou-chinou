# databro-content-ideas

Researches, validates, and structures evidence-backed Databro content ideas (carousels, short-form video scripts, articles, threads) in casual Bahasa Indonesia with mandatory source citations and content planner sync.

Domain: `creative-media` · Type: `specialized`

## When to use

Invoke with `/databro-content-ideas`, or let Claude pick it up automatically when you ask for things like:

- "Bikinin ide konten Databro hari ini tentang Agentic AI"
- "Riset topik machine learning yang lagi rame buat carousel Instagram Databro"
- "Draft script video pendek buat Databro bahas kenapa feature engineering itu penting"
- "Cariin ide konten statistik dan probabilitas buat audience pemula Databro"
- "Sinkronkan ide konten hari ini ke Notion planner Databro"

## Structure

```text
databro-content-ideas/
├── SKILL.md                                  # Core skill instructions, intake gate, and 8-part arc
├── README.md                                 # This human-facing overview
├── config/
│   └── skill.yaml                            # Manifest, policy, categories, and Notion mapping
├── references/
│   ├── CONTENT_IDEA.template.md              # Standard 8-part markdown template
│   ├── databro-content-categories.md         # 8 editorial categories and rotation guide
│   ├── databro-voice-and-tone-guide.md       # Indonesian 'bro' tone, zero em-dash, and fact-checking
│   └── platform-format-specs.md              # Specs for Carousel, Video, Article, and Thread
├── scripts/
│   ├── format_content_idea.py                # Schema and citation validator + Markdown compiler
│   └── sync_notion_planner.py                # Notion planner block schema compiler
├── assets/
│   └── content-idea.starter.json             # Machine-readable starter data example
└── evals/
    └── evals.json                            # Trigger and behavioral evaluation cases
```

## Changelog

### 0.1.0 - 2026-11-10

- Initial release of Databro Content Ideas skill.
- Implemented mandatory upfront intake gate asking topic and platform before research.
- Implemented standard 8-part Databro content arc with verified source citations.
- Added Notion Content Planner payload synchronization script.
- Enforced strict zero em-dash rule and casual Indonesian "bro" tone.
