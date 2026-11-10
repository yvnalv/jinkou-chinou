/**
 * Databro Studio (@databroid / @databro.id : "Belajar Data Science") Isolated Brand Tokens
 * and Standard Base Content Canvas Presets across Social Media Aspect Ratios.
 *
 * Source of Truth for Visual Design (pixel-sampled from the official carousel slides in
 * brand-kit/references/, v0.4.0):
 * - Color Palette: Matte charcoal canvas (#121212), white body text (#FFFFFF), cream wordmark (#F2EFEB),
 *   Lavender question headline (#BB86FC), Teal (#03DAC6), Lime (#C1FF72), Coral warning (#FF5757),
 *   and GitHub Dark code card (#24292E).
 * - Vector Icons: React Icons (react-icons/lu, react-icons/tb, react-icons/fi, react-icons/fa6).
 *   Strictly ban generic AI emojis or clipart.
 * - Punctuation Rule: Never use em-dashes (U+2014) or en-dashes (U+2013) in writing or Closed Captions.
 *   Use colons, hyphens, or arrows.
 * - Voice Tone: Deep, warm baritone (measured F0 ~86-90 Hz), conversational Indonesian ("Kamu/Kita", never "Lo/Gue").
 */

export type DatabroAspectRatioKey = '9:16' | '4:5' | '1:1' | '16:9';

export type DatabroSfxKey =
  | 'keyboard-typing'
  | 'pop-up'
  | 'whoosh-transition'
  | 'mouse-click'
  | 'progress-ticks'
  | 'callout-ding';

export interface DatabroSoundCue {
  /** Global composition frame when this SFX triggers */
  frame: number;
  /** Standard SFX key or custom path inside public/ */
  sfx: DatabroSfxKey | string;
  /** Volume 0.0 to 1.0 (default: 0.55) */
  volume?: number;
  /** Optional duration in frames to trim the sound effect */
  durationInFrames?: number;
}

export interface DatabroCaptionCue {
  text: string;
  startFrame: number;
  endFrame: number;
}

export interface DatabroCanvasPreset {
  id: DatabroAspectRatioKey;
  label: string;
  width: number;
  height: number;
  fps: number;
  /** Persistent top-left Databro lockup (animates ONLY on frame 0..12 of video) */
  logoTopLeft: {
    top: number;
    left: number;
    avatarSize: number;
  };
  /** Persistent top-right social media handle (@databro.id) */
  socialHandleTopRight: {
    top: number;
    right: number;
    text: string;
    color: string;
  };
  /** Content stage box where <TransitionSeries> slides live. Scene content inside it is left-aligned. */
  contentStage: {
    top: number;
    bottom: number;
    left: number;
    right: number;
  };
  /** Fixed Closed Caption coordinate (locked at Y = 1480px on 9:16, zero vertical bounce) */
  closedCaption: {
    y: number;
    left: number;
    right: number;
    fontSize: number;
    maxWordsPerChunk: number;
  };
}

export const DATABRO_CANVAS_PRESETS: Record<
  DatabroAspectRatioKey,
  DatabroCanvasPreset
