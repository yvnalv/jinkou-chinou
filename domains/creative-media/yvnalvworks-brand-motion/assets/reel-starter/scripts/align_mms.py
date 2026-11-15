"""Forced-align the script words to the final voiceover with MMS, then time every caption from the word times.

Pause-based timing is exact at pauses but guesses inside long phrases, and Whisper smears words
across pauses. CTC forced alignment of the known words (MMS-300m, torchaudio forced_align) gives
word times to about 0.06 s.

Run with the remotion-demos/.venv-omnivoice interpreter (torch, torchaudio, transformers):
  "<venv>/Scripts/python.exe" scripts/align_mms.py --reel <reel.json> --audio vo/final-16k.wav \
      --model <mms-fa dir> --captions vo-out/captions.json
Rewrites --captions (and captions.srt next to it) and writes vo-out/mms-words.json.
"""
from __future__ import annotations

import argparse
import json
import re
import warnings
import wave
from pathlib import Path

import numpy as np
import torch
import torchaudio.functional as F
from transformers import Wav2Vec2ForCTC

warnings.filterwarnings("ignore")
SR = 16000
SPOKEN = {"gpt4o": "g p t four o", "3000": "three thousand"}  # how written forms are said


def romanize(word: str) -> str:
    core = re.sub(r"[^0-9A-Za-z']", "", word).lower()
    core = SPOKEN.get(core, core)
    return re.sub(r"[^a-z']", "", core)


def ts(t: float) -> str:
    ms = int(round(t * 1000))
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"00:{m:02d}:{s:02d},{ms:03d}"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--reel", required=True)
    ap.add_argument("--audio", required=True, help="16 kHz mono WAV of the final (sped-up) voiceover")
    ap.add_argument("--model", required=True)
    ap.add_argument("--captions", required=True)
    a = ap.parse_args()

    reel = json.loads(Path(a.reel).read_text(encoding="utf-8"))
    cues = [c[0] for sc in reel["scenes"] for c in sc["cues"]]
    words = [w for c in cues for w in c.split()]
    roman = [romanize(w) for w in words]

    vocab = json.loads((Path(a.model) / "vocab.json").read_text(encoding="utf-8"))
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = Wav2Vec2ForCTC.from_pretrained(a.model).to(device).eval()
    with wave.open(a.audio) as w:
        assert w.getframerate() == SR and w.getnchannels() == 1
        x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    n = len(x)
    x = (x - x.mean()) / (x.std() + 1e-7)
    targets = [vocab[ch] for r in roman for ch in r]
    with torch.inference_mode():
        log_probs = torch.log_softmax(model(torch.from_numpy(x).unsqueeze(0).to(device)).logits.float(), dim=-1)
        ali, scores = F.forced_align(log_probs, torch.tensor([targets], dtype=torch.int32, device=device), blank=vocab["<blank>"])
    spans = F.merge_tokens(ali[0].cpu(), scores[0].exp().cpu())
    ratio = n / log_probs.size(1) / SR
    out, k = [], 0
    for w, r in zip(words, roman):
        sp = spans[k: k + len(r)]
        k += len(r)
        out.append({"text": w, "start": round(sp[0].start * ratio, 3), "end": round(sp[-1].end * ratio, 3),
                    "score": round(float(np.mean([s.score for s in sp])), 3)})
    Path(a.captions).parent.joinpath("mms-words.json").write_text(json.dumps(out, indent=1), encoding="utf-8")

    caps, i = [], 0
    for cid, text in enumerate(cues, 1):
        m = len(text.split())
        ws = out[i: i + m]
        i += m
        caps.append({"id": cid, "start": round(ws[0]["start"], 2), "end": round(ws[-1]["end"], 2), "text": text})
    for j, c in enumerate(caps[:-1]):  # hold through short breaths so captions never blink mid-sentence
        nxt = caps[j + 1]["start"]
        if nxt - c["end"] <= 0.6:
            c["end"] = round(nxt - 0.03, 2)
    caps[-1]["end"] = round(caps[-1]["end"] + 0.3, 2)
    Path(a.captions).write_text("[\n" + ",\n".join("  " + json.dumps(c, ensure_ascii=False) for c in caps) + "\n]\n", encoding="utf-8")
    Path(a.captions).with_name("captions.srt").write_text(
        "".join(f"{c['id']}\n{ts(c['start'])} --> {ts(c['end'])}\n{c['text']}\n\n" for c in caps), encoding="utf-8")
    low = [o["text"] for o in out if o["score"] < 0.3]
    print(json.dumps({"words": len(out), "cues": len(caps), "lowConfidence": low}, indent=1))


if __name__ == "__main__":
    main()
