import React from 'react';
import { AbsoluteFill, Img, interpolate, staticFile, useCurrentFrame } from 'remotion';
import type { LucideIcon } from 'lucide-react';
import { C, CC_Y, CONTENT_LEFT, CONTENT_RIGHT, MONO, SAFE_LEFT } from '../theme';
import { at, clamp, CUES, ease, FPS, pop } from '../timing';

export const Background: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: C.bg }}>
    <Img src={staticFile('yvnalvworks-grain-bg.png')} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
  </AbsoluteFill>
);

/** Small persistent author lockup below the header safe area. */
export const TopLockup: React.FC = () => {
  const f = useCurrentFrame();
  // Hidden on the last cue, where the end card shows the large lockup.
  const o = Math.min(ease(f, 4, 14), 1 - ease(f, at(CUES.length) - 8, 8));
  if (o <= 0) return null;
  return (
    <div style={{ position: 'absolute', left: SAFE_LEFT, top: 168, display: 'flex', alignItems: 'center', gap: 14, opacity: o }}>
      <Img src={staticFile('yovan-avatar-color.png')} style={{ width: 54, height: 54, borderRadius: '50%' }} />
      <div>
        <div style={{ fontWeight: 600, fontSize: 24, color: C.white, lineHeight: 1.15 }}>yvnalvworks</div>
        <div style={{ fontWeight: 400, fontSize: 19, color: C.ivory, lineHeight: 1.2 }}>@yvnalvworks</div>
      </div>
    </div>
  );
};

/** Burned-in captions: sentence case breath groups (up to two lines), centered on Y=1480 inside the safe width. */
export const Captions: React.FC = () => {
  const f = useCurrentFrame();
  const idx = CUES.findIndex((c, i) => {
    const next = CUES[i + 1];
    const endF = next ? Math.min(c.end * FPS + 9, next.start * FPS) : c.end * FPS + 12;
    return f >= c.start * FPS && f < endF;
  });
  if (idx < 0) return null;
  const cue = CUES[idx];
  const p = pop(f, Math.round(cue.start * FPS), 18);
  return (
    <div style={{ position: 'absolute', left: CONTENT_LEFT, width: CONTENT_RIGHT - CONTENT_LEFT, top: CC_Y - 80, height: 160, display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
      <div
        style={{
          fontWeight: 600, fontSize: 46, lineHeight: 1.2, color: C.white, maxWidth: 840, textAlign: 'center', letterSpacing: '-0.01em',
          background: 'rgba(18,18,18,0.78)', border: `1px solid ${C.border}`, borderRadius: 22, padding: '12px 30px',
          transform: `scale(${0.94 + 0.06 * p}) translateY(${(1 - p) * 10}px)`, opacity: Math.min(1, p * 1.6),
        }}
      >
        {cue.text}
      </div>
    </div>
  );
};

/** Lime wipe that hides a hard cut at frame t. */
export const Wipe: React.FC<{ t: number }> = ({ t }) => {
  const f = useCurrentFrame();
  if (f < t - 10 || f > t + 10) return null;
  const x = interpolate(f, [t - 10, t, t + 10], [-1300, 0, 1300], clamp);
  return <div style={{ position: 'absolute', top: -200, left: -100, width: 1280, height: 2320, background: C.lime, transform: `translateX(${x}px) skewX(-10deg)` }} />;
};

type TileProps = {
  icon: LucideIcon; label?: string; size?: number; color?: string; border?: string; scale?: number; opacity?: number;
  style?: React.CSSProperties; badge?: string; glow?: boolean;
};

/** App-style icon tile built from a Lucide glyph (no third-party logos). */
export const AppTile: React.FC<TileProps> = ({ icon: Icon, label, size = 150, color = C.ivory, border = C.border, scale = 1, opacity = 1, style, badge, glow }) => (
  <div style={{ position: 'absolute', width: size, display: 'flex', flexDirection: 'column', alignItems: 'center', transform: `scale(${scale})`, opacity, ...style }}>
    <div
      style={{
        width: size, height: size, borderRadius: size * 0.27, background: C.card, border: `2px solid ${border}`,
        display: 'flex', alignItems: 'center', justifyContent: 'center', position: 'relative',
        boxShadow: glow ? '0 0 50px rgba(193,255,114,0.28)' : '0 18px 40px rgba(0,0,0,0.35)',
      }}
    >
      <Icon size={size * 0.44} color={color} strokeWidth={2} />
      {badge ? (
        <div style={{ position: 'absolute', top: -14, right: -14, background: C.lime, color: C.bg, fontFamily: MONO, fontSize: 18, padding: '4px 10px', borderRadius: 999 }}>{badge}</div>
      ) : null}
    </div>
    {label ? <div style={{ marginTop: 14, fontSize: 24, fontWeight: 500, color: C.ivory, whiteSpace: 'nowrap' }}>{label}</div> : null}
  </div>
);

/** Small mono tag used to flag illustrative numbers. */
export const Tag: React.FC<{ children: React.ReactNode; style?: React.CSSProperties }> = ({ children, style }) => (
  <div style={{ fontFamily: MONO, fontSize: 17, color: C.muted, letterSpacing: '0.04em', ...style }}>{children}</div>
);
