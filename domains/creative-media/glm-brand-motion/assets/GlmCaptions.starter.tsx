import React from 'react';
import { interpolate, useCurrentFrame } from 'remotion';
import {
  GLM_CANVAS_PRESETS,
  GlmAspectRatioKey,
  GlmCanvasPreset,
  GlmCaptionCue,
  glmBrand,
} from './glm.brand.starter';

export interface GlmCaptionsProps {
  captions: GlmCaptionCue[];
  aspectRatio?: GlmAspectRatioKey;
  presetOverride?: GlmCanvasPreset;
}

/**
 * GLM Systems Fixed-Position Closed Captions Component.
 *
 * Locked at a fixed Y coordinate (Y = 920px on 16:9, Y = 1140px on 4:5, Y = 1480px on 9:16)
 * with zero vertical movement. Words transition via smooth opacity cross-fade.
 */
export const GlmCaptions: React.FC<GlmCaptionsProps> = ({
  captions,
  aspectRatio = '16:9',
  presetOverride,
}) => {
  const frame = useCurrentFrame();
  const preset = presetOverride ?? GLM_CANVAS_PRESETS[aspectRatio];

  const currentCue = captions.find(
    (c) => frame >= c.startFrame && frame < c.endFrame
  );

  if (!currentCue) {
    return null;
  }

  const fadeIn = interpolate(
    frame,
    [currentCue.startFrame, currentCue.startFrame + 3],
    [0, 1],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
  );

  const fadeOut = interpolate(
    frame,
    [currentCue.endFrame - 3, currentCue.endFrame],
    [1, 0],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
  );

  const opacity = Math.min(fadeIn, fadeOut);

  return (
    <div
      style={{
        position: 'absolute',
        top: preset.closedCaption.y,
        left: preset.closedCaption.left,
        right: preset.closedCaption.right,
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        textAlign: 'center',
        opacity,
        zIndex: 30,
        pointerEvents: 'none',
      }}
    >
      <div
        style={{
          fontFamily: glmBrand.typography.fontDisplay,
          fontSize: preset.closedCaption.fontSize,
          fontWeight: 800,
          color: glmBrand.colors.textPrimary,
          letterSpacing: '0.02em',
          lineHeight: 1.25,
          textTransform: 'uppercase',
          textShadow: '0 2px 12px rgba(255, 255, 255, 0.8)',
        }}
      >
        {currentCue.text}
      </div>
    </div>
  );
};
