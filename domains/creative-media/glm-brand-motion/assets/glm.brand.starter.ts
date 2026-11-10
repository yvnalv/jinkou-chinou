/**
 * GLM Systems (glmsystems.com : "Intelligent Enterprise Automation") Isolated Brand Tokens
 * and Standard Base Content Canvas Presets across Social Media Aspect Ratios.
 *
 * Source of Truth for Visual Design:
 * - Color Palette: Emerald (#003A40), Lime (#CDFF70), Cool White (#F1F0FA), Dark Charcoal (#111827).
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
    textPrimary: string;
    textSecondary: string;
    textOnDark: string;
    accentPrimary: string;
    accentSecondary: string;
    accentLime: string;
    accentEmerald: string;
    borderSubtle: string;
    borderEmerald: string;
    borderLime: string;
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
    backgroundPrimary: '#F1F0FA', // Cool White base
    backgroundSecondary: '#003A40', // Deep Emerald
    backgroundCard: '#FFFFFF', // Pure White card surface
    surfaceEmerald: '#003A40',
    surfaceLime: '#CDFF70',
    textPrimary: '#111827', // Dark Charcoal
    textSecondary: '#4B5563', // Muted Slate Gray
    textOnDark: '#F1F0FA', // Cool White text on Emerald
    accentPrimary: '#CDFF70', // Signature GLM Lime
    accentSecondary: '#003A40', // Signature GLM Emerald
    accentLime: '#CDFF70',
    accentEmerald: '#003A40',
    borderSubtle: '#E5E7EB',
    borderEmerald: '#003A40',
    borderLime: '#CDFF70',
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
