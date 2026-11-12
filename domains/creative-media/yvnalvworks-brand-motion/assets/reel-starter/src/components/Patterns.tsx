import React from 'react';
import { AbsoluteFill, Img, staticFile, useCurrentFrame } from 'remotion';
import { Check, UserPlus } from 'lucide-react';
import type { LucideIcon } from 'lucide-react';
import { C, CENTER_X, MONO } from '../theme';
import { at, CUES, ease, mix, pop, span } from '../timing';
import { Tag } from './Base';

/** A scene panel that slides in from the right and fades out before `end`. */
export const Panel: React.FC<{ start: number; end: number; children: React.ReactNode }> = ({ start, end, children }) => {
  const f = useCurrentFrame();
  const o = span(f, start, end, 12, 8);
  if (o <= 0) return null;
  const x = (1 - ease(f, start, 16)) * 70 - ease(f, end - 8, 8) * 40;
  return <div style={{ position: 'absolute', inset: 0, opacity: o, transform: `translateX(${x}px)` }}>{children}</div>;
};

/** Mono kicker (e.g. "STEP 02 / 06") above a Poppins Bold title. Left-aligned inside the block. */
export const StepHeading: React.FC<{ kicker: string; title: React.ReactNode; left: number; top?: number; width: number }> = ({ kicker, title, left, top = 330, width }) => (
  <div style={{ position: 'absolute', left, top, width }}>
    <div style={{ fontFamily: MONO, fontSize: 22, color: C.lime, letterSpacing: '0.06em' }}>{kicker}</div>
    <div style={{ marginTop: 10, fontWeight: 700, fontSize: 54, lineHeight: 1.06, letterSpacing: '-0.035em', color: C.white }}>{title}</div>
  </div>
);

/** Phone or app window mockup, centered on x=540. Children are positioned inside it. */
export const PhoneFrame: React.FC<{ title: string; live?: number; top?: number; width?: number; height?: number; shake?: number; children: React.ReactNode }> = ({ title, live = 0, top = 330, width = 620, height = 1000, shake = 0, children }) => {
  const f = useCurrentFrame();
  const enter = pop(f, 0, 16);
  return (
    <div style={{ position: 'absolute', left: CENTER_X - width / 2, top, width, height, borderRadius: 60, background: C.card, border: `2px solid ${C.border}`, overflow: 'hidden', opacity: enter, boxShadow: '0 40px 120px rgba(0,0,0,0.55)', transform: `translate(${shake}px, ${(1 - enter) * 80}px) scale(${0.92 + 0.08 * enter})` }}>
      <div style={{ position: 'absolute', top: 30, left: 36, right: 36, display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div style={{ display: 'flex', gap: 10 }}>{[0, 1, 2].map((d) => <div key={d} style={{ width: 14, height: 14, borderRadius: '50%', background: C.borderHi }} />)}</div>
        <div style={{ fontFamily: MONO, fontSize: 20, color: C.sec }}>{title}</div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8, opacity: live, fontFamily: MONO, fontSize: 20, color: C.lime }}>
          <div style={{ width: 12, height: 12, borderRadius: '50%', background: C.lime }} /> live
        </div>
      </div>
      {children}
    </div>
  );
};

/** Line chart that draws itself; an optional second series (e.g. a crash) draws in red. */
export const LineChart: React.FC<{ good: number[]; bad?: number[]; pGood: number; pBad?: number; width: number; height: number; label: string; value?: string; style?: React.CSSProperties }> = ({ good, bad = [], pGood, pBad = 0, width, height, label, value, style }) => {
  const n = good.length + Math.max(bad.length - 1, 0) - 1;
  const pt = (i: number, v: number) => `${(i / n) * width},${height - (v / 100) * height}`;
  const goodPath = 'M' + good.map((v, i) => pt(i, v)).join(' L');
  const badPath = bad.length ? 'M' + bad.map((v, i) => pt(good.length - 1 + i, v)).join(' L') : '';
  return (
    <div style={{ background: C.bg, borderRadius: 28, border: `2px solid ${C.border}`, padding: '22px 24px', position: 'relative', ...style }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline' }}>
        <div style={{ fontFamily: MONO, fontSize: 20, color: C.sec }}>{label}</div>
        {value ? <div style={{ fontWeight: 700, fontSize: 46, color: pBad > 0.3 ? C.danger : C.lime, letterSpacing: '-0.03em' }}>{value}</div> : null}
      </div>
      <svg width={width} height={height + 10} style={{ marginTop: 14, overflow: 'visible' }}>
        {[0.25, 0.5, 0.75].map((g) => <line key={g} x1={0} x2={width} y1={height * g} y2={height * g} stroke={C.border} strokeWidth={1.5} strokeDasharray="4 8" />)}
        <path d={goodPath} pathLength={1} fill="none" stroke={C.lime} strokeWidth={5} strokeLinecap="round" strokeLinejoin="round" strokeDasharray={1} strokeDashoffset={1 - pGood} />
        {badPath ? <path d={badPath} pathLength={1} fill="none" stroke={C.danger} strokeWidth={5} strokeLinecap="round" strokeLinejoin="round" strokeDasharray={1} strokeDashoffset={1 - pBad} /> : null}
      </svg>
      <Tag style={{ position: 'absolute', right: 24, bottom: 16 }}>illustrative</Tag>
    </div>
  );
};

/** Progress meter, e.g. "Evals passing 4 / 6". `value` may be fractional while animating. */
export const Meter: React.FC<{ icon: LucideIcon; label: string; value: number; total: number; left: number; top: number; width: number; opacity?: number }> = ({ icon: Icon, label, value, total, left, top, width, opacity = 1 }) => {
  const shown = Math.round(value);
  return (
    <div style={{ position: 'absolute', left, top, width, opacity }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12, fontFamily: MONO, fontSize: 21, color: C.sec }}><Icon size={26} color={C.lime} strokeWidth={2} /> {label}</div>
        <div style={{ fontWeight: 700, fontSize: 34, color: shown === total ? C.lime : C.white }}>{shown} / {total}</div>
      </div>
      <div style={{ marginTop: 12, height: 14, borderRadius: 999, background: C.border, overflow: 'hidden' }}>
        <div style={{ width: `${(value / total) * 100}%`, height: '100%', borderRadius: 999, background: C.lime }} />
      </div>
      <Tag style={{ marginTop: 8, textAlign: 'right' }}>illustrative</Tag>
    </div>
  );
};

