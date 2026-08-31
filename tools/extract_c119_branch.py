#!/usr/bin/env python3
"""Extract the paged A0 post-cleanup branch around C119."""
import argparse
import json
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument("trace", type=Path)
p.add_argument("--out", type=Path, required=True)
a = p.parse_args()
data = json.loads(a.trace.read_text(encoding="utf-8"))
rows = data.get("trace", {}).get("records", [])
keep = []
for r in rows:
    try:
        pc = int(r.get("pc", "0"), 0)
    except ValueError:
        continue
    if 0x4564 <= pc <= 0x4578 or r.get("address") in {"0xC119", "0xC0A0", "0xC11D"}:
        keep.append(r)
lines = ["# Branch paginado A0: C119", "", "| Índice | Run | PC | Kind | A | F | DE | HL | Endereço | Valor | Retorno |", "|---:|---:|---|---|---:|---:|---|---|---|---:|---|"]
for i, r in enumerate(keep):
    lines.append(f"| {i} | {r.get('run')} | {r.get('pc')} | {r.get('kind')} | {r.get('a')} | {r.get('f')} | {r.get('d')}/{r.get('e')} | {r.get('h')}/{r.get('l')} | {r.get('address','')} | {r.get('value','')} | {r.get('return_address','')} |")
a.out.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"wrote {a.out}: {len(keep)} rows")
