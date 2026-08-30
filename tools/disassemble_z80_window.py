#!/usr/bin/env python3
"""Disassemble a physical ROM bank window with Capstone's Z80 decoder."""
from pathlib import Path
import argparse
from capstone import Cs, CS_ARCH_Z80, CS_MODE_Z80

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("rom", type=Path)
parser.add_argument("--bank", type=lambda x: int(x, 0), required=True)
parser.add_argument("--start", type=lambda x: int(x, 0), required=True,
                    help="logical CPU address in 0x4000-0x7FFF or 0x8000-0xBFFF")
parser.add_argument("--end", type=lambda x: int(x, 0), required=True)
parser.add_argument("--base", type=lambda x: int(x, 0), default=None,
                    help="disassembly address base; defaults to --start")
a = parser.parse_args()
if not (0 <= a.bank):
    raise SystemExit("bank must be non-negative")
if not (0x4000 <= a.start < 0xC000 and a.start < a.end <= 0xC000):
    raise SystemExit("window must be inside 0x4000-0xBFFF")
rom = a.rom.read_bytes()
offset = a.bank * 0x4000 + (a.start & 0x3FFF)
size = a.end - a.start
code = rom[offset:offset + size]
if len(code) != size:
    raise SystemExit("window exceeds ROM")
md = Cs(CS_ARCH_Z80, CS_MODE_Z80)
md.detail = False
for insn in md.disasm(code, a.base if a.base is not None else a.start):
    print(f"{insn.address:04X}: {insn.bytes.hex(' '):<24} {insn.mnemonic} {insn.op_str}".rstrip())
