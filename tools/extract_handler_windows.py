#!/usr/bin/env python3
"""Extract current-format Z80 disassembly windows around dialogue resolver calls."""
from __future__ import annotations
import argparse
import re
from pathlib import Path

CPU = re.compile(r"^([0-9A-Fa-f]{4}):")
TARGETS = re.compile(r"call\s+(?:0x)?(?:05c16h?|5c16|5beb)", re.I)
WRITES = re.compile(r"c223|c238|c206|5c16", re.I)

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("asm", type=Path)
    ap.add_argument("--context", type=int, default=8)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    lines = args.asm.read_text(encoding="utf-8", errors="replace").splitlines()
    hits = []
    for i, line in enumerate(lines):
        if TARGETS.search(line):
            lo, hi = max(0, i - args.context), min(len(lines), i + args.context + 1)
            hits.append({"line": i + 1, "pc": CPU.match(line).group(1) if CPU.match(line) else None,
                         "window": lines[lo:hi], "nearby_state_refs": [x for x in lines[lo:hi] if WRITES.search(x)]})
    out = ["# Dialogue resolver windows", "", f"count={len(hits)}", ""]
    for n, hit in enumerate(hits, 1):
        out += [f"## candidate {n} pc=0x{hit['pc'] or '????'} line={hit['line']}", ""]
        out += hit["window"] + [""]
    args.out.write_text("\n".join(out), encoding="utf-8")
    print(f"wrote {len(hits)} windows to {args.out}")

if __name__ == "__main__":
    main()
