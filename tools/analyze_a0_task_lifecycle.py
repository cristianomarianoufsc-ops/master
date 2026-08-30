"""Summarize the runtime lifecycle of command A0's scene task.

The capture must contain detailed memory events. This tool is observational:
it never changes RAM or infers a successful scene transition from a loop exit.
"""
from pathlib import Path
import argparse
import json
from collections import defaultdict

p = argparse.ArgumentParser(description=__doc__)
p.add_argument("capture", type=Path)
p.add_argument("--out", type=Path, required=True)
p.add_argument("--group-start", type=lambda x: int(x, 0), default=0xDDF7)
p.add_argument("--group-end", type=lambda x: int(x, 0), default=0xDE16)
p.add_argument("--context", type=int, default=3,
               help="number of trace records around each lifecycle event")
a = p.parse_args()

report = json.loads(a.capture.read_text(encoding="utf-8"))
records = report.get("trace", {}).get("records", [])

def addr(record):
    value = record.get("address")
    return int(value, 0) if isinstance(value, str) else None

def pc(record):
    value = record.get("pc")
    return int(value, 0) if isinstance(value, str) else None

def run(record):
    return record.get("run", "?")

def fmt(value):
    return "?" if value is None else f"0x{value:02X}"

def fmt16(value):
    return "?" if value is None else f"0x{value:04X}"

def is_write(record):
    return record.get("kind") == "mem_write"

def is_read(record):
    return record.get("kind") == "mem_read"

def selected(record):
    address = addr(record)
    return address in {0xC008, 0xC203, 0xDD03, 0xDD97, 0xDDB7} or (
        address is not None and a.group_start <= address <= a.group_end)

selected_records = [(index, record) for index, record in enumerate(records)
                    if selected(record)]

# Keep all writes as hard lifecycle evidence and reads only when they touch the
# waiting flags or command/task selectors.
events = []
for index, record in selected_records:
    address = addr(record)
    if is_write(record) or address in {0xC008, 0xC203, 0xDD03, 0xDD97, 0xDDB7}:
        events.append((index, record))

by_run = defaultdict(list)
for index, record in events:
    by_run[run(record)].append((index, record))

lines = [
    "# A0 task lifecycle analysis",
    "",
    f"Capture result: `{report.get('result', '?')}`; final PC: `{report.get('pc', '?')}`; "
    f"records: `{len(records)}`.",
    "",
    "> This report is observational. It does not force flags, release waits, or "
    "> treat a breakpoint miss as a successful scene transition.",
    "",
    "## Lifecycle events",
    "",
    "| Run | PC | Kind | Address | Value | Banks FFFE/FFFF | Registers A/B/C/D/E/H/L |",
    "|---:|---|---|---|---:|---|---|",
]
for _, record in events:
    regs = "/".join(str(record.get(key, "?")) for key in "abcdefh l".replace(" ", ""))
    banks = f"{record.get('bank_fffe', '?'):02X}/{record.get('bank_ffff', '?'):02X}"
    lines.append(
        f"| {run(record)} | {record.get('pc', '?')} | {record.get('kind', '?')} | "
        f"{record.get('address', '?')} | {record.get('value', '?')} | `{banks}` | `{regs}` |"
    )

lines += ["", "## Run-level transitions", "", "| Run | Writes | PCs | Banks |", "|---:|---|---|---|"]
for run_id in sorted(by_run, key=lambda value: int(value) if str(value).isdigit() else str(value)):
    run_events = by_run[run_id]
    writes = ", ".join(f"{r.get('address', '?')}={r.get('value', '?')}" for _, r in run_events if is_write(r)) or "—"
    pcs = ", ".join(sorted({r.get('pc', '?') for _, r in run_events}))
    banks = ", ".join(sorted({f"{r.get('bank_fffe', '?'):02X}/{r.get('bank_ffff', '?'):02X}" for _, r in run_events}))
    lines.append(f"| {run_id} | `{writes}` | `{pcs}` | `{banks}` |")

lines += ["", "## Summary", ""]
for address in (0xC008, 0xC203, 0xDD03, 0xDD97, 0xDDB7):
    writes = [(run(r), r.get("pc", "?"), r.get("value", "?"))
              for _, r in events if addr(r) == address and is_write(r)]
    lines.append(f"- `0x{address:04X}` writes: `{len(writes)}`; "
                 f"observed values: `{sorted({value for _, _, value in writes})}`.")
group_writes = [(run(r), r.get("pc", "?"), r.get("address", "?"), r.get("value", "?"))
                for _, r in events if is_write(r) and a.group_start <= (addr(r) or -1) <= a.group_end]
lines.append(f"- Group `{fmt16(a.group_start)}–{fmt16(a.group_end)}` writes: `{len(group_writes)}`.")

# Report concise local context around the first writes to DDF7 and DD97.
anchors = [(index, record) for index, record in events
           if is_write(record) and addr(record) in {a.group_start, 0xDD97, 0xDDB7}]
if anchors:
    lines += ["", "## Context around task arming", ""]
    for index, anchor in anchors[:8]:
        lines.append(f"### Run {run(anchor)} at {anchor.get('pc', '?')} writing {anchor.get('address', '?')}={anchor.get('value', '?')}")
        lo = max(0, index - a.context)
        hi = min(len(records), index + a.context + 1)
        for context_record in records[lo:hi]:
            if selected(context_record):
                lines.append(f"- run={run(context_record)} pc={context_record.get('pc', '?')} "
                             f"{context_record.get('kind', '?')} {context_record.get('address', '?')}="
                             f"{context_record.get('value', '?')}")

# Make the evidence boundary explicit for downstream review.
lines += ["", "## Interpretation guard", "", ""
          "A task is considered **armed** only when a write to the group, DD97, or DDB7 "
          "is observed. A task is considered **cleared** only when the trace shows "
          "the corresponding write; a persistent C203 read alone is not evidence "
          "of why the task was not consumed.", ""]
a.out.write_text("\n".join(lines), encoding="utf-8")
print(f"wrote {a.out} ({len(events)} selected lifecycle events)")
