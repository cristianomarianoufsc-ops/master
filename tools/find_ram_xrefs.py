"""Find common Z80 absolute RAM references for selected 16-bit addresses."""
from pathlib import Path
import argparse

ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument("rom", type=Path)
ap.add_argument("targets", nargs="+", type=lambda x: int(x, 0))
a = ap.parse_args()
rom = a.rom.read_bytes()
patterns = {
    "ld_a_mem": lambda lo, hi: [(0x3A, lo, hi)],
    "ld_mem_a": lambda lo, hi: [(0x32, lo, hi)],
    "ld_hl_mem": lambda lo, hi: [(0x2A, lo, hi)],
    "ld_mem_hl": lambda lo, hi: [(0x22, lo, hi)],
}
for target in a.targets:
    lo, hi = target & 0xFF, (target >> 8) & 0xFF
    print(f"TARGET 0x{target:04X}")
    for kind, parts in patterns.items():
        needle = bytes(sum((list(x) for x in parts(lo, hi)), []))
        for off in range(len(rom) - len(needle) + 1):
            if rom[off:off + len(needle)] != needle:
                continue
            bank, within = divmod(off, 0x4000)
            logical = within if bank == 0 else 0x4000 + within
            print(f"  bank={bank:02d} file=0x{off:06X} logical=0x{logical:04X} {kind}")
