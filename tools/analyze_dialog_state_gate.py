"""Summarize the Japanese ROM's scene-to-dialogue state gate."""
from __future__ import annotations
import argparse
import json
from collections import Counter
from pathlib import Path

ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument("capture", type=Path)
ap.add_argument("--audit", type=Path)
ap.add_argument("--out", type=Path, required=True)
a = ap.parse_args()
report = json.loads(a.capture.read_text(encoding="utf-8"))
trace = report.get("trace", {}).get("records", [])
pcs = {"0x48D5", "0x48D7", "0x48DA", "0x4937", "0x4939", "0x494A", "0x4970", "0x4988", "0x4A8D"}
addresses = {"0xC004", "0xC005", "0xC020", "0xC02B", "0xC26C", "0xC203", "0xC205", "0xC206", "0xC223", "0xC238"}
gate = [x for x in trace if x.get("pc") in pcs]
mem = [x for x in trace if x.get("address") in addresses]
lines = ["# Dialog state gate analysis", "", f"Capture: `{a.capture}`", "", "## Result", "", f"- Result: `{report.get('result')}`", f"- Steps: `{report.get('steps')}`", f"- Final PC: `{report.get('pc')}`", f"- Breakpoint: `{report.get('breakpoint')}`", "", "## Gate PC counts", "", "| PC | Events |", "|---|---:|"]
for pc, count in Counter(x.get("pc") for x in gate).most_common():
    lines.append(f"| `{pc}` | {count} |")
lines += ["", "## Register snapshots at gate PCs", "", "| Run | PC | A | F | HL | DE | Banks |", "|---:|---|---|---|---|---|---|"]
for x in gate[:80]:
    if x.get("pc") in {"0x48D5", "0x48D7", "0x48DA", "0x4970"}:
        hl = f"{x.get('h', 0):02X}{x.get('l', 0):02X}" if isinstance(x.get('h'), int) else "?"
        de = f"{x.get('d', 0):02X}{x.get('e', 0):02X}" if isinstance(x.get('d'), int) else "?"
        banks = f"{x.get('bank_fffe')}/{x.get('bank_ffff')}"
        lines.append(f"| {x.get('run')} | `{x.get('pc')}` | `{x.get('a')}` | `{x.get('f')}` | `{hl}` | `{de}` | `{banks}` |")
lines += ["", "## Monitored state writes", "", "| Address | Values | Writers |", "|---|---|---|"]
for address in sorted(addresses):
    xs = [x for x in mem if x.get("address") == address]
    values = sorted({x.get("value") for x in xs if x.get("value") is not None})
    writers = [f"run {x.get('run')} @ {x.get('pc')} = {x.get('value')}" for x in xs if x.get("kind") == "mem_write"]
    lines.append(f"| `{address}` | `{values}` | {', '.join(writers[:16]) or 'none'} |")
if a.audit and a.audit.exists():
    audit = json.loads(a.audit.read_text(encoding="utf-8"))
    lines += ["", "## False-positive audit", "", f"- Status: `{audit.get('status')}`"]
    for issue in audit.get("issues", []):
        lines.append(f"- `{issue.get('code')}`: {issue.get('message')}")
a.out.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(json.dumps({"gate_events": len(gate), "memory_events": len(mem), "out": str(a.out)}, indent=2))
