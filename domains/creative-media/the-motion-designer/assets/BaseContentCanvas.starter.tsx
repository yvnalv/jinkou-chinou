import React from 'react';
import {
  AbsoluteFill,
  Audio,
  Sequence,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import { BrandTheme } from './brand-tokens.starter';
import {
  AspectRatioKey,
  BaseCanvasLayoutSpec,
  STANDARD_CANVAS_PRESETS,
} from './canvas-presets.starter';

export type StandardSfxKey =
  | 'keyboard-typing'
  | 'pop-up'
  | 'whoosh-transition'
  | 'mouse-click'
  | 'progress-ticks'
  | 'callout-ding';

export interface SoundCueItem {
  /** Global composition frame when this sound effect starts */
  frame: number;
  /** Standard SFX name (loads from public/brand-kit/audio/sfx/<sfx>.wav) or custom staticFile path */
  sfx: StandardSfxKey | string;
  /** Volume between 0.0 and 1.0 (default: 0.55) */
  volume?: number;
  /** Optional duration in frames to trim the sound effect */
  durationInFrames?: number;
}

export interface CaptionPhraseCue {
  text: string;
  startFrame: number;
  endFrame: number;
}

export interface BaseContentCanvasProps {
  brand: BrandTheme;
  /** Select standard aspect ratio ('9:16' | '4:5' | '1:1' | '16:9') or pass a customized layout */
  aspectRatio?: AspectRatioKey;
  layoutOverride?: BaseCanvasLayoutSpec;
  /** Top-left brand logo lockup node (animates in ONLY on frame 0..12, never between scenes) */
  topLeftLogoNode?: React.ReactNode;
  /** Optional top-right fixed icon node */
  topRightNode?: React.ReactNode;
  /** Global closed caption timeline locked at layout.closedCaption.y */
  captions?: CaptionPhraseCue[];
  /** Uppercase cardless caption mode (true for TikTok/CapCut style, false for boxed bar) */
  cardlessCaptions?: boolean;
  /** Frame-accurate TikTok / CapCut sound effect cues */
  soundCues?: SoundCueItem[];
  /** Optional background music path inside public/ (e.g. 'brand-kit/audio/bgm/bgm-ambient.wav') */
  bgmSrc?: string;
  bgmVolume?: number;
  /** Optional full voiceover track path inside public/ */
  voiceoverSrc?: string;
  /** Center stage scene content (typically a <TransitionSeries> with CapCut transitions) */
  children: React.ReactNode;
}

/**
 * Standard Base Content Canvas for all brands and social media aspect ratios.
 *
 * Architecture:
 *  - Layer 0: Solid flat canvas background (never transitions).
 *  - Layer 1: Symmetric horizontally & vertically centered stage hosting <TransitionSeries>.
 *  - Layer 2: Fixed Top-Left Brand Lockup (animates ONLY once at frame 0..12, stays static across slides).
 *  - Layer 3: Fixed Closed Captions locked at `layout.closedCaption.y` (zero vertical bounce).
 *  - Layer 4: Frame-accurate Sound Effects (<Audio /> cues), BGM, and Voiceover track.
 */
export const BaseContentCanvas: React.FC<BaseContentCanvasProps> = ({
  brand,
  aspectRatio = '9:16',
  layoutOverride,
  topLeftLogoNode,
  topRightNode,
  captions = [],
  cardlessCaptions = true,
  soundCues = [],
  bgmSrc,
  bgmVolume = 0.14,
  voiceoverSrc,
  children,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const layout = layoutOverride ?? STANDARD_CANVAS_PRESETS[aspectRatio];

  // Top-left logo animates ONLY once at the start of the video (frame 0..12)
  const logoIntro = spring({
    frame,
    fps,
    config: brand.motion.springs.snappy,
  });
  const logoOpacity = interpolate(frame, [0, 10], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const logoTranslateY = interpolate(logoIntro, [0, 1], [-10, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const activeCaption = captions.find(
    (c) => frame >= c.startFrame && frame < c.endFrame
  );

  // Subtle 3-frame opacity fade on phrase change, zero vertical movement
  const captionOpacity = activeCaption
    ? interpolate(
        frame,
        [
          activeCaption.startFrame,
          activeCaption.startFrame + 3,
          activeCaption.endFrame - 3,
          activeCaption.endFrame,
        ],
        [0.25, 1, 1, 0.25],
        { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
      )
    : 0;

  return (
    <AbsoluteFill style={{ backgroundColor: brand.colors.backgroundPrimary }}>
      {/* LAYER 1: Symmetric Horizontally & Vertically Centered Stage (<TransitionSeries>) */}
      <div
        style={{
          position: 'absolute',
          top: layout.contentStage.top,
          bottom: layout.contentStage.bottom,
          left: layout.contentStage.left,
          right: layout.contentStage.right,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          overflow: 'hidden',
        }}
      >
        {children}
      </div>

      {/* LAYER 2A: Persistent Top-Left Brand Lockup (Only animates at frame 0..12) */}
      {topLeftLogoNode && (
        <div
          style={{
            position: 'absolute',
            top: layout.logoTopLeft.top,
            left: layout.logoTopLeft.left,
            opacity: logoOpacity,
            transform: `translateY(${logoTranslateY}px)`,
            zIndex: 20,
          }}
        >
          {topLeftLogoNode}
        </div>
      )}

      {/* LAYER 2B: Optional Persistent Top-Right Icon Slot */}
      {layout.logoTopRight.enabled && topRightNode && (
        <div
          style={{
            position: 'absolute',
            top: layout.logoTopRight.top,
            right: layout.logoTopRight.right,
            opacity: logoOpacity,
            transform: `translateY(${logoTranslateY}px)`,
            zIndex: 20,
          }}
        >
          {topRightNode}
        </div>
      )}

      {/* LAYER 3: Fixed-Position Closed Captions (Locked at layout.closedCaption.y) */}
      {activeCaption && (
        <div
          style={{
            position: 'absolute',
            top: layout.closedCaption.y,
            left: layout.closedCaption.left,
            right: layout.closedCaption.right,
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            textAlign: 'center',
            pointerEvents: 'none',
            opacity: captionOpacity,
            zIndex: 30,
          }}
        >
          <span
            style={{
              fontFamily: brand.typography.fontDisplay,
              fontSize: layout.closedCaption.fontSize,
              fontWeight: 800,
              letterSpacing: '0.02em',
              lineHeight: 1.2,
              color: brand.colors.textPrimary,
              textTransform: cardlessCaptions ? 'uppercase' : 'none',
              backgroundColor: cardlessCaptions
                ? 'transparent'
                : brand.colors.backgroundElevated,
              padding: cardlessCaptions ? 0 : '12px 24px',
              borderRadius: cardlessCaptions ? 0 : 12,
            }}
          >
            {activeCaption.text}
          </span>
        </div>
      )}

      {/* LAYER 4: Background Music, Voiceover & Frame-Accurate TikTok/CapCut Sound Effects */}
      {bgmSrc && <Audio src={staticFile(bgmSrc)} volume={bgmVolume} loop />}
      {voiceoverSrc && <Audio src={staticFile(voiceoverSrc)} volume={1.0} />}
      {soundCues.map((cue, index) => {
        const resolvedPath = cue.sfx.includes('/')
          ? cue.sfx
          : `brand-kit/audio/sfx/${cue.sfx}.wav`;
        return (
          <Sequence
            key={`${cue.sfx}-${cue.frame}-${index}`}
            from={cue.frame}
            durationInFrames={cue.durationInFrames}
          >
            <Audio src={staticFile(resolvedPath)} volume={cue.volume ?? 0.55} />
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};

