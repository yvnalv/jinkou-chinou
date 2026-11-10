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
- **Target Duration**: 45 to 75 seconds (1,350 to 2,250 frames @ 30 FPS).
- **Integration**: Direct handoff to [`databro-brand-motion`](../databro-brand-motion/SKILL.md) for Remotion production using `DatabroBaseCanvas`.
- **Script Structure**:
  - Hook (0-5s): Visual pattern interrupt + verbal hook question.
  - Tension (5-15s): Relatable problem.
  - Core Lesson (15-40s): Fast-paced walkthrough with kinetic subtitles.
  - Actionable Tip (40-55s): Concrete takeaway.
  - Outro (55-60s): Follow & share CTA.

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

