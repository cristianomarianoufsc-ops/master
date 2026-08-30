"""Summarize a run_sms_capture trace and highlight repeated execution patterns."""
from pathlib import Path
import argparse
import collections
import json


def parse_int(value):
    return int(value, 0)


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("trace", type=Path, help="capture JSON or detailed trace JSON")
parser.add_argument("--top", type=int, default=20,
                    help="number of top PCs/addresses to print")
parser.add_argument("--json", action="store_true",
                    help="emit the summary as JSON")
args = parser.parse_args()

source = json.loads(args.trace.read_text(encoding="utf-8"))
if "trace" in source and "records" in source["trace"]:
    trace = source["trace"]["records"]
else:
    trace = source.get("records", [])

pc_counts = collections.Counter(record.get("pc") for record in trace)
kind_counts = collections.Counter(record.get("kind") for record in trace)
address_counts = collections.Counter(
    record.get("address") for record in trace if record.get("address") is not None)
run_counts = collections.Counter(record.get("run") for record in trace)
controller = [record for record in trace if record.get("kind") == "controller_read"]
mapper_writes = [record for record in trace
                 if record.get("kind") == "mem_write"
                 and record.get("address") in {"0xFFFC", "0xFFFD", "0xFFFE", "0xFFFF"}]
summary = {
    "records": len(trace),
    "kinds": kind_counts,
    "top_pcs": pc_counts.most_common(args.top),
    "top_addresses": address_counts.most_common(args.top),
    "runs": {"first": min(run_counts) if run_counts else None,
             "last": max(run_counts) if run_counts else None,
             "distinct": len(run_counts)},
    "controller_reads": controller,
    "mapper_writes": mapper_writes[-args.top:],
}

if args.json:
    print(json.dumps(summary, indent=2, default=lambda value: dict(value)))
else:
    print(f"records: {summary['records']}")
    print(f"runs: {summary['runs']}")
    print("kinds:")
    for kind, count in kind_counts.most_common():
        print(f"  {kind}: {count}")
    print("top PCs:")
    for pc, count in pc_counts.most_common(args.top):
        print(f"  {pc}: {count}")
    print("top addresses:")
    for address, count in address_counts.most_common(args.top):
        print(f"  {address}: {count}")
    print(f"controller reads: {len(controller)}")
    print(f"mapper writes: {len(mapper_writes)}")
