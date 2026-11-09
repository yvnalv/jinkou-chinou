/**
 * Starter Remotion Root registering multi-platform compositions (9:16, 4:5, 16:9)
 * and a single-frame Still graphic.
 */

import React from 'react';
import { Composition, Still } from 'remotion';
import { SAFE_ZONES } from './brand-tokens.starter';
import { SceneTemplate, SceneTemplateProps } from './SceneTemplate.starter';

export const RemotionRoot: React.FC = () => {
  const reelsPreset = SAFE_ZONES['universal-vertical'];
  const feed4x5Preset = SAFE_ZONES['feed-portrait-4-5'];
  const youtubePreset = SAFE_ZONES['youtube-16-9'];

  const defaultProps: SceneTemplateProps = {
    headline: 'Ship Faster with Automated Workflows',
    subheadline: 'Frame-accurate programmatic video powered by Remotion',
    captionText: 'Every element stays inside the social media UI safe zone.',
    platform: 'universal-vertical',
    showSafeZoneGuide: true,
  };

  return (
    <>
      <Composition
        id="ShortFormVertical"
        component={SceneTemplate}
        durationInFrames={150}
        fps={reelsPreset.defaultFps}
        width={reelsPreset.width}
        height={reelsPreset.height}
        defaultProps={defaultProps}
      />

      <Composition
        id="FeedPortrait4x5"
        component={SceneTemplate}
        durationInFrames={150}
        fps={feed4x5Preset.defaultFps}
        width={feed4x5Preset.width}
        height={feed4x5Preset.height}
        defaultProps={{
          ...defaultProps,
          platform: 'feed-portrait-4-5',
        }}
      />

      <Composition
        id="Landscape16x9"
        component={SceneTemplate}
        durationInFrames={300}
        fps={youtubePreset.defaultFps}
        width={youtubePreset.width}
        height={youtubePreset.height}
        defaultProps={{
          ...defaultProps,
          platform: 'youtube-16-9',
        }}
      />

      <Still
        id="SocialThumbnailStill"
        component={SceneTemplate}
        width={1920}
        height={1080}
        defaultProps={{
          ...defaultProps,
          platform: 'web-clean',
          showSafeZoneGuide: false,
        }}
      />
    </>
  );
};

