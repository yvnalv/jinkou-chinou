# GLM Systems : Content Structure and Voiceover Guide

> **Target Platform**: LinkedIn (B2B Landscape `16:9` & Portrait `4:5`), YouTube (`16:9`), Exact Globe+ / Synergy in-app announcements.  
> **Brand Tone**: Enterprise, confident, crisp, practical. Professional English (or Dutch where targeted).  
> **Punctuation Rule**: Strictly **zero em-dashes (`—`)** anywhere in voiceover scripts, video titles, or Closed Captions.

---

## 1. Script-First Production Gate & Dedicated Project Folders

Rendering takes time; rewriting scripts in code is inefficient. Always follow the project encapsulation and sign-off standard:
1. **Dedicated Project Directory**: Every video creation must reside in its own dedicated project folder (e.g. `remotion-demos/<project-slug>/`).
2. **Required Project Files**:
   - `brief.md`: Goals, audience, format, feature checklist, tone, and duration.
   - `storyboard.md`: Scene-by-scene script, exact second and frame timestamps, on-screen text, visual staging, voiceover copy, and SFX cues.
3. **Dual Composition Requirement**: Every project must output two compositions in `Root.tsx`:
   - `*-VO`: Full voiceover narration + background music + SFX.
   - `*-Muziek`: Background music + SFX + text-only (100% understandable on mute).
4. **Reading Pace Verification**: Minimum 0.4s per word, minimum 2.0s per text card, 2.0s post-motion stillness buffer.
5. **User Approval Required**: Await explicit user approval on the script and storyboard before writing Remotion code.

---

## 2. Content Archetypes

### Archetype A : "Flippy" AI Agent for Exact Globe+ Launch & Explainer (`45-66s`)
* **Core Narrative**: Relatable ERP menu fatigue turned into instant conversational automation, proven by 3 real interface demos, prompt chips, role security, and a worldwide launch climax.
* **Scene 1 : The Tension (`0.0s - 6.0s`)**:
  - Visual: Exact Globe+ purchase/sales menu scrolling slowly, semi-opaque white veil (`menu.png`). Mouse cursor clicking through 5 menu items with expanding ripple rings.
  - Headline: *"Still clicking through menus to find <hl>one sales order?</hl>"*
  - SFX: Soft synth intro, keystroke/click ticks at each menu step.
* **Scene 2 : Flippy Arrives (`6.0s - 13.0s`)**:
  - Visual: Flippy swoops in from top-right in an arc, lands at right stage; speech balloon pops up.
  - Speech Balloon: *"Not anymore."*
  - Headline: *"Meet <hl>Flippy.</hl>"*
  - Subtitle: *"Your AI agent inside Exact Globe+ and Synergy."*
  - SFX: Air whoosh (`swoosh`), bubble pop (`pop`).
* **Scene 3 : The Core Promise (`13.0s - 17.0s`)**:
  - Visual: High-impact typography on Cool White backdrop with corner chevrons.
  - Headline: *"You don't search. You <hl>simply ask.</hl>"*
  - SFX: Rising bass groove (`swoosh`).
* **Scene 4 : Demo 1 : Ask for your Data (`17.0s - 25.0s`)**:
  - Visual: Flippy glides to lower-left. Prompt pill *"show my sales order"* appears, then Sales Orders table card unrolls beneath it via `clip-path: inset`.
  - Eyebrow: `ASK FOR YOUR DATA`
  - Headline: *"Your sales orders. <hl>One question</hl> away."*
  - SFX: Query pop, table unroll swoosh.
* **Scene 5 : Demo 2 : Screen-Reader Context (`25.0s - 33.0s`)**:
  - Visual: Order screen with Flippy chat drawer. Camera smoothly zooms 1.32x into the stock verification question: *"Do I have enough stock for this order?"*.
  - Eyebrow: `IT SEES YOUR SCREEN`
  - Headline: *"Open an order. <hl>Ask about it.</hl>"*
  - SFX: Camera riser (`stijg`), swoosh.
* **Scene 6 : Demo 3 : Automated Email Action (`33.0s - 41.0s`)**:
  - Visual: Review & Edit Email modal window appears. Send button pulses with a lime outer focus ring.
  - Eyebrow: `IT DRAFTS THE EMAIL`
  - Headline: *"You check it. You <hl>hit send.</hl>"*
  - SFX: Confirmation glass ping (`ping`), button swoosh.
