"""Deduplicate call-target trace records by execution run and return address."""
from __future__ import annotations
import argparse
import json
from collections import Counter
from pathlib import Path

p = argparse.ArgumentParser(description=__doc__)
p.add_argument("report", type=Path)
p.add_argument("--out", type=Path)
a = p.parse_args()
r = json.loads(a.report.read_text(encoding="utf-8"))
records = r.get("trace", {}).get("records", [])
seen = set()
unique = []
for rec in records:
    if rec.get("kind") != "call_target":
        continue
    key = (rec.get("run"), rec.get("pc"), rec.get("return_address"))
    if key in seen:
        continue
    seen.add(key)
    unique.append(rec)
summary = {
    "source": str(a.report),
    "records": len(records),
    "call_target_records": sum(rec.get("kind") == "call_target" for rec in records),
    "unique_call_entries": len(unique),
    "unique_by_pc": dict(Counter(rec.get("pc") for rec in unique)),
    "entries": unique,
}
text = json.dumps(summary, indent=2, ensure_ascii=False) + "\n"
if a.out:
    a.out.write_text(text, encoding="utf-8")
print(text, end="")
