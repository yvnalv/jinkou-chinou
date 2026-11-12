import React from 'react';
import { AbsoluteFill } from 'remotion';

export interface YvnalvworksBaseCanvasProps {
  children?: React.ReactNode;
  aspectRatio?: '9:16' | '4:5' | '16:9';
  slideNumber?: number;
  totalSlides?: number;
  showWatermark?: boolean;
}

export const YvnalvworksBaseCanvas: React.FC<YvnalvworksBaseCanvasProps> = ({
  children,
  aspectRatio = '9:16',
  slideNumber,
  totalSlides,
  showWatermark = true,
}) => {
  return (
    <AbsoluteFill
      style={{
        backgroundColor: '#121212',
        color: '#F0ECE2',
        fontFamily: "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
        overflow: 'hidden',
      }}
    >
      {/* Top Header / Branding */}
      <div
        style={{
          position: 'absolute',
          top: aspectRatio === '9:16' ? 120 : 60,
          left: 60,
          right: 60,
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          zIndex: 50,
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <img
            src="/assets/logos/yovan-avatar.png"
            alt="Yovan Alvianto"
            style={{ width: 44, height: 44, borderRadius: '50%', border: '1px solid #27272a' }}
          />
          <div>
            <div style={{ fontSize: 18, fontWeight: 700, color: '#FFFFFF', letterSpacing: '-0.02em' }}>
              yvnalvworks
            </div>
            <div style={{ fontSize: 14, color: '#8E8E93', letterSpacing: '-0.01em' }}>
              @yvnalvworks
            </div>
          </div>
        </div>

        {slideNumber && totalSlides && (
          <div
            style={{
              fontSize: 14,
              fontFamily: "'JetBrains Mono', monospace",
              color: '#71717A',
              letterSpacing: '0.05em',
            }}
          >
            {String(slideNumber).padStart(2, '0')} / {String(totalSlides).padStart(2, '0')}
          </div>
        )}
      </div>

      {/* Main Stage Content */}
      <div
        style={{
          position: 'absolute',
          top: aspectRatio === '9:16' ? 240 : 160,
          bottom: aspectRatio === '9:16' ? 320 : 140,
          left: 60,
          right: 60,
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
        }}
      >
        {children}
      </div>

      {/* Footer / Domain Pill */}
      {showWatermark && (
        <div
          style={{
            position: 'absolute',
            bottom: aspectRatio === '9:16' ? 180 : 50,
            left: 60,
            right: 60,
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            fontSize: 14,
            color: '#71717A',
          }}
        >
          <span>yvnalvworks.com</span>
          <span style={{ color: '#C1FF72', fontWeight: 700 }}>SWIPE →</span>
        </div>
      )}
    </AbsoluteFill>
  );
};
