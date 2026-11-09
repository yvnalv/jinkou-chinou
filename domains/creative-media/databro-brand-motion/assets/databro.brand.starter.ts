/**
 * Databro Studio (@databroid — "Belajar Data Science") Isolated Brand Tokens
 * & Standard Base Content Canvas Presets across Social Media Aspect Ratios.
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
  /** Symmetric horizontally & vertically centered stage where <TransitionSeries> slides live */
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
    label: 'Square Feed (1080x1080)',
    width: 1080,
    height: 1080,
    fps: 30,
    logoTopLeft: {
      top: 56,
      left: 72,
      avatarSize: 52,
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
    contentStage: Partial<DatabroCanvasPreset['contentStage']>;
    closedCaption: Partial<DatabroCanvasPreset['closedCaption']>;
  }>
): DatabroCanvasPreset {
  const base = DATABRO_CANVAS_PRESETS[baseKey];
  return {
    ...base,
    fps: overrides.fps ?? base.fps,
    logoTopLeft: { ...base.logoTopLeft, ...overrides.logoTopLeft },
    contentStage: { ...base.contentStage, ...overrides.contentStage },
    closedCaption: { ...base.closedCaption, ...overrides.closedCaption },
  };
}

export type DatabroArchetypeKey =
  | 'code-walkthrough'
  | 'concept-theory'
  | 'opinion-editorial'
  | 'launch-showcase';

export type DatabroOpeningStyleKey =
  | 'paradox-headline'
  | 'code-shock'
  | 'visual-data'
  | 'step-roadmap';

export interface DatabroArchetypeSpec {
  id: DatabroArchetypeKey;
  label: string;
  recommendedDuration: '30s' | '45s' | '60s';
  recommendedOpening: DatabroOpeningStyleKey;
  visualStageLayout: string;
  recommendedAssets: string[];
}

export const DATABRO_ARCHETYPES: Record<DatabroArchetypeKey, DatabroArchetypeSpec> = {
  'code-walkthrough': {
    id: 'code-walkthrough',
    label: 'Hands-on Code & Practical Tool Walkthrough',
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
    label: 'Conceptual, Mental Model & Abstract AI Theory (aibutsimple synthesis)',
    recommendedDuration: '45s',
    recommendedOpening: 'paradox-headline',
    visualStageLayout: '2D Vector Diagram + Scatter Plot Trendline + Kinetic Keywords (#BFFF72)',
    recommendedAssets: [
      'assets/brand-kit/graphics/Untitled design (1).png', // Scatter plot + trendline
      'assets/brand-kit/logos/DATABRO-01-rev-yvnalv-(Circle).png',
    ],
  },
  'opinion-editorial': {
    id: 'opinion-editorial',
    label: 'Tech Opinion, Industry Debate & Career Advice',
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
    label: 'Product, Cloud Feature & Template Drop Showcase',
    recommendedDuration: '30s',
    recommendedOpening: 'step-roadmap',
    visualStageLayout: '3D UI Perspective Card + Ambient Glow + Metric Speedometer',
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
  colors: {
    backgroundPrimary: string;
    backgroundElevated: string;
    terminalChrome: string;
    textPrimary: string;
    textSecondary: string;
    accentPrimary: string;
    accentSecondary: string;
    emblemCircle: string;
    emblemInk: string;
    calloutRed: string;
    semanticSuccess: string;
    semanticWarning: string;
    semanticDanger: string;
    borderSubtle: string;
    // Sampled Authentic Brand Tokens
    dataTeal: string;
    warmCreamTan: string;
    cardDark: string;
    cardBorder: string;
    tableDark: string;
    tableHeader: string;
    tableBorder: string;
    tableText: string;
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
      heavy: { damping: number; stiffness: number; mass: number };
    };
  };
}

export const databroBrand: DatabroBrandTheme = {
  id: 'databro',
  name: 'Databro',
  tagline: 'Belajar Data Science',
  colors: {
    backgroundPrimary: '#111111',
    backgroundElevated: '#0C0C0C',
    terminalChrome: '#1F1F1F',
    textPrimary: '#FFFFFF',
    textSecondary: '#B3B3B3',
    accentPrimary: '#BFFF72', // Signature Electric Lime
    accentSecondary: '#F2EBE1', // Warm Cream
    emblemCircle: '#F0ECE2',
    emblemInk: '#111111',
    calloutRed: '#D92D20', // Error & Gotcha Warning Box
    semanticSuccess: '#BFFF72',
    semanticWarning: '#F59E0B',
    semanticDanger: '#D92D20',
    borderSubtle: '#2E2E2E',
    // Exact sampled tokens from authentic Databro graphics
    dataTeal: '#03DAC6', // Linear regression / scatter plot data points
    warmCreamTan: '#E6DBCF', // Step badge 1.png, 2.png, 3.png cream tint
    cardDark: '#191A1B', // Jupyter / IDE Code Card surface
    cardBorder: '#2C2D2E', // IDE Code Card subtle stroke
    tableDark: '#1F1F1E', // Dataframe table body background
    tableHeader: '#262624', // Dataframe table header background
    tableBorder: '#3B3B39', // Table row separator line
    tableText: '#FAF9F5', // High-contrast table data off-white
  },
  typography: {
    fontDisplay: 'Plus Jakarta Sans, Inter, system-ui, sans-serif',
    fontBody: 'Inter, Plus Jakarta Sans, system-ui, sans-serif',
    fontMono: 'Consolas, JetBrains Mono, monospace',
  },
  motion: {
    springs: {
      snappy: { damping: 18, stiffness: 220, mass: 0.9 },
      smooth: { damping: 24, stiffness: 140, mass: 1.0 },
      bouncy: { damping: 15, stiffness: 240, mass: 0.8 },
      heavy: { damping: 28, stiffness: 90, mass: 1.4 },
    },
  },
};
