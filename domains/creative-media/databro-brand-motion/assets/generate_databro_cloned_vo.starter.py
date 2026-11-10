#!/usr/bin/env python3
"""
Databro Studio voiceover generator (copy into the Remotion project's scripts/ folder).

Two engines:
1. Cloned talent voice (ElevenLabs). Used when both ELEVENLABS_API_KEY and DATABRO_VOICE_ID
   are set. DATABRO_VOICE_ID must be a voice you cloned ONCE from
   brand-kit/audio/voiceover/talent-samples/databro-talent-master-calibration.mp3
   (ElevenLabs: Voices -> Instant Voice Clone). Never falls back to a stock voice.
2. Offline calibrated fallback (edge-tts, id-ID-ArdiNeural, pitch -4Hz, rate -2%), tuned toward
   the talent's measured baritone (F0 about 86-90 Hz, 130-140 WPM).

Both engines apply the phonetic lexicon for English ML terms and strip em/en-dashes.
The offline engine also writes word timings and ready-to-use Closed Caption chunks
(2-4 words, ALL CAPS, original spelling) so captions sync to real speech.

Usage:
  python generate_databro_cloned_vo.py --text "Pernah ngga ..." --out public/vo/scene-01.mp3
  python generate_databro_cloned_vo.py --text-file scene-01.txt --out public/vo/scene-01.mp3 --fps 30

Requires: edge-tts (pip install edge-tts). The ElevenLabs path uses only the standard library.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

VOICE = "id-ID-ArdiNeural"
PITCH = "-4Hz"
RATE = "-2%"
MAX_WORDS_PER_CAPTION = 4

# Phonetic lexicon for natural Indonesian tech pronunciation (spoken text only, never captions)
PHONETIC_REPLACEMENTS = {
    r"\btrain-test-split\b": "tren tes split",
    r"\btrain_test_split\b": "tren tes split",
    r"\bscikit-learn\b": "saikit lern",
    r"\brandom_state\b": "rendom steit",
    r"\bdata leakage\b": "deta likej",
    r"\boverfitting\b": "over-fiting",
    r"\bmachine learning\b": "mesin lerning",
    r"\bagentic AI\b": "ejen-tik e-ai",
    r"\bAI Agents\b": "E-Ai Ejens",
    r"\bAI Agent\b": "E-Ai Ejen",
    r"\bTools\b": "Tuls",
    r"\bTool\b": "Tul",
    r"\bSkills\b": "Skils",
    r"\bSkill\b": "Skil",
    r"\bSOP\b": "Es-O-Pe",
    r"\bLLM\b": "El-El-Em",
    r"\bAPI\b": "E-Pi-Ai",
    r"\bDefinition of Done\b": "Definisi of Dan",
    r"\bQuality Gates\b": "Kwaliti Geits",
}

def strip_dashes(text: str) -> str:
    """Em-dash becomes a comma pause, en-dash a hyphen (Databro bans both in scripts and captions)."""
    text = re.sub(r"\s*—\s*", ", ", text)
    text = text.replace("–", "-")
    return re.sub(r"\s+", " ", text).strip()


def to_phonetic(text: str) -> str:
    for pattern, repl in PHONETIC_REPLACEMENTS.items():
        text = re.sub(pattern, repl, text, flags=re.IGNORECASE)
    return text


def caption_chunks(text: str) -> list[str]:
    """Split the original script into 2-4 word chunks, breaking after sentence punctuation."""
    chunks: list[str] = []
    current: list[str] = []
    for word in text.split():
        current.append(word)
        ends_clause = word[-1] in ".,?!:;"
        if ends_clause and len(current) == 1 and chunks and len(chunks[-1].split()) < MAX_WORDS_PER_CAPTION:
            # A lone clause-ending word ("bro.") joins the previous chunk instead of the next sentence.
            chunks[-1] += " " + current.pop()
            continue
        if len(current) >= MAX_WORDS_PER_CAPTION or (ends_clause and len(current) >= 2):
            chunks.append(" ".join(current))
            current = []
    if current:
        if len(current) == 1 and chunks:
            prev = chunks[-1].split()
            if len(prev) < MAX_WORDS_PER_CAPTION:
                chunks[-1] += " " + current[0]
            else:
                # Keep the 2-4 word rule: move one word from the full previous chunk.
                chunks[-1] = " ".join(prev[:-1])
                chunks.append(" ".join([prev[-1], current[0]]))
        else:
            chunks.append(" ".join(current))
    return chunks


def caption_display(chunk: str) -> str:
    # ALL CAPS, drop trailing commas/periods/ellipses, keep ? and !
    return re.sub(r"[.,:;]+$", "", chunk).upper()


async def synthesize_offline(script: str, out: Path, fps: int) -> dict:
    try:
        import edge_tts
    except ImportError:
        sys.exit("edge-tts is not installed. Run: pip install edge-tts")

    chunks = caption_chunks(script)
    # Build the spoken text chunk by chunk so every spoken character maps back to a caption chunk.
    spoken_parts = [to_phonetic(c) for c in chunks]
    spoken = " ".join(spoken_parts)
    spans, cursor = [], 0
    for part in spoken_parts:
        spans.append((cursor, cursor + len(part)))
        cursor += len(part) + 1

    communicate = edge_tts.Communicate(spoken, VOICE, rate=RATE, pitch=PITCH, boundary="WordBoundary")
    words, audio = [], bytearray()
    search_from = 0
    async for event in communicate.stream():
        if event["type"] == "audio":
            audio.extend(event["data"])
        elif event["type"] == "WordBoundary":
            start_ms = event["offset"] / 10_000
            end_ms = (event["offset"] + event["duration"]) / 10_000
            pos = spoken.find(event["text"], search_from)
            if pos >= 0:
                search_from = pos + len(event["text"])
            words.append({"text": event["text"], "startMs": round(start_ms), "endMs": round(end_ms), "pos": pos})

    out.write_bytes(bytes(audio))

    captions = []
    for idx, (lo, hi) in enumerate(spans):
        hits = [w for w in words if lo <= w["pos"] < hi]
        if not hits:
            continue
        captions.append(
            {
                "text": caption_display(chunks[idx]),
                "startFrame": int(hits[0]["startMs"] / 1000 * fps),
                "endFrame": int(round(hits[-1]["endMs"] / 1000 * fps)),
            }
        )
    # Hold each caption until the next one starts so the line never flickers off mid-sentence.
    for a, b in zip(captions, captions[1:]):
        if b["startFrame"] - a["endFrame"] <= fps // 2:
            a["endFrame"] = b["startFrame"]

    for w in words:
        w.pop("pos")
    speech_end_ms = words[-1]["endMs"] if words else 0
    return {
        "engine": "edge-tts",
        "voice": VOICE,
        "pitch": PITCH,
        "rate": RATE,
        "fps": fps,
        "speechEndMs": speech_end_ms,
        "speechEndFrame": int(round(speech_end_ms / 1000 * fps)),
        "words": words,
        "captions": captions,
    }


def synthesize_elevenlabs(script: str, out: Path, api_key: str, voice_id: str) -> dict:
    payload = {
        "text": to_phonetic(script),
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.60, "similarity_boost": 0.82, "style": 0.10, "use_speaker_boost": True},
    }
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
        data=json.dumps(payload).encode("utf-8"),
        headers={"xi-api-key": api_key, "Content-Type": "application/json", "Accept": "audio/mpeg"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as res:
        out.write_bytes(res.read())
    return {
        "engine": "elevenlabs",
        "voiceId": voice_id,
        "captions": None,
        "note": "No word timings from this engine. Time captions from the audio, or rerun with --engine edge.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a Databro voiceover clip plus caption timings.")
    src = parser.add_mutually_exclusive_group(required=True)
    src.add_argument("--text", help="Script text for one scene")
    src.add_argument("--text-file", type=Path, help="UTF-8 file holding the script for one scene")
    parser.add_argument("--out", type=Path, required=True, help="Output .mp3 path")
    parser.add_argument("--timings", type=Path, help="Output JSON path (default: <out>.json)")
    parser.add_argument("--fps", type=int, default=30, help="Composition fps for caption frames (default 30)")
    parser.add_argument("--engine", choices=["auto", "edge", "elevenlabs"], default="auto")
    args = parser.parse_args()

    script = strip_dashes(args.text if args.text else args.text_file.read_text(encoding="utf-8"))
    if not script:
        sys.exit("Script text is empty.")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    timings_path = args.timings or args.out.with_suffix(".json")

    api_key = os.environ.get("ELEVENLABS_API_KEY")
    voice_id = os.environ.get("DATABRO_VOICE_ID")
    use_cloned = args.engine == "elevenlabs" or (args.engine == "auto" and api_key and voice_id)

    if use_cloned:
        if not (api_key and voice_id):
            sys.exit("ElevenLabs needs ELEVENLABS_API_KEY and DATABRO_VOICE_ID (a voice cloned from the master MP3).")
        try:
            result = synthesize_elevenlabs(script, args.out, api_key, voice_id)
        except urllib.error.URLError as exc:
            sys.exit(f"ElevenLabs request failed: {exc}. Fix the key/voice or rerun with --engine edge.")
    else:
        result = asyncio.run(synthesize_offline(script, args.out, args.fps))

    result.update({"script": script, "audio": str(args.out)})
    timings_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"audio": str(args.out), "timings": str(timings_path), "engine": result["engine"],
                      "speechEndFrame": result.get("speechEndFrame"),
                      "captions": len(result["captions"] or [])}))


if __name__ == "__main__":
    main()
