import React from 'react';
import { interpolate, useCurrentFrame } from 'remotion';
import { DATABRO_BRAND, DatabroBrandTheme } from './databro.brand.starter';

export interface DatabroCaptionsProps {
  phrases: string[];
  brand?: DatabroBrandTheme;
  startFrame?: number;
  endFrame?: number;
}

/**
 * Authentic Databro Studio (@databroid) Closed Captions:
 *  - Cardless (zero background pill or border)
 *  - Short 2-to-4 word chunks in ALL-CAPS ExtraBold #FFFFFF
 *  - Horizontally centered at X = 540px, Y = 1180px
 */
export const DatabroCaptions: React.FC<DatabroCaptionsProps> = ({
  phrases,
  brand = DATABRO_BRAND,
  startFrame = 4,
  endFrame = 88,
}) => {
  const frame = useCurrentFrame();

  if (phrases.length === 0 || frame < startFrame || frame > endFrame) {
    return null;
  }

  const indexFloat = interpolate(
    frame,
    [startFrame, endFrame],
    [0, phrases.length - 0.01],
    {
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
    }
  );
  const activeIndex = Math.floor(indexFloat);
  const currentPhrase = phrases[activeIndex] ?? '';

  return (
    <div
      style={{
        position: 'absolute',
        top: brand.layout.ccTop,
        left: brand.layout.stageLeft,
        right: brand.layout.stageRight,
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        textAlign: 'center',
        pointerEvents: 'none',
        zIndex: 55,
      }}
    >
      <span
        style={{
          fontFamily: brand.typography.sans,
          fontSize: 38,
          fontWeight: 800,
          color: brand.colors.white,
          textTransform: 'uppercase',
          letterSpacing: '0.01em',
          lineHeight: 1.25,
        }}
      >
        {currentPhrase}
      </span>
    </div>
  );
};

