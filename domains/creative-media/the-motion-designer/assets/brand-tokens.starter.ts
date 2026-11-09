/**
 * Brand Token System, Spring Presets & Social Media Platform Safe Zones for Remotion.
 * Keep each brand in its own isolated file (e.g. glm.brand.ts, databro.brand.ts)
 * implementing `BrandTheme` so brand styles never contaminate each other.
 *
 * Enforces `the-uix-designer` craft rules:
 *  - Solid flat semantic color tokens (zero gradients, zero blurry glow orbs)
 *  - Symmetric horizontal insets (`left === right`) so the main content container
 *    and Closed Captions (CC) are always horizontally centered at X = Width / 2
 */

import type { SpringConfig } from 'remotion';

export type SpringPresetName = 'snappy' | 'smooth' | 'bouncy' | 'heavy';

export const SPRING_PRESETS: Record<SpringPresetName, SpringConfig> = {
  snappy: { damping: 18, stiffness: 220, mass: 0.8, overshootClamping: false },
  smooth: { damping: 200, stiffness: 100, mass: 1.0, overshootClamping: true },
  bouncy: { damping: 11, stiffness: 160, mass: 0.9, overshootClamping: false },
  heavy: { damping: 26, stiffness: 90, mass: 1.8, overshootClamping: false },
};

export interface BrandTheme {
  id: string;
  displayName: string;
  tagline?: string;
  website?: string;
  colors: {
    backgroundPrimary: string;
    backgroundSecondary: string;
    surfaceCard: string;
    surfaceBorder: string;
    textPrimary: string;
    textSecondary: string;
    textMuted: string;
    accentPrimary: string;
    accentSecondary: string;
    statusSuccess: string;
    statusWarning: string;
    statusDanger: string;
  };
  typography: {
    headingFontFamily: string;
    bodyFontFamily: string;
    monoFontFamily: string;
    headingWeight: number;
    letterSpacingHeading: string;
  };
  assets: {
    logoLightPath: string;
    logoDarkPath: string;
    iconMarkPath?: string;
  };
  motion: {
    defaultSpring: SpringPresetName;
    cardBorderRadius: number;
  };
  captions: {
    backgroundColor: string;
    textColor: string;
    activeWordColor: string;
    borderRadius: number;
  };
}

export type PlatformPresetId =
  | 'instagram-reels'
  | 'instagram-stories'
  | 'tiktok'
  | 'youtube-shorts'
  | 'facebook-reels'
  | 'universal-vertical'
  | 'feed-portrait-4-5'
  | 'feed-square-1-1'
  | 'youtube-16-9'
  | 'web-clean';

export interface PlatformSafeZone {
  id: PlatformPresetId;
  label: string;
  aspectRatio: '9:16' | '4:5' | '1:1' | '16:9';
  width: number;
  height: number;
  defaultFps: 30 | 60;
  insets: {
    top: number;
    bottom: number;
    left: number;
    right: number;
  };
  ccBand: {
    top: number;
    bottom: number;
    left: number;
    right: number;
  };
  feedCrop4x5?: {
    top: number;
    bottom: number;
  };
}

/**
 * All presets use symmetric horizontal insets (`left === right`) equal to the
 * strictest side dead zone so the main container is 100% horizontally centered
 * while clearing right-side platform action icons.
 */
