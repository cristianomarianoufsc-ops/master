"""Analyze runtime trace records relevant to the text decoder."""
from __future__ import annotations
import argparse
import collections
import json
from pathlib import Path

p = argparse.ArgumentParser(description=__doc__)
p.add_argument("report", type=Path)
p.add_argument("--out", type=Path)
a = p.parse_args()
r = json.loads(a.report.read_text(encoding="utf-8"))
records = r.get("trace", {}).get("records", [])
watched = {"0xC223", "0xC224", "0xC238", "0xC239", "0xC280", "0xC281"}
text_pcs = set()
for n in range(0x96CA, 0x977A):
    text_pcs.add(f"0x{n:04X}")
ram_events = [x for x in records if x.get("address") in watched]
text_events = [x for x in records if x.get("pc") in text_pcs]
summary = {
    "source": str(a.report),
    "capture_result": r.get("result"),
    "steps": r.get("steps"),
    "breakpoint": r.get("breakpoint"),
    "runtime_state_events": len(ram_events),
    "runtime_state_by_address": dict(collections.Counter(x.get("address") for x in ram_events)),
    "runtime_state_values": {
        addr: dict(collections.Counter(x.get("value") for x in ram_events if x.get("address") == addr))
        for addr in sorted(watched)
    },
    "text_decoder_events": len(text_events),
    "text_decoder_pcs": dict(collections.Counter(x.get("pc") for x in text_events)),
    "events": ram_events + text_events,
}
text = json.dumps(summary, indent=2, ensure_ascii=False) + "\n"
if a.out:
    a.out.write_text(text, encoding="utf-8")
print(text, end="")
