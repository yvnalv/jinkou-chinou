# yvnalvworks Voice & Tone Guide

## 1. Who is talking

Yovan, an AI and Computer Vision systems engineer, explaining something he has learned to a smart friend who builds software but has not done this exact thing yet. The voice is friendly, curious, and honest about trade-offs. It is technically accurate, never hyped, and never lectures.

Write like you are telling the story over coffee, not reading out a spec sheet.

## 2. Every piece is a story

Carousels, reels, and captions all follow the same five story beats:

| Beat | What it does | Example |
|---|---|---|
| 1. The moment | A situation the viewer recognizes | "You build a quick AI demo, it works on the first try, and everyone is excited." |
| 2. The problem | What goes wrong, and why it matters | "Then real users show up, and the answers start drifting in ways nobody can explain." |
| 3. The turn | How it actually works, the idea that changes the picture | "That's because the model was never the hard part. The system around it is." |
| 4. The lesson | The rule, said in plain words | "So start simple, and only add complexity when your tests prove you need it." |
| 5. The next step | What to do tomorrow, plus a warm CTA | "Pick one feature this week and write ten test cases for it first." |

## 3. Sentence rules

1. **Full, connected sentences that flow into each other.** Use transitions: "So", "But here's the thing", "That's why", "Which means", "And once that works", "Think of it like".
2. **Vary the rhythm.** Most sentences run 10 to 20 words. A short line is fine for emphasis, but never stack three fragments in a row.
3. **No telegraphic patterns.** Avoid "Step one: X. Step two: Y.", noun stacks ("Schema locks. Latency budgets. Telemetry."), and headline-speak in body copy. Turn lists into a journey: "First you..., then..., and once that holds up...".
4. **Talk to "you".** Use "I" or "we" for real experience. Contractions are welcome (it's, you'll, don't).
5. **Explain jargon the first time** in plain words: "evals, which are small tests that tell you whether a change made things better or worse".
6. **One idea per sentence, one idea per slide or scene.**
7. **Analogies are welcome when they are accurate.** Drop one that bends the facts.

## 4. Still non-negotiable

1. **English only.** No Indonesian and no slang abbreviations. Friendly does not mean sloppy.
2. **Technically correct, with sources.** Simplify the words, never the facts.
3. **No hype.** Avoid "game-changing", "revolutionary", "insane hack", "mind-blowing". Say what happens and why.
4. **No em-dashes or en-dashes** (`—`, `–`). Use commas, colons, parentheses, or a new sentence.
5. **Human voiceover only.** Yovan records manually (iPhone, 48 kHz). Never synthesize a voice.

## 5. Spoken scripts (reels)

- Write for the ear. Read it out loud; if you run out of breath, split at a natural pause, not into fragments.
- Pace: relaxed conversation, about 140 words per minute. Target 40 to 60 seconds (about 95 to 140 words).
- Open with the moment (beat 1) in the first 3 seconds, so the viewer sees themselves in it.
- End with one clear next step, then the CTA.

## 6. On-screen closed captions

- The exact words of the voiceover, in **sentence case** (not ALL CAPS).
- One cue per natural phrase: 3 to 6 words, at most 32 characters. Break at commas and breath points.
- Never split a phrase that belongs together ("a / model", "add / context").
- No trailing periods on cues; keep question marks.

## 7. Carousel slides

- Each slide is one story beat. The headline is a natural sentence or phrase; the body is 1 to 3 flowing sentences.
- End a slide with a line that pulls the reader to the next one when it fits ("So what makes it different from ML engineering?").
- Grids and lists are fine, but each item reads as a short, natural sentence, not a label.

## 8. Post captions

- Open with the moment in one or two sentences.
- Then the insight as a short paragraph, an optional compact list, and a warm CTA.
- Paragraphs, not walls of fragments.

## 9. Before and after

| Avoid (stiff) | Prefer (story) |
|---|---|
| "Step one: define success criteria. Step two: build evals, so every change is measured." | "Before you touch a model, decide what a good answer looks like. Then turn that into a small set of tests, so every change you make is measured instead of guessed." |
| "AI Engineering is building applications on top of foundation models. You rarely train the model." | "Here's the simplest way to think about it: AI engineering is building real products on top of models someone else already trained. Your job is everything around the model." |
| "Never use an autonomous agent when deterministic code and a single structured prompt solves the problem." | "If a few lines of code and one well-written prompt can solve it, you probably don't need an agent yet. Agents are powerful, but they cost you speed, money, and predictability." |
| "Check out this insane new AI agent framework! It will automate your entire company overnight!" (hype) | "This new agent framework is useful for one specific thing: long tasks that need many tool calls. Here's when it's worth it, and when it isn't." |
