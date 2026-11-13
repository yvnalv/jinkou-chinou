# yvnalvworks Voice & Tone Guide

## Table of contents
1. Who is talking
2. The hook (first 2 to 3 seconds)
3. Story structure (reels and carousels)
4. Sentence rhythm
5. AI-ish patterns to avoid
6. Honesty in stories
7. Still non-negotiable
8. Spoken scripts, captions, slides, post captions
9. Worked example: stiff vs story

## 1. Who is talking

Yovan, an AI and Computer Vision systems engineer, telling a friend who builds software about something that surprised him. Warm, curious, a little playful, honest about trade-offs, technically exact. It should sound like a person talking over coffee, never like a narrator reading facts or a model summarizing a document.

The test: read the script out loud. If it sounds like a list of facts with transitions glued between them, it is not a story yet.

## 2. The hook (first 2 to 3 seconds)

The first sentence decides whether anyone watches the rest. It is spoken in **2 to 3 seconds: 8 words or fewer** (about 3 seconds at the usual 1.2x delivery), and the visual says the same thing **from the first frame** (a big number, a broken screen, a surprising result; no slow fade-in, no logo, no greeting).

A hook does one of these:

| Hook type | Example |
|---|---|
| Surprising result | "Your six-word question just cost three thousand tokens." |
| Relatable pain | "Your AI demo worked yesterday. Today it's lying to customers." |
| Curiosity gap | "AI can't count the r's in strawberry, and here's why." |
| Stakes | "Writing this prompt in Indonesian costs a quarter more." |
| Contrarian | "The model is the easiest part of an AI product." |

Never open with: "Hi guys", "In this video", "Today we'll talk about", "Did you know", or a definition ("Tokens are...").

The hook opens a loop. The story must **close that same loop** in the payoff (the three thousand tokens get explained; the strawberry gets counted).

## 3. Story structure

### Reels (as long as the story needs, under 3 minutes)

| Part | Time | What it does |
|---|---|---|
| Hook | 0 to 3 s | One short sentence that opens a question (section 2). |
| Setup | 3 to 12 s | Put the viewer in a concrete moment: what they did, what they saw. "You hit send, you check the usage page..." |
| Discovery | 12 to 40 s | Explain what is really going on, **as a sequence of things that happen**, each one answering the question the last one raised. This is where the facts live, inside the story. |
| Payoff | near the end | Close the hook's loop. The number, the surprise, the "so that's why". |
| Takeaway + CTA | last ~10 s | One thing to try, said like advice to a friend, then "Follow for more". |

Timings shown are for a 60-second reel. Longer reels (up to 3 minutes) stretch the setup and discovery; the hook stays 2 to 3 seconds.

### Carousels

Slide 1 is the hook (the cover headline plus a hook line in the caption). Slides then follow setup, discovery, payoff, takeaway; every slide ends with a reason to swipe.

## 4. Sentence rhythm

- **Spoken, flowing sentences.** Most sentences run 12 to 22 words and carry a cause or a consequence: "because", "so", "which is why", "and that's when", "turns out".
- **One short punch per part, at most.** A short sentence is a drumbeat; three in a row is a robot. Never stack sentences under 7 words.
- **Tell it as events.** "When you hit send, a tokenizer quietly chops your text into pieces" beats "A tokenizer splits text into tokens."
- **Concrete over abstract.** Real words (hello, strawberry), real numbers (6 words, 3,000 tokens), real objects (the usage page, the chat window).
- **Talk to "you".** Contractions everywhere (it's, you're, don't). Jargon gets a plain-words explanation the first time.
- **Questions only when the story needs one.** One question to turn the story is great; a question every line is a quiz.

## 5. AI-ish patterns to avoid

These make a script sound generated. `build_reel_package.py` flags many of them.

- Stacked short declaratives: "Models don't read words. They read tokens. Tokens are numbers."
- "Here's the thing", "Let's dive in", "Let that sink in", "Buckle up", "Game-changer", "Unlock", "In today's world", "The secret", "Spoiler".
- "It's not just X, it's Y" and "Not X. Y." reveal patterns.
- Rule-of-three lists in every paragraph ("faster, cheaper, and better").
- Colon reveals in every sentence ("The answer: tokens.").
- Opening every sentence with "So" or "And".
- Definitions as the first line ("Tokenization is the process of...").
- Summaries that repeat the script ("In short, tokens are...").

## 6. Honesty in stories

First-person anecdotes ("Last week I...") must be **true**. Ask Yovan for a real moment, or use a "you" scenario or a clearly hypothetical one ("Imagine you..."). Measured numbers name their source ("in my test with the GPT-4o tokenizer"). Illustrative numbers on screen carry the `illustrative` tag.

## 7. Still non-negotiable

1. **English only.** No Indonesian and no slang abbreviations. Friendly does not mean sloppy.
2. **Technically correct, with sources.** Simplify the words, never the facts.
3. **No hype** and none of the patterns in section 5.
4. **No em-dashes or en-dashes** (`—`, `–`). Use commas, colons, parentheses, or a new sentence.
5. **Human voiceover only.** Yovan records manually (iPhone, 48 kHz). Never synthesize a voice.

## 8. Formats

### Spoken scripts (reels)
- Write for the ear. If you run out of breath, split at a natural pause, not into fragments.
- About 140 words per minute: 60 seconds is about 140 words, 90 seconds about 210, and the hard ceiling is 3 minutes (about 420 words). Keep it as short as the story allows.
- Mark the hook as its own first sentence in scene 1.

### On-screen closed captions
- The exact voiceover words, in **sentence case**.
- One cue per breath group, not per few words: **3 to 9 words, at most 48 characters**, shown on up to two lines. Longer, natural phrases read as speech; tiny 3-word flashes read as a robot.
- Break at commas and breath points; never split a phrase that belongs together ("a / model"). No trailing periods; keep question marks.

### Carousel slides
- Each slide is one story moment: a natural sentence headline plus 1 to 3 flowing sentences.
- End a slide with a pull to the next one when it fits.

### Post captions
- Start with the hook line, then tell the story in short paragraphs, then the takeaway, CTA, sources, hashtags.

## 9. Worked example: stiff vs story

**Stiff (what we shipped first, avoid):**

> You ask a model one short question, but the usage page says three thousand tokens. Where did they come from? Models don't read words. A tokenizer cuts your text into chunks called tokens, and each one becomes a number. Common words stay whole, but rare words and numbers get split into smaller pieces. And your message is never alone.

Why it fails: no hook in the first 3 seconds (the first sentence is 15 words), and the middle is a row of short declarative facts.

**Story (do this):**

> Your six-word question just cost three thousand tokens. *(hook, 2.5 s)*
>
> And no, the meter isn't broken. When you hit send, the model never actually sees your words, because a tokenizer quietly chops them into little pieces and turns every piece into a number. Easy words like hello stay in one piece, but something like strawberry gets cut into three.
>
> So where did the other three thousand come from? Every message you send carries luggage you never see: the app's hidden instructions, its tool descriptions, and your entire conversation, sent again on every single turn.
>
> You pay for all of it, and reply tokens usually cost more than the ones you sent, so long chats get expensive fast.
>
> So before you ship, paste your prompt into a tokenizer and look at the real number. Follow for more.
