#!/usr/bin/env python3
"""Find literal Z80 CALL/JP references to logical targets across ROM banks."""
import argparse
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument("rom", type=Path)
p.add_argument("targets", nargs="+", type=lambda x: int(x, 0))
a = p.parse_args()
rom = a.rom.read_bytes()
for target in a.targets:
    lo, hi = target & 0xFF, (target >> 8) & 0xFF
    print(f"TARGET 0x{target:04X}")
    for bank in range(len(rom) // 0x4000):
        chunk = rom[bank * 0x4000:(bank + 1) * 0x4000]
        for i in range(len(chunk) - 2):
            op = chunk[i]
            if chunk[i + 1] != lo or chunk[i + 2] != hi:
                continue
            addr = i if bank == 0 else 0x4000 + i
            if op == 0xCD:
                kind = "CALL"
            elif op == 0xC3:
                kind = "JP"
            else:
                continue
            print(f"  bank={bank:02d} file=0x{bank*0x4000+i:06X} logical=0x{addr:04X} {kind}")
