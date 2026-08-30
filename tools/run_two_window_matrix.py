"""Test controller values in the two known causal sampling windows."""
from pathlib import Path
import argparse
import json
import subprocess
import sys

p = argparse.ArgumentParser(description=__doc__)
p.add_argument("rom", type=Path)
p.add_argument("--out", type=Path, required=True)
p.add_argument("--max-steps", type=int, default=900)
p.add_argument("--first-start", type=int, default=260)
p.add_argument("--first-runs", type=int, default=10)
p.add_argument("--second-start", type=int, default=522)
p.add_argument("--second-runs", type=int, default=10)
p.add_argument("--values", default="0x00,0x10,0x20,0x30")
p.add_argument("--dega-io-semantics", action="store_true")
a = p.parse_args()

values = [int(item.strip(), 0) & 0xFF for item in a.values.split(",") if item.strip()]
if not values:
    raise SystemExit("--values must contain at least one value")
if min(a.first_start, a.second_start) < 0 or min(a.first_runs, a.second_runs) < 1:
    raise SystemExit("window starts must be non-negative and run counts positive")
results = []
for first in values:
    for second in values:
        sequence = [0] * a.max_steps
        sequence[a.first_start:a.first_start + a.first_runs] = [first] * a.first_runs
        sequence[a.second_start:a.second_start + a.second_runs] = [second] * a.second_runs
        stem = f"{a.out.stem}-{first:02X}-{second:02X}"
        report_path = a.out.with_name(stem + ".json")
        trace_path = a.out.with_name(stem + "-trace.json")
        command = [sys.executable, str(Path(__file__).with_name("run_sms_capture.py")),
                   str(a.rom), "--max-steps", str(a.max_steps),
                   "--ticks-per-run", "100000", "--scanline-irq",
                   "--dega-frame-schedule", "--irq-every-runs", "0",
                   "--input-sequence", ",".join(f"0x{x:02X}" for x in sequence),
                   "--trace-pc-range", "0x3F00-0x4B20", "--trace-limit", "80000",
                   "--trace-every", "128", "--trace-out", str(trace_path),
                   "--out", str(report_path)]
        if a.dega_io_semantics:
            command.append("--dega-io-semantics")
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL)
        report = json.loads(report_path.read_text(encoding="utf-8"))
        trace = json.loads(trace_path.read_text(encoding="utf-8"))["trace"]["records"]
        reads = [(item["run"], item.get("value")) for item in trace
                 if item.get("kind") == "controller_read"]
        results.append({"first": f"0x{first:02X}", "second": f"0x{second:02X}",
                        "result": report["result"], "pc": report["pc"],
                        "bank_ffff": report["mapper"]["0xFFFF"],
                        "reads": reads, "report": str(report_path),
                        "trace": str(trace_path)})
        print(first, second, report["pc"], report["mapper"]["0xFFFF"], reads)

a.out.write_text(json.dumps({"results": results}, indent=2) + "\n", encoding="utf-8")
