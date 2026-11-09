import React from 'react';
import { interpolate, useCurrentFrame } from 'remotion';
import {
  DATABRO_CANVAS_PRESETS,
  DatabroAspectRatioKey,
  DatabroCanvasPreset,
  DatabroCaptionCue,
  databroBrand,
} from './databro.brand.starter';

export interface DatabroCaptionsProps {
  captions: DatabroCaptionCue[];
  aspectRatio?: DatabroAspectRatioKey;
  presetOverride?: DatabroCanvasPreset;
}

/**
 * Authentic @databroid Cardless Uppercase White Closed Captions (CC).
 *
 * Locked at the exact reference TikTok vertical coordinate (`Y = 1480px` on 1080x1920)
 * at the Root Composition level so captions never bounce vertically or slide away
 * when scenes transition.
 */
export const DatabroCaptions: React.FC<DatabroCaptionsProps> = ({
  captions,
  aspectRatio = '9:16',
  presetOverride,
}) => {
  const frame = useCurrentFrame();
  const preset = presetOverride ?? DATABRO_CANVAS_PRESETS[aspectRatio];

  const active = captions.find(
    (c) => frame >= c.startFrame && frame < c.endFrame
  );
  if (!active) {
    return null;
  }

  // 3-frame opacity cross-fade at the exact fixed Y coordinate (zero vertical movement)
  const fade = interpolate(
    frame,
    [
      active.startFrame,
      active.startFrame + 3,
      active.endFrame - 3,
      active.endFrame,
    ],
    [0.25, 1, 1, 0.25],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
  );

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
        pointerEvents: 'none',
        opacity: fade,
        zIndex: 30,
      }}
    >
      <span
        style={{
          fontFamily: databroBrand.typography.fontDisplay,
          fontSize: preset.closedCaption.fontSize,
          fontWeight: 800,
          letterSpacing: '0.02em',
          lineHeight: 1.2,
          color: databroBrand.colors.textPrimary,
          textTransform: 'uppercase',
        }}
      >
        {active.text}
      </span>
    </div>
  );
};
