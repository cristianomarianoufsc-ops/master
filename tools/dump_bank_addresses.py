#!/usr/bin/env python3
from pathlib import Path
import argparse

parser = argparse.ArgumentParser(description='Dump Z80 CPU addresses from selected ROM banks')
parser.add_argument('rom')
parser.add_argument('addresses', nargs='+', help='hex CPU addresses, e.g. 6867 af55')
parser.add_argument('--banks', default='0-31', help='bank range, e.g. 16-23 or 21')
parser.add_argument('--length', type=int, default=96)
args = parser.parse_args()

rom = Path(args.rom).read_bytes()
if len(rom) % 0x4000:
    raise SystemExit(f'ROM size is not bank-aligned: {len(rom)}')

def parse_range(spec):
    out = []
    for part in spec.split(','):
        if '-' in part:
            a, b = part.split('-', 1)
            out.extend(range(int(a, 0), int(b, 0) + 1))
        else:
            out.append(int(part, 0))
    return out

banks = parse_range(args.banks)
addresses = [int(x, 16) for x in args.addresses]
for bank in banks:
    if bank * 0x4000 >= len(rom):
        continue
    data = rom[bank * 0x4000:(bank + 1) * 0x4000]
    for cpu in addresses:
        if 0x8000 <= cpu < 0xC000:
            off = cpu - 0x8000
        elif 0x4000 <= cpu < 0x8000:
            off = cpu - 0x4000
        else:
            continue
        if off + 1 >= len(data):
            continue
        chunk = data[off:off + args.length]
        print(f'bank={bank:02d} cpu=0x{cpu:04X} file=0x{bank*0x4000+off:06X} bytes={chunk.hex()}')
