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
  GLM_CANVAS_PRESETS,
  GlmAspectRatioKey,
  GlmCanvasPreset,
  glmBrand,
} from './glm.brand.starter';

export interface GlmLogoLockupProps {
  aspectRatio?: GlmAspectRatioKey;
  presetOverride?: GlmCanvasPreset;
  logoSrc?: string;
}

/**
 * Authentic GLM Systems Fixed Top-Left Brand Lockup.
 *
 * Placed at the Root Composition level inside <GlmBaseCanvas /> (OUTSIDE <TransitionSeries>)
 * so it springs in ONLY once at the very beginning of the video (frame 0..12) and stays
 * 100% stationary across all slide/scene transitions.
 */
export const GlmLogoLockup: React.FC<GlmLogoLockupProps> = ({
  aspectRatio = '16:9',
  presetOverride,
  logoSrc = 'brand-kit/logos/GLM-black-Text-Color-Bird.svg',
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const preset = presetOverride ?? GLM_CANVAS_PRESETS[aspectRatio];

  const intro = spring({
    frame,
    fps,
    config: glmBrand.motion.springs.snappy,
  });

  const opacity = interpolate(frame, [0, 10], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const translateY = interpolate(intro, [0, 1], [-10, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <div
      style={{
        position: 'absolute',
        top: preset.logoTopLeft.top,
        left: preset.logoTopLeft.left,
        display: 'flex',
        flexDirection: 'row',
        alignItems: 'center',
        opacity,
        transform: `translateY(${translateY}px)`,
        zIndex: 25,
      }}
    >
      <Img
        src={staticFile(logoSrc)}
        style={{
          width: preset.logoTopLeft.width,
          height: 'auto',
          objectFit: 'contain',
        }}
      />
    </div>
  );
};
