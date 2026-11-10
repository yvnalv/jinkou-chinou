/**
 * GLM Systems (glmsystems.com : "Intelligent Enterprise Automation") Isolated Brand Tokens
 * and Standard Base Content Canvas Presets across Social Media Aspect Ratios.
 *
 * Official Brand Colors (Source of Truth):
 * - Lime (Primary): #CDFF70 | RGB: 205, 255, 112
 * - Emerald: #003A40 | RGB: 0, 58, 64
 * - Stone Grey: #444547 | RGB: 68, 69, 71
 * - Cool White: #F2F0FA | RGB: 242, 240, 250
 *
 * Vector Icons & Punctuation:
 * - Vector Icons: React Icons (react-icons/lu, react-icons/tb, react-icons/fi). Strictly ban AI clipart/emojis.
 * - Mascot: Flippy (The animated Lime Bird representing the AI agent inside Exact Globe+ & Synergy).
 * - Punctuation Rule: Never use em-dashes (—). Use colons (:), arrows (->), or clean hyphens (-).
 * - Primary Aspect Ratio: 16:9 (Landscape B2B LinkedIn/YouTube) & 4:5 (Portrait Feed).
 */

export type GlmAspectRatioKey = '16:9' | '4:5' | '9:16' | '1:1';

export type GlmSfxKey =
  | 'keyboard-typing'
  | 'pop-up'
  | 'whoosh-transition'
  | 'mouse-click'
  | 'progress-ticks'
  | 'callout-ding';

export interface GlmSoundCue {
  /** Global composition frame when this SFX triggers */
  frame: number;
  /** Standard SFX key or custom path inside public/ */
  sfx: GlmSfxKey | string;
  /** Volume 0.0 to 1.0 (default: 0.55) */
  volume?: number;
  /** Optional duration in frames to trim the sound effect */
  durationInFrames?: number;
}

export interface GlmCaptionCue {
  text: string;
  startFrame: number;
  endFrame: number;
}

export interface GlmCanvasPreset {
  id: GlmAspectRatioKey;
  label: string;
  width: number;
  height: number;
  fps: number;
  /** Persistent top-left GLM lockup */
  logoTopLeft: {
    top: number;
    left: number;
    width: number;
  };
  /** Persistent top-right website handle (glmsystems.com) */
  websiteTopRight: {
    top: number;
    right: number;
    text: string;
    color: string;
  };
  /** Symmetric horizontally and vertically centered stage */
  contentStage: {
    top: number;
    bottom: number;
    left: number;
    right: number;
  };
  /** Fixed Closed Caption coordinate */
  closedCaption: {
    y: number;
    left: number;
    right: number;
    fontSize: number;
    maxWordsPerChunk: number;
  };
}

export const GLM_CANVAS_PRESETS: Record<GlmAspectRatioKey, GlmCanvasPreset> = {
  '16:9': {
    id: '16:9',
    label: 'LinkedIn / YouTube Landscape Widescreen (1920x1080)',
    width: 1920,
    height: 1080,
    fps: 30,
    logoTopLeft: {
      top: 54,
      left: 72,
      width: 160,
    },
    websiteTopRight: {
      top: 54,
      right: 72,
      text: 'glmsystems.com',
      color: '#003A40',
    },
    contentStage: {
      top: 140,
      bottom: 160,
      left: 100,
      right: 100,
    },
    closedCaption: {
      y: 920,
      left: 200,
      right: 200,
      fontSize: 34,
      maxWordsPerChunk: 6,
    },
  },
  '4:5': {
    id: '4:5',
    label: 'LinkedIn / Instagram Portrait Feed (1080x1350)',
    width: 1080,
    height: 1350,
    fps: 30,
    logoTopLeft: {
      top: 64,
      left: 72,
      width: 140,
    },
    websiteTopRight: {
      top: 64,
      right: 72,
      text: 'glmsystems.com',
      color: '#003A40',
    },
    contentStage: {
      top: 160,
      bottom: 240,
      left: 72,
      right: 72,
    },
    closedCaption: {
      y: 1140,
      left: 84,
      right: 84,
      fontSize: 32,
      maxWordsPerChunk: 4,
    },
  },
  '9:16': {
    id: '9:16',
    label: 'YouTube Shorts / Reels / Mobile Vertical (1080x1920)',
    width: 1080,
    height: 1920,
    fps: 30,
    logoTopLeft: {
      top: 96,
      left: 84,
      width: 150,
    },
    websiteTopRight: {
      top: 96,
      right: 84,
      text: 'glmsystems.com',
      color: '#003A40',
    },
    contentStage: {
      top: 220,
      bottom: 440,
      left: 84,
      right: 84,
    },
    closedCaption: {
      y: 1480,
      left: 96,
      right: 96,
      fontSize: 36,
      maxWordsPerChunk: 4,
    },
  },
  '1:1': {
    id: '1:1',
    label: 'Square Feed (1080x1080)',
    width: 1080,
    height: 1080,
    fps: 30,
    logoTopLeft: {
      top: 48,
      left: 60,
      width: 130,
    },
    websiteTopRight: {
      top: 48,
      right: 60,
      text: 'glmsystems.com',
      color: '#003A40',
    },
    contentStage: {
      top: 130,
      bottom: 180,
      left: 60,
      right: 60,
    },
    closedCaption: {
      y: 910,
      left: 72,
      right: 72,
      fontSize: 30,
      maxWordsPerChunk: 4,
    },
  },
};

