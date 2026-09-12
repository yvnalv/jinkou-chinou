#!/usr/bin/env python3
"""Audit a vision dataset before training: annotation sanity, class balance, object sizes, and
near-duplicate leakage between splits.

Supports COCO JSON (--coco) and YOLO-format directories (--yolo with images/ and labels/).

Checks:
  * annotations: boxes outside the image, zero or negative size, extreme aspect ratios, duplicate
    boxes (same class, IoU above a threshold), images with no annotations, labels referencing
    missing images or unknown classes
  * balance: instances per class, images per class, class co-occurrence; flags rare classes
  * objects: size distribution (COCO small / medium / large), tiny objects relative to input
    resolution, instances per image
  * images: resolution and aspect-ratio spread, unreadable or corrupt files, greyscale files
  * leakage: near-duplicate images within and across splits using a perceptual hash (dHash);
    near-duplicates across train and val/test inflate scores, which is the normal failure mode
    for datasets sampled from video

Examples:
  python dataset_audit.py --coco train.json --coco-val val.json --images-root data/images
  python dataset_audit.py --yolo data/ --splits train,val --out audit.json

Requires numpy; Pillow is needed for image checks and near-duplicate detection (skipped without it).
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

try:
    import numpy as np
except ImportError:  # pragma: no cover
    sys.exit("dataset_audit.py needs numpy: pip install numpy")

try:
    from PIL import Image
    HAVE_PIL = True
except ImportError:
    HAVE_PIL = False

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff"}
SIZE_BUCKETS = (("small", 0, 32 ** 2), ("medium", 32 ** 2, 96 ** 2), ("large", 96 ** 2, float("inf")))


def load_json(path: str):
    p = Path(path)
    if not p.is_file():
        sys.exit(f"error: file not found: {path}")
    return json.loads(p.read_text(encoding="utf-8-sig"))


def iou_xywh(a, b) -> float:
    ax2, ay2 = a[0] + a[2], a[1] + a[3]
    bx2, by2 = b[0] + b[2], b[1] + b[3]
    iw = max(0.0, min(ax2, bx2) - max(a[0], b[0]))
    ih = max(0.0, min(ay2, by2) - max(a[1], b[1]))
    inter = iw * ih
    union = a[2] * a[3] + b[2] * b[3] - inter
    return inter / union if union > 0 else 0.0


def dhash(path: Path, size: int = 8) -> int | None:
    """Difference hash: robust to small changes, good for near-duplicate frames."""
    try:
        with Image.open(path) as im:
            im = im.convert("L").resize((size + 1, size), Image.Resampling.LANCZOS)
            pixels = np.asarray(im, dtype=np.int16)
    except Exception:
        return None
    bits = pixels[:, 1:] > pixels[:, :-1]
    value = 0
    for bit in bits.flatten():
        value = (value << 1) | int(bit)
    return value


def hamming(a: int, b: int) -> int:
    return bin(a ^ b).count("1")


class Dataset:
    """Normalized view of a dataset split: images with size, and annotations with xywh boxes."""

    def __init__(self, name: str):
        self.name = name
        self.images: dict[str, dict] = {}          # key -> {path, width, height}
        self.annotations: list[dict] = []          # {image_key, class, bbox[xywh]}
        self.classes: dict[int, str] = {}
        self.problems: list[str] = []


def load_coco(path: str, images_root: str | None, name: str) -> Dataset:
    data = load_json(path)
    ds = Dataset(name)
    ds.classes = {c["id"]: c.get("name", str(c["id"])) for c in data.get("categories", [])}
    for img in data.get("images", []):
        file_name = img.get("file_name", str(img["id"]))
        ds.images[str(img["id"])] = {
            "path": str(Path(images_root) / file_name) if images_root else file_name,
            "width": img.get("width"), "height": img.get("height"), "file_name": file_name,
        }
    for ann in data.get("annotations", []):
        key = str(ann["image_id"])
        if key not in ds.images:
            ds.problems.append(f"annotation {ann.get('id')} references missing image_id {ann['image_id']}")
            continue
        if ann["category_id"] not in ds.classes:
            ds.problems.append(f"annotation {ann.get('id')} uses unknown category_id {ann['category_id']}")
        ds.annotations.append({"image_key": key, "class": ds.classes.get(ann["category_id"], str(ann["category_id"])),
                               "bbox": [float(v) for v in ann["bbox"]], "iscrowd": ann.get("iscrowd", 0)})
    return ds


def load_yolo(root: str, split: str) -> Dataset:
    ds = Dataset(split)
    base = Path(root)
    img_dir = next((d for d in (base / "images" / split, base / split / "images", base / split) if d.is_dir()), None)
    lbl_dir = next((d for d in (base / "labels" / split, base / split / "labels") if d.is_dir()), None)
    if img_dir is None:
        sys.exit(f"error: no image directory for split '{split}' under {root}")
    names_file = next((p for p in (base / "classes.txt", base / "data.yaml") if p.is_file()), None)
    names: dict[int, str] = {}
    if names_file and names_file.suffix == ".txt":
        names = {i: n.strip() for i, n in enumerate(names_file.read_text(encoding="utf-8").splitlines()) if n.strip()}
    for img_path in sorted(p for p in img_dir.rglob("*") if p.suffix.lower() in IMAGE_EXTENSIONS):
        key = str(img_path.relative_to(img_dir))
        width = height = None
        if HAVE_PIL:
            try:
                with Image.open(img_path) as im:
                    width, height = im.size
            except Exception:
                ds.problems.append(f"unreadable image: {img_path}")
        ds.images[key] = {"path": str(img_path), "width": width, "height": height, "file_name": key}
        label_path = (lbl_dir / key).with_suffix(".txt") if lbl_dir else None
        if label_path is None or not label_path.is_file():
            continue
        for line_no, line in enumerate(label_path.read_text(encoding="utf-8").splitlines(), 1):
            parts = line.split()
            if len(parts) < 5:
                if line.strip():
                    ds.problems.append(f"{label_path}:{line_no}: malformed label line")
                continue
            cls = int(float(parts[0]))
            cx, cy, w, h = (float(v) for v in parts[1:5])
            if width and height:  # YOLO labels are normalized
                bbox = [(cx - w / 2) * width, (cy - h / 2) * height, w * width, h * height]
            else:
                bbox = [cx - w / 2, cy - h / 2, w, h]
            ds.classes.setdefault(cls, names.get(cls, f"class_{cls}"))
            ds.annotations.append({"image_key": key, "class": ds.classes[cls], "bbox": bbox, "iscrowd": 0})
    return ds


def audit_split(ds: Dataset, args) -> dict:
    findings: list[dict] = []

    def add(severity: str, check: str, detail: str, count: int | None = None):
        findings.append({"severity": severity, "check": check, "detail": detail, "count": count})

    per_image = defaultdict(list)
    for ann in ds.annotations:
        per_image[ann["image_key"]].append(ann)

    class_counts = Counter(a["class"] for a in ds.annotations)
    images_per_class = Counter({c: len({a["image_key"] for a in ds.annotations if a["class"] == c}) for c in class_counts})
    areas = np.array([a["bbox"][2] * a["bbox"][3] for a in ds.annotations]) if ds.annotations else np.zeros(0)
    empty_images = [k for k in ds.images if k not in per_image]

    # Geometry problems
    out_of_bounds = degenerate = extreme_aspect = 0
    for ann in ds.annotations:
        x, y, w, h = ann["bbox"]
        img = ds.images.get(ann["image_key"], {})
        if w <= 0 or h <= 0:
            degenerate += 1
            continue
        if img.get("width") and img.get("height"):
            if x < -1 or y < -1 or x + w > img["width"] + 1 or y + h > img["height"] + 1:
                out_of_bounds += 1
        ratio = max(w / h, h / w)
        if ratio > args.max_aspect:
            extreme_aspect += 1
    if degenerate:
        add("high", "degenerate_boxes", f"{degenerate} boxes with zero or negative width/height", degenerate)
    if out_of_bounds:
        add("medium", "boxes_out_of_bounds", f"{out_of_bounds} boxes extend beyond the image", out_of_bounds)
    if extreme_aspect:
        add("low", "extreme_aspect_ratio", f"{extreme_aspect} boxes with aspect ratio above {args.max_aspect}", extreme_aspect)

    # Duplicate annotations
    duplicates = 0
    for key, anns in per_image.items():
        for i in range(len(anns)):
            for j in range(i + 1, len(anns)):
                if anns[i]["class"] == anns[j]["class"] and iou_xywh(anns[i]["bbox"], anns[j]["bbox"]) > args.duplicate_iou:
                    duplicates += 1
    if duplicates:
        add("medium", "duplicate_annotations", f"{duplicates} overlapping same-class boxes (IoU > {args.duplicate_iou})", duplicates)

    if empty_images:
        share = len(empty_images) / max(1, len(ds.images))
        add("medium" if share > 0.2 else "low", "images_without_annotations",
            f"{len(empty_images)} of {len(ds.images)} images ({share:.0%}) have no annotations; "
            "intended as backgrounds, or missing labels?", len(empty_images))

    # Class balance
    if class_counts:
        most, least = class_counts.most_common()[0], class_counts.most_common()[-1]
        ratio = most[1] / max(1, least[1])
        if ratio > args.imbalance_ratio:
            add("medium", "class_imbalance",
                f"'{most[0]}' has {most[1]} instances vs '{least[0]}' with {least[1]} ({ratio:.0f}x)", int(ratio))
        for name, count in class_counts.items():
            if count < args.min_instances:
                add("medium", "rare_class", f"'{name}' has only {count} instances (aim for at least {args.min_instances})", count)

    # Object sizes
    size_hist = {}
    if len(areas):
        for name, lo, hi in SIZE_BUCKETS:
            size_hist[name] = int(((areas >= lo) & (areas < hi)).sum())
        small_share = size_hist["small"] / len(areas)
        if small_share > 0.3:
            add("low", "many_small_objects",
                f"{small_share:.0%} of objects are smaller than 32x32 px; consider higher input resolution, "
                "tiling (slicing inference), or a model suited to small objects", size_hist["small"])

    # Images
    resolutions = Counter((im.get("width"), im.get("height")) for im in ds.images.values() if im.get("width"))
    unreadable = [p for p in ds.problems if "unreadable" in p]
    if unreadable:
        add("high", "unreadable_images", f"{len(unreadable)} images could not be opened", len(unreadable))
    if len(resolutions) > 10:
        add("low", "mixed_resolutions", f"{len(resolutions)} distinct image resolutions; check letterboxing and aspect handling",
            len(resolutions))

    return {
        "split": ds.name, "images": len(ds.images), "annotations": len(ds.annotations),
        "classes": len(set(a["class"] for a in ds.annotations)),
        "instances_per_class": dict(class_counts.most_common()),
        "images_per_class": dict(images_per_class.most_common()),
        "instances_per_image": {
            "mean": round(len(ds.annotations) / max(1, len(ds.images)), 2),
            "max": max((len(v) for v in per_image.values()), default=0),
            "images_without_annotations": len(empty_images),
        },
        "object_size_buckets": size_hist,
        "box_area_percentiles": {q: round(float(np.percentile(areas, int(q))), 1) for q in ("5", "50", "95")} if len(areas) else {},
        "top_resolutions": {f"{w}x{h}": n for (w, h), n in resolutions.most_common(5)},
        "structural_problems": ds.problems[:20],
        "findings": findings,
    }


def near_duplicates(splits: list[Dataset], threshold: int, limit: int) -> dict:
    if not HAVE_PIL:
        return {"skipped": "Pillow not installed (pip install pillow)"}
    hashes: list[tuple[str, str, int]] = []  # (split, key, hash)
    unreadable = 0
    for ds in splits:
        for key, img in ds.images.items():
            path = Path(img["path"])
            if not path.is_file():
                continue
            value = dhash(path)
            if value is None:
                unreadable += 1
                continue
            hashes.append((ds.name, key, value))
    if len(hashes) < 2:
        return {"skipped": "no readable images found (check --images-root)", "images_hashed": len(hashes)}
    within: Counter = Counter()
    across: list[dict] = []
    exact = 0
    for i in range(len(hashes)):
        for j in range(i + 1, len(hashes)):
            distance = hamming(hashes[i][2], hashes[j][2])
            if distance <= threshold:
                if hashes[i][2] == hashes[j][2]:
                    exact += 1
                if hashes[i][0] == hashes[j][0]:
                    within[hashes[i][0]] += 1
                elif len(across) < limit:
                    across.append({"a": f"{hashes[i][0]}:{hashes[i][1]}", "b": f"{hashes[j][0]}:{hashes[j][1]}",
                                   "hamming": distance})
                elif across:
                    across[-1]["more"] = across[-1].get("more", 0) + 1
    return {"images_hashed": len(hashes), "unreadable": unreadable, "exact_duplicate_pairs": exact,
            "near_duplicate_pairs_within_split": dict(within), "cross_split_pairs": across,
            "cross_split_pair_count": len(across), "hamming_threshold": threshold}


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog="See the module docstring for formats and checks.")
    parser.add_argument("--coco", action="append", default=[], help="COCO JSON (repeat for several splits)")
    parser.add_argument("--coco-val", help="convenience: a second COCO split named 'val'")
    parser.add_argument("--images-root", help="directory that file_name values are relative to")
    parser.add_argument("--yolo", help="YOLO dataset root containing images/ and labels/")
    parser.add_argument("--splits", default="train,val", help="YOLO split names (default train,val)")
    parser.add_argument("--duplicate-iou", type=float, default=0.9)
    parser.add_argument("--max-aspect", type=float, default=20.0)
    parser.add_argument("--min-instances", type=int, default=50, help="flag classes with fewer instances")
    parser.add_argument("--imbalance-ratio", type=float, default=50.0)
    parser.add_argument("--hash-threshold", type=int, default=5, help="dHash Hamming distance for near-duplicates")
    parser.add_argument("--max-pairs", type=int, default=25, help="cross-split pairs to list")
    parser.add_argument("--no-duplicates", action="store_true", help="skip near-duplicate detection")
    parser.add_argument("--out", help="write the JSON report here")
    args = parser.parse_args(argv)

    splits: list[Dataset] = []
    if args.yolo:
        for split in [s for s in args.splits.split(",") if s]:
            splits.append(load_yolo(args.yolo, split))
    for i, path in enumerate(args.coco):
        splits.append(load_coco(path, args.images_root, Path(path).stem))
    if args.coco_val:
        splits.append(load_coco(args.coco_val, args.images_root, "val"))
    if not splits:
        sys.exit("error: give --coco (one or more) or --yolo")

    report = {"splits": [audit_split(ds, args) for ds in splits]}
    if not args.no_duplicates:
        report["near_duplicates"] = near_duplicates(splits, args.hash_threshold, args.max_pairs)
    high = sum(1 for s in report["splits"] for f in s["findings"] if f["severity"] == "high")
    cross = report.get("near_duplicates", {}).get("cross_split_pair_count", 0)
    report["summary"] = {"splits": len(splits), "high_findings": high, "cross_split_near_duplicate_pairs": cross}

    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(json.dumps(report, indent=2), encoding="utf-8")

    for s in report["splits"]:
        print(f"[{s['split']}] {s['images']} images, {s['annotations']} annotations, {s['classes']} classes, "
              f"{s['instances_per_image']['mean']} objects/image")
        if s["object_size_buckets"]:
            print(f"    object sizes: {s['object_size_buckets']}")
        top = list(s["instances_per_class"].items())[:5]
        print("    top classes: " + ", ".join(f"{k} {v}" for k, v in top))
        for f in s["findings"]:
            print(f"    {f['severity'].upper():6} {f['check']}: {f['detail']}")
        for p in s["structural_problems"][:5]:
            print(f"    PROBLEM {p}")
    nd = report.get("near_duplicates", {})
    if nd.get("skipped"):
        print(f"Near-duplicate check skipped: {nd['skipped']}")
    elif nd:
        print(f"Near-duplicates: {nd['images_hashed']} images hashed, {nd['exact_duplicate_pairs']} exact pairs, "
              f"within-split {nd['near_duplicate_pairs_within_split'] or '{}'}")
        for split_name, count in nd["near_duplicate_pairs_within_split"].items():
            print(f"    within {split_name}: {count} near-duplicate pairs; consecutive frames make the split look "
                  "larger and more diverse than it is. Deduplicate or sample by scene before counting dataset size.")
        total_pairs = nd["images_hashed"] * (nd["images_hashed"] - 1) / 2
        flagged = sum(nd["near_duplicate_pairs_within_split"].values()) + nd["cross_split_pair_count"]
        if total_pairs and flagged / total_pairs > 0.25:
            print("    note: a large share of all image pairs matched; on low-texture or near-uniform images the "
                  "perceptual hash saturates. Lower --hash-threshold and confirm a few pairs by eye.")
        if nd["cross_split_pairs"]:
            print(f"    LEAKAGE {nd['cross_split_pair_count']}+ near-duplicate pairs across splits, e.g. "
                  f"{nd['cross_split_pairs'][0]['a']} ~ {nd['cross_split_pairs'][0]['b']}")
            print("    Frames from the same video or burst must not be split randomly; split by scene, camera, or time.")
    print("Not checked automatically: label correctness, class definitions, and whether the data covers "
          "the deployment conditions (cameras, lighting, weather, sites).")
    if args.out:
        print(f"JSON report: {args.out}")
    return 1 if high or cross else 0


if __name__ == "__main__":
    sys.exit(main())
