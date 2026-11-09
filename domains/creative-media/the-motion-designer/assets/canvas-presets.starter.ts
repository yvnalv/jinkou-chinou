/**
 * Standard Base Content Canvas Geometry Presets across Social Media Platforms.
 *
 * Modify or duplicate any preset using `customizeCanvasPreset(preset, overrides)`
 * so background color, logo position, closed caption fixed Y-coordinate, and
 * centered content stage remain 100% consistent across videos and aspect ratios.
 */

export type AspectRatioKey = '9:16' | '4:5' | '1:1' | '16:9';

export interface BaseCanvasLayoutSpec {
  id: AspectRatioKey;
  label: string;
  platforms: string[];
  width: number;
  height: number;
  fps: number;
  /** Fixed top-left brand logo lockup position (animates only on video start) */
  logoTopLeft: {
    top: number;
    left: number;
  };
  /** Optional fixed top-right icon/badge position (set enabled: false to hide) */
  logoTopRight: {
    enabled: boolean;
    top: number;
    right: number;
  };
  /**
   * Symmetric horizontally & vertically centered stage where <TransitionSeries>
   * slides live. `left` MUST equal `right` so content is always dead-center.
   */
  contentStage: {
    top: number;
    bottom: number;
    left: number;
    right: number;
  };
  /**
   * Fixed Closed Caption (CC) coordinate. Locked at a single Y coordinate
   * throughout the entire video with zero vertical movement between scenes.
   */
  closedCaption: {
    y: number;
    left: number;
    right: number;
    fontSize: number;
    maxWordsPerChunk: number;
  };
}

export const STANDARD_CANVAS_PRESETS: Record<AspectRatioKey, BaseCanvasLayoutSpec> = {
  '9:16': {
    id: '9:16',
    label: 'Vertical Full-Screen (1080x1920)',
    platforms: ['TikTok', 'Instagram Reels', 'Instagram Stories', 'YouTube Shorts', 'Facebook Reels'],
    width: 1080,
    height: 1920,
    fps: 30,
    logoTopLeft: {
      top: 108,
      left: 100,
    },
    logoTopRight: {
      enabled: false,
      top: 108,
      right: 100,
    },
    contentStage: {
      top: 250,
      bottom: 490,
      left: 90,
      right: 90,
    },
    closedCaption: {
      y: 1480, // Exact @databroid TikTok fixed caption line (440px above bottom edge)
      left: 110,
      right: 110,
      fontSize: 38,
      maxWordsPerChunk: 4,
    },
  },
  '4:5': {
    id: '4:5',
    label: 'Portrait Feed (1080x1350)',
    platforms: ['Instagram Feed Portrait', 'LinkedIn Vertical Feed', 'Facebook Feed'],
    width: 1080,
    height: 1350,
    fps: 30,
    logoTopLeft: {
      top: 72,
      left: 84,
    },
    logoTopRight: {
      enabled: false,
      top: 72,
      right: 84,
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
    platforms: ['Instagram Square', 'LinkedIn Square', 'X / Twitter Square'],
    width: 1080,
    height: 1080,
    fps: 30,
    logoTopLeft: {
      top: 56,
      left: 72,
    },
    logoTopRight: {
      enabled: false,
      top: 56,
      right: 72,
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
    label: 'Landscape Widescreen (1920x1080)',
    platforms: ['YouTube 16:9', 'LinkedIn Landscape', 'X / Twitter Video', 'Website Hero'],
    width: 1920,
    height: 1080,
    fps: 30,
    logoTopLeft: {
      top: 64,
      left: 96,
    },
    logoTopRight: {
      enabled: false,
      top: 64,
      right: 96,
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
 * Duplicate and customize any standard canvas preset while preserving type safety
 * and enforcing symmetric left === right centering on the content stage.
 */
export function customizeCanvasPreset(
  baseKey: AspectRatioKey,
  overrides: Partial<{
    fps: number;
    logoTopLeft: Partial<BaseCanvasLayoutSpec['logoTopLeft']>;
    logoTopRight: Partial<BaseCanvasLayoutSpec['logoTopRight']>;
    contentStage: Partial<BaseCanvasLayoutSpec['contentStage']>;
    closedCaption: Partial<BaseCanvasLayoutSpec['closedCaption']>;
  }>
): BaseCanvasLayoutSpec {
  const base = STANDARD_CANVAS_PRESETS[baseKey];
  return {
    ...base,
    fps: overrides.fps ?? base.fps,
    logoTopLeft: { ...base.logoTopLeft, ...overrides.logoTopLeft },
    logoTopRight: { ...base.logoTopRight, ...overrides.logoTopRight },
    contentStage: { ...base.contentStage, ...overrides.contentStage },
    closedCaption: { ...base.closedCaption, ...overrides.closedCaption },
  };
}

