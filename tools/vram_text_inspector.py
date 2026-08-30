#!/usr/bin/env python3
"""Inspect a 16 KiB Sega Master System VRAM dump.

The tool is read-only and does not modify ROM/VRAM. It reconstructs 4bpp tiles,
exports a tile sheet, decodes the default SMS name table at 0x3800, reports tile
indices used by each screen cell, and optionally correlates tile bytes with a ROM.
"""
from __future__ import annotations
import argparse, csv, hashlib, json
from pathlib import Path
from PIL import Image, ImageDraw

VRAM_SIZE=0x4000
TILE_SIZE=32

def decode_tile(vram, idx):
    off=idx*TILE_SIZE; d=vram[off:off+TILE_SIZE]
    if len(d)<TILE_SIZE: return [[0]*8 for _ in range(8)]
    out=[]
    for y in range(8):
        row=[]
        for x in range(8):
            bit=7-x; row.append(sum(((d[y*4+p]>>bit)&1)<<p for p in range(4)))
        out.append(row)
    return out

def render_sheet(vram, out, start=0, count=256, scale=2):
    cols=16; rows=(count+cols-1)//cols
    im=Image.new('RGB',(cols*8*scale,rows*8*scale),'black')
    for n in range(count):
        t=decode_tile(vram,start+n)
        for y in range(8):
            for x in range(8):
                v=t[y][x]; c=(v*17,v*17,v*17)
                for yy in range(scale):
                    for xx in range(scale): im.putpixel(((n%cols)*8*scale+x*scale+xx,(n//cols)*8*scale+y*scale+yy),c)
    im.save(out)

def render_nametable(vram,out,scale=2):
    # SMS mode 4 name table: 32 columns x 28 rows, words at 0x3800.
    im=Image.new('RGB',(32*8*scale,28*8*scale),'black')
    for y in range(28):
        for x in range(32):
            p=0x3800+2*(y*32+x)
            idx=(vram[p]|(vram[p+1]<<8))&0x1ff if p+1<len(vram) else 0
            t=decode_tile(vram,idx)
            for yy in range(8):
                for xx in range(8):
                    v=t[yy][xx]; c=(v*17,v*17,v*17)
                    for sy in range(scale):
                        for sx in range(scale): im.putpixel((x*8*scale+xx*scale+sx,y*8*scale+yy*scale+sy),c)
    im.save(out)

def find_rom_matches(vram,rom):
    out=[]
    for idx in range(min(512,len(vram)//32)):
        tile=vram[idx*32:idx*32+32]
        if not any(tile): continue
        hits=[]; pos=rom.find(tile)
        while pos>=0 and len(hits)<32:
            hits.append(pos); pos=rom.find(tile,pos+1)
        if hits: out.append({'vram_tile':idx,'rom_offsets':hits})
    return out

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('vram',type=Path,help='raw 16 KiB VRAM dump')
    ap.add_argument('-o','--out',type=Path,default=Path('vram_analysis'))
    ap.add_argument('--rom',type=Path,help='optional ROM to search for exact tile bytes')
    ap.add_argument('--sheet-start',type=lambda x:int(x,0),default=0)
    ap.add_argument('--sheet-count',type=int,default=256)
    args=ap.parse_args(); vram=args.vram.read_bytes()
    if len(vram)!=VRAM_SIZE: raise SystemExit(f'VRAM must be exactly 16384 bytes, got {len(vram)}')
    args.out.mkdir(parents=True,exist_ok=True)
    render_sheet(vram,args.out/'vram_tiles.png',args.sheet_start,args.sheet_count)
    render_nametable(vram,args.out/'name_table.png')
    cells=[]
    for y in range(28):
        for x in range(32):
            p=0x3800+2*(y*32+x); word=vram[p]|(vram[p+1]<<8)
            cells.append({'x':x,'y':y,'vram_offset':p,'word':word,'tile':word&0x1ff,'priority':bool(word&0x1000),'palette':(word>>11)&1,'flip_h':bool(word&0x0200),'flip_v':bool(word&0x0400)})
    report={'vram':str(args.vram.resolve()),'size':len(vram),'sha256':hashlib.sha256(vram).hexdigest(),'pattern_bytes_used':sum(b!=0 for b in vram[:0x2000]),'name_table_base':'0x3800','cells':cells,'tile_usage':{str(k):sum(c['tile']==k for c in cells) for k in sorted({c['tile'] for c in cells})}}
    if args.rom:
        rom=args.rom.read_bytes(); report['rom']=str(args.rom.resolve()); report['rom_sha256']=hashlib.sha256(rom).hexdigest(); report['rom_matches']=find_rom_matches(vram,rom)
    (args.out/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    with (args.out/'name_table.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=cells[0].keys()); w.writeheader(); w.writerows(cells)
    print(json.dumps({'vram_size':len(vram),'used_tiles':len(report['tile_usage']),'sheet':str((args.out/'vram_tiles.png').resolve()),'name_table':str((args.out/'name_table.png').resolve()),'report':str((args.out/'report.json').resolve())},indent=2))

if __name__=='__main__': main()
