import React from 'react';
import { AbsoluteFill, Audio, Sequence, staticFile } from 'remotion';
import { GlmCaptions } from './GlmCaptions.starter';
import { GlmLogoLockup } from './GlmLogoLockup.starter';
import {
  GLM_CANVAS_PRESETS,
  GlmAspectRatioKey,
  GlmCanvasPreset,
  GlmCaptionCue,
  GlmSoundCue,
  glmBrand,
} from './glm.brand.starter';

export interface GlmBaseCanvasProps {
  aspectRatio?: GlmAspectRatioKey;
  presetOverride?: GlmCanvasPreset;
  theme?: 'cool-white' | 'emerald';
  captions?: GlmCaptionCue[];
  soundCues?: GlmSoundCue[];
  enableBgm?: boolean;
  bgmSrc?: string;
  bgmVolume?: number;
  voiceoverSrc?: string;
  voiceoverCues?: {
    frame: number;
    src: string;
    durationInFrames?: number;
    volume?: number;
  }[];
  logoSrc?: string;
  children: React.ReactNode;
}

/**
 * Standard Base Content Canvas for GLM Systems (glmsystems.com).
 *
 * Persistent vs. Transitioning Layers:
 *  - Layer 0: Solid Cool White (#F2F0FA) or Emerald (#003A40) background.
 *  - Layer 1: Symmetric centered stage (`contentStage`) hosting <TransitionSeries>.
 *  - Layer 2A: Fixed Top-Left GLM Logo Lockup (animates ONLY at frame 0..12).
 *  - Layer 2B: Fixed Top-Right glmsystems.com website mark.
 *  - Layer 3: Fixed Closed Captions (locked at fixed Y with zero vertical movement).
 *  - Layer 4: Frame-accurate SFX, BGM, and Voiceover audio bus.
 */
export const GlmBaseCanvas: React.FC<GlmBaseCanvasProps> = ({
  aspectRatio = '16:9',
  presetOverride,
  theme = 'cool-white',
  captions = [],
  soundCues = [],
  enableBgm = true,
  bgmSrc = 'brand-kit/audio/bgm/bgm-ambient.wav',
  bgmVolume = 0.10,
  voiceoverSrc,
  voiceoverCues = [],
  logoSrc,
  children,
}) => {
  const preset = presetOverride ?? GLM_CANVAS_PRESETS[aspectRatio];
  const isEmerald = theme === 'emerald';
  const bgColor = isEmerald
    ? glmBrand.colors.backgroundSecondary
    : glmBrand.colors.backgroundPrimary;
  const websiteColor = isEmerald
    ? glmBrand.colors.accentPrimary
    : glmBrand.colors.accentSecondary;
  const defaultLogo = isEmerald
    ? 'brand-kit/logos/GLM-BIRD-Color.svg'
    : 'brand-kit/logos/GLM-black-Text-Color-Bird.svg';

  return (
    <AbsoluteFill style={{ backgroundColor: bgColor }}>
      {/* LAYER 1: Centered Content Stage (<TransitionSeries>) */}
      <div
        style={{
          position: 'absolute',
          top: preset.contentStage.top,
          bottom: preset.contentStage.bottom,
          left: preset.contentStage.left,
          right: preset.contentStage.right,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          overflow: 'hidden',
        }}
      >
        {children}
      </div>

      {/* LAYER 2A: Persistent Top-Left GLM Lockup */}
      <GlmLogoLockup
        aspectRatio={aspectRatio}
        presetOverride={preset}
        logoSrc={logoSrc ?? defaultLogo}
      />

      {/* LAYER 2B: Persistent Top-Right Website Handle */}
      {preset.websiteTopRight && (
        <div
          style={{
            position: 'absolute',
            top: preset.websiteTopRight.top,
            right: preset.websiteTopRight.right,
            color: websiteColor,
            fontFamily: glmBrand.typography.fontDisplay,
            fontSize: 22,
            fontWeight: 700,
            letterSpacing: '0.04em',
            zIndex: 25,
            paddingTop: 8,
          }}
        >
          {preset.websiteTopRight.text}
        </div>
      )}

      {/* LAYER 3: Fixed-Position Closed Captions */}
      <GlmCaptions
        captions={captions}
        aspectRatio={aspectRatio}
        presetOverride={preset}
      />

      {/* LAYER 4: BGM, Voiceover & SFX Bus */}
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
