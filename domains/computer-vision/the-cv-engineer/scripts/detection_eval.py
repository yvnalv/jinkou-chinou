#!/usr/bin/env python3
"""Evaluate object detections: COCO-style mAP, operating-point metrics, an error taxonomy, and slices.

Inputs (COCO format):
  --gt          annotations JSON with "images", "annotations" (bbox = [x, y, w, h], category_id), "categories"
  --pred        detection results JSON: a list of {"image_id", "category_id", "bbox", "score"}
                (or a dict with a "annotations"/"detections" key holding that list)

Reports:
  * AP per IoU (0.50, 0.75) and mAP@[0.50:0.95], overall and per class, all-point interpolation
  * AP by object size (small < 32^2, medium < 96^2, large), because small objects usually carry the failures
  * precision, recall, F1 and counts at a chosen score and IoU threshold, plus the F1-optimal score threshold
  * an error taxonomy of false positives at that operating point: duplicate, localization, classification,
    both, background - and missed ground truth
  * per-slice metrics from an optional image-attributes file (camera, lighting, weather, site ...)

Examples:
  python detection_eval.py --gt val.json --pred preds.json --score-threshold 0.4
  python detection_eval.py --gt val.json --pred preds.json --slices attributes.json --out eval.json

Slice file: {"images": {"<image_id>": {"camera": "cam3", "lighting": "night"}}} or a flat {"<image_id>": {...}}.
Requires numpy. mAP follows the COCO definition closely; differences from pycocotools are at the third decimal.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

try:
    import numpy as np
except ImportError:  # pragma: no cover
    sys.exit("detection_eval.py needs numpy: pip install numpy")

IOU_THRESHOLDS = np.round(np.arange(0.5, 0.96, 0.05), 2)
SIZE_RANGES = {"small": (0, 32 ** 2), "medium": (32 ** 2, 96 ** 2), "large": (96 ** 2, float("inf"))}


def load_json(path: str):
    p = Path(path)
    if not p.is_file():
        sys.exit(f"error: file not found: {path}")
    try:
        return json.loads(p.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        sys.exit(f"error: {path}: invalid JSON ({exc})")


def iou_matrix(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """IoU between [x, y, w, h] boxes: a is (N, 4), b is (M, 4)."""
    if len(a) == 0 or len(b) == 0:
        return np.zeros((len(a), len(b)))
    ax1, ay1 = a[:, 0][:, None], a[:, 1][:, None]
    ax2, ay2 = (a[:, 0] + a[:, 2])[:, None], (a[:, 1] + a[:, 3])[:, None]
    bx1, by1 = b[:, 0][None, :], b[:, 1][None, :]
    bx2, by2 = (b[:, 0] + b[:, 2])[None, :], (b[:, 1] + b[:, 3])[None, :]
    inter_w = np.clip(np.minimum(ax2, bx2) - np.maximum(ax1, bx1), 0, None)
    inter_h = np.clip(np.minimum(ay2, by2) - np.maximum(ay1, by1), 0, None)
    inter = inter_w * inter_h
    union = (a[:, 2] * a[:, 3])[:, None] + (b[:, 2] * b[:, 3])[None, :] - inter
    return np.where(union > 0, inter / np.maximum(union, 1e-12), 0.0)


def average_precision(scores: np.ndarray, matched: np.ndarray, n_gt: int) -> float:
    """All-point interpolated AP from detections sorted by score (matched = 1 for TP)."""
    if n_gt == 0:
        return float("nan")
    if len(scores) == 0:
        return 0.0
    order = np.argsort(-scores, kind="mergesort")
    tp = np.cumsum(matched[order])
    fp = np.cumsum(1 - matched[order])
    recall = tp / n_gt
    precision = tp / np.maximum(tp + fp, 1e-12)
    precision = np.maximum.accumulate(precision[::-1])[::-1]  # monotone envelope
    recall = np.r_[0.0, recall]
    precision = np.r_[precision[0] if len(precision) else 1.0, precision]
    return float(np.sum(np.diff(recall) * precision[1:]))


class Evaluator:
    def __init__(self, gt: dict, predictions: list[dict], ignore_crowd: bool = True):
        self.images = {img["id"]: img for img in gt.get("images", [])}
        self.categories = {c["id"]: c.get("name", str(c["id"])) for c in gt.get("categories", [])}
        self.gt_by_image_cat: dict[tuple, list[dict]] = defaultdict(list)
        self.gt_by_cat: dict[int, int] = defaultdict(int)
        self.gt_all: dict[int, list[dict]] = defaultdict(list)
        skipped = 0
        for ann in gt.get("annotations", []):
            if ignore_crowd and ann.get("iscrowd"):
                skipped += 1
                continue
            self.gt_by_image_cat[(ann["image_id"], ann["category_id"])].append(ann)
            self.gt_all[ann["image_id"]].append(ann)
            self.gt_by_cat[ann["category_id"]] += 1
        self.crowd_skipped = skipped
        self.preds_by_image_cat: dict[tuple, list[dict]] = defaultdict(list)
        self.preds_all: dict[int, list[dict]] = defaultdict(list)
        for det in predictions:
            self.preds_by_image_cat[(det["image_id"], det["category_id"])].append(det)
            self.preds_all[det["image_id"]].append(det)
        self.predictions = predictions

    def match(self, iou_threshold: float, category: int | None = None, image_ids=None,
              area_range: tuple[float, float] | None = None):
        """Greedy highest-score-first matching, as COCO does. Returns (scores, matched, n_gt)."""
        scores, matched, n_gt = [], [], 0
        keys = [k for k in set(self.gt_by_image_cat) | set(self.preds_by_image_cat)
                if (category is None or k[1] == category) and (image_ids is None or k[0] in image_ids)]
        for image_id, cat in keys:
            gts = self.gt_by_image_cat.get((image_id, cat), [])
            dets = sorted(self.preds_by_image_cat.get((image_id, cat), []), key=lambda d: -d["score"])
            if area_range is not None:
                keep_gt = [g for g in gts if area_range[0] <= g.get("area", g["bbox"][2] * g["bbox"][3]) < area_range[1]]
            else:
                keep_gt = gts
            n_gt += len(keep_gt)
            if not dets:
                continue
            gt_boxes = np.array([g["bbox"] for g in gts], dtype=float) if gts else np.zeros((0, 4))
            det_boxes = np.array([d["bbox"] for d in dets], dtype=float)
            ious = iou_matrix(det_boxes, gt_boxes)
            used = set()
            in_range = [i for i, g in enumerate(gts) if g in keep_gt]
            for di, det in enumerate(dets):
                best, best_iou = -1, iou_threshold
                for gi in range(len(gts)):
                    if gi in used or ious[di, gi] < best_iou:
                        continue
                    best, best_iou = gi, ious[di, gi]
                if best >= 0:
                    used.add(best)
                    if best in in_range:
                        scores.append(det["score"])
                        matched.append(1)
                    # a detection matched to an out-of-range GT is ignored, as in COCO
                elif area_range is None or area_range[0] <= det["bbox"][2] * det["bbox"][3] < area_range[1]:
                    scores.append(det["score"])
                    matched.append(0)
        return np.array(scores, dtype=float), np.array(matched, dtype=float), n_gt

    def ap(self, iou_threshold: float, category: int | None = None, image_ids=None, area_range=None) -> float:
        return average_precision(*self.match(iou_threshold, category, image_ids, area_range))

    def map_range(self, category: int | None = None, image_ids=None, area_range=None) -> float:
        values = [self.ap(t, category, image_ids, area_range) for t in IOU_THRESHOLDS]
        values = [v for v in values if not np.isnan(v)]
        return float(np.mean(values)) if values else float("nan")

    def operating_point(self, score_threshold: float, iou_threshold: float, image_ids=None) -> dict:
        """Counts and the error taxonomy at one score threshold, across all classes."""
        tp = fp_duplicate = fp_localization = fp_classification = fp_both = fp_background = 0
        matched_gt = 0
        total_gt = 0
        for image_id in set(self.gt_all) | set(self.preds_all):
            if image_ids is not None and image_id not in image_ids:
                continue
            gts = self.gt_all.get(image_id, [])
            total_gt += len(gts)
            dets = sorted([d for d in self.preds_all.get(image_id, []) if d["score"] >= score_threshold],
                          key=lambda d: -d["score"])
            if not gts and not dets:
                continue
            gt_boxes = np.array([g["bbox"] for g in gts], dtype=float) if gts else np.zeros((0, 4))
            gt_cats = np.array([g["category_id"] for g in gts]) if gts else np.zeros(0)
            det_boxes = np.array([d["bbox"] for d in dets], dtype=float) if dets else np.zeros((0, 4))
            ious = iou_matrix(det_boxes, gt_boxes)
            claimed = set()
            for di, det in enumerate(dets):
                same_class = np.where(gt_cats == det["category_id"])[0] if len(gt_cats) else np.array([], dtype=int)
                best_same = max(same_class, key=lambda gi: ious[di, gi], default=-1)
                iou_same = ious[di, best_same] if best_same >= 0 else 0.0
                best_any = int(np.argmax(ious[di])) if ious.shape[1] else -1
                iou_any = ious[di, best_any] if best_any >= 0 else 0.0
                if iou_same >= iou_threshold:
                    if best_same in claimed:
                        fp_duplicate += 1
                    else:
                        claimed.add(best_same)
                        tp += 1
                elif iou_same >= 0.1:
                    fp_localization += 1
                elif iou_any >= iou_threshold:
                    fp_classification += 1
                elif iou_any >= 0.1:
                    fp_both += 1
                else:
                    fp_background += 1
            matched_gt += len(claimed)
        fp = fp_duplicate + fp_localization + fp_classification + fp_both + fp_background
        precision = tp / (tp + fp) if tp + fp else 0.0
        recall = matched_gt / total_gt if total_gt else 0.0
        return {
            "score_threshold": round(score_threshold, 4), "iou_threshold": iou_threshold,
            "true_positives": tp, "false_positives": fp, "missed_ground_truth": total_gt - matched_gt,
            "precision": round(precision, 4), "recall": round(recall, 4),
            "f1": round(2 * precision * recall / (precision + recall), 4) if precision + recall else 0.0,
            "false_positive_types": {"duplicate": fp_duplicate, "localization": fp_localization,
                                     "classification": fp_classification, "both": fp_both, "background": fp_background},
        }


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog="See the module docstring for input formats.")
    parser.add_argument("--gt", required=True, help="COCO-format ground truth JSON")
    parser.add_argument("--pred", required=True, help="COCO-format detection results JSON")
    parser.add_argument("--score-threshold", type=float, default=0.5, help="operating point score (default 0.5)")
    parser.add_argument("--iou-threshold", type=float, default=0.5, help="operating point IoU (default 0.5)")
    parser.add_argument("--slices", help="JSON of per-image attributes for slice metrics")
    parser.add_argument("--include-crowd", action="store_true", help="do not ignore iscrowd annotations")
    parser.add_argument("--out", help="write the JSON report here")
    args = parser.parse_args(argv)

    gt = load_json(args.gt)
    preds = load_json(args.pred)
    if isinstance(preds, dict):
        preds = preds.get("annotations") or preds.get("detections") or preds.get("results") or []
    if not isinstance(preds, list):
        sys.exit("error: predictions must be a list of detections in COCO results format")
    for det in preds:
        missing = {"image_id", "category_id", "bbox", "score"} - set(det)
        if missing:
            sys.exit(f"error: detection missing keys {sorted(missing)}: {det}")

    ev = Evaluator(gt, preds, ignore_crowd=not args.include_crowd)
    unknown_images = {d["image_id"] for d in preds} - set(ev.images)
    unknown_cats = {d["category_id"] for d in preds} - set(ev.categories)

    def clean(value: float):  # NaN is not valid JSON for strict parsers
        return None if np.isnan(value) else round(float(value), 4)

    per_class = {}
    for cat_id, name in sorted(ev.categories.items(), key=lambda kv: kv[1]):
        per_class[name] = {
            "gt_count": ev.gt_by_cat.get(cat_id, 0),
            "ap50": clean(ev.ap(0.5, cat_id)),
            "map50_95": clean(ev.map_range(cat_id)),
        }
    report = {
        "images": len(ev.images), "annotations": sum(ev.gt_by_cat.values()), "detections": len(preds),
        "crowd_annotations_ignored": ev.crowd_skipped,
        "map50_95": clean(ev.map_range()), "ap50": clean(ev.ap(0.5)), "ap75": clean(ev.ap(0.75)),
        "by_size": {name: clean(ev.map_range(area_range=rng)) for name, rng in SIZE_RANGES.items()},
        "per_class": per_class,
        "operating_point": ev.operating_point(args.score_threshold, args.iou_threshold),
        "warnings": [],
    }
    if unknown_images:
        report["warnings"].append(f"{len(unknown_images)} predicted image_ids are not in the ground truth")
    if unknown_cats:
        report["warnings"].append(f"predicted category_ids not in ground truth: {sorted(unknown_cats)[:10]}")

    # F1-optimal threshold sweep
    sweep = []
    for t in np.round(np.arange(0.05, 0.96, 0.05), 2):
        m = ev.operating_point(float(t), args.iou_threshold)
        sweep.append({"score_threshold": float(t), "precision": m["precision"], "recall": m["recall"], "f1": m["f1"]})
    report["threshold_sweep"] = sweep
    report["f1_optimal"] = max(sweep, key=lambda m: m["f1"])

    # Slices
    if args.slices:
        raw = load_json(args.slices)
        attributes = raw.get("images", raw)
        attributes = {int(k) if str(k).isdigit() else k: v for k, v in attributes.items()}
        keys = sorted({k for v in attributes.values() for k in v})
        report["slices"] = {}
        for key in keys:
            groups: dict[str, list] = defaultdict(list)
            for image_id, attrs in attributes.items():
                if key in attrs:
                    groups[str(attrs[key])].append(image_id)
            report["slices"][key] = {}
            for value, ids in sorted(groups.items()):
                ids_set = set(ids)
                op = ev.operating_point(args.score_threshold, args.iou_threshold, image_ids=ids_set)
                report["slices"][key][value] = {
                    "images": len(ids), "map50_95": clean(ev.map_range(image_ids=ids_set)),
                    "recall": op["recall"], "precision": op["precision"],
                }

    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(f"{report['images']} images, {report['annotations']} annotations, {report['detections']} detections")
    print(f"mAP@[.50:.95] {report['map50_95']} | AP50 {report['ap50']} | AP75 {report['ap75']}")
    print(f"by size: small {report['by_size']['small']} | medium {report['by_size']['medium']} | large {report['by_size']['large']}")
    op = report["operating_point"]
    print(f"at score>={op['score_threshold']} IoU>={op['iou_threshold']}: precision {op['precision']} recall {op['recall']} "
          f"F1 {op['f1']} (TP {op['true_positives']}, FP {op['false_positives']}, missed {op['missed_ground_truth']})")
    print("  false positives: " + ", ".join(f"{k} {v}" for k, v in op["false_positive_types"].items()))
    best = report["f1_optimal"]
    print(f"  F1-optimal score threshold {best['score_threshold']} (F1 {best['f1']}, precision {best['precision']}, recall {best['recall']})")
    scored = [(n, m) for n, m in per_class.items() if m["map50_95"] is not None]
    worst = sorted(scored, key=lambda kv: kv[1]["map50_95"])[:5]
    if worst:
        print("weakest classes: " + ", ".join(f"{n} ({m['map50_95']}, n={m['gt_count']})" for n, m in worst))
    empty = [n for n, m in per_class.items() if m["gt_count"] == 0]
    if empty:
        print(f"classes with no ground truth (not scored): {', '.join(empty[:10])}")
    for key, values in report.get("slices", {}).items():
        line = ", ".join(f"{v} mAP {m['map50_95']} recall {m['recall']}" for v, m in values.items())
        print(f"slice {key}: {line}")
    for w in report["warnings"]:
        print(f"WARNING {w}")
    if args.out:
        print(f"JSON report: {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
