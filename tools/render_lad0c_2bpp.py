#!/usr/bin/env python3
from pathlib import Path
from PIL import Image,ImageDraw
import argparse
p=argparse.ArgumentParser(description='Render 16-byte 2bpp glyphs from lad0c')
p.add_argument('rom');p.add_argument('--bank',type=int,default=13);p.add_argument('--cpu',type=lambda x:int(x,16),default=0xad0c);p.add_argument('--count',type=int,default=64);p.add_argument('--out',required=True)
a=p.parse_args();rom=Path(a.rom).read_bytes();data=rom[a.bank*0x4000+a.cpu-0x8000:]
cols=16;scale=2;img=Image.new('RGB',(cols*8*scale,((a.count+cols-1)//cols)*8*scale),(40,40,40));d=ImageDraw.Draw(img)
for g in range(a.count):
 raw=data[g*16:g*16+16]; x0=(g%cols)*16;y0=(g//cols)*16
 for y in range(8):
  p0,p1=raw[y*2:y*2+2]
  for x in range(8):
   c=((p1>>(7-x))&1)*2+((p0>>(7-x))&1)
   q=c*85
   for yy in range(scale):
    for xx in range(scale):img.putpixel((x0+x*scale+xx,y0+y*scale+yy),(q,q,q))
 d.text((x0,y0),f'{g:02X}',fill=(255,0,0))
img.save(a.out);print(f'wrote {a.out}')
