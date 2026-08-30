#!/usr/bin/env python3
from pathlib import Path
import argparse

p=argparse.ArgumentParser(description='Emulate AC31/AC0B mask-table updates')
p.add_argument('rom'); p.add_argument('--bank',type=int,default=19); p.add_argument('--tables',default='ac31:7,ac0b:3'); p.add_argument('--flags',type=lambda x:int(x,16),default=0); p.add_argument('--out',required=True)
a=p.parse_args();rom=Path(a.rom).read_bytes();data=rom[a.bank*0x4000:]
ram={x:0 for x in range(0xd120,0xd140)}
# 04CFD semantics: rotate C right; set/clear target bit according to selected flag.
def apply(cpu,c):
 pos=cpu-0x8000; count=data[pos]; pos+=1
 carry=0
 for _ in range(count):
  addr=data[pos]|data[pos+1]<<8; mask=data[pos+2]; pos+=3
  # emulate RRC C, with initial C as low 8 bits
  old=c; c=((c>>1)|((c&1)<<7))&0xff
  bit=1 if (old&1) else 0
  if addr in ram:
   if bit: ram[addr]|=mask
   else: ram[addr]&=(~mask)&0xff
 return c
for spec in a.tables.split(','):
 name,c=spec.split(':'); apply(int(name,16),int(c,16))
# AC0B and related tables use the same family; emit resulting D12x state.
out=['# Emulated mask-table state','',f'bank={a.bank} flags=0x{a.flags:02X}','']
for addr in sorted(ram): out.append(f'0x{addr:04X},0x{ram[addr]:02X}')
# Candidate accepted-code mask: one byte per code, placeholder derived from nonzero state.
out += ['', '# nonzero D12x entries']
for addr in sorted(ram):
 if ram[addr]: out.append(f'0x{addr:04X}')
Path(a.out).write_text('\n'.join(out)+'\n',encoding='utf-8')
print(f'wrote emulated state to {a.out}')
