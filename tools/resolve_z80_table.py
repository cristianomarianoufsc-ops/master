#!/usr/bin/env python3
from pathlib import Path
import argparse
p=argparse.ArgumentParser(); p.add_argument('rom',type=Path); p.add_argument('--bank',type=int,required=True); p.add_argument('--base',type=lambda x:int(x,0),required=True); p.add_argument('--index',type=lambda x:int(x,0),required=True); a=p.parse_args()
b=a.rom.read_bytes()[a.bank*0x4000:(a.bank+1)*0x4000]
o=(a.base-0x8000) if a.base>=0x8000 else a.base-0x4000
pos=o+2*a.index
lo,hi=b[pos],b[pos+1]
print(f'bank={a.bank} base=0x{a.base:04X} index=0x{a.index:02X} table_offset=0x{pos:04X} pointer=0x{lo|hi<<8:04X} bytes={lo:02X} {hi:02X}')
