# Evaluation

Measuring vision systems so the number predicts production behavior: metrics per task, operating points, error analysis, slices, robustness, and latency measured properly.

## Contents

1. Metrics by task
2. Operating points
3. Error analysis
4. Slices
5. Robustness
6. Latency and throughput
7. Golden sets and regression testing
8. Acceptance criteria

---

## 1. Metrics by task

| Task | Compare models | Run the product |
|---|---|---|
| Detection | mAP@[.50:.95], AP50, AP by object size | Recall at a fixed score and IoU threshold, precision or false alarms per camera-hour |
| Segmentation | mIoU (semantic), mask AP (instance), PQ (panoptic) | Boundary accuracy where it matters, area error for measurement tasks |
| Classification | Accuracy, macro F1, ROC/PR AUC | Precision and recall per class at the threshold, confusion between the costly pairs |
| Tracking | HOTA, IDF1, MOTA | Identity switches per hour, count error per period, fragmentation |
| Keypoints / pose | OKS-based AP | Per-keypoint error in pixels or millimetres |
| OCR / documents | Character and word error rate | End-to-end field accuracy after validation rules; manual-review rate |
| Anomaly / inspection | Image AUROC, pixel AUPRO | Escape rate (missed defects) at the accepted false-reject rate |
| Depth / measurement | Absolute and relative error | Error in physical units at the working distance |

`scripts/detection_eval.py` computes the detection metrics, the operating point, and the error taxonomy from COCO-format files.

## 2. Operating points

* mAP is a ranking summary; no product runs at "all thresholds at once". Choose the score threshold from the cost of false alarms versus misses, or from a capacity limit (how many alerts people can handle), on **validation** data, then confirm on test.
* Report the confusion counts at that threshold (TP, FP, FN) and, for alerting systems, **false alarms per camera per hour** — a number operations teams understand and act on.
* For tracking and counting, evaluate the final number (people per hour, parts per shift), not just per-frame detection.

## 3. Error analysis

Break false positives into causes rather than staring at one number (`detection_eval.py` does this automatically):

| Error | Meaning | Usual fix |
|---|---|---|
| Duplicate | Several detections on one object | NMS settings, or an NMS-free model |
| Localization | Right class, box too loose (IoU below threshold) | More precise labels, higher resolution, longer training |
| Classification | Right box, wrong class | Confusable classes: more data, better class definitions, hierarchical labels |
| Background | Detection on nothing | Hard-negative mining: add those frames as negatives |
| Missed ground truth | No detection | Small or occluded objects, unusual conditions, missing coverage |

Then look at the images themselves: sort by score, review the worst false positives and the missed objects, and check whether the "error" is actually a label error. Label errors in the test set cap your measured ceiling.

## 4. Slices

Report metrics per slice, because averages hide failures: camera and site, lighting (day, night, IR), weather, object size bucket, distance, occlusion level, class, time of day, and any demographic slice when people are involved (`detection_eval.py --slices`). A model that works at 0.85 mAP overall but 0.4 at night on camera 7 is a night failure, not a good model.

## 5. Robustness

Test what production will do to the images: compression artifacts, defocus and motion blur, rain and glare, sensor noise at high gain, IR mode, exposure shifts, partial occlusion, dirty lenses, and camera movement. Build a small perturbation suite and track the score drop; it predicts real-world failures better than clean-set accuracy.

Also test the **negative case**: empty scenes, objects of similar-looking classes, screens and posters showing the target object, reflections.

## 6. Latency and throughput

Measure on the **target device**, with the production pipeline:

* Warm up first (compilation, memory allocation, clock ramp), then measure many runs.
* Report p50, p95, p99 and the maximum, not the mean; alerting systems fail on tails.
* Measure **end to end**: decode, preprocess, inference, post-processing (NMS, tracking), and business logic. Inference is often less than half the budget.
* Note precision (FP32/FP16/INT8), input resolution, batch size, and whether other processes share the device.
* Measure sustained throughput under thermal load, not a 10-second burst; edge devices throttle.
* `scripts/deployment_budget.py` turns measured latency into device counts, and `assets/video_pipeline.template.py` measures end-to-end latency and drop rate for a whole pipeline.

## 7. Golden sets and regression testing

* Keep a **golden set**: a few hundred hand-checked images covering every important condition and failure mode, with stable labels. Every model version runs against it before release.
* Keep a **regression set** of past production failures; a new model must not reintroduce them.
* Version both with the model, and rerun after any change to preprocessing, quantization, or runtime — export bugs and preprocessing mismatches usually show up here first.
* Compare model versions with paired differences on the same images, and look at the flips (newly missed, newly found), not only the aggregate.

## 8. Acceptance criteria

- [ ] Meets the target metric at the chosen operating point on a test set split by scene, camera, or time.
- [ ] Slice results acceptable for every deployment condition; no critical slice far below the average.
- [ ] Error taxonomy reviewed; dominant error types understood and accepted or addressed.
- [ ] Robustness suite passed within the agreed drop.
- [ ] Latency and throughput measured on the target device with the full pipeline, including tails.
- [ ] Exported (and quantized) model verified to match the source model on the golden set.
- [ ] Failure behavior defined: what happens on no detection, low confidence, camera offline, or corrupt frames.
