# Monitoring and Operations

Keeping a deployed vision system honest: what to watch when labels are scarce, how to diagnose a drop, and how to close the data loop.

## Contents

1. What to monitor
2. Camera and image health
3. Drift without labels
4. Getting labels in production
5. Diagnosis playbook
6. Retraining and rollout
7. The data flywheel
8. Runbook

---

## 1. What to monitor

| Layer | Signals |
|---|---|
| Infrastructure | Device up, CPU/GPU load, memory, temperature and throttling, disk, network |
| Stream | Frames in per camera, decode errors, reconnects, analysed fps, queue depth, **drop rate** |
| Model | Inference latency percentiles, detections per frame, score distribution, class mix, model version in use |
| Product | Events per camera-hour, alert rate, operator dismissal rate, time to acknowledge, downstream action rate |
| Quality | Sampled human review accuracy, golden-set results after every release, regression-set results |

Alert on rates and distributions rather than single events: "camera 7 produced zero detections for two hours during working time" is a real alert; one quiet minute is not.

## 2. Camera and image health

Vision systems usually break at the camera, not the model. Check per camera, continuously:

* **Brightness and contrast statistics** (sudden shifts mean exposure changes, lights on or off, or a repositioned camera)
* **Sharpness** (variance of the Laplacian, or a similar focus measure) for defocus, dirt, spider webs, rain on the lens
* **Scene change** (a large jump in a perceptual hash or embedding of the background) meaning the camera moved or the view is blocked
* **Stream freshness** and frame rate; duplicate frames mean a frozen encoder
* **Night/IR mode transitions**, which change appearance completely

These checks catch most "the model stopped working" incidents before anyone looks at the model.

## 3. Drift without labels

Labels arrive late or never, so watch proxies:

* **Prediction drift:** detections per frame, class distribution, mean confidence, and alert rate versus a baseline period. A drop in mean score with stable volume often precedes measurable accuracy loss.
* **Image drift:** embedding drift (average distance of current frames to the training distribution in a backbone's feature space) or simple statistics per camera (brightness, contrast, colour balance, blur).
* **Segment drift:** compare per-camera and per-time-of-day, not globally — a single new camera can be badly served while the average looks fine.
* Treat drift as a **trigger to investigate**, not proof of degradation; confirm with reviewed samples.

## 4. Getting labels in production

* **Operator feedback:** every dismissed or confirmed alert is a label. Make dismissal one click and record the reason.
* **Sampled review:** a fixed number of random frames and events per week, labelled by someone competent, gives an unbiased accuracy estimate (a biased "review only alerts" sample measures precision only, never recall).
* **Downstream truth:** scanned barcodes, scale weights, reject bins, access logs, sales — pair them with predictions to get free ground truth.
* **Shadow mode:** run the new model alongside the old one on live traffic and compare, before switching.

## 5. Diagnosis playbook

When quality drops, work outside-in:

1. **Pipeline:** is the stream up, at the expected fps, with a low drop rate? Any decode errors, restarts, or version changes?
2. **Image:** view recent frames. Camera moved, dirty, defocused, exposure changed, new lighting, seasonal sun, new obstruction?
3. **Config:** did thresholds, regions of interest, model version, or preprocessing change? Compare against the last known-good deployment.
4. **Data:** run drift checks per camera; look for new object types, new packaging, new uniforms, construction, new signage.
5. **Model:** run the golden set and the regression set against the deployed artifact (not the source checkpoint) on the device. Export or quantization problems surface here.
6. **Labels:** if performance "dropped" only in reviewed numbers, check whether the review criteria or reviewers changed.

Record the finding and add a monitor or a test that would have caught it sooner.

## 6. Retraining and rollout

* Retrain on a trigger (drift, new site, new object class, measured drop) or a schedule; always with fresh production data, especially the failures.
* Compare the candidate with the current production model on the **same golden and regression sets** and on recent production samples. Require improvement beyond noise, with no regression on must-pass cases.
* Roll out gradually: shadow → a few cameras or sites → fleet, with metrics watched at each step and a tested rollback (keep the previous artifact on the device).
* Re-verify after every export and quantization step; the winning checkpoint is not what runs on the device.

## 7. The data flywheel

```text
production frames → uncertain, novel, and failed cases selected → annotated (pre-labelled, human-verified)
→ added to dataset version N+1 → retrain → evaluate on golden + regression → staged rollout → repeat
```

Budget for this loop from day one: it is what makes a vision system improve instead of decaying. Keep every dataset version, and record which model was trained on which version.

## 8. Runbook

Written before launch, kept next to the on-call rotation:

* How to see a camera's live view and recent events; how to check device health.
* How to restart a stream, a device, or the service; how to fail over.
* How to roll back the model; where artifacts and versions live.
* Threshold changes: who may change them, how they are recorded, and how the effect is measured.
* Escalation: who owns cameras (facilities), network (IT), and the model (this team).
* What to tell operators when the system is degraded, so trust is not lost silently.
