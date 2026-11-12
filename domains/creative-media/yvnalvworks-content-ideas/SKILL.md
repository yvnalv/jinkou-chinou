---
name: yvnalvworks-content-ideas
description: "Researches, validates, and drafts evidence-backed content ideas for yvnalvworks across AI Engineering, Computer Vision, Edge Systems, and Software Architecture in 100% Technical English. Always asks upfront for target topic and platform before researching papers, documentation, and real production patterns. Formats ideas into technical carousel outlines with a cover headline that follows the published yvnalvworks cover patterns (What X Should Know About Y, numbered Should Know listicles, one lime highlight phrase), video scripts with teleprompter voiceover guides, and syncs directly to the yvnalvworks Content Planner in Notion."
metadata:
  version: 0.2.1
---

# yvnalvworks Content Ideas: Evidence-Backed Technical Content Research

Researches, validates, and structures evidence-backed technical content ideas for **yvnalvworks (Yovan Alvianto : yvnalvworks.com / `@yvnalvworks`)**. Translates cutting-edge AI systems engineering, edge computer vision deployments, foundation model architectures, latency optimizations, and high-performance software engineering into authoritative, pragmatic, and high-signal technical content.

Every idea is written strictly in **100% Technical English**, adheres to zero em-dashes, and enforces mandatory primary source citations (papers, docs, benchmarks, official announcements).

> [!WARNING]
> **CRITICAL GATE (No Unrequested Visual Generation):**
> Do not generate slide images, Figma files, or video compositions unless explicitly instructed by the user.
> This skill focuses on deep factual research, editorial structuring, teleprompter voiceover scripting, and syncing to the yvnalvworks Content Planner in Notion. Visual rendering is handled through `yvnalvworks-brand-motion` or manual approval.

---

## When to Use

* When drafting high-signal technical carousel or reels content ideas for `@yvnalvworks` or `yvnalvworks.com`.
* When planning, outlining, or scripting engineering breakdowns on AI systems, edge computer vision, MLOps, or Python/systems performance.
* When synchronizing approved content topics into the `yvnalvworks Content Planner` in Notion.
* When generating teleprompter voiceover scripts and timestamped closed captions (`.srt` and `.json`) for Yovan's manual voice recording.

## When NOT to Use

* Do not use for Databro Studio content (use `/databro-content-ideas` instead).
* Do not use for GLM Systems enterprise marketing (use `/the-motion-designer` or GLM skills instead).
* Do not use for automated image/video rendering without prior confirmation (use `/yvnalvworks-brand-motion` once the script or outline is approved).

---

## Bundled Resources

| Path | Purpose & When to Load |
|---|---|
| `references/cover-headline-patterns.md` | Open when writing any carousel: cover headline formulas from the published covers, line-break and highlight rules, `coverHeadline` JSON form. |
| `references/CONTENT_IDEA.template.md` | Standard markdown outline template for 5-part carousels and reels companion scripts. |
| `references/yvnalvworks-content-pillars.md` | Detailed breakdown of the 4 core engineering pillars and acceptable topic scopes. |
| `references/yvnalvworks-voice-and-tone-guide.md` | Tone constraints, writing rules, ban on em-dashes, and voiceover guidelines. |
| `references/platform-format-specs.md` | Resolution, aspect ratios, safe zones, and duration limits for Instagram Feed and Reels. |
| `scripts/format_content_idea.py` | Deterministic CLI tool to validate and format content idea JSON into clean markdown (`python scripts/format_content_idea.py <file.json>`). |
| `scripts/sync_notion_planner.py` | Deterministic CLI helper to construct Notion database properties for `📆 yvnalvworks Content Planner` (`python scripts/sync_notion_planner.py <file.json>`). |
| `assets/content-idea.starter.json` | Sample starter JSON payload illustrating valid structure and fields. |

---

## Brand Persona & Core Pillars

**yvnalvworks** represents Yovan Alvianto, an AI & Computer Vision Systems Engineer building production-grade intelligence at the intersection of high-performance software, edge computing, and reliable AI architectures.

### The 4 Content Pillars

1. **AI Engineering & LLM Systems**
   - Golden eval test suites before model selection
   - Non-deterministic error compounding in autonomous agents
   - Strict Pydantic / JSON schema locks and latency budgets
   - Semantic caching, prompt minimization, and small language model (SLM) routing

