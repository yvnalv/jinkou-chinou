# Edge Deployment

Running vision on devices: choosing hardware, exporting and verifying models, quantization, optimizing the pipeline, and managing a fleet. Hardware and runtime facts were verified on 2026-09-11; check current specifications, prices, and support matrices before ordering.

## Contents

1. Edge or server?
2. Hardware landscape
3. Runtimes
4. Export and parity checks
5. Quantization
6. Making it fit the budget
7. Power, thermal, and physical constraints
8. Fleet operations

---

## 1. Edge or server?

| Choose edge when | Choose server when |
|---|---|
| Bandwidth is limited or expensive (video is 2–8 Mbps per camera) | Cameras are few and already on a fast network |
| Privacy or policy forbids video leaving the site | Data may leave, or only crops and events do |
| Latency must be tens of milliseconds (interlocks, robotics, safety) | Seconds are acceptable |
| The site must keep working when the network is down | Central control and frequent model updates matter more |
| Many cameras at many small sites | Few sites with many cameras (a local GPU server is often cheapest) |

Hybrid is the common answer: detect on the edge, send events plus short clips or crops to the centre for heavier models, review, and storage. Sending events instead of video typically cuts bandwidth by three orders of magnitude (`scripts/deployment_budget.py` quantifies it for your numbers).

## 2. Hardware landscape

| Class | Examples | Character |
|---|---|---|
| GPU modules | NVIDIA Jetson family (entry modules around 67 TOPS for roughly $250–300; higher tiers, including Thor-class modules, for multi-stream and transformer workloads) | Most flexible: full CUDA and TensorRT stack, multi-stream video with hardware decode, runs transformers and VLMs |
| NPU accelerators | Hailo-8 / 8L / 10H (about 13–40 TOPS; roughly $70–200 as boards or Raspberry Pi HATs) | Excellent performance per watt and per dollar for CNN detection; constrained operator support, vendor compiler required |
| SBC with NPU | Raspberry Pi 5 with an AI HAT, Rockchip RK3588 boards, Orange Pi | Cheapest per stream; fine for a few cameras at modest fps |
| x86 with integrated GPU/NPU | Intel Core with OpenVINO, industrial fanless PCs | Easy Windows/Linux integration on factory floors; good CPU fallback |
| Mobile | Apple Neural Engine (Core ML), Qualcomm and MediaTek NPUs | On-device apps; per-platform runtimes and formats |
| Smart cameras | Cameras with built-in accelerators (including Raspberry Pi AI cameras and vendor-specific ones) | Zero extra boxes; limited model size and update paths |

Rules of thumb: TOPS numbers are marketing until measured with **your** model at **your** resolution and precision; memory bandwidth and operator support usually decide real throughput; and a device that also decodes video in hardware saves a large slice of the budget.

## 3. Runtimes

| Runtime | Targets | Notes |
|---|---|---|
| TensorRT | NVIDIA GPUs and Jetson | Fastest on NVIDIA; engines are built per GPU architecture, TensorRT version, precision, and input shape — rebuild on every change |
| ONNX Runtime | CPU, CUDA, TensorRT, OpenVINO, DirectML, others | Portable baseline with execution providers; good default for cross-platform code |
| OpenVINO | Intel CPU, iGPU, NPU | Strong CPU performance, mature quantization tooling |
| LiteRT (formerly TensorFlow Lite) | Android, embedded Linux, microcontrollers | Delegates for NNAPI, GPU, Hexagon, Edge TPU |
| ExecuTorch | PyTorch on mobile and embedded | PyTorch-native edge path, growing backend support |
| Core ML | Apple devices | Neural Engine access; convert and profile with Apple's tools |
| Vendor SDKs (Hailo, RKNN, Qualcomm, Ambarella) | Their own accelerators | Best performance on that silicon; check the supported-operator list before choosing a model |

## 4. Export and parity checks

Export is where silent accuracy loss happens. After every export or runtime change:

1. Run the **golden set** through source and exported model; compare detections, not just tensors (allow small numeric differences, but the metric must match within a stated tolerance).
2. Check preprocessing parity explicitly: resize method and interpolation, letterbox padding colour, normalization, channel order (RGB vs BGR), and input layout (NCHW vs NHWC).
3. Check post-processing parity: score threshold, NMS implementation and IoU, class index mapping, coordinate scaling back to the original image.
4. Fix input shapes where possible (dynamic shapes cost performance and can break accelerator support).
5. Version the exported artifact with the source checkpoint, runtime version, precision, and input shape.

## 5. Quantization

| Technique | Typical effect |
|---|---|
| FP16 | About 2× faster, memory halved, usually no measurable accuracy change on GPUs |
| INT8 post-training quantization with a good calibration set | 2–4× faster and 4× smaller; accuracy drop usually under 1% when calibrated well, larger for small objects and transformer blocks |
| Quantization-aware training | Recovers most of the INT8 loss; needs a training run |
| INT4 / mixed precision | Aggressive, hardware-specific; verify per layer |
| Pruning and distillation | Complementary to quantization; distillation into a smaller architecture is often the bigger win |

Calibration set: a few hundred **representative production images** covering lighting, sites, and classes. Do not calibrate on synthetic or clean data. Always re-run the full evaluation after quantization, per slice; a drop that averages 0.5 mAP can be a 10-point drop on night cameras.

## 6. Making it fit the budget

In order of usual payoff:

1. **Analyse fewer frames** (2–5 fps is enough for most analytics; motion or schedule triggers help more).
2. **Crop to regions of interest** and skip empty areas.
3. **Lower resolution** to the minimum that keeps pixels on target; measure the accuracy cost per step.
4. **Quantize** (FP16, then INT8 with verification).
5. **Batch** frames across cameras where latency allows (adds queueing delay).
6. **Cascade:** cheap motion or tiny-model filter first, heavy model only on candidates.
7. **Smaller or distilled architecture**, chosen by measured accuracy-latency curve on the device.
8. **Hardware decode** for video and zero-copy paths between decode and inference.

## 7. Power, thermal, and physical constraints

* Measure sustained throughput after 30+ minutes: devices throttle, and enclosures in the sun are worse.
* Budget power per device and per site (`deployment_budget.py`); passive cooling limits what you can deploy in sealed enclosures.
* Storage wear: logging every frame to an SD card kills it; use ring buffers, industrial storage, or upload.
* Plan for power loss (read-only root filesystems, journaling, safe restart) and for physical access being expensive.

## 8. Fleet operations

* **Provisioning and identity:** each device has an ID, a site, a camera mapping, and known configuration.
* **OTA updates** for model artifacts and software with staged rollout (canary devices first), health checks, and automatic rollback. Never update every site at once.
* **Offline resilience:** buffer events locally, reconcile when the link returns; keep the last known-good model on the device.
* **Remote observability:** device health (CPU, GPU, memory, temperature, disk), camera health (stream up, frame rate, brightness, focus), model version, and inference metrics per device.
* **Security:** signed artifacts, encrypted storage and transport, no default credentials, restricted physical ports, and a patch process.
* **Cost of touch:** every site visit is expensive; design so that recovery, diagnosis, and updates are remote.
