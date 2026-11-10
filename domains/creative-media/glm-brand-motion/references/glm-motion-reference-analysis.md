# GLM Motion Animation Reference Analysis : `glm-flippy-muziek.mp4`

Forensic analysis and motion design preferences extracted directly from authentic GLM production video (`glm-flippy-muziek.mp4`, 1920x1080 @ 30fps, 65.97s) and its source implementation (`glm-flippy.src.html`, `glm-flippy.json`, `flippy-video-script.md`).

---

## 1. Executive Summary & Core Motion Preferences

The authentic GLM motion language is defined by:
1. **Geometric Brand Framing**: Corner chevrons (Emerald `#003A40` top-left, Lime `#CDFF70` bottom-right) rather than a persistent static logo in every frame. The brand identity is maintained by the geometry and the mascot.
2. **Editorial Highlighter Markers (`.hl`)**: Strategic keywords in headings have a vibrant Lime `#CDFF70` highlight underlay bar behind them, creating high editorial impact.
3. **The Living Mascot (Flippy)**: Flippy is not a static watermark. He flies in an arc, banks into turns (tilt proportional to vertical velocity), flaps his wings at 4.5 Hz during flight, rests with a gentle idle breath, and physically delivers prompt chips.
4. **Elevated Double-Shadow Cards**: UI cards and prompt chips feature a crisp 3px Emerald outline combined with a deep diffused soft drop-shadow (`box-shadow: 0 2px 0 3px #003A40, 0 40px 80px rgba(0,37,41,.22)`).
5. **Asymmetric Prompt Chips**: Rounded pills where the bottom-right corner is tightened (`border-radius: 46px 46px 10px 46px`), evoking speech and query tags.
6. **Micro-Animations for UI Proof**: Authentic ERP screenshots come alive with simulated mouse clicks, ripple rings, unrolling tables (`clip-path: inset`), camera zooms (1.32x scale into chat), and pulsing highlight rings on action buttons.
7. **Climax Inversion**: The announcement scene wipes the canvas from Cool White into deep Emerald (`#003A40`) with darker diagonal shading, white typography, and a 14-ray rotating lime radial burst.

---

## 2. Canvas Geometry & Corner Brand Chevrons

Instead of occupying top-left screen space with a static logo box during content scenes, the video employs **architectural corner chevrons**:

```css
/* Top-Left Emerald Chevron */
#tri {
  position: absolute;
  inset: 0;
  pointer-events: none;
  background: #003A40;
  clip-path: polygon(0 0, 160px 0, 356px 190px, 0 563px);
  transform-origin: 0 0;
}

/* Bottom-Right Lime Chevron */
#lime {
  position: absolute;
  inset: 0;
  pointer-events: none;
  background: #CDFF70;
  clip-path: polygon(1920px 741px, 1528px 1012px, 1572px 1080px, 1920px 1080px);
  transform-origin: 1920px 1080px;
}
```

### Dynamic Scaling Behavior
* **Content Scenes (0.0s to 51.5s)**: Scaled to `0.55x` (`transform: scale(0.55)`). Gives generous breathing room for UI demo cards while keeping brand colors anchored in both corners.
* **Trust & Climax Scenes (51.5s to 62.2s)**: Opacity set to `0` (hidden) while the full Emerald sweep takes over.
* **End Card (62.5s to 66.0s)**: Smoothly animates from `0.55x` to `1.0x` full size with `eOut` interpolation, framing the final logo lockup.

---

## 3. Typography Stack & Text Styling

### Font Families
* **Geist** (`500`, `600`, `700`, `800`): Display headings, big numbers, speech balloons, and uppercase eyebrows.
* **Poppins** (`400`, `500`, `600`): Body paragraphs, subtitles, and software UI metadata.

### Text Hierarchy & Tokens
| Level | Font & Weight | Size | Color | Letter Spacing | Distinctive Treatment |
|---|---|---|---|---|---|
| **Eyebrow** | Geist 700 | `24px` | `#003A40` | `0.16em` | Uppercase, accompanied by a 16px circular dot (Lime fill, 3px Emerald outline). |
| **Headline** | Geist 800 | `72px` to `110px` | `#100E0D` | `-0.03em` | Line-height `1.1`. Uses `.hl` highlighter underlay on key phrase. |
| **Subtitle** | Poppins 500 | `36px` | `#4A4F55` | Normal | Line-height `1.35`. |
| **Speech Balloon** | Geist 800 | `46px` | `#CDFF70` | Normal | `#003A40` Emerald pill, `padding: 20px 34px`, `border-radius: 30px` with triangle pointer. |
| **Dark Mode Head** | Geist 800 | `100px` | `#F1F0FA` | `-0.03em` | White text on Emerald, with final punchline word in `#CDFF70` Lime. |

### The Highlighter Underlay Pattern (`.hl`)
```css
.hl {
  background: linear-gradient(
    transparent 58%,
    #CDFF70 58%,
    #CDFF70 92%,
    transparent 92%
  );
  padding: 0 0.08em;
}
```
*Creates a flat highlighter line beneath the text without obscuring letter descenders.*

