import React from 'react';
import { Composition } from 'remotion';
import { Reel } from './Reel';
import { FPS, TOTAL_FRAMES } from './timing';
import { H, W } from './theme';

// Two renders: burned-in captions (preview / direct post) and clean (CapCut voiceover + captions).
export const Root: React.FC = () => (
  <>
    <Composition id="YvnalvworksReel" component={Reel} durationInFrames={TOTAL_FRAMES} fps={FPS} width={W} height={H} defaultProps={{ showCaptions: true }} />
    <Composition id="YvnalvworksReelClean" component={Reel} durationInFrames={TOTAL_FRAMES} fps={FPS} width={W} height={H} defaultProps={{ showCaptions: false }} />
  </>
);
