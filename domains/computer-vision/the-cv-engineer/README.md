# the-cv-engineer

Computer vision engineering persona covering the whole visual AI lifecycle: task framing and capture design (cameras, lenses, lighting, resolution on target), data collection and annotation with quality control, model choice and training, honest evaluation, and deployment from a single edge device to enterprise multi-camera fleets — with quantization, streaming pipelines, monitoring, cost modelling, and camera-privacy law treated as design inputs.

Domain: `computer-vision` · Type: `core`

## When to use

Invoke with `/the-cv-engineer`, or let Claude pick it up automatically when you ask for things like:

- "Detect and count people entering the store from our existing CCTV." (A → F)
- "Our defect detector misses scratches on dark parts." (A/D/F — usually a lighting problem)
- "Can this run on a Jetson at 15 fps, or do we need a server?" (A/E)
- "mAP is 0.82 but operators say it's useless." (D — operating point and slices)
- "Size a 200-camera deployment: devices, bandwidth, storage, cost." (E)
- "Is our face-recognition idea legal in the EU?" (privacy gate)

| Mode | For | Output |
|---|---|---|
| A — Frame & Capture | Task, cameras, feasibility, metrics, budgets | `docs/cv/CV_DESIGN.md` |
| B — Data & Annotation | Coverage, labeling, splits, audits | Annotation guide, dataset versions, audit report |
| C — Model & Train | Zero-shot prototype, then a trained specialist | Training config, tracked runs, checkpoints |
| D — Evaluate | Operating point, slices, error taxonomy, device latency | Eval report, golden and regression sets |
| E — Deploy | Export, quantization, pipeline, rollout, sizing | Artifacts, pipeline, deployment plan |
| F — Operate & Diagnose | Monitoring, camera health, drift, retraining | Monitoring config, runbook, updated datasets |

Gates: **Feasibility** (can a human do it from the image?), **Split** (no near-duplicate leakage), **Budget** (measured on the target device), **Privacy** (lawful basis, prohibited practices, DPIA).

### Scripts and templates on their own

```text
python scripts/dataset_audit.py --coco train.json --coco val.json --images-root images/
python scripts/dataset_audit.py --yolo data/ --splits train,val --out audit.json
python scripts/detection_eval.py --gt val.json --pred preds.json --score-threshold 0.4 --slices attrs.json
python scripts/deployment_budget.py --cameras 24 --fps 5 --infer-ms 18 --decode-ms 6
python scripts/deployment_budget.py --cameras 200 --fps 2 --infer-ms 9 --batch 8 --batch-ms 42 \
    --device-cost 2000 --stream-mbps 4 --cloud-gpu-cost 1.2 --cloud-gpu-streams 40
python assets/video_pipeline.template.py --cameras 8 --fps 15 --infer-ms 25   # architecture and capacity test
```

Requirements: Python 3.10+, numpy; Pillow for image checks and near-duplicate detection. The scripts never require a deep-learning framework, so they run anywhere — you bring the model's predictions and measured latency.

## Structure

```text
the-cv-engineer/
├── SKILL.md                                  # six modes, principles, four gates, rules, definition of done
├── README.md
├── config/
│   └── skill.yaml                            # manifest + machine-readable policy
├── references/
│   ├── framing-and-capture.md                # task choice, optics and lighting, feasibility gate, budgets
│   ├── data-and-annotation.md                # coverage, labeling QA, formats, splits and leakage, data engine
│   ├── models-and-training.md                # detection, segmentation, tracking, OCR, anomaly, VLMs, training
│   ├── evaluation.md                         # metrics per task, operating points, error taxonomy, latency
│   ├── edge-deployment.md                    # hardware, runtimes, export parity, quantization, fleet ops
│   ├── enterprise-systems.md                 # multi-camera architecture, serving, scaling, cost, integration
│   ├── monitoring-and-operations.md          # camera health, drift without labels, diagnosis playbook
│   ├── privacy-and-regulation.md             # EU AI Act, GDPR, BIPA, privacy by design, fairness
│   ├── CV_DESIGN.template.md
│   ├── ANNOTATION_GUIDE.template.md
│   └── DEPLOYMENT_PLAN.template.md
├── scripts/
│   ├── dataset_audit.py                      # annotations, balance, sizes, near-duplicate split leakage
│   ├── detection_eval.py                     # mAP, operating point, FP taxonomy, slices
│   └── deployment_budget.py                  # devices, bandwidth, storage, edge vs server cost
├── assets/
│   └── video_pipeline.template.py            # streaming pipeline with drop policy and latency stats
└── evals/
    └── evals.json
```

Research basis (verified 2026-09-11): current detector families (NMS-free YOLO generations, RF-DETR past 60 mAP on COCO, D-FINE/RT-DETR), promptable and open-vocabulary segmentation (SAM 3 concept segmentation), vision-language models for documents (Qwen3-VL, InternVL) versus specialist OCR, tracking practice (HOTA as the reported metric, ByteTrack/BoT-SORT families, detector quality dominating), edge hardware (Jetson Orin Nano Super ~67 TOPS at ~$299, Hailo-8L/8/10H, Raspberry Pi AI HATs) and runtimes (TensorRT, ONNX Runtime, OpenVINO, LiteRT, ExecuTorch, Core ML), INT8 quantization typically under 1% accuracy loss when calibrated, multi-camera stacks (DeepStream/Triton), industrial anomaly detection (MVTec AD, few-shot and VLM-guided methods), data-centric practice (foundation-model pre-labeling, active learning), and camera-privacy law (EU AI Act prohibitions and 2 August 2026 transparency date, GDPR, BIPA).

## Changelog

### 0.1.0 — 2026-09-12

- Initial version: six modes across the vision lifecycle, Feasibility, Split, Budget, and Privacy gates, eight references, three templates, three scripts (dataset audit with near-duplicate leakage detection, detection evaluation with error taxonomy verified on hand-checked cases, deployment budget calculator verified against hand arithmetic), and a runnable streaming pipeline template.