---

## 4. UI Card Architecture & Prompt Chips

### Floating Application Card
```css
.card {
  position: absolute;
  background: #FFFFFF;
  border-radius: 22px;
  overflow: hidden;
  box-shadow: 
    0 2px 0 3px #003A40,
    0 40px 80px rgba(0, 37, 41, 0.22);
}
```
* **Double Shadow System**: Crisp 3px solid Emerald perimeter ring + deep, diffused 80px blur elevation shadow.

### Prompt Chips (Feature Showcase)
```css
.chip {
  position: absolute;
  left: 880px;
  height: 92px;
  display: flex;
  align-items: center;
  gap: 18px;
  padding: 0 36px 0 30px;
  border-radius: 46px 46px 10px 46px; /* Asymmetric bottom-right corner */
  background: #CDFF70;
  font-family: 'Poppins', sans-serif;
  font-size: 38px;
  font-weight: 500;
  color: #100E0D;
  white-space: nowrap;
  box-shadow: 
    0 2px 0 3px #003A40,
    0 20px 40px rgba(0, 37, 41, 0.18);
  transform-origin: 0 50%;
}
```

---

## 5. Flippy Mascot Vector & Flight Mechanics

### Vector Anatomy
* Sized at `360px x 331px` in SVG viewbox `0 20 500 460`.
* Separated into two distinct SVG groups:
  1. `<g id="body">`: Lime body (`#CDFF70`), black beak (`#221F1F`), black eye circle, and crisp 13px stroke borders.
  2. `<g id="wing">`: Lime wing with 13px stroke border, pivoting around **`(245, 281)`**.

### Wing Flap & Body Physics
```typescript
// Wing flap rotation and body dynamics
if (isMoving) {
  // Fast flapping during flight (4.5 Hz)
  wingRotation = -12 + 30 * Math.sin(2 * Math.PI * 4.5 * t);
  // Flight bobbing
  yOffset = 6 * Math.sin(2 * Math.PI * 4.5 * t + 1);
  // Banking into curves (tilt proportional to vertical velocity)
  tilt = clamp(vy / 60, -14, 14) * faceDirection;
} else if (isAnnouncement) {
  // Wings spread wide and proud for the worldwide launch
  wingRotation = -38 + 5 * Math.sin(2 * Math.PI * 1.1 * t);
  yOffset = 8 * Math.sin(2 * Math.PI * 0.7 * t);
} else {
  // Gentle idle breathing
  wingRotation = -3 + 4 * Math.sin(2 * Math.PI * 0.6 * t);
  yOffset = 6 * Math.sin(2 * Math.PI * 0.5 * t);
  // Periodic casual flap
  const cycle = (t * 0.8) % 4;
  if (cycle < 0.5) {
    wingRotation -= 22 * Math.sin((cycle / 0.5) * Math.PI);
  }
}
```

### Flight Waypoints (Choreography Schedule)
| Waypoint | Time Window | Coordinates `(X, Y)` | Scale | Face | Arc | Action Description |
|---|---|---|---|---|---|---|
| **0** | `0.0s` | `(2250, 160)` | `1.0` | `1` (Left) | - | Waiting off-screen top-right. |
| **1** | `6.0s - 7.9s` | `(1420, 600)` | `1.0` | `1` (Left) | `-150px` | Swoops into frame in a downward arc; lands on right side. |
| **2** | `17.0s - 18.3s` | `(300, 905)` | `0.5` | `1` (Left) | `-140px` | Glides to bottom-left corner to clear stage for live demo cards. |
| **3** | `41.5s - 42.45s` | `(790, 346)` | `0.42` | `-1` (Right) | `+90px` | Flips orientation to face right; delivers prompt chip 1. |
| **4** | `43.25s - 44.05s` | `(790, 476)` | `0.42` | `-1` (Right) | `-70px` | Steps down to deliver prompt chip 2. |
| **5** | `44.85s - 45.65s` | `(790, 606)` | `0.42` | `-1` (Right) | `-70px` | Steps down to deliver prompt chip 3. |
| **6** | `46.45s - 47.25s` | `(790, 736)` | `0.42` | `-1` (Right) | `-70px` | Steps down to deliver prompt chip 4. |
| **7** | `48.05s - 48.85s` | `(790, 866)` | `0.42` | `-1` (Right) | `-70px` | Steps down to deliver prompt chip 5. |
| **8** | `51.6s - 52.7s` | `(1500, 560)` | `0.8` | `1` (Left) | `-160px` | Arcs over to right side; lands next to Lock icon. |
| **9** | `56.0s - 57.0s` | `(1380, 560)` | `1.5` | `1` (Left) | `-90px` | Grows to 1.5x at center-right; wings spread wide for launch. |
| **10** | `61.7s - 62.6s` | `(2300, -150)` | `1.1` | `-1` (Right) | `-80px` | Exits stage top-right before final End Card lockup appears. |

---

## 6. Live UI Micro-Animations

