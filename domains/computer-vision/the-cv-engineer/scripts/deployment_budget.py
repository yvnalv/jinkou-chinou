#!/usr/bin/env python3
"""Size a vision deployment: how many streams fit on a device, how many devices are needed, and what
edge versus server costs in compute, bandwidth, and money.

Everything is computed from numbers you supply. The script never invents hardware performance:
measure your model's latency on the target device (batch 1 and, if you batch, at your batch size)
and pass it in. Assumptions are printed with the result.

Inputs:
  --cameras N                 number of camera streams
  --fps F                     frames per second that must be ANALYSED per stream (often far below capture fps)
  --infer-ms MS               measured model latency per frame on the target device (batch 1)
  [--batch B --batch-ms MS]   measured latency for a full batch (throughput mode)
  [--decode-ms MS]            per-frame decode and preprocess cost (often 20-50% of the budget)
  [--extra-ms MS]             tracking, business logic, drawing, messaging per frame
  [--devices-available N]     check whether a planned fleet is enough
  [--device-cost USD --device-power-w W --energy-cost USD_PER_KWH]
  [--utilization 0.7]         headroom target: never plan for 100% busy
  [--stream-mbps M]           per-camera video bitrate, for the "send video to the cloud" comparison
  [--event-kb K --events-per-hour E]  payload when only events leave the device
  [--cloud-gpu-cost USD_PER_HOUR --cloud-gpu-streams N]  server-side alternative
  [--retention-days D]        storage estimate for recorded video

Examples:
  python deployment_budget.py --cameras 24 --fps 5 --infer-ms 18 --decode-ms 6 --utilization 0.7
  python deployment_budget.py --cameras 200 --fps 2 --infer-ms 9 --batch 8 --batch-ms 42 \
      --device-cost 2000 --device-power-w 60 --energy-cost 0.25 --stream-mbps 4 --cloud-gpu-cost 1.2 --cloud-gpu-streams 40

Standard library only.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                formatter_class=argparse.RawDescriptionHelpFormatter,
                                epilog="See the module docstring for all inputs and examples.")
    p.add_argument("--cameras", type=int, required=True)
    p.add_argument("--fps", type=float, required=True, help="analysed frames per second per camera")
    p.add_argument("--infer-ms", type=float, required=True, help="measured inference latency per frame (batch 1)")
    p.add_argument("--batch", type=int, default=1)
    p.add_argument("--batch-ms", type=float, help="measured latency for one full batch")
    p.add_argument("--decode-ms", type=float, default=0.0)
    p.add_argument("--extra-ms", type=float, default=0.0, help="tracking, logic, encoding, messaging per frame")
    p.add_argument("--utilization", type=float, default=0.7, help="target maximum utilization (default 0.7)")
    p.add_argument("--devices-available", type=int)
    p.add_argument("--device-cost", type=float, help="capital cost per device")
    p.add_argument("--device-power-w", type=float)
    p.add_argument("--energy-cost", type=float, default=0.0, help="currency per kWh")
    p.add_argument("--stream-mbps", type=float, help="per-camera bitrate if video is sent off-site")
    p.add_argument("--event-kb", type=float, help="payload size per event if only events are sent")
    p.add_argument("--events-per-hour", type=float, default=0.0)
    p.add_argument("--cloud-gpu-cost", type=float, help="hourly cost of one server GPU instance")
    p.add_argument("--cloud-gpu-streams", type=float, help="streams one server GPU instance handles (measured)")
    p.add_argument("--retention-days", type=float)
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)

    if not 0 < args.utilization <= 1:
        sys.exit("error: --utilization must be between 0 and 1")
    if args.batch > 1 and not args.batch_ms:
        sys.exit("error: --batch needs --batch-ms (measured latency for the whole batch)")

    per_frame_infer = (args.batch_ms / args.batch) if args.batch > 1 else args.infer_ms
    per_frame_total = per_frame_infer + args.decode_ms + args.extra_ms
    device_fps_capacity = 1000.0 / per_frame_total if per_frame_total else float("inf")
    usable_fps = device_fps_capacity * args.utilization
    required_fps = args.cameras * args.fps
    devices_needed = -(-required_fps // usable_fps) if usable_fps else float("inf")  # ceil
    streams_per_device = usable_fps / args.fps if args.fps else float("inf")

    # Worst-case latency for one frame: queueing behind a full batch plus processing
    worst_case_latency_ms = per_frame_total * args.batch if args.batch > 1 else per_frame_total

    result = {
        "inputs": {k: v for k, v in vars(args).items() if v is not None and k != "json"},
        "per_frame_ms": {"inference": round(per_frame_infer, 2), "decode": args.decode_ms,
                         "extra": args.extra_ms, "total": round(per_frame_total, 2)},
        "device_capacity_fps": round(device_fps_capacity, 1),
        "usable_fps_at_utilization": round(usable_fps, 1),
        "streams_per_device": round(streams_per_device, 2),
        "required_fps_total": round(required_fps, 1),
        "devices_needed": int(devices_needed),
        "frame_budget_ms_per_stream": round(1000.0 / args.fps, 1) if args.fps else None,
        "worst_case_frame_latency_ms": round(worst_case_latency_ms, 1),
        "notes": [],
    }
    if args.devices_available is not None:
        result["fleet_check"] = {
            "available": args.devices_available,
            "sufficient": args.devices_available >= devices_needed,
            "utilization_if_used": round(required_fps / (args.devices_available * device_fps_capacity), 3)
            if args.devices_available else None,
        }
    if args.device_cost or args.device_power_w:
        capex = (args.device_cost or 0) * result["devices_needed"]
        power_kw = (args.device_power_w or 0) * result["devices_needed"] / 1000
        energy_month = power_kw * 24 * 30 * args.energy_cost
        result["edge_cost"] = {"capex": round(capex, 2), "power_kw": round(power_kw, 3),
                               "energy_per_month": round(energy_month, 2),
                               "note": "excludes cameras, network, mounting, installation, and maintenance"}
    if args.stream_mbps:
        result["bandwidth"] = {
            "video_offsite_mbps": round(args.stream_mbps * args.cameras, 1),
            "video_offsite_tb_per_month": round(args.stream_mbps * args.cameras * 3600 * 24 * 30 / 8 / 1e6, 2),
        }
        if args.event_kb:
            events_mbps = args.event_kb * 8 / 1000 * (args.events_per_hour * args.cameras) / 3600
            result["bandwidth"]["events_only_mbps"] = round(events_mbps, 4)
            if events_mbps > 0:
                result["bandwidth"]["reduction_factor"] = round((args.stream_mbps * args.cameras) / events_mbps, 1)
    if args.cloud_gpu_cost and args.cloud_gpu_streams:
        instances = -(-args.cameras // args.cloud_gpu_streams)
        monthly = instances * args.cloud_gpu_cost * 24 * 30
        result["server_alternative"] = {
            "instances": int(instances), "cost_per_month": round(monthly, 2),
            "note": "add egress/ingest bandwidth, storage, and the latency of sending frames off-site",
        }
        if "edge_cost" in result:
            edge_year = result["edge_cost"]["capex"] + result["edge_cost"]["energy_per_month"] * 12
            server_year = monthly * 12
            result["server_alternative"]["edge_vs_server_year_1"] = {
                "edge": round(edge_year, 2), "server": round(server_year, 2),
                "cheaper": "edge" if edge_year < server_year else "server",
            }
    if args.retention_days and args.stream_mbps:
        result["storage"] = {"tb_for_retention": round(args.stream_mbps * args.cameras * 3600 * 24 *
                                                       args.retention_days / 8 / 1e6, 2)}

    if args.fps and per_frame_total > 1000.0 / args.fps * 1:
        result["notes"].append("one device cannot keep up with a single stream at this fps; reduce fps, resolution, "
                               "or model size, or use a faster device")
    if args.batch > 1:
        result["notes"].append(f"batching {args.batch} frames raises throughput but adds queueing delay; worst-case "
                               f"frame latency is about {result['worst_case_frame_latency_ms']} ms")
    if args.decode_ms == 0:
        result["notes"].append("decode/preprocess set to 0 ms: measure it, it is often 20-50% of the pipeline budget "
                               "unless you use hardware decoding")
    if args.utilization > 0.85:
        result["notes"].append("utilization above 85% leaves no headroom for bursts, retries, or thermal throttling")
    result["notes"].append("latency figures must come from the target device at the production resolution, precision "
                           "(FP16/INT8), and pipeline; datacenter GPU benchmarks do not transfer to edge modules")

    if args.json:
        print(json.dumps(result, indent=2))
        return 0
    fb = result["frame_budget_ms_per_stream"]
    print(f"Per frame: inference {result['per_frame_ms']['inference']} ms + decode {args.decode_ms} ms + extra "
          f"{args.extra_ms} ms = {result['per_frame_ms']['total']} ms")
    print(f"One device: {result['device_capacity_fps']} fps capacity, {result['usable_fps_at_utilization']} fps usable "
          f"at {args.utilization:.0%} utilization -> {result['streams_per_device']} streams at {args.fps} fps each")
    print(f"Workload: {args.cameras} cameras x {args.fps} fps = {result['required_fps_total']} fps "
          f"-> {result['devices_needed']} device(s); per-stream frame budget {fb} ms, "
          f"worst-case frame latency {result['worst_case_frame_latency_ms']} ms")
    if "fleet_check" in result:
        fc = result["fleet_check"]
        print(f"Fleet check: {fc['available']} available -> {'ENOUGH' if fc['sufficient'] else 'NOT ENOUGH'}"
              + (f" (utilization {fc['utilization_if_used']:.0%})" if fc["utilization_if_used"] else ""))
    if "edge_cost" in result:
        e = result["edge_cost"]
        print(f"Edge cost: capex {e['capex']}, power {e['power_kw']} kW, energy {e['energy_per_month']}/month")
    if "bandwidth" in result:
        b = result["bandwidth"]
        line = f"Bandwidth: streaming video off-site {b['video_offsite_mbps']} Mbps ({b['video_offsite_tb_per_month']} TB/month)"
        if "events_only_mbps" in b:
            line += f"; events only {b['events_only_mbps']} Mbps ({b.get('reduction_factor')}x less)"
        print(line)
    if "storage" in result:
        print(f"Storage: {result['storage']['tb_for_retention']} TB for {args.retention_days} days of video")
    if "server_alternative" in result:
        s = result["server_alternative"]
        print(f"Server alternative: {s['instances']} GPU instance(s), {s['cost_per_month']}/month")
        if "edge_vs_server_year_1" in s:
            c = s["edge_vs_server_year_1"]
            print(f"  year 1: edge {c['edge']} vs server {c['server']} -> {c['cheaper']} is cheaper on these numbers")
    for n in result["notes"]:
        print(f"Note: {n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