> = {
  '9:16': {
    id: '9:16',
    label: 'TikTok / Instagram Reels / YouTube Shorts (1080x1920)',
    width: 1080,
    height: 1920,
    fps: 30,
    logoTopLeft: {
      top: 108,
      left: 100,
      avatarSize: 64,
    },
    socialHandleTopRight: {
      top: 108,
      right: 100,
      text: '@databro.id',
      color: '#F2EFEB',
    },
    contentStage: {
      top: 250,
      bottom: 490,
      left: 90,
      right: 90,
    },
    closedCaption: {
      y: 1480, // Exact @databroid TikTok fixed caption line
      left: 110,
      right: 110,
      fontSize: 38,
      maxWordsPerChunk: 4,
    },
  },
  '4:5': {
    id: '4:5',
    label: 'Instagram / LinkedIn Portrait Feed (1080x1350)',
    width: 1080,
    height: 1350,
    fps: 30,
    logoTopLeft: {
      top: 72,
      left: 84,
      avatarSize: 56,
    },
    socialHandleTopRight: {
      top: 72,
      right: 84,
      text: '@databro.id',
      color: '#F2EFEB',
    },
    contentStage: {
      top: 180,
      bottom: 260,
      left: 84,
      right: 84,
    },
    closedCaption: {
      y: 1140,
      left: 96,
      right: 96,
      fontSize: 34,
      maxWordsPerChunk: 4,
    },
  },
  '1:1': {
    id: '1:1',
    label: 'Instagram / LinkedIn Square Feed (1080x1080)',
    width: 1080,
    height: 1080,
    fps: 30,
    logoTopLeft: {
      top: 56,
      left: 72,
      avatarSize: 52,
    },
    socialHandleTopRight: {
      top: 56,
      right: 72,
      text: '@databro.id',
      color: '#F2EFEB',
    },
    contentStage: {
      top: 150,
      bottom: 210,
      left: 72,
      right: 72,
    },
    closedCaption: {
      y: 910,
      left: 84,
      right: 84,
      fontSize: 32,
      maxWordsPerChunk: 4,
    },
  },
  '16:9': {
    id: '16:9',
    label: 'YouTube / Landscape Widescreen (1920x1080)',
    width: 1920,
    height: 1080,
    fps: 30,
    logoTopLeft: {
      top: 64,
      left: 96,
      avatarSize: 56,
    },
    socialHandleTopRight: {
      top: 64,
      right: 96,
      text: '@databro.id',
      color: '#F2EFEB',
    },
    contentStage: {
      top: 160,
      bottom: 200,
      left: 140,
      right: 140,
    },
    closedCaption: {
      y: 920,
      left: 240,
      right: 240,
      fontSize: 36,
      maxWordsPerChunk: 6,
    },
  },
};

/**
 * Duplicate and customize any Databro Base Content Canvas preset across platforms.
 */
export function customizeDatabroCanvas(
  baseKey: DatabroAspectRatioKey,
  overrides: Partial<{
    fps: number;
    logoTopLeft: Partial<DatabroCanvasPreset['logoTopLeft']>;
    socialHandleTopRight: Partial<DatabroCanvasPreset['socialHandleTopRight']>;
    contentStage: Partial<DatabroCanvasPreset['contentStage']>;
    closedCaption: Partial<DatabroCanvasPreset['closedCaption']>;
  }>
): DatabroCanvasPreset {
  const base = DATABRO_CANVAS_PRESETS[baseKey];
  return {
    ...base,
    fps: overrides.fps ?? base.fps,
    logoTopLeft: { ...base.logoTopLeft, ...overrides.logoTopLeft },
    socialHandleTopRight: { ...base.socialHandleTopRight, ...overrides.socialHandleTopRight },
    contentStage: { ...base.contentStage, ...overrides.contentStage },
    closedCaption: { ...base.closedCaption, ...overrides.closedCaption },
  };
}

export type DatabroArchetypeKey =
  | 'code-walkthrough' // Step-by-Step Technical Tutorial
  | 'concept-theory' // Data Science / AI Concept Explainer
  | 'tool-listicle' // Tool / Library Listicle
  | 'launch-showcase' // Product / Feature Launch Reel
  | 'opinion-editorial'; // Career / Opinion Editorial

export type DatabroOpeningStyleKey =
  | 'paradox-headline'
  | 'code-shock'
  | 'visual-data'
  | 'step-roadmap';

export interface DatabroArchetypeSpec {
  id: DatabroArchetypeKey;
  label: string;
  recommendedDuration: '15s' | '30s' | '45s' | '60s';
  recommendedOpening: DatabroOpeningStyleKey;
  visualStageLayout: string;
  recommendedAssets: string[];
}

