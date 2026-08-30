#!/usr/bin/env python3
from pathlib import Path
import argparse

p=argparse.ArgumentParser(description='Emulate routine 05B3E for lad0c glyph data')
p.add_argument('rom'); p.add_argument('--bank',type=int,default=13); p.add_argument('--cpu',type=lambda x:int(x,16),default=0xad0c); p.add_argument('--glyphs',type=int,default=32); p.add_argument('--out',required=True)
a=p.parse_args(); rom=Path(a.rom).read_bytes(); bank=rom[a.bank*0x4000:(a.bank+1)*0x4000]
base=a.cpu-0x8000
if base<0 or base>=len(bank): raise SystemExit('CPU address outside 0x8000 bank window')
source=bank[base:]
# 0x9720 shifts the character index four times: lad0c + code*0x10.
# 05B3E receives BC=0x0208: two passes, eight source bytes per pass.
def transform(g):
 src=g*0x10
 out=bytearray(0x80)
 for outer in range(2):
  for i in range(8):
   val=source[src]; src+=1
   off=outer*0x40+i*2
   out[off]=val; out[off+1]=0
 return bytes(out)
allout=bytearray()
for g in range(a.glyphs): allout += transform(g)
Path(a.out).write_bytes(allout)
print(f'wrote {len(allout)} bytes ({a.glyphs} glyphs) to {a.out}')