/** Vertical step rail: done steps get a lime check, the active step glows lime. */
export const StepRail: React.FC<{ icons: LucideIcon[]; active: number; x: number; top: number; gap: number; size?: number }> = ({ icons, active, x, top, gap, size = 84 }) => {
  const f = useCurrentFrame();
  const bottom = top + gap * (icons.length - 1);
  const fill = active < 0 ? 0 : (active / (icons.length - 1)) * (bottom - top);
  return (
    <>
      <svg width={1080} height={1920} style={{ position: 'absolute', inset: 0 }}>
        <line x1={x} x2={x} y1={top} y2={bottom} stroke={C.border} strokeWidth={4} strokeLinecap="round" />
        <line x1={x} x2={x} y1={top} y2={top + fill} stroke={C.lime} strokeWidth={4} strokeLinecap="round" />
      </svg>
      {icons.map((Icon, i) => {
        const isActive = i === active;
        const done = i < active;
        return (
          <div key={i} style={{ position: 'absolute', left: x - size / 2, top: top + i * gap - size / 2, width: size, height: size, transform: `scale(${pop(f, 6 + i * 5) * (isActive ? 1.1 : 1)})` }}>
            <div style={{ width: size, height: size, borderRadius: '50%', background: C.card, border: `${isActive ? 4 : 2}px solid ${isActive ? C.lime : done ? C.borderHi : C.border}`, display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: isActive ? '0 0 46px rgba(193,255,114,0.35)' : 'none' }}>
              <Icon size={size * 0.42} color={isActive ? C.lime : done ? C.ivory : C.muted} strokeWidth={2} />
            </div>
            {done ? (
              <div style={{ position: 'absolute', right: -6, bottom: -6, width: 30, height: 30, borderRadius: '50%', background: C.lime, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <Check size={20} color={C.bg} strokeWidth={3} />
              </div>
            ) : null}
          </div>
        );
      })}
    </>
  );
};

/** End card on the last cue: large avatar, handle, lime "Follow for more" button. */
export const EndCard: React.FC = () => {
  const f = useCurrentFrame();
  const t = at(CUES.length) - 2;
  if (f < t) return null;
  const p = pop(f, t, 16);
  const btn = pop(f, t + 10);
  return (
    <AbsoluteFill style={{ alignItems: 'center', justifyContent: 'center', paddingBottom: 240 }}>
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', opacity: Math.min(1, p * 1.4), transform: `translateY(${(1 - p) * 40}px)` }}>
        <Img src={staticFile('yovan-avatar-color.png')} style={{ width: 170, height: 170, borderRadius: '50%', border: `3px solid ${C.lime}` }} />
        <div style={{ marginTop: 28, fontSize: 56, fontWeight: 700, color: C.white, letterSpacing: '-0.04em' }}>yvnalvworks</div>
        <div style={{ fontSize: 32, color: C.ivory }}>@yvnalvworks</div>
        <div style={{ marginTop: 40, display: 'flex', alignItems: 'center', gap: 14, padding: '20px 40px', borderRadius: 999, background: C.lime, color: C.bg, fontSize: 34, fontWeight: 600, transform: `scale(${btn})` }}>
          <UserPlus size={36} color={C.bg} strokeWidth={2} /> Follow for more
        </div>
        <div style={{ marginTop: 26, fontFamily: MONO, fontSize: 24, color: C.sec, opacity: ease(f, t + 16, 10) }}>yvnalvworks.com</div>
      </div>
    </AbsoluteFill>
  );
};

/** Interpolate node positions between layouts (rail -> line -> loop) with two progress values. */
export const morph = (a: { x: number; y: number }, b: { x: number; y: number }, c: { x: number; y: number }, p1: number, p2: number) => ({
  x: mix(mix(a.x, b.x, p1), c.x, p2),
  y: mix(mix(a.y, b.y, p1), c.y, p2),
});