export const DATABRO_ARCHETYPES: Record<DatabroArchetypeKey, DatabroArchetypeSpec> = {
  'code-walkthrough': {
    id: 'code-walkthrough',
    label: 'Step-by-Step Technical Tutorial (code, terminal, installer walkthrough)',
    recommendedDuration: '60s',
    recommendedOpening: 'code-shock',
    visualStageLayout: 'IDE Card + Dataframe Table + Terminal Command + Step Badges (1, 2, 3)',
    recommendedAssets: [
      'assets/brand-kit/graphics/1.png',
      'assets/brand-kit/graphics/2.png',
      'assets/brand-kit/graphics/3.png',
      'assets/brand-kit/graphics/Table.png',
      'assets/brand-kit/graphics/output.png',
      'assets/brand-kit/graphics/Untitled design.png', // Python Logo
    ],
  },
  'concept-theory': {
    id: 'concept-theory',
    label: 'Data Science / AI Concept Explainer (mental models, 2D diagrams)',
    recommendedDuration: '45s',
    recommendedOpening: 'paradox-headline',
    visualStageLayout: '2D Vector Diagram + React Icons + Highlight Cards (#03DAC6 / #BB86FC / #C1FF72)',
    recommendedAssets: [
      'assets/brand-kit/graphics/Untitled design (1).png', // Scatter plot + trendline
      'assets/brand-kit/logos/DATABRO-01-rev-yvnalv-(Circle).png',
    ],
  },
  'tool-listicle': {
    id: 'tool-listicle',
    label: 'Tool / Library Listicle (e.g. 3 Python Library Wajib Buat Data Engineer)',
    recommendedDuration: '45s',
    recommendedOpening: 'step-roadmap',
    visualStageLayout: 'Numbered Step Badges + One React Icon per Item + One-line Verdict + Mini Code Card',
    recommendedAssets: [
      'assets/brand-kit/graphics/1.png',
      'assets/brand-kit/graphics/2.png',
      'assets/brand-kit/graphics/3.png',
    ],
  },
  'opinion-editorial': {
    id: 'opinion-editorial',
    label: 'Career / Opinion Editorial (roadmaps, career myths, AI news)',
    recommendedDuration: '30s',
    recommendedOpening: 'paradox-headline',
    visualStageLayout: 'Kinetic Typography + High-Contrast Metric Cards + Quote Callouts',
    recommendedAssets: [
      'assets/brand-kit/logos/DATABRO-01-rev-yvnalv-(White)-Landscape.png',
      'assets/brand-kit/logos/DATABRO-01-rev-yvnalv-(Circle).png',
    ],
  },
  'launch-showcase': {
    id: 'launch-showcase',
    label: 'Product / Feature Launch Reel',
    recommendedDuration: '15s',
    recommendedOpening: 'step-roadmap',
    visualStageLayout: '3D UI Perspective Card + Flat Lime Metric Badges + Metric Speedometer (no glow)',
    recommendedAssets: [
      'assets/brand-kit/logos/DATABRO-01-rev-yvnalv-(White).png',
      'assets/databro-avatar.jpg',
    ],
  },
};

