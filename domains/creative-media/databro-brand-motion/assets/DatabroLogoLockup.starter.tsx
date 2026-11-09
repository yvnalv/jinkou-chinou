import React from 'react';
import { Img, staticFile } from 'remotion';
import { DATABRO_BRAND, DatabroBrandTheme } from './databro.brand.starter';

export interface DatabroLogoLockupProps {
  brand?: DatabroBrandTheme;
}

/**
 * Authentic Databro Studio (@databroid) Top-Left Fixed Brand Lockup:
 *  - Circular Warm Cream (#F2EBE1) illustrated avatar
 *  - Stacked "Databro" (Bold White) + "Belajar Data Science" (Light Gray)
 *  - No top-right box or clutter
 */
export const DatabroLogoLockup: React.FC<DatabroLogoLockupProps> = ({
  brand = DATABRO_BRAND,
}) => {
  return (
    <div
      style={{
        position: 'absolute',
        top: brand.layout.logoTop,
        left: brand.layout.logoLeft,
        display: 'flex',
        alignItems: 'center',
        gap: 16,
        zIndex: 60,
      }}
    >
      <div
        style={{
          width: 68,
          height: 68,
          borderRadius: '50%',
          backgroundColor: brand.colors.cream,
          overflow: 'hidden',
          flexShrink: 0,
        }}
      >
        <Img
          src={staticFile(brand.avatarFile)}
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
            fontFamily: brand.typography.sans,
            fontSize: 38,
            fontWeight: 700,
            color: brand.colors.white,
            lineHeight: 1.05,
            letterSpacing: '-0.02em',
          }}
        >
          {brand.displayName}
        </span>
        <span
          style={{
            fontFamily: brand.typography.sans,
            fontSize: 19,
            fontWeight: 400,
            color: brand.colors.muted,
            lineHeight: 1.25,
            marginTop: 2,
          }}
        >
          {brand.subtitle}
        </span>
      </div>
    </div>
  );
};

