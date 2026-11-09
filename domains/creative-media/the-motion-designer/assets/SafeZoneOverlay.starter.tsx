/**
 * Studio Safe-Zone Overlay Guide for Social Media UI Dead Zones.
 * Renders semi-transparent overlays showing where Instagram, TikTok, YouTube, etc.
 * place their native UI buttons, captions, and 4:5 feed crops.
 *
 * Automatically hides itself when `useRemotionEnvironment().isRendering === true`
 * so the guide never appears in exported MP4/MOV/GIF files.
 */

import React from 'react';
import { AbsoluteFill, useRemotionEnvironment } from 'remotion';
import { PlatformPresetId, SAFE_ZONES } from './brand-tokens.starter';

export interface SafeZoneOverlayProps {
  platform: PlatformPresetId;
  enabled?: boolean;
}

export const SafeZoneOverlay: React.FC<SafeZoneOverlayProps> = ({
  platform,
  enabled = true,
}) => {
  const { isRendering } = useRemotionEnvironment();

  if (isRendering || !enabled) {
    return null;
  }

  const zone = SAFE_ZONES[platform];
  const { top, bottom, left, right } = zone.insets;
  const ccHeight = zone.ccBand.bottom - zone.ccBand.top;

  return (
    <AbsoluteFill style={{ pointerEvents: 'none', zIndex: 9999, fontFamily: 'monospace' }}>
      {/* Top Platform Header Dead Zone */}
      <div
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          height: top,
          backgroundColor: 'rgba(239, 68, 68, 0.22)',
          borderBottom: '2px dashed rgba(239, 68, 68, 0.8)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          color: '#FCA5A5',
          fontSize: 18,
          fontWeight: 700,
        }}
      >
        TOP UI DEAD ZONE ({top}px): Status Bar / Header / 4:5 Crop
      </div>

      {/* Bottom Platform Caption / Scrubber Dead Zone */}
      <div
        style={{
          position: 'absolute',
          bottom: 0,
          left: 0,
          right: 0,
          height: bottom,
          backgroundColor: 'rgba(239, 68, 68, 0.22)',
          borderTop: '2px dashed rgba(239, 68, 68, 0.8)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          color: '#FCA5A5',
          fontSize: 18,
          fontWeight: 700,
        }}
      >
        BOTTOM UI DEAD ZONE ({bottom}px): Handle / Caption / Audio / Scrubber
      </div>

      {/* Right Engagement Icons Stack Dead Zone */}
      <div
        style={{
          position: 'absolute',
          top,
          bottom,
          right: 0,
          width: right,
          backgroundColor: 'rgba(245, 158, 11, 0.22)',
          borderLeft: '2px dashed rgba(245, 158, 11, 0.85)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          writingMode: 'vertical-rl',
          color: '#FDE68A',
          fontSize: 16,
          fontWeight: 700,
        }}
      >
        RIGHT UI STACK ({right}px): Like / Comment / Repost / Share
      </div>

      {/* Symmetric Left Margin */}
      <div
        style={{
          position: 'absolute',
          top,
          bottom,
          left: 0,
          width: left,
          backgroundColor: 'rgba(245, 158, 11, 0.14)',
          borderRight: '1px dashed rgba(245, 158, 11, 0.6)',
        }}
      />

      {/* Safe Closed Caption (CC) Band */}
      <div
        style={{
          position: 'absolute',
          top: zone.ccBand.top,
          left: zone.ccBand.left,
          right: zone.ccBand.right,
          height: ccHeight,
          backgroundColor: 'rgba(16, 185, 129, 0.16)',
          border: '2px dashed rgba(16, 185, 129, 0.85)',
          borderRadius: 12,
          display: 'flex',
          alignItems: 'flex-start',
          justifyContent: 'flex-end',
          padding: '6px 12px',
          color: '#6EE7B7',
          fontSize: 15,
          fontWeight: 700,
        }}
      >
        CC / SUBTITLE SAFE BAND (Y: {zone.ccBand.top} to {zone.ccBand.bottom}px)
      </div>

      {/* Optional 4:5 Instagram Home Feed Crop Indicator */}
      {zone.feedCrop4x5 && (
        <div
          style={{
            position: 'absolute',
            top: zone.feedCrop4x5.top,
            bottom: zone.feedCrop4x5.bottom,
            left: 0,
            right: 0,
            borderTop: '2px solid rgba(56, 189, 248, 0.85)',
            borderBottom: '2px solid rgba(56, 189, 248, 0.85)',
          }}
        />
      )}
    </AbsoluteFill>
  );
};