1. **Scene 1 : Menu Cursor Navigation**:
   - Cursor moves along 5 menu coordinates (`[74, 296]`, `[86, 334]`, `[80, 144]`, `[84, 372]`, `[70, 523]`).
   - Clicking triggers a concentric ring ripple expanding from `0.4` to `1.4` scale with fading opacity.
2. **Scene 4 : Inset Unroll on Data Table**:
   - `clip-path: inset(0 0 ${lerp(85.5, 0, progress)}% 0 round 22px)`
   - Smoothly reveals the table from top to bottom beneath the prompt pill.
3. **Scene 5 : Focused Camera Zoom**:
   - `transform: scale(1.32); transform-origin: 100% 22%`
   - Smoothly zooms right into the Flippy chat drawer and order stock verification.
4. **Scene 6 : Action Button Pulsing Focus Ring**:
   - A rounded box (`border: 6px solid #CDFF70; box-shadow: 0 0 0 3px #003A40`) pulses over the "Send" button (`scale(1 + 0.08 * sin(t))`).
5. **Scene 9 : Radial Sunburst Explosion**:
   - 14 radial lime tick rays shooting outward from behind Flippy (`rotate(i * 360 / 14 deg)`), extending up to 150px length.

---

## 7. Scene-by-Scene Blueprint & Audio Synchronization

| Scene | Time Window | Energy | Visual Focus | Key Text & Highlighting | Synced Audio Cue |
|---|---|---|---|---|---|
| **1. The Tension** | `0.0s - 6.0s` | `0.50` | Exact Globe+ Menu, mouse clicking | "Still clicking through menus to find <hl>one sales order?</hl>" | Soft piano/synth intro, click tick SFX at each menu item |
| **2. Flippy Flies In** | `6.0s - 13.0s` | `0.65` | Flippy swoops in, balloon pops | Balloon: "Not anymore."<br>Head: "Meet <hl>Flippy.</hl>"<br>Sub: "Your AI agent inside Exact Globe+ and Synergy." | `swoosh` (6.2s, 7.4s), `pop` on balloon (8.32s) |
| **3. The Promise** | `13.0s - 17.0s` | `0.60` | High-contrast statement | "You don't search.<br>You <hl>simply ask.</hl>" | Smooth bass groove, `swoosh` (14.1s) |
| **4. Demo : Data** | `17.0s - 25.0s` | `0.70` | Sales Orders unrolling card | Eyebrow: "ASK FOR YOUR DATA"<br>"Your sales orders. <hl>One question</hl> away." | `swoosh` (17.2s), `pop` on query pill (19.02s), table unroll `swoosh` (20.0s) |
| **5. Demo : Screen Reader** | `25.0s - 33.0s` | `0.70` | Order screen + chat drawer zoom | Eyebrow: "IT SEES YOUR SCREEN"<br>"Open an order. <hl>Ask about it.</hl>" | `swoosh` (26.0s), camera zoom `stijg` riser (27.6s) |
| **6. Demo : Email Draft** | `33.0s - 41.0s` | `0.75` | Review & Edit Email, Send pulse | Eyebrow: "IT DRAFTS THE EMAIL"<br>"You check it. You <hl>hit send.</hl>" | `swoosh` (33.6s), glass `ping` on Send button pulse (37.0s) |
| **7. Feature Breadth** | `41.0s - 51.0s` | `0.85` | 5 Prompt Chips delivered by Flippy | "And a lot <hl>more.</hl>"<br>• Customers in Germany<br>• Stockout in 60 days?<br>• Recode ABC to XYZ<br>• Read Excel file<br>• EUR to USD rate | Rhythmic `pop` SFX per chip (42.58s, 44.18s, 45.78s, 47.38s, 48.98s) |
| **8. Trust & Security** | `51.5s - 55.5s` | `0.60` | Animated Lock icon + Role rights | "Works within your rights.<br><hl>Never around them.</hl>" | `swoosh` (51.8s), solid `pop` on lock snap (52.02s) |
| **9. The Climax** | `56.0s - 61.5s` | `0.95` | Emerald sweep, giant Flippy, sunburst | Eyebrow: "NOW LIVE"<br>Balloon: "Big news!"<br>"Flippy is now live for Exact users worldwide." | Major `swoosh` (56.2s), crescendo `ping` (57.1s), `pop` (57.32s) |
| **10. End Card** | `62.5s - 66.0s` | `0.30` | Dual birds logo, corner chevrons | "GLM SYSTEMS"<br>"Meet Flippy"<br>"glmsystems.com" | Final resolving downbeat chord on kick (62.5s) |

---

## 8. Summary of Reusable Remotion Components

To faithfully reproduce this exact animation quality, the following reusable building blocks are codified in `glm-brand-motion`:
1. `<GlmCornerChevrons scale={0.55} />` (Dynamic corner geometry).
2. `<GlmHighlight text="keyword" />` (The `.hl` highlighter underlay).
3. `<GlmCard>` (The double-shadow floating application container).
4. `<GlmChip>` (The asymmetric prompt pill).
5. `<GlmFlippy>` (The animated SVG bird with physics-driven wing flapping, flight banking, and waypoint engine).
6. `<GlmSpeechBalloon>` (The rounded speech bubble with pointer).

