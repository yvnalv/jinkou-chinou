// Transcribe voiceover takes with whisper.cpp (local, offline) and save word-level timestamps.
// Usage: node scripts/transcribe.mjs vo/take2-16k.wav [more.wav ...]
import path from 'node:path';
import fs from 'node:fs';
import { downloadWhisperModel, installWhisperCpp, toCaptions, transcribe } from '@remotion/install-whisper-cpp';

const WHISPER_DIR = path.resolve('whisper.cpp');
const VERSION = '1.5.5';
const MODEL = 'small.en';

await installWhisperCpp({ to: WHISPER_DIR, version: VERSION });
await downloadWhisperModel({ model: MODEL, folder: WHISPER_DIR });

for (const input of process.argv.slice(2)) {
  const out = await transcribe({
    inputPath: path.resolve(input),
    whisperPath: WHISPER_DIR,
    whisperCppVersion: VERSION,
    model: MODEL,
    tokenLevelTimestamps: true,
  });
  const { captions } = toCaptions({ whisperCppOutput: out });
  const words = captions.map((c) => ({ text: c.text.trim(), start: c.startMs / 1000, end: c.endMs / 1000 }));
  const target = input.replace(/\.wav$/, '.words.json');
  fs.writeFileSync(target, JSON.stringify(words, null, 1));
  console.log(`${input}: ${words.map((w) => w.text).join(' ')}`);
}
