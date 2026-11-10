import React from 'react';
import { AbsoluteFill, Audio, Sequence, staticFile } from 'remotion';
import { DatabroCaptions } from './DatabroCaptions.starter';
import { DatabroLogoLockup, DatabroSocialHandle } from './DatabroLogoLockup.starter';
import {
  DATABRO_CANVAS_PRESETS,
  DATABRO_TRANSITION_TIMING,
  DatabroAspectRatioKey,
  DatabroCanvasPreset,
  DatabroCaptionCue,
  DatabroSoundCue,
  databroBrand,
} from './databro.brand.starter';

export interface DatabroBaseCanvasProps {
  /** Select standard aspect ratio ('9:16' | '4:5' | '1:1' | '16:9') or pass presetOverride */
  aspectRatio?: DatabroAspectRatioKey;
  presetOverride?: DatabroCanvasPreset;
  /** Global Closed Caption timeline locked at Y = 1480px (on 9:16) */
  captions?: DatabroCaptionCue[];
  /** Frame-accurate TikTok / CapCut sound effect cues */
  soundCues?: DatabroSoundCue[];
  /** Enable default ambient background music ('brand-kit/audio/bgm/bgm-ambient.wav') */
  enableBgm?: boolean;
  bgmSrc?: string;
  bgmVolume?: number;
  /** Optional single voiceover audio path inside public/ */
  voiceoverSrc?: string;
  /** Optional per-scene voiceover audio segments synced to scene start frames */
  voiceoverCues?: {
    frame: number;
    src: string;
    durationInFrames?: number;
    volume?: number;
  }[];
  /** Avatar image path inside public/ */
  avatarSrc?: string;
  /** Content-stage <TransitionSeries> scenes (scene content is left-aligned inside the stage) */
  children: React.ReactNode;
}

/**
 * Standard Base Content Canvas for Databro Studio (@databroid).
 *
 * Modify or duplicate `DATABRO_CANVAS_PRESETS` via `customizeDatabroCanvas()`
 * to adapt the entire video layout across TikTok/Reels (9:16), Instagram Feed (4:5),
 * Square (1:1), or YouTube (16:9).
 *
 * Persistent vs. Transitioning Layers:
 *  - Layer 0: Solid #121212 matte charcoal canvas (never transitions).
 *  - Layer 1: Content stage (`contentStage`) hosting <TransitionSeries>. Scenes lay out
 *    left-aligned (lavender headline, white subline, visual below), like the carousel slides.
 *  - Layer 2A: Fixed top-left Databro lockup (`top: 108, left: 100` on 9:16): animates ONLY at frame 0..12.
 *  - Layer 2B: Fixed top-right @databro.id handle (`top: 108, right: 100` on 9:16): fades in at frame 0..10.
 *  - Layer 3: Fixed Closed Captions (`Y = 1480px` on 9:16): zero vertical movement.
 *  - Layer 4: Frame-accurate TikTok SFX (`keyboard-typing`, `pop-up`, `whoosh-transition`, etc.), BGM and voiceover.
 */
export const DatabroBaseCanvas: React.FC<DatabroBaseCanvasProps> = ({
  aspectRatio = '9:16',
  presetOverride,
  captions = [],
  soundCues = [],
  enableBgm = true,
  bgmSrc = 'brand-kit/audio/bgm/bgm-ambient.wav',
  bgmVolume = DATABRO_TRANSITION_TIMING.bgmVolume,
  voiceoverSrc,
  voiceoverCues = [],
  avatarSrc = 'brand-kit/logos/databro-avatar.jpg',
  children,
}) => {
  const preset = presetOverride ?? DATABRO_CANVAS_PRESETS[aspectRatio];

  return (
    <AbsoluteFill
      style={{ backgroundColor: databroBrand.colors.backgroundPrimary }}
    >
      {/* LAYER 1: Content Stage (<TransitionSeries>). Left-aligned by default, like the carousel slides.
          Hero moments (emblem pop, giant keyword, CTA) may center themselves inside their own scene. */}
      <div
        style={{
          position: 'absolute',
          top: preset.contentStage.top,
          bottom: preset.contentStage.bottom,
          left: preset.contentStage.left,
          right: preset.contentStage.right,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'stretch',
          justifyContent: 'flex-start',
          textAlign: 'left',
          overflow: 'hidden',
        }}
      >
        {children}
      </div>

      {/* LAYER 2A: Persistent Top-Left Databro Lockup (Animates ONLY at frame 0..12) */}
      <DatabroLogoLockup
        aspectRatio={aspectRatio}
        presetOverride={preset}
        avatarSrc={avatarSrc}
      />

      {/* LAYER 2B: Persistent Top-Right @databro.id Handle */}
      <DatabroSocialHandle aspectRatio={aspectRatio} presetOverride={preset} />

      {/* LAYER 3: Fixed-Position Closed Captions (Locked at Y = 1480px on 9:16) */}
      <DatabroCaptions
        captions={captions}
        aspectRatio={aspectRatio}
        presetOverride={preset}
      />

      {/* LAYER 4: BGM, Voiceover & Frame-Accurate TikTok/CapCut Sound Effects */}
      {enableBgm && bgmSrc && (
        <Audio src={staticFile(bgmSrc)} volume={bgmVolume} loop />
      )}
      {voiceoverSrc && <Audio src={staticFile(voiceoverSrc)} volume={1.0} />}
      {voiceoverCues.map((vo, index) => (
        <Sequence
          key={`vo-${vo.frame}-${index}`}
          from={vo.frame}
          durationInFrames={vo.durationInFrames}
        >
          <Audio src={staticFile(vo.src)} volume={vo.volume ?? 1.0} />
        </Sequence>
      ))}
      {soundCues.map((cue, index) => {
        const resolvedPath = cue.sfx.includes('/')
          ? cue.sfx
          : `brand-kit/audio/sfx/${cue.sfx}.wav`;
        return (
          <Sequence
            key={`${cue.sfx}-${cue.frame}-${index}`}
            from={cue.frame}
            durationInFrames={cue.durationInFrames}
          >
            <Audio src={staticFile(resolvedPath)} volume={cue.volume ?? 0.55} />
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};

