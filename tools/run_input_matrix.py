"""Run timed controller masks and summarize the SMS capture outcomes."""
from pathlib import Path
import argparse
import json
import subprocess
import sys

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("rom", type=Path)
parser.add_argument("--out", type=Path, required=True)
parser.add_argument("--max-steps", type=int, default=650)
parser.add_argument("--press-start", type=int, default=260)
parser.add_argument("--press-runs", type=int, default=30)
parser.add_argument("--masks", default="0xFE,0xFD,0xFB,0xF7,0xEF,0xDF,0xBF,0x7F")
args = parser.parse_args()

masks = [int(value.strip(), 0) & 0xFF for value in args.masks.split(",")]
prefix = [0xFF] * args.press_start
suffix = [0xFF] * args.press_runs
results = []
for mask in masks:
    sequence = prefix + [mask] * args.press_runs + suffix
    sequence_arg = ",".join(f"0x{value:02X}" for value in sequence)
    report_path = args.out.with_name(f"{args.out.stem}-{mask:02X}.json")
    trace_path = args.out.with_name(f"{args.out.stem}-{mask:02X}-trace.json")
    command = [sys.executable, str(Path(__file__).with_name("run_sms_capture.py")),
               str(args.rom), "--max-steps", str(args.max_steps),
               "--ticks-per-run", "100000", "--vdp-wait-reads", "2",
               "--scanline-irq", "--dega-frame-schedule", "--irq-every-runs", "0",
               "--input-sequence", sequence_arg, "--trace-pc-range", "0x0000-0x4B20",
               "--trace-limit", "150000", "--trace-out", str(trace_path),
               "--out", str(report_path)]
    subprocess.run(command, check=True, stdout=subprocess.DEVNULL)
    report = json.loads(report_path.read_text(encoding="utf-8"))
    trace = report["trace"]["records"]
    controller = [item for item in trace if item["kind"] == "controller_read"]
    results.append({
        "mask": f"0x{mask:02X}",
        "result": report["result"],
        "steps": report["steps"],
        "pc": report["pc"],
        "sp": report["sp"],
        "bank_fffe": report["mapper"]["0xFFFE"],
        "bank_ffff": report["mapper"]["0xFFFF"],
        "irq_count": sum(item["kind"] == "irq_injected" for item in trace),
        "controller_reads": [(item["run"], item["value"]) for item in controller],
        "report": str(report_path),
        "trace": str(trace_path),
    })

args.out.write_text(json.dumps({
    "rom": str(args.rom),
    "press_start": args.press_start,
    "press_runs": args.press_runs,
    "results": results,
}, indent=2) + "\n", encoding="utf-8")
for item in results:
    print(item["mask"], item["pc"], item["bank_ffff"],
          "irq=" + str(item["irq_count"]),
          "reads=" + str(item["controller_reads"]))
