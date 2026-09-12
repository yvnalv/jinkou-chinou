# Enterprise Vision Systems

Architecture for many cameras, many sites, and many models: ingest, pipelines, scaling, storage, multi-camera logic, and cost. Verified on 2026-09-11.

## Contents

1. Reference architecture
2. Ingest and decode
3. Inference serving
4. Pipeline frameworks
5. Multi-camera and cross-camera logic
6. Events, storage, and retention
7. Scaling and reliability
8. Cost model
9. Integration and security

---

## 1. Reference architecture

```text
cameras ──RTSP/ONVIF──> ingest + decode ──> preprocess ──> inference (batched) ──> tracking
   │                                                                   │
   └── local recording (NVR/VMS)                          post-processing and rules
                                                                       │
                                            events ──> message bus ──> storage, alerting, dashboards,
                                                                        search, human review, retraining pool
```

Decide early **where each stage runs**: fully on the edge, fully central, or hybrid (edge detection, central heavy models and storage). That decision drives bandwidth, cost, privacy, and failure behavior more than the model choice does.

## 2. Ingest and decode

* RTSP is the common camera protocol (ONVIF for discovery and control); WebRTC for low-latency viewing; some sites push to RTMP/SRT.
* **Decode is expensive.** Use hardware decoders (NVDEC on NVIDIA, Quick Sync on Intel, the SoC's decoder on edge modules) and keep frames on the accelerator to avoid copies.
* Analyse a subset of frames (2–5 fps is typical); decode only what you analyse where the codec allows, or drop frames immediately after decode.
* Handle the realities: streams drop and reconnect, timestamps jump, cameras reboot, some deliver B-frames or variable frame rate. Mark gaps rather than pretending continuity.
* Keep a per-camera clock offset if you correlate across cameras.

## 3. Inference serving

* **Batch across cameras** (not across time) to use GPUs efficiently, with a batch timeout so latency stays bounded.
* Model servers (Triton and similar) give dynamic batching, multiple frameworks, model versioning, concurrent model instances, and metrics; a plain service is fine for one model and modest scale.
* Separate **model instances per GPU** and pin workers; measure streams per GPU with your model and resolution, then plan capacity with headroom (`scripts/deployment_budget.py`).
* Multi-model pipelines: run the cheap detector on every analysed frame, and heavier models (attribute classifiers, re-identification, VLMs) only on crops or events.
* Kubernetes with GPU scheduling for large fleets; keep node types matched to model requirements and remember that TensorRT engines are built per GPU architecture.

## 4. Pipeline frameworks

| Option | When it fits |
|---|---|
| Custom Python/C++ with a queueing design (`assets/video_pipeline.template.py`) | A few streams per node, full control, simple ops |
| GStreamer-based stacks, including NVIDIA DeepStream | Many streams per GPU with hardware decode, batching, tracking and messaging built in; steeper learning curve, NVIDIA-centric |
| Vendor video-analytics platforms (including NVIDIA's microservice stacks) | Large multi-camera deployments where you want reference pipelines, multi-camera tracking, and Kubernetes/Helm deployment out of the box |
| VMS integrations (Milestone, Genetec and others) | The customer already runs a VMS; you provide analytics as a plugin or receive streams from it |

Whatever the framework, keep the model behind a stable interface so it can be swapped without rewriting the pipeline.

## 5. Multi-camera and cross-camera logic

* **Zones and rules** (line crossing, intrusion, dwell time, occupancy) live above tracking; define them per camera in image coordinates, or in world coordinates via calibration (homography to a floor plan) when cameras overlap.
* **Cross-camera identity** (re-identification) is hard: appearance changes with viewpoint and lighting, galleries grow, and errors compound. Use spatial-temporal constraints (which camera can follow which, and how fast), keep gallery lifetimes short, and measure identity errors explicitly.
* **Calibration** (intrinsics, homography, camera-to-map transforms) enables counting, speed, and distance measurement; it must be re-done when a camera moves.
* Deduplicate events seen by several cameras before alerting humans.

## 6. Events, storage, and retention

* Emit **structured events** (camera, timestamp, type, confidence, track ID, zone, model version, a crop or clip reference), not raw frames, onto a message bus (MQTT at the edge, Kafka centrally).
* Store crops and short clips for evidence and for retraining; store full video only where required (it dominates storage cost: one 4 Mbps camera is roughly 1.3 TB per month).
* Define retention per data class and enforce deletion; personal data retention is a legal question (`references/privacy-and-regulation.md`).
* Index events for search (time, camera, type, attributes) — operators need "show me all forklift near-misses last week", not a video scrubber.

## 7. Scaling and reliability

* **Backpressure everywhere:** bounded queues, drop oldest frames, never block the decoder. Measure drop rate as a first-class metric.
* **Failure isolation:** one bad camera or corrupt stream must not take down a node; supervise and restart per stream.
* **Degradation plan:** what happens when the GPU is saturated (reduce fps, skip secondary models), when the network is down (buffer locally), when a model fails to load (keep previous version).
* Capacity planning with measured numbers and headroom for bursts and thermal limits; plan for camera growth.
* Observability: per-stream fps in and out, queue depth, drop rate, inference latency percentiles, GPU utilization and memory, event rates per camera.

## 8. Cost model

Per camera per year, count: device or share of server GPU, power, network (uplink and egress), storage and retention, licences (VMS, analytics, model licences), installation and maintenance visits, and the human time to review alerts. Alert review is often the largest operational cost, which makes precision at the operating point a financial metric, not only a technical one.

`scripts/deployment_budget.py` computes device counts, bandwidth, storage, and an edge-versus-server comparison from your measured numbers.

## 9. Integration and security

* Deliver value where people work: alerts into the VMS, dashboards, tickets, PLC signals, or the app; a standalone dashboard nobody opens is a failed project.
* Provide a review interface: operators must see why an alert fired (crop, clip, score) and be able to mark it wrong — that feedback is the retraining set.
* Network security: cameras on a segmented VLAN, no direct internet exposure, changed default credentials, signed firmware.
* Access control and audit for video and events; log who watched what where personal data is involved.
* Vendor lock-in: keep models, event schemas, and datasets portable even when using a vendor platform.
