# Data and Annotation

Collecting images and video that represent reality, labelling them consistently, splitting them honestly, and growing the dataset with a data engine.

## Contents

1. Collection and coverage
2. Annotation guidelines and quality
3. Formats
4. Splits and leakage
5. Augmentation
6. Synthetic data and the domain gap
7. Auto-labeling and active learning
8. Dataset audit

---

## 1. Collection and coverage

Build a **coverage matrix** of the conditions the system will meet, and count examples per cell:

| Dimension | Examples |
|---|---|
| Site and camera | Each installation, each camera model, each viewpoint |
| Time | Day, night, dusk; weekdays and weekends; seasons |
| Weather and light | Sun, cloud, rain, snow, fog, headlights, IR mode |
| Subject variation | Sizes, distances, poses, occlusion, colours, materials, packaging variants |
| Rare but critical | The defect types, the safety violations, the edge cases that justify the project |

Rules: collect from the **production cameras** wherever possible (public datasets rarely match your optics and angles), keep raw originals, record metadata (camera, timestamp, settings, site) for slicing later, and plan a continuous trickle of new data rather than one big collection.

For rare events, capture pre-event buffers (ring buffers around triggers) so hard positives are not lost.

## 2. Annotation guidelines and quality

The annotation guide is the real specification of the model's behavior (`references/ANNOTATION_GUIDE.template.md`):

* **Class definitions** with inclusion and exclusion rules, and worked examples of each.
* **Edge-case rules** decided once, written down: occluded objects (label if more than X% visible), truncated at the image border, reflections and screens, groups and crowds, very small or blurred objects, ambiguous classes, "don't care" regions.
* **Geometry rules:** tight boxes versus amodal boxes, mask precision, keypoint visibility flags, how to handle overlapping instances.
* **Quality process:** annotator training, a gold set with known answers, double-labelling a sample to measure agreement (report it), review of disagreements, and periodic re-calibration. Label errors put a ceiling on measurable accuracy.
* Treat the guide as versioned code: when a rule changes, note which data follows which version, and re-label affected sets.

## 3. Formats

| Format | Shape | Notes |
|---|---|---|
| COCO JSON | `images`, `annotations` (bbox `[x, y, w, h]` absolute, segmentation, keypoints), `categories` | The common interchange format; most eval tooling expects it |
| YOLO txt | One file per image, `class cx cy w h` normalized 0–1 | Simple, training-friendly; loses image size unless read separately |
| Pascal VOC XML | Per-image XML with absolute `xmin, ymin, xmax, ymax` | Legacy but still around |
| Masks | PNG label maps or RLE in COCO | Watch palette versus index encoding |

Convert once, keep one source of truth, and validate after every conversion (`scripts/dataset_audit.py`); silent coordinate or class-index errors are common.

## 4. Splits and leakage

Video and burst photography produce **near-duplicate frames**. A random split puts almost identical images in train and test, which inflates every metric.

Split by the unit that varies in production, in this order of preference:

1. **By scene or session** (a recording, a shift, a production batch)
2. **By camera or site** (tests whether the model transfers to a new installation, the usual business question)
3. **By time** (train on earlier weeks, test on later ones)
4. By object identity (person, vehicle, product) when the same subject recurs

Also: keep augmented copies with their original; never let the same physical object appear in both splits; check for duplicate files and near-duplicates (`dataset_audit.py`); and hold out one whole camera or site as a generalization test even when you split by scene.

## 5. Augmentation

* **Match the deployment distribution:** brightness, contrast, colour jitter, blur, noise, JPEG compression, weather effects, small rotations and scale changes, random crops.
* **Respect the task's invariances:** horizontal flips are wrong for text and for left/right-specific classes; vertical flips are wrong for most surveillance; rotation is fine for top-down inspection.
* Strong policies (mosaic, mixup, copy-paste) help detection with limited data; disable them for the last epochs so the model finishes on realistic images.
* Augment training data only. Test-time augmentation is an inference technique with its own cost and must be measured separately.
* Augmentation cannot create coverage that does not exist: it will not teach night behavior from day-only data.

## 6. Synthetic data and the domain gap

Rendered or generated images help when real data is scarce, dangerous, or privacy-sensitive (rare defects, accidents, people in restricted areas). Expect a **domain gap**: models trained on synthetic images alone usually degrade on real ones. Mitigate with domain randomization (textures, lighting, camera poses), a real-image fine-tuning stage, and evaluation **only on real data**.

## 7. Auto-labeling and active learning (the data engine)

Modern practice is to label the *right* data rather than more data:

```text
model → run on unlabelled pool → select (uncertain, disagreeing, rare, novel embeddings)
      → pre-label with a foundation model (promptable segmentation, open-vocabulary detection)
      → human corrects rather than draws → retrain → repeat
```

* **Pre-labeling** with a strong zero-shot model turns annotation into verification, which is several times faster. Always keep the human in the loop for classes that matter.
* **Selection strategies:** low-confidence or high-entropy predictions, disagreement between two models, embedding-space coverage (cluster and sample), and near-duplicate filtering before sending anything to annotators.
* **Mine production failures**: the frames that caused false alarms or misses are the most valuable training data you will ever get.
* Track dataset versions and which model was trained on which version.

## 8. Dataset audit

Run before every training round:

```text
python <skill-dir>/scripts/dataset_audit.py --coco train.json --coco val.json --images-root images/
python <skill-dir>/scripts/dataset_audit.py --yolo data/ --splits train,val
```

It reports class balance, object sizes, malformed and duplicate annotations, images without labels, resolution spread, and near-duplicate images within and across splits. It cannot judge label *correctness* or whether the data covers deployment conditions; that needs human review against the coverage matrix and the annotation guide.
