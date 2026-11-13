---
name: yvnalvworks-content-ideas
description: "Researches, validates, and drafts evidence-backed content ideas for yvnalvworks across AI Engineering, Computer Vision, Edge Systems, and Software Architecture, written as friendly stories that open with a 2 to 3 second hook and flow like natural speech, while staying technically accurate. Always asks upfront for target topic and platform before researching papers, documentation, and real production patterns. Formats ideas into story-driven carousel outlines with a cover headline that follows the published yvnalvworks cover patterns (What X Should Know About Y, numbered Should Know listicles, one lime highlight phrase), conversational reel scripts with a cover headline, teleprompter voiceover guides and natural-phrase closed captions, post captions, and syncs to the yvnalvworks Content Planner in Notion."
metadata:
  version: 0.7.1
---

# yvnalvworks Content Ideas: Evidence-Backed Technical Storytelling

Researches, validates, and structures evidence-backed technical content ideas for **yvnalvworks (Yovan Alvianto : yvnalvworks.com / `@yvnalvworks`)**. Turns AI systems engineering, edge computer vision, foundation models, latency work, and high-performance software into **friendly stories that are easy to follow**: a moment the viewer recognizes, the problem, the turn, the lesson, and the next step.

Every idea is written in **English that flows like a conversation**: full, connected sentences, plain-language explanations of jargon, and no stiff fragments. The facts stay exact, every claim has a primary source (papers, docs, benchmarks, official announcements), and em-dashes stay banned. The full voice rules are in `references/yvnalvworks-voice-and-tone-guide.md`.

> [!WARNING]
> **CRITICAL GATE (No Unrequested Visual Generation):**
> Do not generate slide images, Figma files, or video compositions unless explicitly instructed by the user.
> This skill focuses on deep factual research, storytelling structure, teleprompter voiceover scripting, and syncing to the yvnalvworks Content Planner in Notion. Visual rendering is handled through `yvnalvworks-brand-motion` or manual approval.

---

## When to Use

* When drafting carousel or reels content ideas for `@yvnalvworks` or `yvnalvworks.com`.
* When planning, outlining, or scripting engineering stories on AI systems, edge computer vision, MLOps, or Python/systems performance.
* When writing post captions, teleprompter voiceover scripts, and timestamped closed captions (`.srt` and `.json`) for Yovan's manual voice recording.
* When synchronizing approved content topics into the `yvnalvworks Content Planner` in Notion.

## When NOT to Use

* Do not use for Databro Studio content (use `/databro-content-ideas` instead).
* Do not use for GLM Systems enterprise marketing (use `/the-motion-designer` or GLM skills instead).
* Do not use for automated image/video rendering without prior confirmation (use `/yvnalvworks-brand-motion` once the script or outline is approved).

---

## Bundled Resources

| Path | Purpose & When to Load |
|---|---|
| `references/yvnalvworks-voice-and-tone-guide.md` | Open before writing any copy: the storytelling voice, the five story beats, sentence rules, caption rules, and before/after examples. |
| `references/cover-headline-patterns.md` | Open when writing any carousel: cover headline formulas from the published covers, line-break and highlight rules, `coverHeadline` JSON form. |
| `references/CONTENT_IDEA.template.md` | Standard markdown outline for story-driven carousels and reels companion scripts. |
| `references/yvnalvworks-content-pillars.md` | Detailed breakdown of the 4 core engineering pillars and acceptable topic scopes. |
| `references/platform-format-specs.md` | Resolution, aspect ratios, safe zones, slide counts, durations, and caption format for Instagram Feed and Reels. |
| `scripts/format_content_idea.py` | Deterministic CLI tool to validate and format content idea JSON into clean markdown (`python scripts/format_content_idea.py <file.json>`). |
| `scripts/build_reel_package.py` | Builds a reel package from one `reel.json`: `reels-script.txt`, `teleprompter-voiceover-guide.txt`, `captions.srt`, `captions.json`, `content-spec.json`, and `cover-spec.json` (the 9:16 cover for `/yvnalvworks-brand-motion`). Requires a valid `coverHeadline`. Keeps captions that are already aligned to a recorded voiceover (`video.voiceover.captionsAligned`) unless `--force-captions`. Enforces captions = spoken words, sentence case, 3 to 9 words and 48 characters per cue, no dashes, and the hook (first sentence 8 words or fewer); reports `styleWarnings` for AI-ish writing (`python <skill-dir>/scripts/build_reel_package.py <reel.json> [--out <dir>]`; prints JSON with duration and `inTarget`). |
| `scripts/sync_notion_planner.py` | Deterministic CLI helper to construct Notion database properties for `📆 yvnalvworks Content Planner` (`python scripts/sync_notion_planner.py <file.json>`). |
| `assets/content-idea.starter.json` | Sample starter JSON payload illustrating valid structure and fields. |
| `assets/reel.starter.json` | Sample `reel.json` for `build_reel_package.py`: scenes with spoken line, caption cues, on-screen text, visual plan, emphasis, Lucide icons, and sources. |

---

## Brand Persona & Core Pillars

**yvnalvworks** represents Yovan Alvianto, an AI & Computer Vision Systems Engineer building production-grade intelligence at the intersection of high-performance software, edge computing, and reliable AI architectures. On camera and in captions he sounds like a friendly senior engineer telling a story, not a spec sheet.

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

## 6 Editorial Principles

