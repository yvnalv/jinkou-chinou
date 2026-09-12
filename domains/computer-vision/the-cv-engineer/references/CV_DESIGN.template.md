# Vision System Design — <use case>

| | |
|---|---|
| Status | <Draft / Agreed> |
| Owner | <who decides and maintains> |
| Sites and cameras | <n sites, n cameras, types> |
| Date | <date>; hardware, model, and legal facts checked on <date> |

## 1. Decision and Value

- **Decision or action the system drives:** <who or what acts on each output>
- **Today:** <manual check, existing system, nothing> and its performance
- **Value:** <defects caught, incidents prevented, hours saved, throughput>
- **Cost of a false alarm / a miss:** <…> / <…>

## 2. Vision Task

| | |
|---|---|
| Task | <classification / detection / segmentation / keypoints / tracking / OCR / anomaly / VLM> |
| Classes or concepts | <list, with definitions in the annotation guide> |
| Trigger | <every frame at N fps / motion / sensor / schedule> |
| Output | <event, count, measurement, mask, text> |
| Decision latency budget | <ms or s, end to end> |

## 3. Capture

| Camera / site | Model and lens | Resolution on target | Mounting and angle | Lighting | Environment | Notes |
|---|---|---|---|---|---|---|
| <cam1 / site A> | <…> | <px on object at working distance> | <…> | <…> | <indoor/outdoor, night, weather> | <…> |

Feasibility check: can a person do the task from these images? <evidence>. Changes needed to capture: <…>

## 4. Data Plan

- Coverage matrix: <dimensions and target counts per cell>
- Sources: <production cameras, historical recordings, public datasets, synthetic>
- Annotation: <who labels, tool, guide version, QA and agreement target>
- Splits: <by scene / camera / time> because <…>
- Volume target for v1: <n images, n instances per class>

## 5. Model Plan

| Stage | Approach | Why |
|---|---|---|
| Prototype | <zero-shot model> | Feasibility and pre-labeling |
| v1 | <architecture, size, input resolution> | <accuracy vs latency on target device> |
| Later | <distillation, quantization, task-specific heads> | <…> |

Licences checked: <model code and weights, and their implications for this product>.

## 6. Metrics and Acceptance

| Metric | Baseline | Target | Measured on |
|---|---|---|---|
| <recall at N false alarms per camera-hour> | <…> | <…> | <test split by camera/time> |
| <latency p95 end to end on device> | — | <…> | <target hardware> |
| <per-slice minimum (night, camera 7, small objects)> | <…> | <…> | <…> |

## 7. Deployment

| | |
|---|---|
| Where inference runs | <edge device model / on-prem GPU / cloud> and why |
| Runtime and precision | <TensorRT/ONNX/OpenVINO/LiteRT; FP16/INT8> |
| Streams per device (measured) | <…> |
| Devices needed | <from deployment_budget.py> |
| Bandwidth and storage | <Mbps, TB/month, retention> |
| Failure behavior | <camera down, device down, model fails to load, network down> |
| Update strategy | <OTA, staged rollout, rollback> |

## 8. Integration

<Where events go (VMS, MQTT, API, dashboard, PLC), who sees alerts, how operators give feedback, what happens on an alert.>

## 9. Privacy and Compliance

- People filmed: <employees / public / none>; biometric processing: <yes/no>
- Lawful basis and notices: <…>; DPIA: <status>
- Regulatory category: <ordinary processing / AI Act high-risk / prohibited practice check done>
- Privacy measures: <edge-only, blurring, retention, masked zones, access control>

## 10. Risks and Open Questions

| # | Risk or question | Impact | Mitigation / owner | Status |
|---|---|---|---|---|
| 1 | <e.g. night performance unknown> | <high> | <collect night data before commitment> | <open> |
