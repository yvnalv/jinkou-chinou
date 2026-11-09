#!/usr/bin/env python3
"""
Synthesizes a clean, royalty-free default TikTok / CapCut SFX & BGM .wav pack
using only the Python standard library (wave, math, struct, random).

Generated files:
  - sfx/keyboard-typing.wav   (Mechanical key clack burst synced to typewriter text)
  - sfx/pop-up.wav            (Clean CapCut pitch-sweep bubble pop for emblem/card entry)
  - sfx/whoosh-transition.wav (Filtered noise air whoosh for slide/zoom transitions)
  - sfx/mouse-click.wav       (Crisp double-transient UI mouse click)
  - sfx/progress-ticks.wav    (Rapid digital progress ticks for loading bars)
  - sfx/callout-ding.wav      (Warm two-tone harmonic chime for red callout boxes)
  - bgm/bgm-ambient.wav       (Subtle -22 dBFS warm synth pad loop)

Usage:
  python generate_default_sfx.py --out path/to/assets/brand-kit/audio
"""

from __future__ import annotations

import argparse
import math
import random
import struct
import wave
from pathlib import Path

SAMPLE_RATE = 44100


def write_wav(path: Path, samples: list[float]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        frames = bytearray()
        for s in samples:
            clamped = max(-0.98, min(0.98, s))
            frames.extend(struct.pack("<h", int(clamped * 32767)))
        wf.writeframes(bytes(frames))


def synth_pop_up() -> list[float]:
    """Clean CapCut-style upward pitch-sweep bubble pop (140ms)."""
    duration = 0.14
    n = int(SAMPLE_RATE * duration)
    out: list[float] = []
    phase = 0.0
    for i in range(n):
        t = i / SAMPLE_RATE
        progress = t / duration
        # Pitch sweeps rapidly from 240 Hz to 760 Hz
        freq = 240.0 + 520.0 * (progress ** 1.4)
        phase += 2.0 * math.pi * freq / SAMPLE_RATE
        env = math.sin(math.pi * progress) * math.exp(-progress * 3.2)
        out.append(math.sin(phase) * env * 0.65)
    return out


def synth_mouse_click() -> list[float]:
    """Crisp two-part mechanical mouse click (75ms)."""
    duration = 0.075
    n = int(SAMPLE_RATE * duration)
    rng = random.Random(42)
    out: list[float] = []
    for i in range(n):
        t = i / SAMPLE_RATE
        # Initial down-click at t=0, release click at t=0.028s
        env1 = math.exp(-t * 260.0)
        env2 = math.exp(-max(0.0, t - 0.028) * 320.0) if t >= 0.028 else 0.0
        tone = math.sin(2.0 * math.pi * 1850.0 * t) * 0.6 + (rng.uniform(-1, 1) * 0.4)
        out.append(tone * (env1 * 0.75 + env2 * 0.45))
    return out


def synth_keyboard_typing() -> list[float]:
    """Mechanical keyboard typing sequence (0.9s, ~10 crisp keystrokes)."""
    duration = 0.90
    n = int(SAMPLE_RATE * duration)
    rng = random.Random(101)
    out = [0.0] * n
    strike_times = [0.02, 0.09, 0.17, 0.24, 0.33, 0.41, 0.50, 0.58, 0.67, 0.76]
    for idx, st in enumerate(strike_times):
        start_i = int(st * SAMPLE_RATE)
        freq = 1400.0 + (idx % 4) * 160.0
        click_len = int(0.045 * SAMPLE_RATE)
        for j in range(click_len):
            if start_i + j >= n:
                break
            t = j / SAMPLE_RATE
            env = math.exp(-t * 220.0)
            thock = math.sin(2.0 * math.pi * 320.0 * t) * math.exp(-t * 95.0) * 0.5
            clack = (math.sin(2.0 * math.pi * freq * t) * 0.5 + rng.uniform(-1, 1) * 0.5) * env
            out[start_i + j] += (thock + clack) * 0.55
    return out


def synth_whoosh_transition() -> list[float]:
    """Smooth CapCut air whoosh using simple low-pass filtered noise (0.28s)."""
    duration = 0.28
    n = int(SAMPLE_RATE * duration)
    rng = random.Random(77)
    out: list[float] = []
    lp = 0.0
    for i in range(n):
        t = i / SAMPLE_RATE
        progress = t / duration
        # Envelope peaks in the middle
        env = math.sin(math.pi * progress) ** 1.8
        # Filter cutoff sweeps up then down
        alpha = 0.04 + 0.18 * math.sin(math.pi * progress)
        white = rng.uniform(-1.0, 1.0)
        lp = lp + alpha * (white - lp)
        swoosh_tone = math.sin(2.0 * math.pi * (160.0 + 220.0 * math.sin(math.pi * progress)) * t) * 0.25
        out.append((lp * 0.85 + swoosh_tone) * env * 0.65)
    return out


def synth_progress_ticks() -> list[float]:
    """Rapid subtle digital ticks while progress bar fills (0.75s)."""
    duration = 0.75
    n = int(SAMPLE_RATE * duration)
    out = [0.0] * n
    num_ticks = 14
    for k in range(num_ticks):
        st = k * (duration / num_ticks)
        start_i = int(st * SAMPLE_RATE)
        freq = 920.0 + k * 35.0
        tick_len = int(0.022 * SAMPLE_RATE)
        for j in range(tick_len):
            if start_i + j >= n:
                break
            t = j / SAMPLE_RATE
            env = math.exp(-t * 280.0)
            out[start_i + j] += math.sin(2.0 * math.pi * freq * t) * env * 0.42
    return out


def synth_callout_ding() -> list[float]:
    """Subtle crisp harmonic chime when red callout box locks in (0.38s)."""
    duration = 0.38
    n = int(SAMPLE_RATE * duration)
    out: list[float] = []
    for i in range(n):
        t = i / SAMPLE_RATE
        env = math.exp(-t * 11.0)
        f1 = math.sin(2.0 * math.pi * 1046.5 * t)  # C6
        f2 = math.sin(2.0 * math.pi * 1567.98 * t) * 0.55  # G6
        out.append((f1 + f2) * env * 0.42)
    return out


def synth_bgm_ambient() -> list[float]:
    """Subtle warm ambient synth pad loop (5.0s, -22 dBFS under voiceover)."""
    duration = 5.0
    n = int(SAMPLE_RATE * duration)
    out: list[float] = []
    # Warm Fmaj7 chord frequencies (F3, A3, C4, E4)
    freqs = [174.61, 220.00, 261.63, 329.63]
    for i in range(n):
        t = i / SAMPLE_RATE
        # Smooth fade in/out at loop boundaries
        fade = 1.0
        if t < 0.25:
            fade = t / 0.25
        elif t > duration - 0.25:
            fade = (duration - t) / 0.25
        sample = sum(math.sin(2.0 * math.pi * f * t) for f in freqs) / len(freqs)
        out.append(sample * fade * 0.12)
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate default TikTok/CapCut SFX & BGM .wav pack.")
    parser.add_argument("--out", required=True, help="Target audio folder (creates sfx/ and bgm/ subfolders).")
    args = parser.parse_args()

    base = Path(args.out).resolve()
    sfx_dir = base / "sfx"
    bgm_dir = base / "bgm"

    files = {
        sfx_dir / "pop-up.wav": synth_pop_up(),
        sfx_dir / "mouse-click.wav": synth_mouse_click(),
        sfx_dir / "keyboard-typing.wav": synth_keyboard_typing(),
        sfx_dir / "whoosh-transition.wav": synth_whoosh_transition(),
        sfx_dir / "progress-ticks.wav": synth_progress_ticks(),
        sfx_dir / "callout-ding.wav": synth_callout_ding(),
        bgm_dir / "bgm-ambient.wav": synth_bgm_ambient(),
    }

    for path, samples in files.items():
        write_wav(path, samples)
        print(f"[OK] Generated {path.relative_to(base)} ({len(samples) / SAMPLE_RATE:.2f}s)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

