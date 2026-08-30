#!/usr/bin/env python3
"""Exact emulator for the fixed-slot routine at 04D16.

04D16 receives HL=table in the paged data bank and BC=source RAM. The table
format is: count byte, followed by count records of little-endian destination
address plus one mask byte. For each record it tests (BC), and, only when the
source byte is non-zero, ORs the mask into the destination byte. BC advances
one byte per record. The routine uses EXX, but the observable operation is
represented directly here.
"""
from pathlib import Path
import argparse

p = argparse.ArgumentParser(description="Exact 04D16 emulator")
p.add_argument("rom")
p.add_argument("--bank", type=int, default=19, help="physical bank containing the table")
p.add_argument("--table", type=lambda x: int(x, 0), required=True)
p.add_argument("--source", default="", help="source bytes as hex, one byte per record")
p.add_argument("--source-base", type=lambda x: int(x, 0), default=0xC032)
p.add_argument("--ram-base", type=lambda x: int(x, 0), default=0xD120)
p.add_argument("--ram-size", type=lambda x: int(x, 0), default=0x40)
p.add_argument("--out", required=True)
a = p.parse_args()

rom = Path(a.rom).read_bytes()
bank = rom[a.bank * 0x4000:(a.bank + 1) * 0x4000]
def read8(cpu):
    pos = cpu - 0x8000
    if not 0 <= pos < len(bank):
        raise ValueError(f"CPU address outside bank window: 0x{cpu:04X}")
    return bank[pos]

hl = a.table
count = read8(hl)
hl += 1
source = bytes.fromhex(a.source) if a.source else bytes([0] * count)
if len(source) < count:
    raise ValueError(f"source has {len(source)} bytes, but table needs {count}")
ram = {addr: 0 for addr in range(a.ram_base, a.ram_base + a.ram_size)}
records = []
for i in range(count):
    dest = read8(hl) | (read8(hl + 1) << 8)
    mask = read8(hl + 2)
    hl += 3
    value = source[i]
    before = ram.get(dest, 0)
    after = before | mask if value else before
    if dest in ram:
        ram[dest] = after
    records.append((i, dest, mask, value, before, after))

out = [
    "# Exact 04D16 emulation",
    f"bank={a.bank} table=0x{a.table:04X} count={count}",
    f"source_base=0x{a.source_base:04X} source={source[:count].hex()}",
    "",
    "## records",
]
for i, dest, mask, value, before, after in records:
    out.append(f"{i:02d}: dest=0x{dest:04X} mask=0x{mask:02X} source=0x{value:02X} before=0x{before:02X} after=0x{after:02X}")
out += ["", "## resulting RAM"]
for addr in sorted(ram):
    if ram[addr]:
        out.append(f"0x{addr:04X},0x{ram[addr]:02X}")
Path(a.out).write_text("\n".join(out) + "\n", encoding="utf-8")
print(f"wrote {a.out}")
