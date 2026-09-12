"""Streaming video inference pipeline template. Copy into the project as e.g. src/pipeline.py.

The structure matters more than the model: a camera produces frames whether or not you are ready,
so a real-time pipeline must drop frames on purpose, batch deliberately, and measure latency end to
end. This template runs as-is with a synthetic source and a fake detector, so you can size and test
the architecture before any model exists, then swap in the real pieces:

  * replace FakeDetector with a real one (TensorRT, ONNX Runtime, OpenVINO, LiteRT, PyTorch ...)
    by implementing infer(frames) -> list of detections per frame
  * replace SyntheticSource with a decoder (OpenCV VideoCapture, GStreamer, DeepStream, PyAV)
  * replace PrintSink with your event publisher (MQTT, Kafka, HTTP, database)

Design rules built in:
  * bounded queues with an explicit drop policy: when inference cannot keep up, drop the OLDEST
    frames, never block the camera reader (a blocked reader drifts behind real time forever)
  * batching with a timeout so latency stays bounded when traffic is light
  * per-frame timestamps and end-to-end latency percentiles, not just throughput
  * a stable interface so the model can be swapped without touching the pipeline

Run:  python video_pipeline.template.py --cameras 4 --fps 10 --seconds 10 --infer-ms 25 --batch 4
"""

from __future__ import annotations

import argparse
import queue
import statistics
import threading
import time
from dataclasses import dataclass, field
from typing import Any, Protocol


@dataclass
class Frame:
    camera_id: str
    frame_id: int
    captured_at: float
    image: Any = None            # numpy array in a real pipeline
    meta: dict = field(default_factory=dict)


@dataclass
class Result:
    frame: Frame
    detections: list[dict]
    inferred_at: float


class Detector(Protocol):
    def infer(self, frames: list[Frame]) -> list[list[dict]]:
        """Return one list of detections per input frame."""


class FakeDetector:
    """Stand-in with a configurable cost, for sizing the pipeline before the model exists."""

    def __init__(self, per_frame_ms: float, batch_overhead_ms: float = 2.0):
        self.per_frame_ms = per_frame_ms
        self.batch_overhead_ms = batch_overhead_ms

    def infer(self, frames: list[Frame]) -> list[list[dict]]:
        time.sleep((self.batch_overhead_ms + self.per_frame_ms * len(frames)) / 1000)
        return [[{"class": "person", "score": 0.9, "bbox": [10, 10, 40, 80]}] for _ in frames]


class SyntheticSource(threading.Thread):
    """Produces frames at a fixed rate, like a camera. Replace with a real decoder."""

    def __init__(self, camera_id: str, fps: float, out: queue.Queue, stop: threading.Event, stats: dict):
        super().__init__(daemon=True)
        self.camera_id, self.fps, self.out, self.stop, self.stats = camera_id, fps, out, stop, stats

    def run(self) -> None:
        interval = 1.0 / self.fps
        next_at = time.perf_counter()
        frame_id = 0
        while not self.stop.is_set():
            now = time.perf_counter()
            if now < next_at:
                time.sleep(min(next_at - now, 0.005))
                continue
            next_at += interval
            frame_id += 1
            frame = Frame(self.camera_id, frame_id, time.perf_counter())
            self.stats["captured"] += 1
            try:
                self.out.put_nowait(frame)
            except queue.Full:
                # Drop the OLDEST frame: stale frames are worthless in real time.
                try:
                    self.out.get_nowait()
                    self.stats["dropped"] += 1
                    self.out.put_nowait(frame)
                except queue.Empty:
                    pass


class InferenceWorker(threading.Thread):
    def __init__(self, detector: Detector, src: queue.Queue, sink, stop: threading.Event,
                 batch_size: int, batch_timeout_s: float, stats: dict):
        super().__init__(daemon=True)
        self.detector, self.src, self.sink, self.stop = detector, src, sink, stop
        self.batch_size, self.batch_timeout_s, self.stats = batch_size, batch_timeout_s, stats

    def _collect(self) -> list[Frame]:
        batch: list[Frame] = []
        deadline = time.perf_counter() + self.batch_timeout_s
        while len(batch) < self.batch_size:
            timeout = max(0.0, deadline - time.perf_counter())
            try:
                batch.append(self.src.get(timeout=timeout if batch else 0.1))
            except queue.Empty:
                break
        return batch

    def run(self) -> None:
        while not self.stop.is_set():
            batch = self._collect()
            if not batch:
                continue
            outputs = self.detector.infer(batch)
            now = time.perf_counter()
            for frame, detections in zip(batch, outputs):
                self.stats["processed"] += 1
                self.stats["latencies"].append((now - frame.captured_at) * 1000)
                self.sink(Result(frame, detections, now))


