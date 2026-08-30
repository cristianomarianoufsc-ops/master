#!/usr/bin/env python3
"""Emulate the fixed-slot routine at 08BD5/04BD5.

The paged table contains count records of (little-endian address, mask).
04BD5 reads RAM[address], tests mask, and writes a boolean byte (01/00) to a
sequential output buffer. The caller's EXX state determines the output base;
this tool makes the two roles explicit instead of conflating DE registers.
"""
from pathlib import Path
import argparse

p = argparse.ArgumentParser(description="Exact 04BD5 emulator")
p.add_argument("rom")
p.add_argument("--bank", type=int, default=19)
p.add_argument("--table", type=lambda x: int(x, 0), required=True)
p.add_argument("--out-base", type=lambda x: int(x, 0), default=0xC032)
p.add_argument("--set", dest="sets", action="append", default=[], metavar="ADDR=VALUE")
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
records = []
output = []
for i in range(count):
    addr = read8(hl) | (read8(hl + 1) << 8)
    mask = read8(hl + 2)
    hl += 3
    value = ram.get(addr, 0)
    result = 1 if (value & mask) else 0
    dest = a.out_base + i
    output.append(result)
    records.append((i, addr, mask, value, result, dest))

lines = [
    "# Exact 04BD5 emulation",
    f"bank={a.bank} table=0x{a.table:04X} count={count}",
    f"out_base=0x{a.out_base:04X} output={bytes(output).hex()}",
    "",
    "## records",
]
for i, addr, mask, value, result, dest in records:
    lines.append(f"{i:02d}: read=0x{addr:04X} mask=0x{mask:02X} value=0x{value:02X} result=0x{result:02X} write=0x{dest:04X}")
Path(a.out).write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"wrote {a.out}")
