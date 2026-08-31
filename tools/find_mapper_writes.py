#!/usr/bin/env python3
"""List literal Z80 writes to the SMS mapper register FFFF."""
from __future__ import annotations
import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("rom", type=Path)
parser.add_argument("--register", type=lambda s: int(s, 0), default=0xFFFF)
args = parser.parse_args()
rom = args.rom.read_bytes()
pattern = bytes((0x32, args.register & 0xFF, (args.register >> 8) & 0xFF))
for offset in range(len(rom) - 2):
    if rom[offset:offset + 3] != pattern:
        continue
    bank, inner = divmod(offset, 0x4000)
    cpu = inner if bank == 0 else 0x4000 + inner
    value = rom[offset - 1] if offset >= 2 and rom[offset - 2] == 0x3E else None
    if value is not None:
        value_text = f"literal=0x{value:02X}"
    else:
        value_text = "literal=unknown"
    print(f"bank={bank:02d} file=0x{offset:06X} cpu=0x{cpu:04X} {value_text}")
