# Remotion Core API Reference (v4.x Ground Truth)

This reference defines the verified, official Remotion (`remotion` package) APIs, hooks, components, and anti-hallucination rules based on [`remotion-dev/remotion`](https://github.com/remotion-dev/remotion). Never invent undocumented hooks or props.

---

## 1. The Golden Rule of Remotion Determinism

Remotion renders videos by spawning multiple headless browser tabs that render different frames in parallel (`frame = 0`, `frame = 45`, `frame = 120`...). Therefore, **every frame must be a pure, deterministic function of `useCurrentFrame()`**.

### Strictly Banned Patterns (Will Break Renders)
| Banned Pattern | Why It Fails in Remotion | Correct Remotion Replacement |
|---|---|---|
| `transition: all 0.3s ease` | CSS transitions depend on real-time wall-clock browser ticks, not frame numbers. Parallel tabs capture inconsistent mid-transition states. | `interpolate(frame, [0, 9], [0, 1], { extrapolateRight: 'clamp' })` or `spring()` |
| `@keyframes` / Tailwind `animate-*` | CSS keyframe animations run on browser load time rather than `useCurrentFrame()`. | `interpolate()` or `Math.sin(frame / 10)` |
| `requestAnimationFrame` / `setInterval` / `setTimeout` | Timers fire asynchronously outside Remotion's frame capture cycle. | Compute state directly from `useCurrentFrame()` |
| `useState` + `useEffect` for animation | React state mutations inside `useEffect` cause extra re-renders after frame capture. | Derive values synchronously during render from `useCurrentFrame()` |
| `<img src="..." />` | Headless Chromium may screenshot the frame before the image finishes decoding. | `<Img src={staticFile('logo.png')} />` from `'remotion'` |
| `<video src="..." />` | HTML5 `<video>` seeking is asynchronous and inaccurate across frames. | `<OffthreadVideo src={staticFile('clip.mp4')} />` from `'remotion'` |

---

## 2. Core Hooks (`import { ... } from 'remotion'`)

### `useCurrentFrame(): number`
Returns the current 0-indexed frame number (`0` to `durationInFrames - 1`).
* **Inside a `<Sequence from={30}>`**: `useCurrentFrame()` automatically shifts to become **relative to the sequence start** (returns `0` when the main timeline is at frame `30`)!

### `useVideoConfig(): VideoConfig`
Returns the composition's metadata:
```typescript
const { width, height, fps, durationInFrames, id, defaultProps } = useVideoConfig();
```
Always convert seconds to frames using `fps` (e.g., `const twoSeconds = 2 * fps;`) so animations stay timing-accurate if `fps` changes from `30` to `60`.

### `useRemotionEnvironment()`
Returns environment flags:
```typescript
const { isRendering, isStudio, isPlayer } = useRemotionEnvironment();
```
Use `isRendering` to hide studio-only guides (like `<SafeZoneOverlay />`) during final MP4/MOV export.

---

## 3. Animation Primitives: `spring()` and `interpolate()`

### `spring()` — Physics-Driven Motion
```typescript
import { spring, useCurrentFrame, useVideoConfig } from 'remotion';

const frame = useCurrentFrame();
const { fps } = useVideoConfig();

const scale = spring({
  frame,               // Subtract delay here OR pass `delay` option
  fps,
  delay: 10,           // Optional: wait 10 frames before starting spring
  durationInFrames: 30,// Optional: stretch/compress spring to exact frame count
  from: 0,             // Default: 0
  to: 1,               // Default: 1
  config: {
    damping: 14,       // Default: 10 (higher = less oscillation; 200 = critically damped, no bounce)
    stiffness: 120,    // Default: 100 (higher = faster, snappier)
    mass: 1,           // Default: 1 (higher = heavier, slower acceleration)
    overshootClamping: false, // Set true to prevent exceeding `to` value
  },
});
```

### `interpolate()` — Keyframe Mapping & Easing
```typescript
import { interpolate, Easing, useCurrentFrame } from 'remotion';

const frame = useCurrentFrame();

// Always clamp both ends unless unbounded extrapolation is intentional!
const opacity = interpolate(frame, [0, 15, 75, 90], [0, 1, 1, 0], {
  extrapolateLeft: 'clamp',
  extrapolateRight: 'clamp',
  easing: Easing.bezier(0.16, 1, 0.3, 1), // Optional custom cubic-bezier
});
```

### `interpolateColors()` — Smooth Color Transitions
```typescript
import { interpolateColors, useCurrentFrame } from 'remotion';

const backgroundColor = interpolateColors(
  frame,
  [0, 30],
  ['#0F172A', '#2563EB']
);
```

---

## 4. Layout & Timeline Components

### `<AbsoluteFill>`
A full-bleed `div` with `position: 'absolute', top: 0, left: 0, right: 0, bottom: 0, width: '100%', height: '100%', display: 'flex', flexDirection: 'column'`. Stack multiple `<AbsoluteFill>` components to layer backgrounds, main content, captions, and overlays.

### `<Sequence>`
Time-shifts children on the timeline:
```tsx
<Sequence from={30} durationInFrames={60} name="Hero Title Reveal">
  <HeroTitle /> {/* Inside HeroTitle, useCurrentFrame() starts at 0 on global frame 30 */}
</Sequence>
```
* Note: By default, `<Sequence>` wraps children in an `<AbsoluteFill>`. Pass `layout="none"` if rendering inside a flex/grid container or Three.js `<ThreeCanvas>`.

### `<Series>`
Plays scenes back-to-back sequentially without manual `from` math:
```tsx
import { Series } from 'remotion';

<Series>
  <Series.Sequence durationInFrames={60}>
    <IntroScene />
  </Series.Sequence>
  <Series.Sequence offset={-10} durationInFrames={90}>
    {/* offset={-10} overlaps 10 frames with previous scene */}
    <FeatureScene />
  </Series.Sequence>
</Series>
```

---

## 5. Asset & Media Components

### `staticFile(relativePath: string)`
Resolves files inside the project's `public/` directory safely across Studio, Player, and CLI rendering:
```tsx
import { Img, OffthreadVideo, Audio, staticFile } from 'remotion';

<Img src={staticFile('brands/glm/logo.svg')} style={{ width: 240 }} />
<OffthreadVideo src={staticFile('demos/dashboard-capture.mp4')} startFrom={0} endAt={150} volume={0} />
<Audio src={staticFile('audio/voiceover.mp3')} volume={(f) => interpolate(f, [0, 15], [0, 1], { extrapolateRight: 'clamp' })} />
```

### Waiting for Custom Fonts or Async Data (`delayRender` / `continueRender`)
When loading local brand fonts (`FontFace`) or fetching JSON before rendering:
```typescript
import { delayRender, continueRender, cancelRender } from 'remotion';
import { useEffect, useState } from 'react';

const [handle] = useState(() => delayRender('Loading brand font'));

useEffect(() => {
  const font = new FontFace('BrandSans', `url(${staticFile('fonts/BrandSans-Bold.woff2')})`);
  font.load()
    .then((loaded) => {
      document.fonts.add(loaded);
      continueRender(handle);
    })
    .catch((err) => cancelRender(err));
}, [handle]);
```

---

## 6. Registering Compositions & Dynamic Metadata (`Root.tsx`)

Use `<Composition>` for videos and `<Still>` for single-frame graphics. Use `calculateMetadata` when duration or dimensions depend on props:
```tsx
import React from 'react';
import { Composition, Still } from 'remotion';
import { MainVideo, mainVideoSchema } from './MainVideo';

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="MainPromo"
        component={MainVideo}
        durationInFrames={450}
        fps={30}
        width={1080}
        height={1920}
        schema={mainVideoSchema}
        defaultProps={{
          brandId: 'glm',
          headline: 'Automate Your Workflow in Seconds',
          platform: 'instagram-reels',
          showSafeZoneGuide: true,
        }}
      />
    </>
  );
};
```

