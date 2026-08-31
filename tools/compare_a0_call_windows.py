#!/usr/bin/env python3
"""Compare causal windows immediately before the fixed and paged A0 CALLs."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("fixed_trace", type=Path)
parser.add_argument("paged_trace", type=Path)
parser.add_argument("--out", type=Path, required=True)
parser.add_argument("--context", type=int, default=12)
args = parser.parse_args()

def records(path: Path):
    data = json.loads(path.read_text(encoding="utf-8"))
    return data.get("trace", {}).get("records", [])

def entries(path: Path, expected_return: str):
    rows = records(path)
    hits = [i for i, e in enumerate(rows)
            if e.get("kind") == "call_target" and e.get("return_address") == expected_return]
    result = []
    for i in hits:
        result.append({"index": i, "entry": rows[i],
                       "context": rows[max(0, i - args.context):i + 1]})
    return result

fixed = entries(args.fixed_trace, "0x0536")
paged = entries(args.paged_trace, "0x456C")
lines = ["# Comparação das janelas causais A0", "",
         "A janela termina na entrada instrumentada de `0x8B62`; os registros anteriores são a evidência imediatamente precedente observada pelo capturador.", "",
         "| Caminho | Trace | Entradas encontradas | Retornos |", "|---|---|---:|---|",
         f"| Fixo | `{args.fixed_trace}` | {len(fixed)} | `0x0536` |",
         f"| Paginado | `{args.paged_trace}` | {len(paged)} | `0x456C` |", ""]
for title, groups in (("Fixo (`0x0533 → 0x0536`)", fixed), ("Paginado (`0x4569 → 0x456C`)", paged)):
    lines += [f"## {title}", ""]
    for n, group in enumerate(groups, 1):
        e = group["entry"]
        lines += [f"### Ocorrência {n} — bloco `{e.get('run')}`", "",
                  f"Entrada: PC `{e.get('pc')}`, retorno `{e.get('return_address')}`, banco `FFFE={e.get('bank_fffe')}`, `FFFF={e.get('bank_ffff')}`, SP `{e.get('sp')}`.", "",
                  "| Índice | PC | Kind | Run | A | F | BC | DE | HL | IX | IY | SP | Endereço | Valor |", "|---:|---|---|---:|---:|---:|---|---|---|---|---|---|---|---:|"]
        for i, r in enumerate(group["context"], start=group["index"] - len(group["context"]) + 1):
            regs = lambda pair: (str(r.get(pair[0], "?")) + "/" + str(r.get(pair[1], "?")))
            lines.append(f"| {i} | {r.get('pc')} | {r.get('kind')} | {r.get('run')} | {r.get('a','?')} | {r.get('f','?')} | {regs(('b','c'))} | {regs(('d','e'))} | {regs(('h','l'))} | {r.get('ix','?')} | {r.get('iy','?')} | {r.get('sp')} | {r.get('address','')} | {r.get('value','')} |")
        lines.append("")
args.out.write_text("\n".join(lines), encoding="utf-8")
print(f"wrote {args.out}: fixed={len(fixed)}, paged={len(paged)}")