export const SAFE_ZONES: Record<PlatformPresetId, PlatformSafeZone> = {
  'instagram-reels': {
    id: 'instagram-reels',
    label: 'Instagram Reels (9:16 + 4:5 Feed Crop)',
    aspectRatio: '9:16',
    width: 1080,
    height: 1920,
    defaultFps: 30,
    insets: { top: 285, bottom: 672, left: 120, right: 120 },
    ccBand: { top: 1080, bottom: 1220, left: 120, right: 120 },
    feedCrop4x5: { top: 285, bottom: 285 },
  },
  'instagram-stories': {
    id: 'instagram-stories',
    label: 'Instagram Stories (9:16)',
    aspectRatio: '9:16',
    width: 1080,
    height: 1920,
    defaultFps: 30,
    insets: { top: 250, bottom: 340, left: 80, right: 80 },
    ccBand: { top: 1360, bottom: 1520, left: 80, right: 80 },
  },
  tiktok: {
    id: 'tiktok',
    label: 'TikTok In-Feed (9:16)',
    aspectRatio: '9:16',
    width: 1080,
    height: 1920,
    defaultFps: 30,
    insets: { top: 240, bottom: 660, left: 160, right: 160 },
    ccBand: { top: 1080, bottom: 1220, left: 160, right: 160 },
  },
  'youtube-shorts': {
    id: 'youtube-shorts',
    label: 'YouTube Shorts (9:16)',
    aspectRatio: '9:16',
    width: 1080,
    height: 1920,
    defaultFps: 30,
    insets: { top: 288, bottom: 672, left: 160, right: 160 },
    ccBand: { top: 1080, bottom: 1220, left: 160, right: 160 },
  },
  'facebook-reels': {
    id: 'facebook-reels',
    label: 'Facebook Reels (9:16)',
    aspectRatio: '9:16',
    width: 1080,
    height: 1920,
    defaultFps: 30,
    insets: { top: 260, bottom: 650, left: 160, right: 160 },
    ccBand: { top: 1080, bottom: 1220, left: 160, right: 160 },
  },
  'universal-vertical': {
    id: 'universal-vertical',
    label: 'Universal Short-Form Master (IG + TikTok + Shorts + FB)',
    aspectRatio: '9:16',
    width: 1080,
    height: 1920,
    defaultFps: 30,
    insets: { top: 288, bottom: 672, left: 160, right: 160 },
    ccBand: { top: 1080, bottom: 1220, left: 160, right: 160 },
    feedCrop4x5: { top: 285, bottom: 285 },
  },
  'feed-portrait-4-5': {
    id: 'feed-portrait-4-5',
    label: 'Feed Portrait 4:5 (Instagram / LinkedIn / Facebook)',
    aspectRatio: '4:5',
    width: 1080,
    height: 1350,
    defaultFps: 30,
    insets: { top: 96, bottom: 160, left: 96, right: 96 },
    ccBand: { top: 1020, bottom: 1160, left: 96, right: 96 },
  },
  'feed-square-1-1': {
    id: 'feed-square-1-1',
    label: 'Feed Square 1:1 (Instagram / LinkedIn / X)',
    aspectRatio: '1:1',
    width: 1080,
    height: 1080,
    defaultFps: 30,
    insets: { top: 80, bottom: 140, left: 80, right: 80 },
    ccBand: { top: 810, bottom: 920, left: 80, right: 80 },
  },
  'youtube-16-9': {
    id: 'youtube-16-9',
    label: 'YouTube & Landscape HD (16:9)',
    aspectRatio: '16:9',
    width: 1920,
    height: 1080,
    defaultFps: 60,
    insets: { top: 96, bottom: 160, left: 140, right: 140 },
    ccBand: { top: 790, bottom: 900, left: 200, right: 200 },
  },
  'web-clean': {
    id: 'web-clean',
    label: 'Website / Presentation / Docs Loop (16:9)',
    aspectRatio: '16:9',
    width: 1920,
    height: 1080,
    defaultFps: 60,
    insets: { top: 64, bottom: 80, left: 96, right: 96 },
    ccBand: { top: 860, bottom: 970, left: 160, right: 160 },
  },
};

export const DEFAULT_NEUTRAL_BRAND: BrandTheme = {
  id: 'neutral',
  displayName: 'Neutral Studio',
  tagline: 'Programmatic Motion Graphics',
  website: 'example.com',
  colors: {
    backgroundPrimary: '#0B0F17',
    backgroundSecondary: '#111827',
    surfaceCard: '#131B2E',
    surfaceBorder: '#1E293B',
    textPrimary: '#F8FAFC',
    textSecondary: '#94A3B8',
    textMuted: '#64748B',
    accentPrimary: '#0EA5E9',
    accentSecondary: '#10B981',
    statusSuccess: '#10B981',
    statusWarning: '#F59E0B',
    statusDanger: '#EF4444',
  },
  typography: {
    headingFontFamily: 'Inter, system-ui, sans-serif',
    bodyFontFamily: 'Inter, system-ui, sans-serif',
    monoFontFamily: 'JetBrains Mono, monospace',
    headingWeight: 700,
    letterSpacingHeading: '-0.025em',
  },
  assets: {
    logoLightPath: 'brands/neutral/logo-light.svg',
    logoDarkPath: 'brands/neutral/logo-dark.svg',
  },
  motion: {
    defaultSpring: 'snappy',
    cardBorderRadius: 16,
  },
  captions: {
    backgroundColor: '#131B2E',
    textColor: '#F8FAFC',
    activeWordColor: '#0EA5E9',
    borderRadius: 12,
  },
};
