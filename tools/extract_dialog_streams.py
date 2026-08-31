#!/usr/bin/env python3
"""Resolve dialogue table pointers and classify the pointed blocks."""
from __future__ import annotations
import argparse
import json
from pathlib import Path

BANK_SIZE = 0x4000

def cpu_to_offset(cpu: int, bank: int) -> int | None:
    if 0x8000 <= cpu < 0xC000:
        return bank * BANK_SIZE + (cpu - 0x8000)
    return None

def read_until_ff(data: bytes, limit: int) -> bytes:
    chunk = data[:limit]
    end = chunk.find(b"\xff")
    return chunk if end < 0 else chunk[:end + 1]

def classify(raw: bytes) -> tuple[str, dict]:
    body = raw[:-1] if raw.endswith(b"\xff") else raw
    markers = sum(x in (0xfb, 0xfc, 0xfd, 0xfe, 0xee) for x in body)
    low = sum(x <= 0x7f for x in body)
    words = sum(0x8000 <= int.from_bytes(body[i:i+2], "little") < 0xc000
                for i in range(0, max(0, len(body)-1), 2))
    if markers >= 2 or words >= 3:
        label = "bytecode_or_structure"
    elif body and low / len(body) >= 0.8:
        label = "text_or_glyph_stream"
    else:
        label = "mixed_or_unknown"
    return label, {"length": len(raw), "markers": markers, "low_byte_ratio": round(low / len(body), 3) if body else 0, "cpu_word_like_pairs": words}

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("rom", type=Path)
    ap.add_argument("--tables", required=True, help="comma-separated CPU addresses, e.g. 0xb124,0xb228")
    ap.add_argument("--bank", type=int, default=22)
    ap.add_argument("--entries", type=int, default=0x41)
    ap.add_argument("--max-bytes", type=int, default=512)
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    rom = a.rom.read_bytes()
    tables = [int(x.strip(), 0) for x in a.tables.split(",") if x.strip()]
    records = []
    for table in tables:
        table_off = cpu_to_offset(table, a.bank)
        if table_off is None or table_off + 2 > len(rom):
            records.append({"table": hex(table), "error": "table outside CPU window"})
            continue
        entries = []
        for index in range(a.entries):
            pos = table_off + 2 * index
            if pos + 2 > len(rom): break
            ptr = int.from_bytes(rom[pos:pos+2], "little")
            ptr_off = cpu_to_offset(ptr, a.bank)
            if ptr_off is None:
                entries.append({"index": index, "pointer": hex(ptr), "kind": "invalid_or_other_bank"})
                continue
            raw = read_until_ff(rom[ptr_off:], a.max_bytes)
            kind, stats = classify(raw)
            entries.append({"index": index, "pointer": hex(ptr), "kind": kind, "stats": stats, "hex": raw.hex()})
        records.append({"table": hex(table), "bank": a.bank, "entries": entries})
    report = {"rom": str(a.rom), "bank": a.bank, "tables": records}
    a.out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    total = sum(len(x.get("entries", [])) for x in records)
    text = sum(1 for x in records for e in x.get("entries", []) if e.get("kind") == "text_or_glyph_stream")
    code = sum(1 for x in records for e in x.get("entries", []) if e.get("kind") == "bytecode_or_structure")
    print(json.dumps({"tables": len(records), "entries": total, "text_candidates": text, "bytecode_candidates": code, "report": str(a.out)}, indent=2))

if __name__ == "__main__": main()
