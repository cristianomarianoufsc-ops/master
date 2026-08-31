"""Apply exact same-length byte patches with precondition checks.

The tool is intentionally conservative: every patch must provide the exact
original bytes, replacements must have equal length, and the input is never
modified in place.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument("input", type=Path)
ap.add_argument("output", type=Path)
ap.add_argument("--patches", type=Path, required=True,
                help="JSON list of {offset, expected, replacement, label}")
a = ap.parse_args()
source = a.input.read_bytes()
patches = json.loads(a.patches.read_text(encoding="utf-8"))
result = bytearray(source)
applied = []
for item in patches:
    offset = int(item["offset"], 0) if isinstance(item["offset"], str) else int(item["offset"])
    expected = bytes.fromhex(item["expected"])
    replacement = bytes.fromhex(item["replacement"])
    if len(expected) != len(replacement):
        raise SystemExit(f"{item.get('label', offset)}: replacement length differs")
    if offset < 0 or offset + len(expected) > len(result):
        raise SystemExit(f"{item.get('label', offset)}: patch outside ROM")
    actual = bytes(result[offset:offset + len(expected)])
    if actual != expected:
        raise SystemExit(f"{item.get('label', offset)}: expected {expected.hex()} but found {actual.hex()}")
    result[offset:offset + len(expected)] = replacement
    applied.append({"label": item.get("label", f"0x{offset:X}"), "offset": f"0x{offset:X}", "length": len(expected)})
if len(result) != len(source):
    raise SystemExit("ROM size changed")
a.output.parent.mkdir(parents=True, exist_ok=True)
a.output.write_bytes(result)
manifest = a.output.with_suffix(a.output.suffix + ".manifest.json")
manifest.write_text(json.dumps({"input": str(a.input), "output": str(a.output), "size": len(result), "patches": applied}, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"output": str(a.output), "size": len(result), "patches": len(applied), "manifest": str(manifest)}, indent=2))
