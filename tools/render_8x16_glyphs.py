#!/usr/bin/env python3
from pathlib import Path
from PIL import Image, ImageDraw
import argparse

p=argparse.ArgumentParser()
p.add_argument('rom')
p.add_argument('--bank',type=int,default=13)
p.add_argument('--cpu',type=lambda x:int(x,16),default=0xad0c)
p.add_argument('--count',type=int,default=64)
p.add_argument('--out',required=True)
a=p.parse_args()
rom=Path(a.rom).read_bytes(); off=a.bank*0x4000+(a.cpu-0x8000)
buf=rom[off:off+a.count*0x40]
cols=16; scale=2
im=Image.new('L',(cols*8*scale,((a.count+cols-1)//cols)*16*scale),0)
d=ImageDraw.Draw(im)
for n in range(a.count):
 t=buf[n*64:(n+1)*64]
 if len(t)<64: break
 for y in range(16):
  for x in range(8):
   v=0
   for pl in range(4): v|=((t[pl*16+y]>>(7-x))&1)<<pl
   im.putpixel((n%cols*16+x*scale,n//cols*32+y*scale),v*17)
 d.text((n%cols*16,n//cols*32),f'{n:02X}',fill=255)
im.save(a.out)
print(f'wrote {a.count} 8x16 glyphs to {a.out}')
