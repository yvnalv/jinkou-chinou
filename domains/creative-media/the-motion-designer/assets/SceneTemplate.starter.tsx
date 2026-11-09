/**
 * Reference Frame-Deterministic Remotion Scene.
 * Demonstrates:
 *  - 100% `useCurrentFrame()` driven animation (zero CSS transitions or timers)
 *  - Fixed Top-Left Brand Logo & Top-Right Geometric SVG Icon Header
 *  - Vertically & Horizontally Centered Main Content Container (`left === right`)
 *  - Solid flat semantic color tokens (zero CSS gradients, zero em-dashes, sentence case)
 *  - Horizontally Centered Closed Captions (CC) in the Platform Safe Band
 */

import React from 'react';
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import {
  BrandTheme,
  DEFAULT_NEUTRAL_BRAND,
  PlatformPresetId,
  SAFE_ZONES,
  SPRING_PRESETS,
} from './brand-tokens.starter';
import { SafeZoneOverlay } from './SafeZoneOverlay.starter';

export interface SceneTemplateProps {
  headline: string;
  subheadline: string;
  captionText?: string;
  platform: PlatformPresetId;
  brand?: BrandTheme;
  showSafeZoneGuide?: boolean;
}

export const SceneTemplate: React.FC<SceneTemplateProps> = ({
  headline,
  subheadline,
  captionText,
  platform,
  brand = DEFAULT_NEUTRAL_BRAND,
  showSafeZoneGuide = false,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const safeZone = SAFE_ZONES[platform];
  const springConfig = SPRING_PRESETS[brand.motion.defaultSpring];

  const headerProgress = spring({ frame, fps, delay: 0, config: springConfig });
  const titleProgress = spring({ frame, fps, delay: 6, config: springConfig });
  const cardProgress = spring({ frame, fps, delay: 14, config: SPRING_PRESETS.smooth });

  const titleTranslateY = interpolate(titleProgress, [0, 1], [32, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const cardScale = interpolate(cardProgress, [0, 1], [0.94, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const ccOpacity = interpolate(frame, [10, 22], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const headerHeight = 56;
  const stageTop = safeZone.insets.top + headerHeight + 16;
  const stageBottom = safeZone.height - safeZone.ccBand.top + 16;

  return (
    <AbsoluteFill
      style={{
        backgroundColor: brand.colors.backgroundPrimary,
        color: brand.colors.textPrimary,
        fontFamily: brand.typography.bodyFontFamily,
      }}
    >
      {/* Fixed Top Header: Top-Left Logo & Top-Right Geometric SVG Icon */}
      <div
        style={{
          position: 'absolute',
          top: safeZone.insets.top,
          left: safeZone.insets.left,
          right: safeZone.insets.right,
          height: headerHeight,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          opacity: headerProgress,
        }}
      >
        {/* Top-Left Brand Wordmark */}
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: 12,
          }}
        >
          <div
            style={{
              width: 16,
              height: 16,
              borderRadius: 4,
              backgroundColor: brand.colors.accentPrimary,
            }}
          />
          <span
            style={{
              fontFamily: brand.typography.headingFontFamily,
              fontSize: 24,
              fontWeight: 700,
              color: brand.colors.textPrimary,
              letterSpacing: '-0.02em',
            }}
          >
            {brand.displayName}
          </span>
        </div>

        {/* Top-Right Geometric SVG Icon */}
        <div
          style={{
            width: 44,
            height: 44,
            borderRadius: 12,
            backgroundColor: brand.colors.surfaceCard,
            border: `1px solid ${brand.colors.surfaceBorder}`,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}
        >
          <svg
            width={22}
            height={22}
            viewBox="0 0 24 24"
            fill="none"
            stroke={brand.colors.accentPrimary}
            strokeWidth={2}
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <rect x="3" y="3" width="7" height="7" rx="1" />
            <rect x="14" y="3" width="7" height="7" rx="1" />
            <rect x="14" y="14" width="7" height="7" rx="1" />
            <rect x="3" y="14" width="7" height="7" rx="1" />
          </svg>
        </div>
      </div>

      {/* Vertically & Horizontally Centered Main Content Container */}
      <div
        style={{
          position: 'absolute',
          top: stageTop,
          bottom: stageBottom,
          left: safeZone.insets.left,
          right: safeZone.insets.right,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          textAlign: 'center',
          gap: 24,
        }}
      >
        {/* Main Headline in Sentence Case */}
        <h1
          style={{
            fontFamily: brand.typography.headingFontFamily,
            fontWeight: brand.typography.headingWeight,
            letterSpacing: brand.typography.letterSpacingHeading,
            fontSize: safeZone.aspectRatio === '16:9' ? 64 : 56,
            lineHeight: 1.12,
            margin: 0,
            opacity: titleProgress,
            transform: `translateY(${titleTranslateY}px)`,
          }}
        >
          {headline}
        </h1>

        {/* Solid Elevated Feature Card */}
        <div
          style={{
            width: '100%',
            backgroundColor: brand.colors.surfaceCard,
            border: `1px solid ${brand.colors.surfaceBorder}`,
            borderRadius: brand.motion.cardBorderRadius,
            padding: 32,
            opacity: cardProgress,
            transform: `scale(${cardScale})`,
          }}
        >
          <p
            style={{
              fontSize: 28,
              lineHeight: 1.45,
              color: brand.colors.textSecondary,
              margin: 0,
            }}
          >
            {subheadline}
          </p>
        </div>
      </div>

      {/* Horizontally Centered Closed Captions (CC) Safe Band */}
      {captionText && (
        <div
          style={{
            position: 'absolute',
            top: safeZone.ccBand.top,
            left: safeZone.ccBand.left,
            right: safeZone.ccBand.right,
            height: safeZone.ccBand.bottom - safeZone.ccBand.top,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            opacity: ccOpacity,
          }}
        >
          <div
            style={{
              backgroundColor: brand.captions.backgroundColor,
              border: `1px solid ${brand.colors.surfaceBorder}`,
              color: brand.captions.textColor,
              borderRadius: brand.captions.borderRadius,
              padding: '14px 24px',
              fontSize: 28,
              fontWeight: 600,
              textAlign: 'center',
              lineHeight: 1.35,
            }}
          >
            {captionText}
          </div>
        </div>
      )}

      {/* Studio-Only Safe-Zone Guide (Auto-hidden during MP4/MOV export) */}
      <SafeZoneOverlay platform={platform} enabled={showSafeZoneGuide} />
    </AbsoluteFill>
  );
};
