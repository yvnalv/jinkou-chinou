# Vision Deployment Plan — <system> v<version>

| | |
|---|---|
| Scope | <sites, cameras, models> |
| Target | <edge devices / on-prem GPU / cloud / hybrid> |
| Owner and on-call | <team, rotation> |
| Date | <date> |

## 1. Model Artifact

| | |
|---|---|
| Source checkpoint | <run id, dataset version, commit> |
| Export | <ONNX / TensorRT engine / OpenVINO IR / LiteRT / Core ML>, version <…> |
| Precision and input | <FP16 / INT8>, <resolution>, <batch>, <fixed/dynamic shapes> |
| Parity check | Golden set: source <metric> vs exported <metric> (tolerance <…>) — <pass/fail> |
| Quantization calibration | <n images, from which cameras and conditions> |
| Preprocessing | <resize mode, letterbox colour, normalization, channel order> — identical in training and serving |

## 2. Capacity

From `deployment_budget.py` with **measured** latency:

| | |
|---|---|
| Measured latency per frame on target | <inference / decode / post-processing> |
| Streams per device at <n> fps | <…> |
| Cameras and analysed fps | <…> |
| Devices needed (at <x>% utilization) | <…> |
| Worst-case frame latency | <…> |
| Bandwidth and storage | <Mbps, TB/month, retention> |

## 3. Pipeline

<Diagram or description: ingest → decode → preprocess → inference → tracking → rules → events. Queue sizes, drop policy, batch size and timeout, workers per device.>

Backpressure: <what is dropped first and how it is measured>.

## 4. Rollout

| Stage | Scope | Success criteria | Duration | Rollback trigger |
|---|---|---|---|---|
| Shadow | <n cameras, no alerts emitted> | <agreement with current system / metrics> | <…> | <…> |
| Canary | <1 site> | <alert rate, precision on reviewed alerts, drop rate, latency> | <…> | <…> |
| Fleet | <all sites> | <…> | <…> | <…> |

Rollback: <previous artifact location, command, expected time to restore>.

## 5. Monitoring and Alerts

| Signal | Threshold | Action | Owner |
|---|---|---|---|
| Drop rate | <> 5% for 10 min> | <reduce fps / investigate> | <…> |
| Camera brightness or sharpness shift | <…> | <check camera> | <facilities> |
| Detections per hour vs baseline | <±50%> | <investigate> | <…> |
| Latency p95 | <> budget> | <…> | <…> |
| Device temperature | <> limit> | <…> | <…> |

## 6. Operations

- Runbook location: <…>
- Update procedure (OTA, staged, signed artifacts): <…>
- Offline behavior and buffering: <…>
- Support contacts: cameras <…>, network <…>, model <…>

## 7. Compliance Sign-off

- Signage and notices in place: <…>
- DPIA / legal review: <status, date>
- Retention and deletion configured: <…>
- Access control and audit: <…>

## 8. Open Risks

| # | Risk | Likelihood / impact | Mitigation | Owner |
|---|---|---|---|---|
| 1 | <…> | <…> | <…> | <…> |
