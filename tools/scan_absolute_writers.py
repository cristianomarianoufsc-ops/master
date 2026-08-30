"""Find Z80 absolute stores to selected RAM addresses in an SMS ROM."""
from pathlib import Path
import argparse

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("rom", type=Path)
parser.add_argument("--addresses", default="0xC008,0xC203")
parser.add_argument("--context", type=int, default=24)
args = parser.parse_args()

rom = args.rom.read_bytes()
addresses = [int(value.strip(), 0) for value in args.addresses.split(",")]
patterns = {
    address: bytes((0x32, address & 0xFF, (address >> 8) & 0xFF))
    for address in addresses
}
print(f"rom={args.rom} size=0x{len(rom):X}")
for address, pattern in patterns.items():
    print(f"target=0x{address:04X} pattern={pattern.hex(' ')}")
    offset = 0
    count = 0
    while True:
        offset = rom.find(pattern, offset)
        if offset < 0:
            break
        bank, bank_offset = divmod(offset, 0x4000)
        cpu_address = bank_offset if bank_offset < 0x4000 else 0
        start = max(0, offset - args.context)
        end = min(len(rom), offset + len(pattern) + args.context)
        print(f"  file=0x{offset:06X} bank={bank} bank_offset=0x{bank_offset:04X} "
              f"cpu_fixed=0x{cpu_address:04X} bytes={rom[start:end].hex(' ')}")
        offset += 1
        count += 1
    print(f"  count={count}")
