#!/usr/bin/env python3
from pathlib import Path
from PIL import Image, ImageDraw
import argparse

p=argparse.ArgumentParser(description='Render transformed 05B3E tile buffer')
p.add_argument('bin'); p.add_argument('--count',type=int,default=32); p.add_argument('--out',required=True)
a=p.parse_args(); raw=Path(a.bin).read_bytes(); w=8; h=8; cols=8; scale=2
sheet=Image.new('RGB',(cols*w*scale,((a.count+cols-1)//cols)*h*scale),(32,32,32))
for g in range(a.count):
 tile=raw[g*0x80:g*0x80+0x40]
 x0=(g%cols)*w*scale; y0=(g//cols)*h*scale
 for y in range(h):
  planes=tile[y*4:y*4+4]
  for x in range(w):
   c=0
   for bit,pv in enumerate(planes): c |= ((pv>>(7-x))&1)<<bit
   q=255 if c else 0
   for yy in range(scale):
    for xx in range(scale): sheet.putpixel((x0+x*scale+xx,y0+y*scale+yy),(q,q,q))
 d=ImageDraw.Draw(sheet); d.text((x0,y0),f'{g:02X}',fill=(255,0,0))
sheet.save(a.out)
print(f'wrote {a.out}')
