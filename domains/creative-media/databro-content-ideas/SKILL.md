---
name: databro-content-ideas
description: "Researches, validates, and drafts evidence-backed content ideas for Databro Studio (@databroid) across AI, data science, machine learning, Python, and statistics in casual Bahasa Indonesia ('bro' tone). Always asks upfront for the target topic and content format/platform before conducting deep factual research across papers, docs, news, and official sources. Formats ideas into Databro's standard 8-part content arc (Title, Subtitle, Background Hook, Bridging Explanation, Real-World Case, Actionable Solution, Summary Insight, Closing CTA) with verified citations, and syncs to workspace markdown and Notion content planner."
metadata:
  version: 0.1.0
---

# Databro Content Ideas : Evidence-Backed AI & Data Science Content Research

Researches, validates, and structures evidence-backed technical content ideas for Databro Studio (`@databroid` / `@databro.id`). Translates machine learning algorithms, agentic AI breakthroughs, data science workflows, Python tricks, and pure statistics into relatable, casual Bahasa Indonesia ("bro" tone) without sacrificing mathematical rigor or technical accuracy.

Every idea follows Databro's proven 8-part content arc, strictly adheres to zero em-dashes, and enforces mandatory primary source citations (papers, docs, benchmarks, official announcements).

---

## When to Use

- Use when planning daily or weekly content for Databro social channels (Instagram, LinkedIn, TikTok, X).
- Use when exploring fresh AI news, papers, and agentic trends from the past 24 to 48 hours to create timely educational posts.
- Use when drafting step-by-step data science tutorials, chart reading guides, or Python code tips.
- Use when preparing content briefs before producing Remotion videos with `/databro-brand-motion`.
- Use when populating or updating the user's Notion "📆 Databro Content Planner" database.

## When Not to Use

- Do not use for writing production Remotion code or rendering motion graphics (use `/databro-brand-motion` or `/the-motion-designer` instead).
- Do not use for corporate B2B enterprise software topics outside Databro's niche (use `/glm-brand-motion` for GLM Systems / Exact ERP).
- Do not use for raw tabular data analysis or building ML pipelines (use `/exploratory-data-analysis` or `/the-ml-engineer`).

---

## Bundled Resources

| Path | Purpose & When to Open |
|---|---|
| `references/CONTENT_IDEA.template.md` | Standard 8-part markdown schema. Open when drafting and formatting the final content output. |
| `references/databro-content-categories.md` | The 8 core editorial categories and rotation guide. Open to review topic scopes or pick fresh angles. |
| `references/databro-voice-and-tone-guide.md` | Indonesian "bro" tone rules, technical English terms, zero-em-dash rule, and fact-checking policy. |
| `references/platform-format-specs.md` | Constraints for Carousels (4:5), Short-form video (9:16), LinkedIn articles, and X threads. |
| `scripts/format_content_idea.py` | Validates required fields, citations, and zero em-dashes: `python <skill-dir>/scripts/format_content_idea.py --input <file.json> --output <file.md>`. |
| `scripts/sync_notion_planner.py` | Compiles Notion block schema and properties for the Databro Content Planner database: `python <skill-dir>/scripts/sync_notion_planner.py --input <file.json> --dry-run`. |
| `assets/content-idea.starter.json` | JSON schema starter showing the exact field layout and structure. |

---

## Workflow

### Step 0 : The Mandatory Upfront Intake Gate (Always Ask First)

Never jump straight into researching or generating an idea without user confirmation. Always prompt the user upfront with three clear questions:

1. **Target Topic or Category Angle**:
   - Machine Learning Concepts (algorithms, loss functions, evaluation)
   - Data Science Workflow (EDA, cleaning, visualization, feature engineering)
   - AI News & Trends (Agentic AI, model releases, papers from past 24-48h)
   - RAG & LLM Techniques (Vector DBs, chunking, embeddings, rerankers)
   - Pure Math & Statistics (Probability, distributions, hypothesis testing)
   - Hands-on Tutorials / How-To (Python snippets, chart interpretation)
   - Real-World Datasets (Indonesian data, salary surveys, benchmarks)
   - Applied Domain Analytics (Business, fintech, health, marketing cases)
   - Or: Specific topic requested by user / "Surprise me with fresh 24h trends"
2. **Target Platform & Content Format**:
   - Instagram / LinkedIn Carousel (8-part slide breakdown, 4:5 ratio)
   - Short-Form Video Script (TikTok / Reels / Shorts 9:16 with motion cues)
   - LinkedIn Article / Long-Form Technical Essay
   - X / Twitter Technical Thread
3. **Output Destination**:
   - Dated workspace Markdown file (`outputs/content-idea-YYYY-MM-DD.md`)
   - Notion Content Planner database (`📆 Databro Content Planner`)
   - Both

---

### Step 1 : Fact-Based Deep Research (Zero Assumption)

Once the user confirms the topic and format:
1. **Search Authoritative Sources**:
   - For AI news & trends: Check arXiv papers, official lab releases (Anthropic, DeepMind, OpenAI, Meta), GitHub trending repositories, and official engineering blogs.
   - For real-world datasets: Inspect Kaggle dataset documentation, BPS Indonesia reports, Stack Overflow Developer Surveys, or official company tech blogs.
   - For statistical/math concepts: Review standard statistical definitions and derivations.
