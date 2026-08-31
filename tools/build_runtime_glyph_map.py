#!/usr/bin/env python3
"""Build an auditable runtime C280 code-to-glyph map.

The text loop treats a non-zero C280[code] as acceptance and then uses the
original code as the glyph selector. This tool deliberately reports that
semantics instead of inventing a second translation table: glyph_index is the
accepted code, source_offset is code*0x10 in lad0c, and transformed_offset is
code*0x80 after the 05B3E-style transformation.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


def parse_hex_stream(value: str) -> bytes:
    return bytes.fromhex(value)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--capture", type=Path, required=True,
                    help="run_sms_capture JSON report containing c280.values")
    ap.add_argument("--streams", type=Path, required=True,
                    help="extract_dialog_streams JSON report")
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--source-cpu", default="0xAD0C")
    ap.add_argument("--source-bank", type=lambda x: int(x, 0), default=13)
    ap.add_argument("--source-stride", type=lambda x: int(x, 0), default=0x10)
    ap.add_argument("--transformed-stride", type=lambda x: int(x, 0), default=0x80)
    args = ap.parse_args()

    capture = json.loads(args.capture.read_text(encoding="utf-8"))
    values = capture.get("c280", {}).get("values")
    if not isinstance(values, list) or len(values) != 0x100:
        raise SystemExit("capture does not contain exactly 256 C280 values")
    accepted = {code for code, value in enumerate(values) if value}

    streams = json.loads(args.streams.read_text(encoding="utf-8"))
    occurrences = Counter()
    stream_count = 0
    for table in streams.get("tables", []):
        for entry in table.get("entries", []):
            raw_hex = entry.get("hex", "")
            if not raw_hex:
                continue
            stream_count += 1
            for code in parse_hex_stream(raw_hex):
                if code in accepted:
                    occurrences[code] += 1

    lines = [
        "# Runtime C280 code-to-glyph map",
        "",
        "This report uses a runtime capture, not the heuristic D12x expansion.",
        "A code is accepted when `C280[code]` is non-zero; the text loop then",
        "uses that same code as the glyph selector.",
        "",
        f"- capture result: `{capture.get('result')}` at PC `{capture.get('pc')}`",
        f"- C280 non-zero entries: **{len(accepted)}**",
        f"- streams scanned: **{stream_count}**",
        f"- source: bank `{args.source_bank}`, CPU `{args.source_cpu}`, stride `0x{args.source_stride:X}`",
        f"- transformed stride after 05B3E model: `0x{args.transformed_stride:X}`",
        "",
        "| Code | C280 value | Glyph index | Source offset | Transformed offset | Stream occurrences |",
        "|---:|---:|---:|---:|---:|---:|",
    ]
    for code in sorted(accepted):
        lines.append(
            f"| `0x{code:02X}` | `0x{values[code]:02X}` | `{code}` "
            f"| `0x{code * args.source_stride:04X}` "
            f"| `0x{code * args.transformed_stride:04X}` "
            f"| {occurrences[code]} |"
        )
    lines += [
        "",
        "## Interpretation limits",
        "",
        "The capture stopped before the dialogue breakpoint, so this map is a",
        "runtime snapshot of the current execution path, not yet the final game-wide",
        "C280 table. Stream occurrence counts are structural cross-references and",
        "do not prove that a stream is narrative text.",
    ]
    args.out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({
        "accepted_codes": len(accepted),
        "streams_scanned": stream_count,
        "nonzero_occurrences": sum(occurrences.values()),
        "out": str(args.out),
    }, indent=2))


if __name__ == "__main__":
    main()
