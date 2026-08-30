#!/usr/bin/env python3
from pathlib import Path
import argparse
p=argparse.ArgumentParser(description='Emulate handler 9E70 scene initialization')
p.add_argument('rom');p.add_argument('--bank',type=int,default=21);p.add_argument('--first',type=lambda x:int(x,0),default=0x18);p.add_argument('--last',type=lambda x:int(x,0),default=0x30);p.add_argument('--out',required=True)
a=p.parse_args();rom=Path(a.rom).read_bytes();bank=rom[a.bank*0x4000:(a.bank+1)*0x4000]
def off(cpu): return cpu-0x8000
base=0xCF00; base_src=bank[off(0x5f7e):off(0x5f7e)+0xa14]
out=[]
for c205 in range(a.first,a.last+1):
 ram=bytearray(0x10000);ram[base:base+len(base_src)]=base_src
 idx=(c205-0x18)*2; table=off(0x5f4c)+idx
 dest=bank[table]|(bank[table+1]<<8)
 s0=off(0x6046); s1=off(0x604a)
 if dest+0x14>0x10000: out.append(f'C205=0x{c205:02X} dest=0x{dest:04X} invalid');continue
 ram[dest:dest+4]=bank[s0:s0+4];ram[dest+0x10:dest+0x14]=bank[s1:s1+4]
 # dump the patched scene buffer and the two modified record areas
 fn=Path(a.out).with_suffix(''); fn=fn.parent/(fn.name+f'_c205_{c205:02X}.bin');fn.write_bytes(ram[base:base+0xa14])
 markers=[f'{i:04X}:{b:02X}' for i,b in enumerate(ram[base:base+0xa14]) if b in (0xfb,0xfc,0xfd,0xfe,0xff,0xee)]
 out.append(f'C205=0x{c205:02X} dest=0x{dest:04X} patch0={ram[dest:dest+4].hex()} patch1={ram[dest+0x10:dest+0x14].hex()} markers={" ".join(markers[:50])}')
Path(a.out).write_text('\n'.join(out)+'\n',encoding='utf-8');print(f'wrote {len(out)} patched buffers to {a.out}')