1. **Hook first, then a story**: The first sentence is a hook of 8 words or fewer (2 to 3 seconds) that opens a question; the rest is a story that closes it. Facts live inside the story as things that happen, never as a row of statements.
2. **Sounds like a person, not a model**: Flowing spoken sentences of 12 to 22 words that carry cause and consequence ("because", "so", "which is why"), at most one short punch per part, "you" and contractions, jargon explained the first time. Never stack short sentences, and avoid the AI-ish patterns in the voice guide (section 5).
3. **Accurate, never hyped**: Simplify the words, never the facts. No hype words. Every claim traces to a primary source.
4. **Systems over models**: Models are just components. The interesting part is evaluation, data, latency, cost, and architecture.
5. **English only, zero em-dashes**: No Indonesian or slang abbreviations. Never use em-dashes (`—`) or en-dashes (`–`); use commas, colons, parentheses, or a new sentence.
6. **Human voiceover only**: Never synthesize an AI voice. Always provide a teleprompter guide and natural-phrase, sentence-case closed captions for manual recording.

---

## Story Structure

Reels run **Hook (0 to 3 s) → Setup → Discovery → Payoff → Takeaway + CTA (last ~10 s)**, as long as the story needs and under 3 minutes; the payoff answers the hook. Carousels use the same arc across slides. Full rules, the AI-ish pattern list, and a worked stiff-vs-story example: `references/yvnalvworks-voice-and-tone-guide.md`. The five beats below map onto it.

1. **The moment (Slide 1 / Cover + Hook)**: The slide shows the `coverHeadline`, an audience-promise headline in 3 to 4 hand-broken lines with exactly one `[[lime]]` phrase, following `references/cover-headline-patterns.md`. The `hookStatement` is a relatable moment told in one or two flowing sentences (e.g., "You build a quick AI demo, it works on the first try, and everyone is excited. Then real users show up."). It opens the caption and the reel.
2. **The problem**: What goes wrong in practice and why it matters, told as what happens to the viewer, not as an "anti-pattern" label.
3. **The turn (how it actually works)**: The idea that changes the picture, often a simple framework or breakdown with Lucide 2px monoline icons. Each item reads as a short natural sentence.
4. **The lesson**: The rule in plain words, with the reason behind it (e.g., "If a few lines of code and one good prompt can solve it, you probably don't need an agent yet.").
5. **The next step + CTA**: One concrete thing to try, then a warm call to action linking to `yvnalvworks.com/projects` or the article.

Carousels run 5 to 10 slides; a beat can span more than one slide.

---

## Workflow

### Step 1: Upfront Intake Gate
Confirm with the user:
1. Target pillar and topic angle.
2. Target platform (Instagram Carousel 4:5, Instagram Reels 9:16, LinkedIn Article).
3. Output path (`D:\yvnalv\Onedrive\04. yvnalvworks\Contents\...`) and Notion sync option.

### Step 2: Technical Research & Evidence Verification
- Search official documentation, ArXiv papers, and engineering benchmarks.
- Verify empirical numbers and extract the principles worth telling.

### Step 3: Draft the Story
- Open `references/yvnalvworks-voice-and-tone-guide.md` and map the research onto the five beats before writing a sentence.
- For carousels: Write the `coverHeadline` from `references/cover-headline-patterns.md` (offer 2 to 3 options with line breaks and the highlight marked), then draft the slides as flowing story beats with Lucide icon recommendations, plus the post caption.
- For reels: Write `reel.json` in the reel folder (start from `assets/reel.starter.json`): a `coverHeadline` (every reel or video gets a cover, written with the same formulas and rules as carousel covers in `references/cover-headline-patterns.md`; offer 2 to 3 options), a conversational spoken script (as long as the story needs, under 3 minutes, about 140 words per minute), caption cues in sentence case cut at breath groups (3 to 9 words, max 48 characters, up to two lines), and for every scene a **visual plan**: one concrete animated metaphor per story beat (a product mockup for the moment, a breaking chart or wrong answer for the problem, a step rail or app-style icon tiles for the turn, a transformation such as a line bending into a loop for the lesson, an avatar end card for the CTA), with Lucide icon names and no third-party logos. The teleprompter guide asks for one take per scene so `/yvnalvworks-brand-motion` can sync the voice later. Then run `python <skill-dir>/scripts/build_reel_package.py <reel.json>` to generate the script, teleprompter guide, captions, and spec, and write `caption.txt`. The video itself is made with `/yvnalvworks-brand-motion`.
- Read every spoken line out loud in your head. Rewrite anything that sounds like a list of facts. `build_reel_package.py` must report the hook within 8 words and **zero `styleWarnings`** (stacked short sentences, choppy average, stock phrases) before handing over.
- Validate with `python <skill-dir>/scripts/format_content_idea.py <file.json>` before handing over.

### Step 4: Notion Content Planner Sync
- Register entry into the `📆 yvnalvworks Content Planner` database (`5a915afd-b3c1-8274-836c-87fe398765ee`).

---

## Definition of Done

A task run of `yvnalvworks-content-ideas` is complete when:
1. Upfront intake gate questions were confirmed with the user.
2. Topic was verified with primary technical sources and benchmark citations.
3. Copy opens with a hook of 8 words or fewer and reads as a flowing story whose payoff answers the hook: English only, zero style warnings, jargon explained, zero em-dashes.
4. Carousels carry a `coverHeadline` that passes the cover rules (3 to 4 lines, max 18 characters per line, exactly one highlight).
5. Reels ship `reel.json` (with a valid `coverHeadline`) plus the generated teleprompter guide, script with a visual plan per scene, sentence-case natural-phrase captions (`.srt` and `.json`), spec, `cover-spec.json`, and a post caption.
6. Output was saved to the designated OneDrive path.
7. Topic was registered in the Notion Content Planner database.