2. **Computer Vision & Edge AI**
   - High-throughput camera pipelines (GStreamer, DeepStream, V4L2)
   - Real-world distribution shifts, sensor noise, glare, and shadow invariants
   - Edge acceleration on NVIDIA Jetson, Hailo NPUs, TensorRT, and ONNX Runtime
   - Slice audits over aggregate metrics (why 98% mAP models fail in production)

3. **Production Machine Learning & MLOps**
   - Feature stores, continuous retraining loops, and automated data curation
   - High-entropy failure mining from production telemetry
   - Calibration, reliability diagrams, and out-of-distribution detection

4. **High-Performance Software Engineering**
   - Python 3.14+ performance, memory profiling, and C++/Rust extensions
   - Asynchronous concurrency, message queues, and low-latency IPC
   - Clean architectural boundaries, system design, and pragmatic trade-offs

---

## 5 Editorial Principles

1. **Pragmatic Over Hyped**: Focus on real production engineering challenges rather than toy marketing demos.
2. **Systems Over Models**: Models are just components. The competitive edge is in evaluation, data curation, latency budgets, and architecture.
3. **Strict 100% Technical English**: Clear, concise, active voice, industry-standard engineering terminology. Slang and casual colloquialisms are strictly prohibited.
4. **Zero Em-Dashes**: Never use em-dashes (`—`) or en-dashes (`–`) for rhetorical parentheticals. Use colons, parentheses, or separate crisp sentences instead.
5. **Human Voiceover Only**: Never synthesize AI voiceover. Always provide teleprompter recording guides and 2-4 word ALL-CAPS SRT captions for manual voice recording.

---

## The 5-Part Narrative Arc

Every technical post (carousel or video) follows this proven technical framework:

1. **Slide 1 / Cover + Hook**: The slide shows the `coverHeadline`, an audience-promise headline in 3 to 4 hand-broken lines with exactly one `[[lime]]` phrase, following `references/cover-headline-patterns.md` (e.g., "What AI Engineers / Should Know / About [[Microsoft / Agent Framework]]"). The `hookStatement`, a counter-intuitive technical reality (e.g., "Building an AI feature is easy. Running an AI Engineering project is a completely different discipline."), opens the caption and the reel.
2. **Slide 2 / Tension (Industry Anti-Pattern)**: Contrast naive industry practices ("Vibe Coding") against disciplined engineering realities.
3. **Slide 3 / Framework (Visual Architecture)**: High-signal modular system breakdown using authentic Lucide 2px monoline vector icons.
4. **Slide 4 / Golden Rule (Engineering Law)**: A definitive architectural thesis (e.g., "Never use an autonomous agent when deterministic code and a single structured prompt solves the problem.").
5. **Slide 5 / Takeaway & CTA (Next Step)**: Core summary quote linking to `yvnalvworks.com/projects` or articles with a bookmark CTA.

---

## Workflow

### Step 1: Upfront Intake Gate
Confirm with the user:
1. Target pillar and topic angle.
2. Target platform (Instagram Carousel 4:5, Instagram Reels 9:16, LinkedIn Article).
3. Output path (`D:\yvnalv\Onedrive\04. yvnalvworks\Contents\...`) and Notion sync option.

### Step 2: Technical Research & Evidence Verification
- Search official documentation, ArXiv papers, and engineering benchmarks.
- Verify empirical numbers and extract architectural principles.

### Step 3: Draft Narrative Arc & Script
- For carousels: Write the `coverHeadline` from `references/cover-headline-patterns.md` (offer 2 to 3 options with line breaks and the highlight marked), then draft all 5 slides adhering to the 5-part arc with Lucide icon recommendations.
- Validate with `python <skill-dir>/scripts/format_content_idea.py <file.json>` before handing over.
- For reels: Draft spoken script (35-45s) and matching teleprompter recording guide with 2-4 word ALL-CAPS SRT closed captions.

### Step 4: Notion Content Planner Sync
- Register entry into the `📆 yvnalvworks Content Planner` database (`5a915afd-b3c1-8274-836c-87fe398765ee`).

---

## Definition of Done

A task run of `yvnalvworks-content-ideas` is complete when:
1. Upfront intake gate questions were confirmed with the user.
2. Topic was verified with primary technical sources and benchmark citations.
3. Content conforms strictly to 100% Technical English and zero em-dashes.
4. Carousels carry a `coverHeadline` that passes the cover rules (3 to 4 lines, max 18 characters per line, exactly one highlight).
5. Teleprompter voiceover guide and closed caption subtitles were delivered (if video format).
6. Output was saved to the designated OneDrive path.
7. Topic was registered in the Notion Content Planner database.