export function customizeGlmCanvas(
  baseKey: GlmAspectRatioKey,
  overrides: Partial<{
    fps: number;
    logoTopLeft: Partial<GlmCanvasPreset['logoTopLeft']>;
    websiteTopRight: Partial<GlmCanvasPreset['websiteTopRight']>;
    contentStage: Partial<GlmCanvasPreset['contentStage']>;
    closedCaption: Partial<GlmCanvasPreset['closedCaption']>;
  }>
): GlmCanvasPreset {
  const base = GLM_CANVAS_PRESETS[baseKey];
  return {
    ...base,
    fps: overrides.fps ?? base.fps,
    logoTopLeft: { ...base.logoTopLeft, ...overrides.logoTopLeft },
    websiteTopRight: { ...base.websiteTopRight, ...overrides.websiteTopRight },
    contentStage: { ...base.contentStage, ...overrides.contentStage },
    closedCaption: { ...base.closedCaption, ...overrides.closedCaption },
  };
}

export interface GlmBrandTheme {
  id: 'glm';
  name: 'GLM Systems';
  tagline: 'Intelligent Enterprise Automation';
  website: 'glmsystems.com';
  colors: {
    backgroundPrimary: string;
    backgroundSecondary: string;
    backgroundCard: string;
    surfaceEmerald: string;
    surfaceLime: string;
    surfaceStone: string;
    textPrimary: string;
    textSecondary: string;
    textOnDark: string;
    accentPrimary: string;
    accentSecondary: string;
    accentLime: string;
    accentEmerald: string;
    lime: string;
    emerald: string;
    stoneGrey: string;
    coolWhite: string;
    borderSubtle: string;
    borderEmerald: string;
    borderLime: string;
    borderStone: string;
    semanticSuccess: string;
    semanticWarning: string;
    semanticDanger: string;
  };
  icons: {
    sourceOfTruth: 'react-icons';
    allowedPackages: string[];
    banned: string[];
  };
  typography: {
    fontDisplay: string;
    fontDisplayGeist: string;
    fontBody: string;
    fontMono: string;
  };
  motion: {
    springs: {
      snappy: { damping: number; stiffness: number; mass: number };
      smooth: { damping: number; stiffness: number; mass: number };
      bouncy: { damping: number; stiffness: number; mass: number };
      gentle: { damping: number; stiffness: number; mass: number };
    };
  };
}

export const glmBrand: GlmBrandTheme = {
  id: 'glm',
  name: 'GLM Systems',
  tagline: 'Intelligent Enterprise Automation',
  website: 'glmsystems.com',
  colors: {
    backgroundPrimary: '#F2F0FA', // Cool White base (RGB: 242, 240, 250)
    backgroundSecondary: '#003A40', // Deep Emerald (RGB: 0, 58, 64)
    backgroundCard: '#FFFFFF', // Pure White card surface
    surfaceEmerald: '#003A40',
    surfaceLime: '#CDFF70', // Primary Lime (RGB: 205, 255, 112)
    surfaceStone: '#444547', // Stone Grey surface (RGB: 68, 69, 71)
    textPrimary: '#444547', // Stone Grey primary text (RGB: 68, 69, 71)
    textSecondary: '#666666', // Secondary muted text
    textOnDark: '#F2F0FA', // Cool White text on Emerald
    accentPrimary: '#CDFF70', // Signature GLM Lime
    accentSecondary: '#003A40', // Signature GLM Emerald
    accentLime: '#CDFF70',
    accentEmerald: '#003A40',
    lime: '#CDFF70', // Official Lime
    emerald: '#003A40', // Official Emerald
    stoneGrey: '#444547', // Official Stone Grey
    coolWhite: '#F2F0FA', // Official Cool White
    borderSubtle: '#E5E7EB',
    borderEmerald: '#003A40',
    borderLime: '#CDFF70',
    borderStone: '#444547',
    semanticSuccess: '#10B981',
    semanticWarning: '#F59E0B',
    semanticDanger: '#EF4444',
  },
  icons: {
    sourceOfTruth: 'react-icons',
    allowedPackages: ['react-icons/lu', 'react-icons/tb', 'react-icons/fi'],
    banned: ['ai-generated-emojis', 'generic-ai-clipart'],
  },
  typography: {
    fontDisplay: 'Poppins, system-ui, sans-serif',
    fontDisplayGeist: 'Geist, system-ui, sans-serif',
    fontBody: 'Poppins, Inter, system-ui, sans-serif',
    fontMono: 'JetBrains Mono, Consolas, monospace',
  },
  motion: {
    springs: {
      snappy: { damping: 16, stiffness: 180, mass: 0.8 },
      smooth: { damping: 20, stiffness: 120, mass: 1 },
      bouncy: { damping: 12, stiffness: 150, mass: 0.9 },
      gentle: { damping: 24, stiffness: 90, mass: 1 },
    },
  },
};

