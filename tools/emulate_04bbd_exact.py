#!/usr/bin/env python3
"""Emulate the fixed-slot 04BBD bit-mask producer.

The routine reads a count followed by (little-endian RAM address, mask)
records from a paged ROM table. It tests each RAM byte, and packs matching
records into one output byte using successive bits 0..7. The input RAM state
is explicit because it is produced dynamically by the preceding game flow.
"""
from pathlib import Path
import argparse

p = argparse.ArgumentParser(description="Exact 04BBD emulator")
p.add_argument("rom")
p.add_argument("--bank", type=int, default=19,
               help="physical bank containing the table")
p.add_argument("--table", type=lambda x: int(x, 0), required=True,
               help="CPU address of the count/record table")
p.add_argument("--set", dest="sets", action="append", default=[],
               metavar="ADDR=VALUE", help="RAM byte value; may be repeated")
p.add_argument("--out", required=True)
a = p.parse_args()

rom = Path(a.rom).read_bytes()
bank = rom[a.bank * 0x4000:(a.bank + 1) * 0x4000]

def read8(cpu):
    pos = cpu - 0x8000
    if not 0 <= pos < len(bank):
        raise ValueError(f"CPU address outside data bank: 0x{cpu:04X}")
    return bank[pos]

ram = {}
for item in a.sets:
    key, value = item.split("=", 1)
    ram[int(key, 0)] = int(value, 0) & 0xFF

hl = a.table
count = read8(hl)
hl += 1
output = 0
records = []
for index in range(count):
    addr = read8(hl) | (read8(hl + 1) << 8)
    mask = read8(hl + 2)
    hl += 3
    value = ram.get(addr, 0)
    matched = bool(value & mask)
    bit = 1 << index if index < 8 else 0
    if matched and index < 8:
        output |= bit
    records.append((index, addr, mask, value, matched, bit))

lines = [
    "# Exact 04BBD emulation",
    f"bank={a.bank} table=0x{a.table:04X} count={count}",
    f"output=0x{output:02X}",
    "",
    "> The routine packs record matches into bits 0..7. Tables with more than",
    "> eight records are not valid single-byte 04BBD outputs and are reported",
    "> for inspection rather than silently truncated in the game model.",
    "",
    "## records",
]
for index, addr, mask, value, matched, bit in records:
    lines.append(
        f"{index:02d}: read=0x{addr:04X} mask=0x{mask:02X} "
        f"value=0x{value:02X} match={int(matched)} "
        f"output_bit=0x{bit:02X}"
    )
Path(a.out).write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"wrote {a.out}")
