# Annotation Guide — <dataset / project> v<version>

This guide defines the labels. The model can only be as consistent as this document. Every rule change gets a new version, and affected data is re-labelled or tagged with the old version.

| | |
|---|---|
| Task | <bounding boxes / polygons / masks / keypoints / classification / text> |
| Tool | <CVAT, Label Studio, Roboflow, …> |
| Annotators | <team, training date> |
| Reviewer | <who adjudicates> |
| Version | <v1.2, date, what changed> |

## 1. Classes

| Class | Include | Do NOT include | Example images |
|---|---|---|---|
| <person> | <whole or partly visible people, including reflections? decide> | <mannequins, photos on posters, statues> | <links or file names> |
| <forklift> | <…> | <pallet jacks, tow tractors> | <…> |

Decide and record: are ambiguous objects labelled with a separate "uncertain" class, skipped, or marked as "don't care" regions?

## 2. Geometry rules

- **Boxes:** tight around visible pixels <or amodal, covering the estimated full extent — pick one>. Include or exclude shadows, carried items, and attached parts: <decide>.
- **Occlusion:** label objects visible above <X>%; below that, <skip / mark occluded>. Add an `occluded` attribute when the tool supports it.
- **Truncation at the image border:** label the visible part if at least <X>% or <N> pixels are visible.
- **Minimum size:** do not label objects smaller than <N × N> pixels.
- **Crowds and groups:** label individually up to <N>; beyond that use a crowd region marked `iscrowd`.
- **Masks:** follow the object boundary within <N> pixels; holes and thin structures: <rule>.
- **Keypoints:** visibility flags <visible / occluded but inferable / not annotated>; order and naming as in <diagram>.

## 3. Attributes (if any)

| Attribute | Values | When to set |
|---|---|---|
| <occluded> | <none / partial / heavy> | <…> |
| <time_of_day> | <day / night / IR> | <from the frame, not the timestamp> |

## 4. Hard cases (worked examples)

| Situation | Decision | Why |
|---|---|---|
| <person on a screen or poster> | <do not label> | <not physically present> |
| <reflection in glass> | <do not label> | <duplicate of a real object> |
| <object behind a fence> | <label, mark occluded> | <still detectable and relevant> |
| <motion-blurred object> | <label if recognizable> | <matches production conditions> |
| <part of a pallet of identical items> | <label each up to 20, then crowd> | <consistent counting> |

Add every new question and its answer here; do not resolve them in chat and forget.

## 5. Quality process

- Training: every annotator labels the <N>-image training set and discusses disagreements before production work.
- Gold set: <N> images with agreed labels, mixed into batches; annotators below <X>% agreement are retrained.
- Double labelling: <X>% of images are labelled twice; agreement is measured <IoU-based / kappa> and reported per batch.
- Review: <all / X%> of batches reviewed by <reviewer>; corrections are fed back to the annotator.
- Audit: `python <skill-dir>/scripts/dataset_audit.py` on every delivery — malformed boxes, duplicates, class balance, near-duplicates.

## 6. Delivery

- Format: <COCO JSON / YOLO txt / masks>, file naming <convention>, one file per <…>.
- Metadata to preserve: <camera, timestamp, site, conditions>.
- Definition of done for a batch: <all images labelled, audit clean, review complete, agreement above target>.
