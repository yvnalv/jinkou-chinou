import React from 'react';
import { AbsoluteFill } from 'remotion';
import { DatabroLogoLockup, DatabroSocialHandle } from './DatabroLogoLockup.starter';
import { DATABRO_CANVAS_PRESETS, DatabroAspectRatioKey, databroBrand } from './databro.brand.starter';

/**
 * Databro video cover (Reels / TikTok / Shorts thumbnail). Every video deliverable ships one.
 *
 * Register it as its own composition with the video's width and height (31 frames) and render
 * frame 30 so the lockup intro (frame 0..12) has settled:
 *   npx remotion still src/index.ts <VideoId>Cover out/cover.png --frame=30
 *
 * Layout (references/databro-video-cover-spec.md): #121212 canvas, lockup + handle, no captions,
 * left-aligned column with a lavender headline (wrap the topic term in <CoverLime>), a white hook
 * line, and one key visual from the video. On 9:16 keep everything inside Y 380..1500 so the
 * 3:4 profile-grid crop and the 4:5 feed preview stay readable.
 */

const C = databroBrand.colors;
const T = databroBrand.typography;

/** The single lime keyword inside the lavender headline. */
export const CoverLime: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <span style={{ color: C.accentLime }}>{children}</span>
);

export interface DatabroVideoCoverProps {
  /** Lavender headline. Wrap exactly one keyword in <CoverLime>. Use <br /> for line breaks (max 3 lines). */
  headline: React.ReactNode;
  /** White hook line (max 2 lines). Wrap the question part in <b>. */
  hook?: React.ReactNode;
  /** One key visual taken from the video: diagram, code card, metric, or versus split. */
  visual?: React.ReactNode;
  /** Optional element above the headline, e.g. a cream emblem with an icon, or a coral warning line. */
  kicker?: React.ReactNode;
  aspectRatio?: DatabroAspectRatioKey;
  /** Headline font size in px. 120..132 on 9:16; scale down for 4:5 / 1:1 / 16:9. */
  headlineSize?: number;
  avatarSrc?: string;
}

export const DatabroVideoCover: React.FC<DatabroVideoCoverProps> = ({
  headline,
  hook,
  visual,
  kicker,
  aspectRatio = '9:16',
  headlineSize,
  avatarSrc,
}) => {
  const preset = DATABRO_CANVAS_PRESETS[aspectRatio];
  const tall = aspectRatio === '9:16';
  const size = headlineSize ?? (tall ? 128 : aspectRatio === '16:9' ? 96 : 92);
  const side = tall ? 100 : preset.contentStage.left + 16;
  return (
    <AbsoluteFill style={{ backgroundColor: C.backgroundPrimary }}>
      <AbsoluteFill
        style={{
          padding: `${tall ? 0 : preset.contentStage.top}px ${side}px 0 ${side}px`,
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          alignItems: 'flex-start',
          gap: tall ? 52 : 32,
        }}
      >
        {kicker}
        <div
          style={{
            fontFamily: T.fontDisplay,
            fontWeight: 800,
            fontSize: size,
            lineHeight: 1.02,
            letterSpacing: '-0.02em',
            color: C.accentLavender,
          }}
        >
          {headline}
        </div>
        {hook && (
          <div
            style={{
              fontFamily: T.fontBody,
              fontSize: Math.round(size * 0.36),
              lineHeight: 1.3,
              color: C.textPrimary,
              maxWidth: 880,
            }}
          >
            {hook}
          </div>
        )}
        {visual && <div style={{ marginTop: tall ? 12 : 4, alignSelf: 'stretch' }}>{visual}</div>}
      </AbsoluteFill>
      <DatabroLogoLockup aspectRatio={aspectRatio} avatarSrc={avatarSrc} />
      <DatabroSocialHandle aspectRatio={aspectRatio} />
    </AbsoluteFill>
  );
};
