"""Summarize streams classified as text_or_glyph_stream."""
from __future__ import annotations
import argparse
import json
from pathlib import Path

p = argparse.ArgumentParser(description=__doc__)
p.add_argument("json_files", nargs="+", type=Path)
a = p.parse_args()
for path in a.json_files:
    data = json.loads(path.read_text(encoding="utf-8"))
    print(f"== {path} ==")
    count = 0
    for table in data.get("tables", []):
        for entry in table.get("entries", []):
            if entry.get("kind") != "text_or_glyph_stream":
                continue
            count += 1
            print(json.dumps({
                "table": table.get("table"),
                "bank": table.get("bank"),
                "index": entry.get("index"),
                "pointer": entry.get("pointer"),
                "kind": entry.get("kind"),
                "stats": entry.get("stats"),
                "hex": entry.get("hex"),
            }, ensure_ascii=False))
    print(f"count={count}")
