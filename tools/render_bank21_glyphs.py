#!/usr/bin/env python3
from pathlib import Path
from PIL import Image, ImageDraw
import argparse

p = argparse.ArgumentParser(description='Render 4bpp SMS glyph blocks from a bank')
p.add_argument('rom')
p.add_argument('--bank', type=int, default=21)
p.add_argument('--cpu', type=lambda x: int(x, 16), default=0xAD0C)
p.add_argument('--count', type=int, default=64)
p.add_argument('--out', required=True)
a = p.parse_args()
rom = Path(a.rom).read_bytes()
base = a.bank * 0x4000 + (a.cpu - 0x8000)
buf = rom[base:base + a.count*0x40]
cols = 16
scale = 2
sheet = Image.new('L', (cols*8*scale, ((a.count+cols-1)//cols)*8*scale), 0)
for idx in range(a.count):
    tile = buf[idx*0x40:(idx+1)*0x40]
    if len(tile) < 0x40: break
    for y in range(8):
        for x in range(8):
            # SMS 4bpp tile planes are each 8 bytes, one byte per row.
            px = 0
            for plane in range(4):
                px |= ((tile[plane*8+y] >> (7-x)) & 1) << plane
            sheet.putpixel((idx%cols*8*scale+x*scale, idx//cols*8*scale+y*scale), px*17)
    ImageDraw.Draw(sheet).text((idx%cols*8*scale, idx//cols*8*scale), f'{idx:02X}', fill=255)
sheet.save(a.out)
print(f'wrote {a.count} glyphs to {a.out}')
