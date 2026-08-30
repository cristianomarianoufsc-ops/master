#!/usr/bin/env python3
"""Model the ROM's mask-table initialization from an explicit RAM snapshot.

This is intentionally not a full CPU emulator. It reproduces the confirmed
semantics of 04BBD, 04BD5, 04D16 and 04CFD, in the order used by the bank-21
initialization code. Dynamic RAM values must be supplied explicitly as
ADDR=VALUE arguments or as a JSON object; missing bytes default to zero and
are reported.
"""
from pathlib import Path
import argparse
import json

TABLE_BANK = 19

p = argparse.ArgumentParser(description=__doc__)
p.add_argument("rom")
p.add_argument("--ram-json", type=Path,
               help="JSON object with hexadecimal or decimal address keys")
p.add_argument("--set", dest="sets", action="append", default=[],
               metavar="ADDR=VALUE")
p.add_argument("--out", required=True)
a = p.parse_args()

rom = Path(a.rom).read_bytes()
bank = rom[TABLE_BANK * 0x4000:(TABLE_BANK + 1) * 0x4000]

def read8(cpu):
    pos = cpu - 0x8000
    if not 0 <= pos < len(bank):
        raise ValueError(f"CPU address outside bank 19: 0x{cpu:04X}")
    return bank[pos]

def parse_int(value):
    return int(str(value), 0)

ram = {}
if a.ram_json:
    raw = json.loads(a.ram_json.read_text(encoding="utf-8"))
    for key, value in raw.items():
        ram[parse_int(key)] = parse_int(value) & 0xFF
for item in a.sets:
    key, value = item.split("=", 1)
    ram[parse_int(key)] = parse_int(value) & 0xFF

missing = set()
def ram8(addr):
    if addr not in ram:
        missing.add(addr)
        return 0
    return ram[addr]

def table_records(table):
    hl = table
    count = read8(hl)
    hl += 1
    records = []
    for _ in range(count):
        addr = read8(hl) | read8(hl + 1) << 8
        mask = read8(hl + 2)
        hl += 3
        records.append((addr, mask))
    return records

def emu_04bbd(table):
    out = 0
    records = table_records(table)
    for index, (addr, mask) in enumerate(records):
        if index >= 8:
            continue
        if ram8(addr) & mask:
            out |= 1 << index
    return out, records

def emu_04bd5(table, out_base):
    out = []
    records = table_records(table)
    for addr, mask in records:
        out.append(1 if ram8(addr) & mask else 0)
    for index, value in enumerate(out):
        ram[out_base + index] = value
    return out, records

def emu_04d16(table, source_base):
    records = table_records(table)
    changes = []
    for index, (dest, mask) in enumerate(records):
        source = ram.get(source_base + index, 0)
        before = ram.get(dest, 0)
        after = before | mask if source else before
        ram[dest] = after
        changes.append((index, dest, mask, source, before, after))
    return changes

def emu_04cfd(table, c):
    records = table_records(table)
    changes = []
    c &= 0xFF
    for index, (dest, mask) in enumerate(records):
        carry = c & 1
        c = ((c >> 1) | (carry << 7)) & 0xFF
        before = ram.get(dest, 0)
        after = before | mask if carry else before & (~mask & 0xFF)
        ram[dest] = after
        changes.append((index, dest, mask, carry, before, after))
    return c, changes

# Confirmed 04BBD calls at 4A8D..4B0D.
queries = [
    ("AB89", 0xAB89, "signature_low"),
    ("ABA2", 0xABA2, "signature_high"),
    ("ABBB", 0xABBB, "C022"),
    ("ABC5", 0xABC5, "C025"),
    ("ABDE", 0xABDE, "C026"),
    ("ABE5", 0xABE5, "C027"),
    ("ABFE", 0xABFE, "C028"),
    ("AC1E", 0xAC1E, "C215"),
    ("AC31", 0xAC31, "C205"),
    ("AC0B", 0xAC0B, "C281_count"),
    ("ACD5", 0xACD5, "C251"),
]
results = []
for name, table, destination in queries:
    value, records = emu_04bbd(table)
    results.append({"name": name, "table": table, "destination": destination,
                    "count": len(records), "value": value})
    if destination.startswith("C") and destination not in ("C281_count",):
        ram[parse_int("0x" + destination)] = value

c281_count = next(x["value"] for x in results if x["name"] == "AC0B")
for i in range(c281_count):
    ram[0xC281 + i] = 1

buffers = []
for name, table, out_base in (("AC47", 0xAC47, 0xC032),
                              ("AC6C", 0xAC6C, 0xC2B0),
                              ("ACB5", 0xACB5, 0xC2D0),
                              ("ACBC", 0xACBC, 0xC2E0)):
    values, records = emu_04bd5(table, out_base)
    buffers.append({"table": name, "out_base": out_base,
                    "count": len(records), "hex": bytes(values).hex()})

# The confirmed calls immediately following the 04BD5 phase.
mask_calls = []
for name, table, c_addr in (("ABBB", 0xABBB, 0xC022),
                            ("ABC5", 0xABC5, 0xC025),
                            ("ABDE", 0xABDE, 0xC026),
                            ("ABE5", 0xABE5, 0xC027),
                            ("ABFE", 0xABFE, 0xC028),
                            ("AC1E", 0xAC1E, 0xC215),
                            ("AC31", 0xAC31, 0xC205),
                            ("ACD5", 0xACD5, 0xC251)):
    c = ram.get(c_addr, 0)
    new_c, changes = emu_04cfd(table, c)
    mask_calls.append({"table": name, "c_addr": c_addr, "initial_c": c,
                       "final_c": new_c, "changes": len(changes)})

lines = [
    "# Runtime initialization emulation",
    f"rom_size={len(rom)} table_bank={TABLE_BANK}",
    f"input_ram_bytes={len(ram) - sum(1 for x in ram if 0xC000 <= x < 0xD000)}",
    f"missing_ram_addresses={','.join(f'0x{x:04X}' for x in sorted(missing)) or 'none'}",
    "",
    "## 04BBD outputs",
]
for item in results:
    lines.append(f"{item['name']}: table=0x{item['table']:04X} count={item['count']} "
                 f"destination={item['destination']} value=0x{item['value']:02X}")
lines += ["", "## 04BD5 buffers"]
for item in buffers:
    lines.append(f"{item['table']}: out=0x{item['out_base']:04X} count={item['count']} hex={item['hex']}")
lines += ["", f"C281_count={c281_count}", "", "## 04CFD calls"]
for item in mask_calls:
    lines.append(f"{item['table']}: C=0x{item['initial_c']:02X} -> 0x{item['final_c']:02X} records={item['changes']}")
lines += ["", "## resulting RAM (non-zero)"]
for addr in sorted(ram):
    if ram[addr]:
        lines.append(f"0x{addr:04X},0x{ram[addr]:02X}")
Path(a.out).write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"wrote {a.out}")
