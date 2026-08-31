#!/usr/bin/env python3
"""Align Z80 routines between ROMs using opcode/length fingerprints.

Immediate values and addresses differ between regional builds, so the
fingerprint keeps the first opcode byte and decoded instruction length while
ignoring operand bytes. Results are candidates for review, not patch offsets.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import z80

BANK = 0x4000


def integer(value: str) -> int:
    return int(value, 0)


def decode(rom: bytes, bank: int, start: int, end: int):
    builder = z80.Z80InstrBuilder()
    base = bank * BANK
    pos = start
    out = []
    while pos < end:
        off = base + (pos - 0x4000)
        raw = rom[off:off + 4]
        if not raw:
            break
        try:
            ins = builder.build_instr(pos, raw)
            size = getattr(ins, "size", 1) or 1
        except Exception:
            size = 1
        out.append({"cpu": pos, "file": off, "size": size,
                    "opcode": rom[off], "text": str(ins) if 'ins' in locals() else "db"})
        pos += size
    return out


def fingerprint(items, index, length):
    return tuple((x["opcode"], x["size"]) for x in items[index:index + length])


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("reference", type=Path)
    ap.add_argument("target", type=Path)
    ap.add_argument("--reference-bank", type=int, required=True)
    ap.add_argument("--target-bank", type=int, required=True)
    ap.add_argument("--reference-start", type=integer, required=True)
    ap.add_argument("--reference-end", type=integer, required=True)
    ap.add_argument("--target-start", type=integer, required=True)
    ap.add_argument("--target-end", type=integer, required=True)
    ap.add_argument("--window", type=int, default=12)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    ref = args.reference.read_bytes()
    target = args.target.read_bytes()
    ref_items = decode(ref, args.reference_bank, args.reference_start, args.reference_end)
    target_items = decode(target, args.target_bank, args.target_start, args.target_end)
    results = []
    for i in range(max(0, len(ref_items) - args.window + 1)):
        sig = fingerprint(ref_items, i, args.window)
        hits = []
        for j in range(max(0, len(target_items) - args.window + 1)):
            if fingerprint(target_items, j, args.window) == sig:
                hits.append(target_items[j]["cpu"])
        if hits:
            results.append({"reference_cpu": ref_items[i]["cpu"],
                            "reference_file": ref_items[i]["file"],
                            "target_hits": hits, "unique": len(hits) == 1,
                            "window_instructions": args.window,
                            "signature": [list(x) for x in sig]})
    report = {"reference": str(args.reference), "target": str(args.target),
              "reference_bank": args.reference_bank, "target_bank": args.target_bank,
              "reference_range": [args.reference_start, args.reference_end],
              "target_range": [args.target_start, args.target_end],
              "window": args.window, "matches": results}
    args.out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"reference_instructions": len(ref_items),
                      "target_instructions": len(target_items),
                      "matches": len(results),
                      "unique_matches": sum(x["unique"] for x in results),
                      "report": str(args.out)}, indent=2))


if __name__ == "__main__":
    main()
