/**
 * Reference Frame-Deterministic Remotion Scene.
 * Demonstrates:
 *  - 100% `useCurrentFrame()` driven animation (zero CSS transitions or timers)
 *  - Clamped `interpolate()` and physical `spring()` presets
 *  - Isolated `BrandTheme` tokens
 *  - Platform UI Safe-Zone container + Closed Caption (CC) safe band placement
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

  // Staggered spring entrances (0f -> badge, 6f -> headline, 14f -> card)
  const badgeProgress = spring({ frame, fps, delay: 0, config: springConfig });
  const titleProgress = spring({ frame, fps, delay: 6, config: springConfig });
  const cardProgress = spring({ frame, fps, delay: 14, config: SPRING_PRESETS.smooth });

  const titleTranslateY = interpolate(titleProgress, [0, 1], [36, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const cardScale = interpolate(cardProgress, [0, 1], [0.92, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const ccOpacity = interpolate(frame, [12, 24], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: brand.colors.backgroundPrimary,
        color: brand.colors.textPrimary,
        fontFamily: brand.typography.bodyFontFamily,
      }}
    >
      {/* Safe Content Box — Guaranteed clear of Top, Bottom, Left, and Right UI Overlays */}
      <div
        style={{
          position: 'absolute',
          top: safeZone.insets.top,
          bottom: safeZone.insets.bottom,
          left: safeZone.insets.left,
          right: safeZone.insets.right,
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'flex-start',
          paddingTop: 24,
        }}
      >
        {/* Brand Badge */}
        <div
          style={{
            alignSelf: 'flex-start',
            backgroundColor: brand.colors.surfaceCard,
            border: `1px solid ${brand.colors.surfaceBorder}`,
            borderRadius: 999,
            padding: '10px 22px',
            fontSize: 22,
            fontWeight: 700,
            color: brand.colors.accentSecondary,
            opacity: badgeProgress,
            transform: `scale(${interpolate(badgeProgress, [0, 1], [0.85, 1], {
              extrapolateLeft: 'clamp',
              extrapolateRight: 'clamp',
            })})`,
            marginBottom: 28,
          }}
        >
          {brand.displayName}
        </div>

        {/* Main Headline */}
        <h1
          style={{
            fontFamily: brand.typography.headingFontFamily,
            fontWeight: brand.typography.headingWeight,
            letterSpacing: brand.typography.letterSpacingHeading,
            fontSize: safeZone.aspectRatio === '16:9' ? 68 : 60,
            lineHeight: 1.12,
            margin: '0 0 20px 0',
            opacity: titleProgress,
            transform: `translateY(${titleTranslateY}px)`,
          }}
        >
          {headline}
        </h1>

        {/* Feature Card */}
        <div
          style={{
            marginTop: 16,
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

      {/* Closed Caption (CC) Safe Band — Never blocked by Instagram/TikTok/Shorts UI */}
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
              color: brand.captions.textColor,
              borderRadius: brand.captions.borderRadius,
              padding: '14px 24px',
              fontSize: 30,
              fontWeight: 700,
              textAlign: 'center',
              lineHeight: 1.3,
              boxShadow: '0 8px 24px rgba(0, 0, 0, 0.35)',
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

