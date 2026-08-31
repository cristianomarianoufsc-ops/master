#!/usr/bin/env python3
"""Summarize register and memory dependencies inside each A0 routine entry."""
from __future__ import annotations
import argparse
import json
from pathlib import Path

p = argparse.ArgumentParser(description=__doc__)
p.add_argument("trace", type=Path)
p.add_argument("--out", type=Path, required=True)
p.add_argument("--target", default="0x8B62")
p.add_argument("--context", type=int, default=160)
a = p.parse_args()

def pc(e):
    try: return int(e.get("pc", "0"), 0)
    except (TypeError, ValueError): return -1

data = json.loads(a.trace.read_text(encoding="utf-8"))
rows = data.get("trace", {}).get("records", [])
target = int(a.target, 0)
hits = [i for i, e in enumerate(rows) if e.get("kind") == "call_target" and pc(e) == target]
lines = ["# Dependências observadas na rotina A0", "", f"Trace: `{a.trace}`", f"Entradas: `{len(hits)}`", ""]
for n, idx in enumerate(hits, 1):
    entry = rows[idx]
    end = min(len(rows), idx + a.context)
    window = rows[idx:end]
    pcs = sorted({e.get("pc") for e in window})
    mem = [e for e in window if e.get("kind") in {"mem_read", "mem_write"}]
    writes = sorted({e.get("address") for e in mem if e.get("kind") == "mem_write"})
    reads = sorted({e.get("address") for e in mem if e.get("kind") == "mem_read"})
    lines += [f"## Entrada {n} — bloco `{entry.get('run')}`, retorno `{entry.get('return_address')}`", "",
              f"Bancos: `FFFE={entry.get('bank_fffe')}`, `FFFF={entry.get('bank_ffff')}`; entrada A/F `{entry.get('a')}/{entry.get('f')}`; DE `{entry.get('d')}/{entry.get('e')}`; HL `{entry.get('h')}/{entry.get('l')}`.", "",
              f"PCs visitados: {', '.join(sorted(pcs))}", "",
              f"Leituras: {', '.join(reads) if reads else 'nenhuma'}", f"Escritas: {', '.join(writes) if writes else 'nenhuma'}", "",
              "| Ordem | PC | Kind | A | F | BC | DE | HL | Endereço | Valor |", "|---:|---|---|---:|---:|---|---|---|---|---:|"]
    for j, e in enumerate(window):
        pair = lambda x, y: f"{e.get(x, '?')}/{e.get(y, '?')}"
        lines.append(f"| {j} | {e.get('pc')} | {e.get('kind')} | {e.get('a','?')} | {e.get('f','?')} | {pair('b','c')} | {pair('d','e')} | {pair('h','l')} | {e.get('address','')} | {e.get('value','')} |")
    lines.append("")
a.out.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"wrote {a.out}: entries={len(hits)}")
