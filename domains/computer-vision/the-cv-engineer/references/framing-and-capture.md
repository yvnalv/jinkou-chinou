# Framing and Capture

Choosing the vision task, designing the capture system, and setting budgets before any model work.

The camera is part of the model: more vision projects are saved by moving a light or changing a lens than by changing architecture.

## Contents

1. From decision to vision task
2. Task selection
3. The capture system
4. The feasibility gate
5. Metrics that match the decision
6. Budgets: accuracy, latency, cost
7. Build, fine-tune, or buy

---

## 1. From decision to vision task

Write the chain before choosing a model:

```text
Decision:    Stop the line when a defective part passes station 4
Action:      Alert the operator and log the part; stop after 3 in 5 minutes
Prediction:  Is this part defective, and where is the defect?
Unit:        One image per part, triggered by a sensor
Task:        Anomaly detection (few defect examples) or segmentation (if defect types are known)
Constraint:  Decision within 200 ms on a fanless industrial PC on the line
```

Ask: what happens on a false alarm, and on a miss? Those costs set the operating point, the review process, and how good the model must be.

## 2. Task selection

| Question | Task | Output |
|---|---|---|
| Is this whole image X? | Classification | Label + score |
| Where are the objects and how many? | Object detection | Boxes + classes + scores |
| Which pixels belong to what? | Semantic / instance / panoptic segmentation | Masks |
| Where are the parts of the object? | Keypoints / pose | Points |
| Which object is this over time? | Detection + tracking | Track IDs, trajectories |
| What text is in the image? | OCR / document AI | Text, layout, fields |
| Is this abnormal, without knowing the defect types? | Anomaly detection | Score + heatmap |
| How far away is it? | Depth / stereo / 3D | Depth map, point cloud |
| What is happening in this clip? | Video / action recognition | Clip or temporal labels |
| Open-ended questions about images | Vision-language model | Text answer, grounded regions |

Prefer the simplest task that supports the decision: counting objects that cross a line needs detection plus tracking, not segmentation; "is the shelf empty" may be classification on a cropped region rather than detection of every product.

## 3. The capture system

Design or audit capture first; it is cheaper and more effective than model work.

| Element | What to get right |
|---|---|
| Placement and angle | Objects unoccluded, consistent viewpoint, minimal perspective distortion; mount rigidly (vibration blurs and shifts regions of interest) |
| Resolution on target | Pixels **on the object**, not sensor megapixels. Rules of thumb: about 20–30 px height for detecting a person, 50+ px for classification, 20+ px character height for OCR. Compute from sensor, lens, and distance before buying |
| Lens and field of view | Focal length sets coverage and pixel density; watch distortion at wide angles and depth of field at close range |
| Lighting | The highest-leverage variable: controlled, diffuse, consistent light beats any model. Avoid backlight and mixed sources; consider domes, bars, polarizers, or IR; for inspection, structured or multi-angle lighting exposes defects |
| Exposure and motion | Shutter fast enough to freeze motion (motion blur destroys small-object detection); global shutter for fast motion; fixed exposure and white balance where possible so appearance stays stable |
| Environment | Weather, dust, condensation, day-night cycles, seasonal sun angles, vibration, temperature |
| Compression and transport | Heavy H.264/H.265 compression creates artifacts that hurt small objects; prefer higher bitrate or on-camera analysis; sync clocks across cameras |
| Consistency over time | Same camera model, firmware, and settings across sites; record settings as metadata; changes will otherwise show up as "model drift" |

## 4. The feasibility gate

Before training anything:

- [ ] Can a person reliably do the task from the same image or video? If not, fix capture (resolution, lighting, angle, frame rate) or redefine the task. A model cannot see what is not in the pixels.
- [ ] Do two annotators agree on the labels? Disagreement caps achievable accuracy.
- [ ] Are the rare and hard cases (the ones that matter) actually captured?
- [ ] Is there a physical or rule-based solution (a sensor, a barcode, a fixture, a light curtain) that is cheaper and more reliable than vision?

## 5. Metrics that match the decision

Research metrics summarize; production needs the operating point.

* **Detection:** mAP compares models, but the product cares about recall at a fixed false-alarm rate (or alarms per camera per hour) at a chosen score and IoU threshold.
* **Counting / flow:** counting error per period, not per-frame mAP.
* **Tracking:** identity errors matter (HOTA, IDF1), not just per-frame detection.
* **Inspection:** escape rate (missed defects) versus false-reject rate, weighted by the cost of each.
* **OCR:** character/word error rate and, more usefully, end-to-end field accuracy after post-processing.
* **All:** latency at the percentile that matters (p95 or p99), throughput, and cost per camera.

## 6. Budgets: accuracy, latency, cost

Write three numbers before designing: required quality at the operating point, latency budget per frame end to end (decode + preprocess + inference + post-processing + business logic), and cost per camera per year (hardware, power, bandwidth, licences, maintenance).

Tradeoffs to state explicitly:

| Lever | Gains | Costs |
|---|---|---|
| Higher input resolution | Small-object accuracy | Latency grows roughly with pixel count |
| Bigger model | Accuracy | Latency, memory, power, device cost |
| Lower analysed frame rate | Throughput, cost | Missed fast events; worse tracking |
| Quantization (INT8) | 2–4× speed, less memory | Small accuracy drop, needs calibration and verification |
| Edge processing | Privacy, bandwidth, resilience | Device cost, fleet management, harder updates |
| Server processing | Bigger models, easier updates | Bandwidth, egress cost, latency, data exposure |
| Cascades (cheap filter then heavy model) | Large average savings | More moving parts; the cheap stage sets the recall ceiling |

## 7. Build, fine-tune, or buy

1. **Zero-shot foundation models first** (open-vocabulary detectors, promptable segmentation, vision-language models) to test feasibility in hours and to pre-label data.
2. **Fine-tune a small specialist** for production: cheaper, faster, more predictable, and usually more accurate on your domain.
3. **Cloud vision APIs** suit generic tasks (common objects, standard documents, faces where legal) with low volume and no latency or privacy constraints; they lose on cost at scale, on domain-specific classes, and where data cannot leave.
4. **Check licences** before adopting a model: some popular detector implementations are AGPL (which affects proprietary products unless licensed commercially), while others are Apache-2.0 or MIT. Verify the licence of weights *and* code.
