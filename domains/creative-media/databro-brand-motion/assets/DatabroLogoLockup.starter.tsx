import React from 'react';
import {
  Img,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import {
  DATABRO_CANVAS_PRESETS,
  DatabroAspectRatioKey,
  DatabroCanvasPreset,
  databroBrand,
} from './databro.brand.starter';

export interface DatabroLogoLockupProps {
  /** Select aspect ratio preset ('9:16' | '4:5' | '1:1' | '16:9') or pass a customized preset */
  aspectRatio?: DatabroAspectRatioKey;
  presetOverride?: DatabroCanvasPreset;
  /** Path inside public/ for the circular Databro avatar */
  avatarSrc?: string;
}

/**
 * Authentic @databroid Fixed Top-Left Brand Lockup.
 *
 * Placed at the Root Composition level inside <DatabroBaseCanvas /> (OUTSIDE <TransitionSeries>)
 * so it springs in ONLY once at the very beginning of the video (frame 0..12) and stays
 * 100% stationary across all slide/scene transitions.
 */
export const DatabroLogoLockup: React.FC<DatabroLogoLockupProps> = ({
  aspectRatio = '9:16',
  presetOverride,
  avatarSrc = 'brand-kit/logos/databro-avatar.jpg',
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const preset = presetOverride ?? DATABRO_CANVAS_PRESETS[aspectRatio];

  const intro = spring({
    frame,
    fps,
    config: databroBrand.motion.springs.snappy,
  });

  const opacity = interpolate(frame, [0, 10], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const translateY = interpolate(intro, [0, 1], [-10, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const avatarSize = preset.logoTopLeft.avatarSize;

  return (
    <div
      style={{
        position: 'absolute',
        top: preset.logoTopLeft.top,
        left: preset.logoTopLeft.left,
        display: 'flex',
        flexDirection: 'row',
        alignItems: 'center',
        gap: 14,
        opacity,
        transform: `translateY(${translateY}px)`,
        zIndex: 25,
      }}
    >
      <div
        style={{
          width: avatarSize,
          height: avatarSize,
          borderRadius: avatarSize / 2,
          backgroundColor: databroBrand.colors.emblemCircle,
          overflow: 'hidden',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          flexShrink: 0,
        }}
      >
        <Img
          src={staticFile(avatarSrc)}
          style={{
            width: '100%',
            height: '100%',
            objectFit: 'cover',
          }}
        />
      </div>

      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
        }}
      >
        <span
          style={{
            fontFamily: databroBrand.typography.fontDisplay,
            fontSize: Math.round(avatarSize * 0.56),
            fontWeight: 700,
            letterSpacing: '-0.02em',
            lineHeight: 1.05,
            color: databroBrand.colors.textPrimary,
          }}
        >
          {databroBrand.name}
        </span>
        <span
          style={{
            fontFamily: databroBrand.typography.fontBody,
            fontSize: Math.round(avatarSize * 0.28),
            fontWeight: 400,
            lineHeight: 1.25,
            color: databroBrand.colors.textSecondary,
          }}
        >
          {databroBrand.tagline}
        </span>
      </div>
    </div>
  );
};
