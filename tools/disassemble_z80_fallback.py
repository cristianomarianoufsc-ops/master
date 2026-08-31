"""Disassemble a physical SMS ROM window with the project's z80 decoder."""
from pathlib import Path
import argparse
import z80

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("rom", type=Path)
parser.add_argument("--bank", type=lambda x: int(x, 0), required=True)
parser.add_argument("--start", type=lambda x: int(x, 0), required=True)
parser.add_argument("--end", type=lambda x: int(x, 0), required=True)
args = parser.parse_args()
if not (0 <= args.bank and 0x4000 <= args.start < args.end <= 0xC000):
    raise SystemExit("invalid bank/window")
rom = args.rom.read_bytes()
builder = z80.Z80InstrBuilder()
base = args.bank * 0x4000
pos = args.start
while pos < args.end:
    off = base + (pos - 0x4000)
    raw = rom[off:off + 4]
    try:
        ins = builder.build_instr(pos, raw)
        size = getattr(ins, "size", 1) or 1
        text = str(ins)
    except Exception as exc:
        size = 1
        text = f"db {rom[off]:02X} ; {exc}"
    print(f"{pos:04X}: {rom[off:off+size].hex(' '):<12} {text}")
    pos += size
