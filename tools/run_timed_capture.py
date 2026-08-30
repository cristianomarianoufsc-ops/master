#!/usr/bin/env python3
"""Run run_sms_capture.py with a generated timed controller sequence."""
from pathlib import Path
import argparse
import subprocess
import sys

p = argparse.ArgumentParser(description=__doc__)
p.add_argument("rom", type=Path)
p.add_argument("--out", type=Path, required=True)
p.add_argument("--trace-out", type=Path, required=True)
p.add_argument("--max-steps", type=int, default=1100)
p.add_argument("--press-start", type=int, default=260)
p.add_argument("--press-runs", type=int, default=30)
p.add_argument("--value", type=lambda x: int(x, 0), default=0x10)
p.add_argument("--default", type=lambda x: int(x, 0), default=0x00)
p.add_argument("--trace-memory-range", default=None)
p.add_argument("--trace-pc-range", default="0x0000-0x8D00")
p.add_argument("--trace-every", type=int, default=32)
p.add_argument("--trace-limit", type=int, default=150000)
p.add_argument("--trace-forced-addresses", default="0xC008,0xC203")
p.add_argument("--trace-exec-range", default=None)
p.add_argument("--dega-io-semantics", action="store_true")
a = p.parse_args()
if a.press_start < 0 or a.press_runs < 1:
    raise SystemExit("press-start must be non-negative and press-runs positive")
sequence = [a.default & 0xFF] * a.press_start
sequence += [a.value & 0xFF] * a.press_runs
sequence += [a.default & 0xFF] * max(0, a.max_steps - len(sequence))
command = [sys.executable, str(Path(__file__).with_name("run_sms_capture.py")),
           str(a.rom), "--max-steps", str(a.max_steps),
           "--ticks-per-run", "100000", "--scanline-irq",
           "--dega-frame-schedule", "--irq-every-runs", "0",
           "--input-sequence", ",".join(f"0x{x:02X}" for x in sequence),
           "--trace-pc-range", a.trace_pc_range, "--trace-limit", str(a.trace_limit),
           "--trace-every", str(a.trace_every), "--trace-out", str(a.trace_out),
           "--trace-forced-addresses", a.trace_forced_addresses,
           "--out", str(a.out)]
if a.trace_exec_range:
    command += ["--trace-exec-range", a.trace_exec_range]
if a.dega_io_semantics:
    command.append("--dega-io-semantics")
if a.trace_memory_range:
    command += ["--trace-memory-range", a.trace_memory_range]
subprocess.run(command, check=True)