2. **Extract Concrete Evidence**:
   - Record exact benchmark numbers, architectural components, paper findings, or dataset columns.
   - Collect exact source URLs. Never fabricate or assume statistics or performance claims.

---

### Step 2 : Compose the 8-Part Databro Narrative Arc

Draft the idea adhering strictly to Databro's proven 8-part content arc (`references/CONTENT_IDEA.template.md`):

1. **Part 1 : Title / Headline**: Short, punchy concept name in Indonesian + English terms.
2. **Part 2 : Subtitle / Framing Question**: One-line hook question setting up the immediate "why".
3. **Part 3 : Background & Relatable Friction**: 2 to 3 sentences describing a real everyday friction in casual Indonesian ("bro" tone).
4. **Part 4 : Bridging Explanation & Core Concept**: Crystal-clear definition structured as a Markdown comparison table, ASCII flow, or concise bullets.
5. **Part 5 : Real-World Case Study & Benchmark Numbers**: Authentic production scenario, company case, or paper experiment numbers proving why the concept matters.
6. **Part 6 : Actionable Solution / Future Knowledge**: Practical takeaway: clean Python code snippet, step-by-step workflow, or tool recommendation.
7. **Part 7 : Summary Pull-Quote**: One memorable, quotable takeaway pull-quote.
8. **Part 8 : Closing Call-to-Action (CTA)**: Engagement hook tailored for the platform ("Save dulu buat nanti, jangan lupa share ke temen lu ya bro!").
9. **Evidence & Sources**: Mandatory list of verified URLs or "Source: Evergreen fundamentals".

---

### Step 3 : Formatting & Validation

1. Save the idea structured as a JSON file or use `scripts/format_content_idea.py`.
2. Run validation:
   ```bash
   python <skill-dir>/scripts/format_content_idea.py --input <path/to/idea.json> --output outputs/content-idea-YYYY-MM-DD.md
   ```
3. Confirm that:
   - All 8 parts are fully fleshed out.
   - Zero em-dashes (`—`) or en-dashes (`–`) exist in the text.
   - All cited links are active, primary sources.

---

### Step 4 : Content Planner Synchronization

If the user requested Notion synchronization:
1. Run `python <skill-dir>/scripts/sync_notion_planner.py --input <path/to/idea.json> --dry-run` to compile the Notion API page schema.
2. Map fields to the "📆 Databro Content Planner" database (`collection://23e15afd-b3c1-81b6-8bdc-000bba4d54c4`):
   - **Name**: `(Post) Title` (or `(Video)`, `(Article)`, `(Thread)`)
   - **Status**: `Idea 💡`
   - **Platform**: `Instagram` / `Linkedin` / `TikTok` / `Tweet` / `Blog Post`
   - **Post Type**: `Post` / `Video` / `Article` / `Thread`
   - **Category**: `Education` / `Tutorial` / `Study Case` / `Insights`
   - **Assign**: `["9021b873-2895-42d9-b8ec-44eb292dbae1"]` (Yovan Alvianto)
   - **Page Body**: Full 8-part content breakdown and source citations.
3. Present the compiled output and file path to the user.

---

### Step 5 : Optional Handoff to Motion Production

If the user approves the idea and wants to produce a video or animated carousel:
- Inform the user: *"Ide konten ini siap dianimasikan menggunakan `/databro-brand-motion`. Mau langsung kita bikinin script video Remotion-nya bro?"*
- Hand off seamlessly to `databro-brand-motion` using the 8-part arc as the storyboard outline.

---

## Rules

### 1. Mandatory Upfront Gate (Always Ask First)
* Never jump directly to researching or generating a content idea without first asking the user the 3 intake questions (Topic, Platform, Destination).

### 2. Strict Fact-Based Research (Zero Assumption)
* Never guess, assume, or hallucinate benchmark scores, paper citations, or company metrics.
* Every claim must be supported by an authentic primary source URL (paper, official docs, dataset repository, or verified tech blog).
* Pure math fundamentals and basic Python syntax can cite `"Source: Evergreen fundamentals"`.

### 3. Absolute Ban on Em-Dashes (`—`)
* Strictly zero em-dashes (`—`) or en-dashes (`–`) across all titles, copy, markdown files, and Notion entries. Use colons (`:`), hyphens (`-`), or parentheses.

### 4. Databro Voice and Tone Integrity
* Casual Bahasa Indonesia ("bro" tone), friendly, humble, and peer-to-peer.
* Standard technical terms remain in English (`feature engineering`, `data leakage`, `embeddings`, `vector search`, `overfitting`).
* High signal-to-noise ratio: crisp Markdown tables and concrete numbers instead of generic motivational fluff.

---

## Definition of Done

A task run of `databro-content-ideas` is complete when:
1. The user was asked upfront for the topic and platform format, and provided input or selected an option.
2. Topic facts, numbers, and case studies were verified against primary sources.
3. The idea was composed across all 8 parts of the Databro narrative arc with verified citations and zero em-dashes.
4. Output was validated and saved as a dated Markdown file (`outputs/content-idea-YYYY-MM-DD.md`).
5. If requested, Notion planner schema was compiled or synced to the user's database.
6. A concise summary was presented to the user with a prompt to optionally proceed to `/databro-brand-motion`.
