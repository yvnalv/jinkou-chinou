import { Easing, interpolate, spring } from 'remotion';
import cues from './data/captions.json';

// Every beat is keyed to a caption cue, so re-timing captions.json (after recording
// the voiceover) re-syncs the whole animation on the next render.
export const FPS = 30;
export type Cue = { id: number; start: number; end: number; text: string };
export const CUES = cues as Cue[];

/** First frame of caption cue `id` (1-based). */
export const at = (id: number) => Math.round(CUES[id - 1].start * FPS);
/** Last frame of caption cue `id`. */
export const until = (id: number) => Math.round(CUES[id - 1].end * FPS);
export const TOTAL_FRAMES = Math.round((CUES[CUES.length - 1].end + 2.2) * FPS);

export const clamp = { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' } as const;

/** Springy 0 -> 1 starting at frame `start`. */
export const pop = (f: number, start: number, damping = 14) =>
  spring({ frame: f - start, fps: FPS, config: { damping, stiffness: 170, mass: 0.8 } });

/** Smooth eased 0 -> 1 over `dur` frames from `start`. */
export const ease = (f: number, start: number, dur = 15) =>
  interpolate(f, [start, start + dur], [0, 1], { ...clamp, easing: Easing.bezier(0.22, 1, 0.36, 1) });

/** 0 -> 1 -> 0 visibility window with fades. */
export const span = (f: number, start: number, end: number, fadeIn = 10, fadeOut = 10) =>
  Math.min(ease(f, start, fadeIn), 1 - ease(f, end - fadeOut, fadeOut));

export const mix = (a: number, b: number, t: number) => a + (b - a) * t;

/** Deterministic pseudo-random in [0, 1). */
export const rand = (seed: number) => {
  const x = Math.sin(seed * 127.1 + 311.7) * 43758.5453;
  return x - Math.floor(x);
};
