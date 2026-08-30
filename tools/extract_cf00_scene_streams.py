#!/usr/bin/env python3
from pathlib import Path
import argparse

p=argparse.ArgumentParser(description='Extract scene streams selected by handler 9E70')
p.add_argument('rom');p.add_argument('--bank',type=int,default=21);p.add_argument('--first',type=lambda x:int(x,0),default=0x18);p.add_argument('--last',type=lambda x:int(x,0),default=0x30);p.add_argument('--out',required=True)
a=p.parse_args();rom=Path(a.rom).read_bytes();bank=rom[a.bank*0x4000:(a.bank+1)*0x4000]
def at(cpu,n=1): return bank[cpu-0x8000:cpu-0x8000+n]
# Handler uses the table at 5F4C, then adds the selected word to base 6046.
base_idx=0x5f4c-0x8000; base_data=0x6046-0x8000
out=[]
for c205 in range(a.first,a.last+1):
 idx=(c205-0x18)*2
 off=int.from_bytes(bank[base_idx+idx:base_idx+idx+2],'little')
 src=base_data+off
 if src<0 or src+0xa14>len(bank):
  out.append(f'C205=0x{c205:02X} off=0x{off:04X} src=OUT_OF_BANK');continue
 stream=bank[src:src+0xa14]
 path=Path(a.out).with_suffix('')
 path.parent.mkdir(parents=True,exist_ok=True)
 fn=path.parent/(path.name+f'_c205_{c205:02X}.bin');fn.write_bytes(stream)
 # Preserve a compact preview and positions of control markers.
 markers=[]
 for i,b in enumerate(stream):
  if b in (0xfb,0xfc,0xfd,0xfe,0xff,0xee): markers.append(f'{i:04X}:{b:02X}')
 out.append(f'C205=0x{c205:02X} off=0x{off:04X} cpu_src=0x{0x6046+off:04X} file_src=0x{a.bank*0x4000+src:06X} markers={" ".join(markers[:40])}')
Path(a.out).write_text('\n'.join(out)+'\n',encoding='utf-8')
print(f'wrote {len(out)} stream records to {a.out}')
