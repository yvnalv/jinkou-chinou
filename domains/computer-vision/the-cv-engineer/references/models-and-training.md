# Models and Training

Which model family fits which task, how to get from zero-shot prototype to deployable specialist, and training practice that holds up. Model names and results change fast; the families and tradeoffs below were verified on 2026-09-11, so check current benchmarks, licences, and releases before committing.

## Contents

1. Strategy: zero-shot, then specialize
2. Backbones and pretraining
3. Detection
4. Segmentation
5. Classification
6. Tracking
7. OCR and document AI
8. Anomaly and defect detection
9. Vision-language models
10. Training practice
11. Small objects and high resolution

---

## 1. Strategy: zero-shot, then specialize

```text
prototype with a foundation model (open-vocabulary detection, promptable segmentation, a VLM)
→ measure on your data → use it to pre-label → fine-tune a small specialist → distill / quantize for the target device
```

Foundation models answer "is this feasible?" in hours without labels. Specialist models win in production on latency, cost, predictability, and usually accuracy in-domain. Keep the foundation model in the loop as a labeling and evaluation tool.

## 2. Backbones and pretraining

* Self-supervised backbones (the DINO family, and successors such as DINOv3) give strong general features; frozen features plus a light head are a fast baseline, especially with little labelled data.
* Convolutional backbones remain efficient at small sizes and on edge accelerators; transformer backbones scale better with data and resolution but need more memory and care on edge runtimes (check operator support).
* Always start from pretrained weights; training from scratch needs far more data and rarely wins.

## 3. Detection

| Family | Character | Use when |
|---|---|---|
| YOLO-style one-stage detectors (current generations are NMS-free and export-friendly) | Fast, small, huge ecosystem, easy export to edge runtimes | Edge and real-time work, many streams, tight power budgets |
| Real-time DETR variants (RT-DETR, RF-DETR, D-FINE, DEIM) | Transformer decoders, no NMS, strong accuracy; the best now pass 60 mAP on COCO | GPU servers, accuracy-critical work, crowded scenes, good domain transfer |
| Two-stage detectors (Faster R-CNN and descendants) | Slower, still solid for high-precision offline work | Batch analysis where latency does not matter |
| Open-vocabulary detectors (OWL-style, Grounding DINO, YOLO-World and successors) | Detect classes described in text, no training | Prototyping, rare classes, pre-labeling, changing class lists |

Practical notes: decide NMS-free versus NMS early (it changes post-processing and export), keep the anchor/assignment defaults unless you have evidence, and check the licence of both code and weights.

## 4. Segmentation

* **Semantic** (per-pixel class), **instance** (per-object masks), **panoptic** (both). Pick the one the decision needs; instance masks cost more to annotate and to run.
* **Promptable segmentation** (the Segment Anything family, now with open-vocabulary concept prompts and video tracking) is excellent for annotation acceleration, interactive tools, and zero-shot masks; for fixed-class production work a fine-tuned specialist is usually cheaper and more consistent.
* Masks are expensive to label: consider boxes plus a promptable model to generate masks, with human verification.

## 5. Classification

* Fine-tune a pretrained backbone; freeze early layers when data is scarce. Use class weights or balanced sampling for imbalance, and label smoothing for noisy labels.
* Prefer classification on a **cropped region** (from a detector or a fixed region of interest) over whole-image classification when the object is small.
* Calibrate scores if a threshold drives an action.

## 6. Tracking

* Tracking quality is dominated by **detection quality**: fix the detector before tuning association.
* **Motion-only trackers** (SORT-style, ByteTrack, OC-SORT) are fast and enough for well-separated objects with steady motion.
* **Appearance-aware trackers** (BoT-SORT with re-identification embeddings, DeepSORT descendants) help with crossings, occlusions, and lookalike crowds, at extra cost; add re-identification only when identity switches are the measured problem.
* Camera-motion compensation matters for moving or vibrating cameras.
* Report **HOTA** (and IDF1) rather than MOTA alone; MOTA hides identity errors.
* Cross-camera identity (re-identification across views) is a much harder problem: plan for gallery management, appearance drift, and privacy constraints.

## 7. OCR and document AI

* **Pipeline OCR** (detection + recognition, for example PaddleOCR-style or docTR) is fast, cheap, and predictable for known layouts and high volumes.
* **VLM-based extraction** handles messy, varied documents and direct field extraction with no layout engineering, at higher cost and latency; strong general VLMs now exceed 95% field accuracy on many forms, and a fine-tuned small VLM can match them for a specific form type.
* Preprocessing still pays: deskew, denoise, crop to the document, ensure about 20–30 px character height (roughly 300 dpi for scans).
* Evaluate on **end-to-end field accuracy** after post-processing and validation rules, not only character error rate.

## 8. Anomaly and defect detection

* Use it when defects are rare, varied, or unknown in advance and you mostly have images of good parts.
* Embedding-based methods (memory-bank approaches such as PatchCore, and distribution methods such as PaDiM) train on normal images only and give pixel-level heatmaps; they are strong baselines on industrial benchmarks and need few images.
* Few-shot and zero-shot VLM-based inspection is now viable for cold starts; verify on your parts before trusting it.
* Once enough defect examples exist, a supervised detector or segmenter usually beats pure anomaly detection for the known defect types; hybrid setups are common.
* Fix lighting and fixturing first: most "hard" inspection problems are capture problems.

## 9. Vision-language models

Use a VLM when the output is text or a decision over open-ended visual content: captioning, visual question answering, document understanding, content moderation, or describing scenes an ontology cannot enumerate. Current open models (the Qwen-VL and InternVL families among others) are competitive with proprietary ones on many benchmarks.

Tradeoffs: high latency and cost per image, non-deterministic text output that needs structured-output constraints and validation, weaker precise localization than specialist detectors, and prompt-injection risk from text inside images. For high-volume fixed tasks, distill into a specialist.

## 10. Training practice

* **Baselines first:** a pretrained model without fine-tuning, and a simple heuristic (background subtraction, template matching, colour thresholds) — some industrial problems are solved by classical methods.
* Standard recipe: transfer learning, cosine schedule with warmup, AdamW, early stopping on a validation split, mixed precision, fixed seeds, and a held-out test set used once.
* Log everything (config, data version, metrics, sample predictions) to an experiment tracker; vision runs are long and easy to confuse.
* Track validation loss **and** the production metric (recall at the operating point); they diverge.
* Class imbalance: balanced sampling, loss weighting, or hard-example mining; never resample the validation set.
* Save checkpoints with the exact preprocessing (resize mode, letterbox, normalization, colour order); a mismatch between training and inference preprocessing is the most common silent accuracy loss.

## 11. Small objects and high resolution

* Increase input resolution before increasing model size when objects are small (accuracy usually tracks pixels on target).
* **Tiled / sliced inference** (overlapping crops, merged with NMS) finds small objects in large images at the cost of more compute per frame.
* Crop to regions of interest (lanes, conveyor, shelf) and skip the rest of the frame.
* Match anchors or assignment ranges to your object sizes; verify with the size buckets in `scripts/detection_eval.py` and `scripts/dataset_audit.py`.
