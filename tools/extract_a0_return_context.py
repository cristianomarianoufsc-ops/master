#!/usr/bin/env python3
"""Extract focused call/return context around the A0 cleanup path."""
from pathlib import Path
import argparse
import json

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("trace", type=Path)
parser.add_argument("--out", type=Path, required=True)
parser.add_argument("--context", type=int, default=8)
args = parser.parse_args()

def pc(event):
    try:
        return int(event.get("pc", "0"), 0)
    except (TypeError, ValueError):
        return -1

data = json.loads(args.trace.read_text(encoding="utf-8"))
events = data.get("trace", data).get("records", [])
targets = {0x4496, 0x8B81, 0x8B8B, 0x8B93}
hits = [i for i, event in enumerate(events) if pc(event) in targets]
rows = []
for index in hits:
    start = max(0, index - args.context)
    end = min(len(events), index + args.context + 1)
    rows.append({"target_index": index, "target": events[index], "context": events[start:end]})

lines = ["# Contexto de retorno da tarefa A0", "", f"Trace: `{args.trace}`", f"Registros: `{len(events)}`", f"Ocorrências: `{len(hits)}`", ""]
for n, row in enumerate(rows, 1):
    target = row["target"]
    lines += [f"## Ocorrência {n}", "", f"Alvo: `{target.get('pc')}` no bloco `{target.get('run')}`; SP `{target.get('sp')}`; topo `{target.get('stack0')}/{target.get('stack1')}`.", "", "| Índice | Run | PC | Kind | Endereço | Valor | SP | Topo | Bancos | A/B/C/D/E/H/L |", "|---:|---:|---|---|---|---:|---|---|---|---|"]
    for i, event in enumerate(row["context"], start=row["target_index"] - args.context):
        regs = "/".join(str(event.get(k, "?")) for k in "abcdefhl")
        lines.append(f"| {i} | {event.get('run')} | {event.get('pc')} | {event.get('kind')} | {event.get('address', '')} | {event.get('value', '')} | {event.get('sp')} | {event.get('stack0')}/{event.get('stack1')} | {event.get('bank_fffe')}/{event.get('bank_ffff')} | {regs} |")
    lines.append("")
args.out.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"wrote {args.out} ({len(hits)} hits)")
