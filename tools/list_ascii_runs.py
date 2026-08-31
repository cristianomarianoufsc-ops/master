"""List printable ASCII runs from a ROM."""
from pathlib import Path
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("rom", type=Path)
ap.add_argument("--minimum", type=int, default=8)
ap.add_argument("--limit", type=int, default=200)
a = ap.parse_args()
data = a.rom.read_bytes()
runs = []
start = None
for i, b in enumerate(data + b"\0"):
    printable = 0x20 <= b <= 0x7E
    if printable and start is None:
        start = i
    elif not printable and start is not None:
        if i - start >= a.minimum:
            runs.append((start, data[start:i].decode("ascii")))
        start = None
for off, text in runs[:a.limit]:
    print(f"0x{off:06X} bank={off//0x4000:02d} cpu=0x{0x4000+(off%0x4000):04X} {text}")
