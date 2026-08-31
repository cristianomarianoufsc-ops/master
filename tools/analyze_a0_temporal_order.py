#!/usr/bin/env python3
"""Order A0 state-machine, IRQ handler, and VDP scheduler events."""
import argparse
import json
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument("trace", type=Path)
p.add_argument("--out", type=Path, required=True)
a = p.parse_args()
data = json.loads(a.trace.read_text(encoding="utf-8"))
rows = data.get("trace", {}).get("records", [])
lines = [
    "# Ordem temporal A0/IRQ/scheduler",
    "",
    "| Seq | Run | PC | Kind | Address | Value | A | F | SP |",
    "|---:|---:|---|---|---|---:|---:|---:|---|",
]
selected = 0
for seq, r in enumerate(rows):
    try:
        pc = int(r.get("pc", "0"), 16)
    except ValueError:
        continue
    if not (
        0x07E5 <= pc <= 0x07F2
        or 0x1809 <= pc <= 0x181F
        or 0x06CE <= pc <= 0x06E5
        or r.get("address") in {"0xC0A0", "0xC080", "0xC112"}
    ):
        continue
    selected += 1
    lines.append(
        f"| {seq} | {r.get('run')} | {r.get('pc')} | {r.get('kind')} | "
        f"{r.get('address', '')} | {r.get('value', '')} | {r.get('a')} | "
        f"{r.get('f')} | {r.get('sp')} |"
    )
a.out.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"wrote {a.out}: selected={selected}")
