"""Audit SMS capture reports/traces for evidence-quality risks.

The tool reports warnings, not proof of correctness. Exit status is nonzero when
an error-level risk is detected, making it suitable for CI or a continuation gate.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def issue(level, code, message, evidence=None):
    item = {"level": level, "code": code, "message": message}
    if evidence is not None:
        item["evidence"] = evidence
    return item


def audit_report(report, trace=None):
    issues = []
    if report.get("result") != "breakpoint":
        issues.append(issue("error", "BREAKPOINT_NOT_REACHED",
                            "A captura não atingiu o breakpoint declarado.",
                            {"result": report.get("result"), "pc": report.get("pc"),
                             "breakpoint": report.get("breakpoint")}))
    if report.get("result") == "error":
        issues.append(issue("error", "CAPTURE_ERROR", "A captura terminou com erro."))
    timing = report.get("timing", {})
    if not timing.get("scanline_irq") or not timing.get("dega_frame_schedule"):
        issues.append(issue("warning", "NON_REFERENCE_TIMING",
                            "A execução não usou simultaneamente o agendamento de frame do Dega e IRQ por scanline."))
    if report.get("steps", 0) <= 1:
        issues.append(issue("warning", "TOO_FEW_RUNS", "Há poucos blocos de execução para sustentar uma conclusão."))
    if trace is None:
        issues.append(issue("error", "TRACE_MISSING", "O relatório não possui trace associado."))
        return issues
    records = trace.get("trace", {}).get("records", [])
    limit = trace.get("trace", {}).get("limit")
    if limit and len(records) >= limit:
        issues.append(issue("error", "TRACE_SATURATED",
                            "O trace atingiu o limite e pode ter omitido eventos posteriores.",
                            {"records": len(records), "limit": limit}))
    if not records:
        issues.append(issue("error", "TRACE_EMPTY", "O trace não contém eventos."))
        return issues
    kinds = Counter(item.get("kind") for item in records)
    requested = sum(item.get("kind") == "irq_requested" for item in records)
    accepted = sum(item.get("kind") == "irq_injected" for item in records)
    if requested != accepted:
        issues.append(issue("warning", "IRQ_REQUEST_ACCEPT_MISMATCH",
                            "Há IRQs solicitadas que não foram aceitas pelo Z80 ou eventos aceitos sem solicitação equivalente.",
                            {"requested": requested, "accepted": accepted}))
    if any(item.get("kind") == "irq_injected" and item.get("pc") != "0x0038"
           for item in records):
        issues.append(issue("error", "IRQ_VECTOR_INVALID",
                            "Foi registrado aceite de IRQ fora do vetor IM1 0x0038."))
    controller = [item for item in records if item.get("kind") == "controller_read"]
    if not controller:
        issues.append(issue("warning", "NO_CONTROLLER_READ",
                            "Nenhuma leitura de controle foi observada no trace."))
    else:
        values = {item.get("value") for item in controller}
        if len(values) > 1:
            issues.append(issue("warning", "INPUT_NOT_STABLE",
                                "A captura amostrou valores de controle diferentes; atribuições causais exigem correlação temporal.",
                                {"values": sorted(values)}))
    for address in ("0xC008", "0xC203"):
        reads = [item.get("value") for item in records
                 if item.get("kind") == "mem_read" and item.get("address") == address]
        writes = [item.get("value") for item in records
                  if item.get("kind") == "mem_write" and item.get("address") == address]
        if reads and len(set(reads)) == 1 and len(reads) > 1000:
            issues.append(issue("warning", "FLAG_STUCK",
                                f"{address} permaneceu constante em muitas leituras; isso pode ser espera real ou modelo incompleto.",
                                {"reads": len(reads), "value": reads[0], "writes": writes}))
    pcs = Counter(item.get("pc") for item in records)
    if pcs:
        pc, count = pcs.most_common(1)[0]
        if count / len(records) >= 0.75:
            issues.append(issue("warning", "DOMINANT_PC_LOOP",
                                "Um único PC domina o trace; conclusões de progresso podem ser falso positivo de loop.",
                                {"pc": pc, "count": count, "records": len(records)}))
    return issues


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path)
    parser.add_argument("--trace", type=Path,
                        help="trace JSON; por padrão usa o objeto trace dentro do relatório")
    parser.add_argument("--out", type=Path, help="salva o resultado completo em JSON")
    args = parser.parse_args()
    report = load(args.report)
    trace = load(args.trace) if args.trace else report
    issues = audit_report(report, trace)
    result = {
        "report": str(args.report),
        "trace": str(args.trace) if args.trace else str(args.report),
        "status": "risk" if any(x["level"] == "error" for x in issues) else ("review" if issues else "pass"),
        "issues": issues,
    }
    text = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.out:
        args.out.write_text(text, encoding="utf-8")
    print(text, end="")
    return 1 if result["status"] == "risk" else 0


if __name__ == "__main__":
    sys.exit(main())
