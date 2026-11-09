# Official `@remotion/*` Packages & Capabilities

This reference documents the verified `@remotion/*` ecosystem packages.

> [!IMPORTANT]
> **Version Parity Rule**: Every `@remotion/*` package and `remotion` itself in `package.json` **must use the exact same version string** (e.g. `4.0.242` without `^` or `~` drift). Run `npx remotion versions` to check and fix version mismatches.

---

## 1. Scene Transitions (`@remotion/transitions`)

Install: `npm i @remotion/transitions`

Replaces manual `<Sequence>` overlap math with declarative transitions (`fade`, `slide`, `wipe`, `flip`, `clockWipe`):

```tsx
import { TransitionSeries, linearTiming, springTiming } from '@remotion/transitions';
import { slide } from '@remotion/transitions/slide';
import { fade } from '@remotion/transitions/fade';
import { wipe } from '@remotion/transitions/wipe';

export const MultiSceneVideo: React.FC = () => {
  return (
    <TransitionSeries>
      <TransitionSeries.Sequence durationInFrames={90}>
        <HookScene />
      </TransitionSeries.Sequence>

      <TransitionSeries.Transition
        presentation={slide({ direction: 'from-bottom' })}
        timing={springTiming({ config: { damping: 200 }, durationInFrames: 20 })}
      />

      <TransitionSeries.Sequence durationInFrames={120}>
        <ProductDemoScene />
      </TransitionSeries.Sequence>

      <TransitionSeries.Transition
        presentation={fade()}
        timing={linearTiming({ durationInFrames: 15 })}
      />

      <TransitionSeries.Sequence durationInFrames={90}>
        <OutroCtaScene />
      </TransitionSeries.Sequence>
    </TransitionSeries>
  );
};
```
* **Frame Budget Formula**: Total frames $= (90 + 120 + 90) - (20 + 15) = 265$ frames.

---

## 2. Vector Shapes & SVG Path Animation (`@remotion/shapes` & `@remotion/paths`)

Install: `npm i @remotion/shapes @remotion/paths`

### `@remotion/shapes`
Renders crisp parametric SVG vectors (`<Rect>`, `<Circle>`, `<Triangle>`, `<Star>`, `<Polygon>`, `<Ellipse>`, `<Heart>`, `<Pie>`):
```tsx
import { Circle, Star, Pie } from '@remotion/shapes';

<Pie radius={100} progress={0.75} fill="#3B82F6" stroke="#1D4ED8" strokeWidth={4} />
<Star points={5} innerRadius={40} outerRadius={90} fill="#F59E0B" />
```

### `@remotion/paths`
Animates SVG stroke drawing (`evolvePath`), path morphing (`interpolatePath`), and point-along-path tracking (`getPointAtLength`):
```tsx
import { evolvePath } from '@remotion/paths';
import { interpolate, useCurrentFrame } from 'remotion';

const frame = useCurrentFrame();
const progress = interpolate(frame, [0, 45], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
const strokeProps = evolvePath(progress, 'M 10 80 Q 95 10 180 80 T 350 80');

<svg width={400} height={160}>
  <path d="M 10 80 Q 95 10 180 80 T 350 80" stroke="#10B981" strokeWidth={8} fill="none" {...strokeProps} />
</svg>
```

---

## 3. Google Fonts (`@remotion/google-fonts`)

Install: `npm i @remotion/google-fonts`

Automatically blocks frame rendering until the web font is downloaded and ready:
```tsx
import { loadFont } from '@remotion/google-fonts/PlusJakartaSans';
import { loadFont as loadMono } from '@remotion/google-fonts/JetBrainsMono';

const { fontFamily } = loadFont('normal', { weights: ['500', '700', '800'], subsets: ['latin'] });
const { fontFamily: monoFamily } = loadMono();
```

---

## 4. Lottie Animations (`@remotion/lottie`)

Install: `npm i @remotion/lottie`

Plays Adobe After Effects `.json` or LottieFiles animations synchronized to `useCurrentFrame()`:
```tsx
import { Lottie, LottieAnimationData } from '@remotion/lottie';
// Always fetch/load the JSON using delayRender/continueRender or static import
<Lottie animationData={badgeAnimationJson} style={{ width: 300, height: 300 }} />
```

---

## 5. 3D Scenes with Three.js (`@remotion/three`)

Install: `npm i @remotion/three three @types/three @react-three/fiber @react-three/drei`

* Always use `<ThreeCanvas width={width} height={height}>` from `@remotion/three` instead of `@react-three/fiber`'s `<Canvas>`.
* Never use R3F's `useFrame()` delta timer for animation; read `const frame = useCurrentFrame()` inside your 3D mesh components!
* When using `<Sequence>` inside `<ThreeCanvas>`, pass `<Sequence layout="none">` because HTML `<div>` wrappers cannot live inside a Three.js scene graph.

---

## 6. Subtitles & Word-by-Word Captions (`@remotion/captions`)

Install: `npm i @remotion/captions`

Groups word-level timestamps into TikTok/Reels-style pages (`createTikTokStyleCaptions`):
```tsx
import { createTikTokStyleCaptions, Caption } from '@remotion/captions';

const { pages } = createTikTokStyleCaptions({
  captions,
  combineTokensWithinMilliseconds: 1200, // Group words into short readable phrases
});
```
* **Always position caption containers inside the platform's CC Safe Band** (`references/social-media-safe-zones.md`) so Instagram/TikTok/Shorts UI never blocks them.

---

## 7. Audio Visualization (`@remotion/media-utils`)

Install: `npm i @remotion/media-utils`

Use `useAudioData(audioSrc)` and `visualizeAudio({ fps, frame, audioData, numberOfSamples: 32 })` to drive beat-reactive bars, bass-pulsing logos, or voiceover waveforms.

---

## 8. Interactive Web Embeds (`@remotion/player`)

Install: `npm i @remotion/player`

Renders any Remotion composition live at 60fps inside a React/Next.js web application without exporting an MP4:
```tsx
import { Player } from '@remotion/player';
import { MainVideo } from './remotion/MainVideo';

<Player
  component={MainVideo}
  inputProps={{ brandId: 'databro', headline: 'Live Interactive Preview' }}
  durationInFrames={300}
  compositionWidth={1920}
  compositionHeight={1080}
  fps={60}
  controls
  loop
  style={{ width: '100%', borderRadius: 12 }}
/>
```

