#!/usr/bin/env python3
"""Summarize the dynamic lifecycle of the scene-loading flags C008/C203.

The input is a capture JSON or a trace JSON produced by run_sms_capture.py.
The tool deliberately reports observations only; it does not infer that a
flag write is causal and never modifies the ROM or capture.
"""
from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import argparse
import json


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("capture", type=Path,
                    help="capture JSON, or trace JSON with a top-level trace")
parser.add_argument("--out", type=Path, default=None,
                    help="optional Markdown report path")
parser.add_argument("--window", type=int, default=2,
                    help="number of trace records around each flag write")
args = parser.parse_args()
if args.window < 0:
    raise SystemExit("--window must be non-negative")

payload = json.loads(args.capture.read_text(encoding="utf-8"))
trace = payload.get("trace", {})
records = trace.get("records", [])
if not isinstance(records, list):
    raise SystemExit("trace.records must be a list")

flag_addresses = {"0xC008", "0xC203"}


def normalize_address(value):
    try:
        return f"0x{int(str(value), 0):04X}"
    except (TypeError, ValueError):
        return str(value)


writes = [
    (index, record) for index, record in enumerate(records)
    if record.get("kind") == "mem_write"
    and normalize_address(record.get("address")) in flag_addresses
]

by_flag = defaultdict(list)
for index, record in writes:
    by_flag[normalize_address(record["address"])].append((index, record))

runs = defaultdict(lambda: defaultdict(list))
for index, record in writes:
    runs[record.get("run", -1)][normalize_address(record["address"])].append((index, record))


def grouped_writes(address):
    groups = {}
    for index, record in by_flag[address]:
        signature = (record.get("pc"), record.get("value"),
                     record.get("bank_fffe"), record.get("bank_ffff"))
        if signature not in groups:
            groups[signature] = {"signature": signature, "count": 0,
                                 "first_index": index, "last_index": index,
                                 "first_run": record.get("run", "?"),
                                 "last_run": record.get("run", "?"),
                                 "record": record}
        group = groups[signature]
        group["count"] += 1
        group["last_index"] = index
        group["last_run"] = record.get("run", "?")
    return sorted(groups.values(), key=lambda group: group["first_index"])


def fmt_record(record):
    address = record.get("address", "?")
    value = record.get("value", "?")
    return (f"run={record.get('run', '?')} pc={record.get('pc', '?')} "
            f"{address}={value} "
            f"banks=({record.get('bank_fffe', '?')},{record.get('bank_ffff', '?')})")


def markdown():
    lines = ["# Ciclo de vida dos flags de carregamento de cena", "",
             f"Fonte: `{args.capture}`", "",
             "## Resumo", "",
             f"- Registros de trace: {len(records)}",
             f"- Escritas de `C008`: {len(by_flag['0xC008'])}",
             f"- Escritas de `C203`: {len(by_flag['0xC203'])}", ""]

    for address in ("0xC008", "0xC203"):
        lines += [f"## Escritas de `{address}`", ""]
        if not by_flag[address]:
            lines.append("Nenhuma escrita foi registrada.")
            lines.append("")
            continue
        lines += ["| Ocorrências | Índices | Blocos | PC | Valor | FFFE | FFFF |", "|---:|---|---|---|---:|---:|---:|"]
        for group in grouped_writes(address):
            record = group["record"]
            indexes = (str(group["first_index"]) if group["first_index"] == group["last_index"]
                       else f"{group['first_index']}–{group['last_index']}")
            runs_text = (str(group["first_run"]) if group["first_run"] == group["last_run"]
                         else f"{group['first_run']}–{group['last_run']}")
            lines.append(
                f"| {group['count']} | {indexes} | {runs_text} | {record.get('pc', '?')} | "
                f"{record.get('value', '?')} | {record.get('bank_fffe', '?')} | "
                f"{record.get('bank_ffff', '?')} |"
            )
        lines.append("")

    lines += ["## Escritas agrupadas por bloco", ""]
    relevant_runs = {run: values for run, values in runs.items()
                     if values.get("0xC203") or any(
                         record.get("value") != 3
                         for _, record in values.get("0xC008", []))}
    if relevant_runs:
        lines += ["| Bloco | C008 (valores) | C203 (valores) | PCs envolvidos |",
                  "|---:|---|---|---|"]
        for run in sorted(relevant_runs):
            c008 = [str(r.get("value", "?")) for _, r in relevant_runs[run].get("0xC008", [])]
            c203 = [str(r.get("value", "?")) for _, r in relevant_runs[run].get("0xC203", [])]
            pcs = sorted({r.get("pc", "?") for values in relevant_runs[run].values()
                          for _, r in values})
            lines.append(f"| {run} | {', '.join(c008) or '—'} | "
                         f"{', '.join(c203) or '—'} | {', '.join(pcs)} |")
        lines.append("")
    else:
        lines += ["Nenhuma escrita de flag foi registrada no trace.", ""]

    lines += ["## Janelas locais das escritas", "",
              "As janelas abaixo são contexto do trace, não prova de causalidade.", ""]
    context_groups = []
    for address in ("0xC008", "0xC203"):
        context_groups.extend(grouped_writes(address))
    for group in context_groups:
        index = group["first_index"]
        record = group["record"]
        start = max(0, index - args.window)
        end = min(len(records), index + args.window + 1)
        suffix = f" ({group['count']} ocorrências com a mesma assinatura)" if group["count"] > 1 else ""
        lines.append(f"### Registro {index}: {fmt_record(record)}{suffix}")
        lines.append("")
        lines.append("```text")
        lines.extend(f"{i}: {fmt_record(item)}" for i, item in enumerate(records[start:end], start))
        lines += ["```", ""]

    lines += ["## Interpretação operacional", "",
              "Use este relatório para correlacionar os escritores dinâmicos com as rotinas paginadas e os bancos ativos. "
              "Um flag constante ou uma escrita repetida não deve ser tratado como conclusão de carregamento sem confirmar "
              "a rotina consumidora e a progressão normal do jogo.", ""]
    return "\n".join(lines)

report = markdown()
if args.out:
    args.out.write_text(report, encoding="utf-8")
else:
    print(report)

print(json.dumps({
    "records": len(records),
    "writes": {address: len(by_flag[address]) for address in sorted(flag_addresses)},
    "runs_with_writes": sorted(runs),
    "pcs": sorted({record.get("pc") for _, record in writes}),
}, indent=2))
