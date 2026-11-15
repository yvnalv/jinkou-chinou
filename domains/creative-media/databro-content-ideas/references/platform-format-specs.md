# Platform Format Specifications

This reference provides technical constraints and structural guidelines for tailoring Databro content across different social media platforms.

---

## 1. Instagram & LinkedIn Carousel (Primary Format)

- **Canvas Aspect Ratio**: `4:5` (1080x1350px) for Instagram Feed, `1:1` or `4:5` for LinkedIn.
- **Slide Count**: Typically 7 to 9 slides (Standard: 8-part arc).
- **Slide Breakdown**:
  - Slide 1: Cover / Hook (Punchy Title in white + #BB86FC lavender question header + Databro avatar lockup).
  - Slide 2: Background / Problem setup (Relatable tension).
  - Slide 3: The Big Shift / Core Definition (Comparison table or diagram).
  - Slide 4: Deep Dive / How it works under the hood.
  - Slide 5: Real-World Case Study (Numbers and real application).
  - Slide 6: Actionable Takeaway / Code snippet or 3-step solution.
  - Slide 7: Summary Pull-Quote.
  - Slide 8: Engagement CTA ("Save & Share ya bro!").

---

## 2. Short-Form Video (TikTok / Instagram Reels / YouTube Shorts)

- **Canvas Aspect Ratio**: `9:16` (1080x1920px).
- **Target Duration**: 45 to 90 seconds (1,350 to 2,700 frames @ 30 FPS). Size the script for the final reel: the creator records at about 123 to 125 words per minute including natural pauses, and the recording is sped up **1.2x** (range 1.1x to 1.2x, pitch kept), so the reel runs at about 148 words per minute: roughly 110 to 220 spoken words.
- **Integration**: Hand off to the `/databro-brand-motion` skill for Remotion production on `DatabroBaseCanvas`.
- **Cover (required)**: Every video ships with a dedicated cover image, never a grabbed frame. Plan it with the script in a `cover` object:
  - `headline`: lavender question, at most 3 lines (about 11 to 12 characters per line on a 1080x1920 cover).
  - `limeKeyword`: the single topic term shown in lime; it must appear inside the headline.
  - `hook`: one white line, at most 2 lines, usually the video's opening question.
  - `visual`: one key visual taken from the video (diagram, code card, metric, or versus split).
  - The rendered cover keeps headline, hook, and visual inside Y 380 to 1500 so the Instagram 3:4 profile grid and the 4:5 feed preview stay readable.
- **Script Structure (a story, not a list)**:
  - Hook (0 to 3 s): one line of 9 words or fewer that opens a question or surprise, with a visual pattern interrupt.
  - Setup (3 to 12 s): the everyday moment where the topic shows up.
  - Discovery (12 to 50 s): how it really works, told as cause and effect; numbers appear as things that happen.
  - Payoff (50 to 60 s): the moment that answers the hook.
  - Takeaway + CTA (last 8 to 12 s): one practical action, then save/follow.
  - Flowing spoken sentences of about 10 to 22 words; no colon-dictated lists or "pertama/kedua/ketiga" in the voiceover (on-screen numbering is fine). Full rules: `references/databro-voice-and-tone-guide.md`, section 2.
  - Every beat carries one concrete visual idea for the animation.

---

## 3. LinkedIn Article & Long-Form Newsletter

- **Aspect Ratio for Banner**: `16:9` (1920x1080px).
- **Word Count**: 800 to 1,500 words.
- **Structure**:
  - Executive Summary (TL;DR).
  - The Industry Problem / Context.
  - Deep Technical Architecture / Methodology.
  - Empirical Results / Benchmarks.
  - Practical Implementation Guide (Python snippets).
  - Databro Editorial Commentary.

---

## 4. X (Twitter) Technical Thread

- **Length**: 5 to 8 tweets.
- **Thread Anatomy**:
  - Tweet 1: High-curiosity hook statement + "Gini penjelasannya (A Thread) 🧵".
  - Tweet 2: The friction / why traditional approaches fail.
  - Tweet 3-5: Core mechanisms explained with bullet points and clean ASCII diagrams.
  - Tweet 6: Real-world benchmark or code snippet.
  - Tweet 7: One-sentence golden insight.
  - Tweet 8: Bookmark/retweet prompt and profile link.

