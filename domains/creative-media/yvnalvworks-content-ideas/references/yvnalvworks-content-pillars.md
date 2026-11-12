# yvnalvworks Content Pillars & Technical Focus

This document establishes the four foundational content pillars for Yovan Alvianto's personal engineering brand (`@yvnalvworks` / `yvnalvworks.com`).

---

## 1. AI Engineering & LLM Systems
Focus: Moving beyond prompt engineering into reliable, deterministic software systems wrapped around foundation models.

- **Golden Eval Suites First**: Why picking a model before writing 30-50 gold assertion tests is architectural malpractice.
- **Complexity Ladder**: Direct deterministic code -> Single structured prompt -> Workflow/Chaining -> RAG -> Autonomous Agent (only when non-determinism is tolerable).
- **Interface Hardening**: Enforcing strict Pydantic schemas, regex validations, and zero tolerance for unstructured markdown output.
- **Latency & Cost Ceilings**: Time-to-First-Token (TTFT), semantic caching (Redis / SQLite vector caches), and SLM routing.

---

## 2. Computer Vision & Edge AI
Focus: Deploying high-framerate, low-latency visual models onto physical edge hardware in noisy, uncontrolled physical environments.

- **Model Generalization**: Why 98% validation accuracy collapses on factory floors and edge cameras due to sensor gain, lens distortion, glare, and vibration.
- **Slice Audits**: Why global mAP hides critical tail-distribution failures (e.g., low-light or occluded objects).
- **Edge Run-times**: TensorRT engines, ONNX Runtime optimization, Hailo NPU compilation, and NVIDIA Jetson hardware tuning.
- **Camera Pipelines**: Zero-copy memory pipelines, GStreamer pipelines, V4L2 drivers, and hardware decoders (NVDEC).

---

## 3. Production Machine Learning & MLOps
Focus: The lifecycle, monitoring, and automated feedback loops of production predictive models.

- **Active Learning & Mining**: Pulling high-entropy failure frames directly from production inference back into retraining datasets.
- **Data Distribution Engineering**: Augmenting with physics-based sensor noise and shadow-invariant color transforms rather than switching model backbones.
- **Feature Stores & Drift Detection**: Population Stability Index (PSI), Wasserstein distance drift monitoring, and feature lineage.

---

## 4. High-Performance Software Engineering
Focus: Systems-level programming, language runtimes, concurrency, and architecture.

- **Python 3.14+ Performance**: Free-threaded GIL improvements, JIT compiler optimizations, and memory profiling.
- **Native Extensions**: Offloading compute-heavy loops to C++ or Rust via PyO3.
- **Low-Latency IPC**: Shared memory (IPC), UNIX domain sockets, and ZeroMQ for inter-process communication in vision systems.