export const GLM_TRANSITION_TIMING = {
  transitionDurationFrames: 12,
  headDelayFrames: 10,
  tailDelayFrames: 14,
  outroHoldFrames: 24,
};

/**
 * Authentic GLM Geometric Architecture & Motion Preferences
 * Extracted directly from production video glm-flippy-muziek.mp4.
 */
export const GLM_MOTION_PREFERENCES = {
  /** Corner chevron clip paths framing the 1920x1080 canvas */
  chevrons: {
    topLeftEmerald: {
      clipPath: 'polygon(0 0, 160px 0, 356px 190px, 0 563px)',
      transformOrigin: '0 0',
      backgroundColor: '#003A40',
    },
    bottomRightLime: {
      clipPath: 'polygon(1920px 741px, 1528px 1012px, 1572px 1080px, 1920px 1080px)',
      transformOrigin: '1920px 1080px',
      backgroundColor: '#CDFF70',
    },
    scaleContent: 0.55,
    scaleEndCard: 1.0,
  },
  /** Text highlighter underlay bar behind key phrases */
  highlighter: {
    background: 'linear-gradient(transparent 58%, #CDFF70 58%, #CDFF70 92%, transparent 92%)',
    padding: '0 0.08em',
  },
  /** Double shadow elevation for UI demo cards */
  cardShadow: '0 2px 0 3px #003A40, 0 40px 80px rgba(0, 37, 41, 0.22)',
  /** Asymmetric prompt chip with tightened bottom-right corner */
  chip: {
    height: 92,
    borderRadius: '46px 46px 10px 46px',
    backgroundColor: '#CDFF70',
    color: '#100E0D',
    boxShadow: '0 2px 0 3px #003A40, 0 20px 40px rgba(0, 37, 41, 0.18)',
  },
  /** Flippy Mascot vector hinge and flight constants */
  flippy: {
    viewBox: '0 20 500 460',
    wingPivot: { x: 245, y: 281 },
    flightFlapFreqHz: 4.5,
    flightBobAmpPx: 6,
    maxBankingTiltDeg: 14,
  },
  /** 11 Waypoints schedule across 66s video */
  waypoints: [
    { t0: 0, t1: 0, x: 2250, y: 160, s: 1.0, face: 1 },
    { t0: 6.0, t1: 7.9, x: 1420, y: 600, s: 1.0, face: 1, arc: -150 },
    { t0: 17.0, t1: 18.3, x: 300, y: 905, s: 0.5, face: 1, arc: -140 },
    { t0: 41.5, t1: 42.45, x: 790, y: 346, s: 0.42, face: -1, arc: 90 },
    { t0: 43.25, t1: 44.05, x: 790, y: 476, s: 0.42, face: -1, arc: -70 },
    { t0: 44.85, t1: 45.65, x: 790, y: 606, s: 0.42, face: -1, arc: -70 },
    { t0: 46.45, t1: 47.25, x: 790, y: 736, s: 0.42, face: -1, arc: -70 },
    { t0: 48.05, t1: 48.85, x: 790, y: 866, s: 0.42, face: -1, arc: -70 },
    { t0: 51.6, t1: 52.7, x: 1500, y: 560, s: 0.8, face: -1, after: 1, arc: -160 },
    { t0: 56.0, t1: 57.0, x: 1380, y: 560, s: 1.5, face: 1, arc: -90 },
    { t0: 61.7, t1: 62.6, x: 2300, y: -150, s: 1.1, face: -1, arc: -80 },
  ],
};
