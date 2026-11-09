/**
 * Isolated Brand Token Profile for Databro Studio (@databroid)
 * Sampled from official @databroid TikTok motion videos.
 */

export const DATABRO_BRAND = {
  id: 'databro',
  displayName: 'Databro',
  subtitle: 'Belajar Data Science',
  handle: '@databroid',
  avatarFile: 'databro-avatar.jpg',
  colors: {
    canvas: '#111111',
    lime: '#BFFF72',
    cream: '#F2EBE1',
    white: '#FFFFFF',
    muted: '#B3B3B3',
    calloutRed: '#D92D20',
    terminalHeader: '#1F1F1F',
    terminalBody: '#0A0A0A',
    terminalBorder: '#2E2E2E',
  },
  typography: {
    sans: '"Plus Jakarta Sans", "Poppins", "Inter", -apple-system, BlinkMacSystemFont, sans-serif',
    mono: '"Consolas", "JetBrains Mono", monospace',
  },
  motion: {
    springs: {
      snappy: { damping: 16, stiffness: 220, mass: 0.8 },
      smooth: { damping: 200, stiffness: 100, mass: 1.0 },
      pop: { damping: 13, stiffness: 200, mass: 0.85 },
    },
  },
  layout: {
    width: 1080,
    height: 1920,
    logoTop: 220,
    logoLeft: 88,
    stageLeft: 130,
    stageRight: 130,
    stageTop: 400,
    stageBottom: 760,
    ccTop: 1180,
  },
} as const;

export type DatabroBrandTheme = typeof DATABRO_BRAND;

