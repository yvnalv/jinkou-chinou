import { loadFont as loadPoppins } from '@remotion/google-fonts/Poppins';
import { loadFont as loadMono } from '@remotion/google-fonts/JetBrainsMono';

export const { fontFamily: POPPINS } = loadPoppins('normal', {
  weights: ['400', '500', '600', '700'],
  subsets: ['latin'],
});
export const { fontFamily: MONO } = loadMono('normal', { weights: ['500'], subsets: ['latin'] });

// yvnalvworks tokens (assets/brand-kit/guidelines/yvnalvworks.tokens.json)
export const C = {
  bg: '#121212',
  card: '#18181b',
  border: '#27272a',
  borderHi: '#3f3f46',
  lime: '#C1FF72',
  white: '#FFFFFF',
  ivory: '#F0ECE2',
  sec: '#8E8E93',
  muted: '#71717A',
  danger: '#EF4444',
};

// 9:16 stage. Content is centered on x=540 with mirrored margins, so it reads centered
// while staying clear of the right action strip (960-1080) and the header (0-150).
export const W = 1080;
export const H = 1920;
export const CENTER_X = 540;
export const SAFE_LEFT = 60; // author lockup only
export const CONTENT_LEFT = 120;
export const CONTENT_RIGHT = 960;
export const CC_Y = 1480;