class PrintSink:
    """Turns detections into events. Replace with your publisher; keep it non-blocking."""

    def __init__(self, quiet: bool = True):
        self.quiet = quiet
        self.events = 0

    def __call__(self, result: Result) -> None:
        if result.detections:
            self.events += 1
            if not self.quiet:
                print(f"{result.frame.camera_id} frame {result.frame.frame_id}: {len(result.detections)} detections")


def run_pipeline(cameras: int, fps: float, seconds: float, detector: Detector, batch: int,
                 queue_size: int, batch_timeout_ms: float, workers: int, quiet: bool = True) -> dict:
    stop = threading.Event()
    frames: queue.Queue = queue.Queue(maxsize=queue_size)
    stats = {"captured": 0, "dropped": 0, "processed": 0, "latencies": []}
    sink = PrintSink(quiet)
    sources = [SyntheticSource(f"cam{i + 1}", fps, frames, stop, stats) for i in range(cameras)]
    infer_workers = [InferenceWorker(detector, frames, sink, stop, batch, batch_timeout_ms / 1000, stats)
                     for _ in range(workers)]
    started = time.perf_counter()
    for t in sources + infer_workers:
        t.start()
    time.sleep(seconds)
    stop.set()
    for t in sources + infer_workers:
        t.join(timeout=2)
    elapsed = time.perf_counter() - started
    latencies = sorted(stats["latencies"])

    def pct(p: float):
        return round(latencies[min(len(latencies) - 1, int(p * len(latencies)))], 1) if latencies else None

    return {
        "elapsed_s": round(elapsed, 2), "cameras": cameras, "requested_fps_total": round(cameras * fps, 1),
        "captured": stats["captured"], "processed": stats["processed"], "dropped": stats["dropped"],
        "drop_rate": round(stats["dropped"] / max(1, stats["captured"]), 3),
        "achieved_fps": round(stats["processed"] / elapsed, 1),
        "latency_ms": {"p50": pct(0.5), "p95": pct(0.95), "p99": pct(0.99),
                       "max": round(latencies[-1], 1) if latencies else None},
        "events": sink.events,
    }


def main() -> int:
    p = argparse.ArgumentParser(description="Size and test a streaming inference pipeline.")
    p.add_argument("--cameras", type=int, default=4)
    p.add_argument("--fps", type=float, default=10.0, help="analysed fps per camera")
    p.add_argument("--seconds", type=float, default=10.0)
    p.add_argument("--infer-ms", type=float, default=25.0, help="per-frame inference cost of the fake detector")
    p.add_argument("--batch", type=int, default=1)
    p.add_argument("--batch-timeout-ms", type=float, default=50.0)
    p.add_argument("--queue-size", type=int, default=8, help="small queues keep latency low and drop early")
    p.add_argument("--workers", type=int, default=1, help="inference workers (1 per accelerator is typical)")
    p.add_argument("--verbose", action="store_true")
    args = p.parse_args()

    result = run_pipeline(args.cameras, args.fps, args.seconds, FakeDetector(args.infer_ms), args.batch,
                          args.queue_size, args.batch_timeout_ms, args.workers, quiet=not args.verbose)
    print(f"{result['cameras']} cameras x {args.fps} fps = {result['requested_fps_total']} fps requested")
    print(f"captured {result['captured']}, processed {result['processed']}, dropped {result['dropped']} "
          f"({result['drop_rate']:.1%}), achieved {result['achieved_fps']} fps over {result['elapsed_s']}s")
    print(f"end-to-end latency ms: {result['latency_ms']}")
    if result["drop_rate"] > 0.05:
        print("Dropping frames: the pipeline cannot keep up. Lower fps or resolution, use a smaller or quantized "
              "model, add workers or devices, or analyse only regions/events of interest.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