* **Scene 7 : Feature Breadth Chips (`41.0s - 51.0s`)**:
  - Visual: Flippy turns right and physically delivers 5 asymmetric prompt chips one by one down the screen.
  - Headline: *"And a lot <hl>more.</hl>"*
  - Chips: "Sales orders for customers in Germany", "Will we run out in 60 days?", "Recode item ABC to XYZ", "Read this Excel file", "What is the EUR to USD rate?".
  - SFX: Rhythmic pop per chip.
* **Scene 8 : Enterprise Trust Anchor (`51.5s - 55.5s`)**:
  - Visual: Animated Emerald/Lime padlock snaps shut on left stage; Flippy perches on right.
  - Headline: *"Works within your rights. <hl>Never around them.</hl>"*
  - SFX: Solid lock snap pop.
* **Scene 9 : The Worldwide Announcement Climax (`56.0s - 61.5s`)**:
  - Visual: Canvas wipes to deep Emerald (`#003A40`) with darker diagonal sweep. Flippy grows to 1.5x at center with 14 rotating lime sunburst rays bursting outward.
  - Eyebrow: `NOW LIVE`
  - Speech Balloon: *"Big news!"*
  - Headline: *"Flippy is now live for Exact users worldwide."*
  - SFX: Major swoosh, crescendo chime ping.
* **Scene 10 : Outro End Card (`62.5s - 66.0s`)**:
  - Visual: Corner chevrons expand to full scale; official GLM SYSTEMS dual bird logo lockup centers with "Meet Flippy" and "glmsystems.com".
  - SFX: Resolving downbeat kick chord.

---

### Archetype B : AI Plus Agent for Exact Synergy Workflow Demo (`30-45s`)
* **Focus**: Workflow automation, approval requests, CRM account intelligence, and colleague lookups.
* **Beat 1 : Portal Friction (`0.0s - 8.0s`)**:
  - Headline: *"How much time does your team spend creating leave requests and tracking approvals?"*
  - Visual: Synergy request forms and document tree.
* **Beat 2 : Natural Language Workflow (`8.0s - 20.0s`)**:
  - Prompt: *"Create a leave request for next Monday"*
  - Result: Request card generates instantly with pre-filled dates, manager routing, and approval button.
  - React Icons: `LuWorkflow`, `LuCalendar`, `LuCheckCircle`.
* **Beat 3 : CRM & Colleague Visibility (`20.0s - 32.0s`)**:
  - Prompt: *"Show resource info for John Tan"* / *"List my open opportunities"*
  - Card: Clean White card on `#F2F0FA` Cool White displaying employee status or sales pipeline.
* **Beat 4 : Endcard (`32.0s - 40.0s+`)**:
  - Headline: *"AI assistance directly inside Exact Synergy."*
  - CTA: *"glmsystems.com"*. Minimum `2.5 seconds` hold.

---

### Archetype C : B2B Feature Spotlight (Stock Depletion Forecast / Recode) (`20-35s`)
* **Focus**: Single-capability deep-dive (e.g., Stock Depletion Horizon or Excel Bulk Recode).
* **Structure**:
  - Problem (5s): *"Running out of stock before procurement notices?"*
  - AI Solution (15s): Predictive depletion horizon with risk tiers: Stockout, At Risk, Healthy.
  - CTA (5s): *"Discover AI Plus Agent at glmsystems.com"*.

---

## 3. Audio-Visual Timing and Breathing Room Standards

1. **Post-Transition Settle Buffer (`HeadDelay = 10 to 12 frames`)**:
   - Visual slide enters and completes transition.
   - Settle buffer runs in visual stillness.
   - Voiceover begins only after the incoming slide settles.
2. **Pre-Transition Speech Silence Buffer (`TailDelay = 12 to 14 frames`)**:
   - Voiceover completes speaking.
   - Scene holds in quiet stillness for `12 to 14 frames` before the next transition starts.
3. **Outro Tail Hold (`24 frames`)**:
   - Hold for `24 frames` (0.8s) minimum before video terminates.

---

## 4. Voiceover & Closed Caption Formatting

* **Voice Profiles**:
  - Global B2B English: `en-US-AndrewNeural` or `en-GB-RyanNeural` (calm, authoritative, executive).
  - Domestic Dutch: `nl-NL-MaartenNeural` (clear, articulate).
  - Cadence: Normal speaking pace (`rate="+0%"` to `"-2%"`, ~130-140 WPM).
* **Closed Captions**:
  - Locked at `Y = 920px` (`16:9`) or `Y = 1140px` (`4:5`).
  - Rendered in Poppins font with zero vertical movement.
  - Zero em-dashes in caption text.