export interface DatabroBrandTheme {
  id: 'databro';
  name: 'Databro';
  tagline: 'Belajar Data Science';
  socialHandle: '@databro.id';
  colors: {
    backgroundPrimary: string;
    backgroundElevated: string;
    backgroundSurface: string;
    backgroundCodeCard: string;
    terminalChrome: string;
    textPrimary: string;
    textBrand: string;
    textSecondary: string;
    accentPrimary: string;
    accentSecondary: string;
    accentLavender: string;
    accentCyan: string;
    accentLime: string;
    /** @deprecated Same value as accentLavender. The slides use a single purple. */
    accentViolet: string;
    accentCoralRed: string;
    emblemCircle: string;
    emblemInk: string;
    calloutRed: string;
    semanticSuccess: string;
    semanticWarning: string;
    semanticDanger: string;
    borderSubtle: string;
    borderWhite: string;
    tableHeaderFill: string;
    tableHeaderInk: string;
    tableBorder: string;
    quoteBar: string;
    quoteText: string;
    syntax: {
      keyword: string;
      argument: string;
      number: string;
      comment: string;
      variable: string;
      function: string;
    };
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

export const databroBrand: DatabroBrandTheme = {
  id: 'databro',
  name: 'Databro',
  tagline: 'Belajar Data Science',
  socialHandle: '@databro.id',
  colors: {
    // Values below are pixel-sampled from brand-kit/references/ carousel slides unless noted.
    backgroundPrimary: '#121212', // Matte charcoal canvas
    backgroundElevated: '#1E1E1E', // Card surface (not in slides; keep subtle)
    backgroundSurface: '#1E1E1E',
    backgroundCodeCard: '#24292E', // GitHub Dark code card
    terminalChrome: '#1F1F1F',
    textPrimary: '#FFFFFF', // Body text, sublines, Closed Captions
    textBrand: '#F2EFEB', // "Databro" wordmark, tagline, @databro.id handle
    textSecondary: '#CCCCCC', // Muted labels, diagram strokes
    accentPrimary: '#C1FF72', // Signature lime: "#1:" subheads, "Takeaway quote:", brain icon
    accentSecondary: '#F0ECE2', // Warm cream emblem circle
    accentLavender: '#BB86FC', // Question headlines ("Pernah ngga....", "Apa itu ...?")
    accentCyan: '#03DAC6', // Training / good metrics, table header fill
    accentLime: '#C1FF72', // Alias of accentPrimary
    accentViolet: '#BB86FC', // Deprecated alias of accentLavender
    accentCoralRed: '#FF5757', // Bad metrics ("62%"), pitfalls
    emblemCircle: '#F0ECE2',
    emblemInk: '#121212',
    calloutRed: '#D92D20', // 3px terminal / button callout box (from tutorial reels)
    semanticSuccess: '#03DAC6',
    semanticWarning: '#F59E0B',
    semanticDanger: '#FF5757',
    borderSubtle: '#2E2E2E',
    borderWhite: '#FFFFFF',
    tableHeaderFill: '#03DAC6',
    tableHeaderInk: '#121212',
    tableBorder: '#FFFFFF', // Table cell outlines
    quoteBar: '#CCCCCC', // Left bar of the takeaway quote
    quoteText: '#CED3DA', // Serif takeaway quote text
    syntax: {
      // GitHub Dark theme, as used on the "Implementasi pakai Python" slide
      keyword: '#F97583', // from, import, def
      argument: '#FFAB70', // test_size=, random_state=
      number: '#79B8FF', // 0.30, 42
      comment: '#6A737D', // # Step 1: ...
      variable: '#E1E4E8', // X_train, y_train
      function: '#E1E4E8', // train_test_split
    },
  },
  icons: {
    sourceOfTruth: 'react-icons',
    allowedPackages: ['react-icons/lu', 'react-icons/tb', 'react-icons/fi', 'react-icons/fa6'],
    banned: ['ai-generated-emojis', 'generic-ai-clipart'],
  },
  typography: {
    fontDisplay: 'Plus Jakarta Sans, Inter, system-ui, sans-serif',
    fontBody: 'Inter, Plus Jakarta Sans, system-ui, sans-serif',
    // JetBrains Mono first: loadable via @remotion/google-fonts, so renders match on any machine.
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

/**
 * Standard transition timing buffer rules for Databro videos:
 * Enforces smooth visual settling and clear audio playback without clipping.
 */
export const DATABRO_TRANSITION_TIMING = {
  transitionDurationFrames: 12,
  headDelayFrames: 10, // Settle delay after transition completes before speech starts
  tailDelayFrames: 14, // Speech tail silence buffer before next transition begins
  outroHoldFrames: 24, // Outro hold before video ends
  bgmVolume: 0.08, // Ambient BGM under voiceover
};
