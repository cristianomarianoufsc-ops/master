#!/usr/bin/env python3
"""Align two same-size SMS ROMs using exact local binary signatures.

The tool does not assume that physical offsets are equal. It searches each
signature from the reference ROM in the target ROM, first within the same
16 KiB bank and then globally, and reports unique candidates and deltas.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

BANK = 0x4000


def parse_int(value: str) -> int:
    return int(value, 0)


def occurrences(haystack: bytes, needle: bytes):
    start = 0
    while True:
        pos = haystack.find(needle, start)
        if pos < 0:
            return
        yield pos
        start = pos + 1


def ascii_runs(data: bytes, minimum: int = 8):
    runs = []
    start = None
    for i, value in enumerate(data + b"\0"):
        printable = 0x20 <= value <= 0x7E
        if printable and start is None:
            start = i
        elif not printable and start is not None:
            if i - start >= minimum:
                runs.append((start, data[start:i].decode("ascii")))
            start = None
    return runs


def find_signature(reference: bytes, target: bytes, offset: int, window: int):
    offset = max(0, min(offset, len(reference)))
    half = max(1, window // 2)
    begin = max(0, offset - half)
    end = min(len(reference), begin + window)
    begin = max(0, end - window)
    signature = reference[begin:end]
    same_bank_start = (begin // BANK) * BANK
    same_bank_end = min(len(target), same_bank_start + BANK)
    local = list(occurrences(target[same_bank_start:same_bank_end], signature))
    local = [same_bank_start + x for x in local]
    global_hits = list(occurrences(target, signature))
    return {
        "reference_offset": begin,
        "signature_length": len(signature),
        "signature_sha1": __import__("hashlib").sha1(signature).hexdigest(),
        "same_bank_hits": local,
        "global_hits": global_hits,
        "reference_bank": begin // BANK,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("reference", type=Path, help="ROM used as reference (e.g. USA)")
    parser.add_argument("target", type=Path, help="ROM to align (e.g. Japan)")
    parser.add_argument("--offset", action="append", type=parse_int, default=[],
                        help="reference physical offset to align; may be repeated")
    parser.add_argument("--window", type=int, default=32,
                        help="signature size in bytes (default: 32)")
    parser.add_argument("--ascii-min", type=int, default=8,
                        help="minimum printable run length to list")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    reference = args.reference.read_bytes()
    target = args.target.read_bytes()
    if len(reference) % BANK or len(target) % BANK:
        raise SystemExit("both ROMs must have sizes that are multiples of 0x4000")

    offsets = args.offset or [x for x, _ in ascii_runs(reference, args.ascii_min)[:32]]
    alignments = [find_signature(reference, target, x, args.window) for x in offsets]
    for item, requested in zip(alignments, offsets):
        item["requested_offset"] = requested
        item["reference_file_offset"] = item["reference_offset"]
        item["reference_cpu_window"] = item["reference_offset"] % BANK + 0x4000
        hits = item["same_bank_hits"] or item["global_hits"]
        item["selected_hits"] = hits
        item["deltas"] = [x - item["reference_offset"] for x in hits]
        item["unique"] = len(hits) == 1

    report = {
        "reference": str(args.reference),
        "target": str(args.target),
        "reference_size": len(reference),
        "target_size": len(target),
        "banks": len(reference) // BANK,
        "window": args.window,
        "ascii_runs_reference": [
            {"offset": offset, "text": text}
            for offset, text in ascii_runs(reference, args.ascii_min)
        ],
        "alignments": alignments,
    }
    args.out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    unique = sum(x["unique"] for x in alignments)
    print(json.dumps({"signatures": len(alignments), "unique": unique,
                      "report": str(args.out)}, indent=2))


if __name__ == "__main__":
    main()
