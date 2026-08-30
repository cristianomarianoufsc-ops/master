#!/usr/bin/env python3
"""Recover candidate SMS VRAM blocks from a Mednafen gzip save state.

Mednafen save states are emulator-internal and do not expose a public VRAM offset.
This tool therefore scores every aligned 16 KiB window against tile-occupancy
signatures inferred from a screenshot. It is a candidate extractor, not a proof
that a window is VRAM. It never modifies the state or ROM.
"""
from __future__ import annotations
import argparse, gzip, hashlib, json
from pathlib import Path
from collections import Counter
from PIL import Image

VRAM=0x4000; TILE=32

def mask_from_tile(d):
    if len(d)<32:return 0
    m=0
    for y in range(8):
        for x in range(8):
            bit=7-x; v=0
            for p in range(4): v |= ((d[y*4+p]>>bit)&1)<<p
            if v: m |= 1<<(y*8+x)
    return m

def screenshot_masks(path):
    im=Image.open(path).convert('RGB')
    w,h=im.size
    # The local Mednafen captures use a 4x scaled 256x192 SMS viewport with
    # 96 px top/bottom letterbox. Otherwise center-crop and resize conservatively.
    if (w,h)==(1024,960): im=im.crop((0,96,1024,864)).resize((256,192),Image.Resampling.NEAREST)
    else: im=im.resize((256,192),Image.Resampling.NEAREST)
    out=[]
    for ty in range(24):
        for tx in range(32):
            m=0
            for y in range(8):
                for x in range(8):
                    r,g,b=im.getpixel((tx*8+x,ty*8+y));
                    # Occupancy signature is robust to palette differences.
                    if max(r,g,b)>45: m |= 1<<(y*8+x)
            out.append(m)
    return Counter(out)

def score_window(raw, off, wanted):
    # Count how many distinct visible 8x8 patterns are present in the candidate.
    have=Counter(mask_from_tile(raw[off+i*32:off+(i+1)*32]) for i in range(512))
    score=0; exact=0
    for m,n in wanted.items():
        # Empty screen cells are common and provide no evidence of VRAM.
        if m == 0: continue
        if m in have:
            score += min(n,have[m]); exact += 1
    # A real VRAM tile set normally has varied graphics; heavily uniform
    # windows are state padding/RAM and should rank below richer candidates.
    diversity=len([m for m in have if m != 0])
    score += min(diversity,64)
    return score,exact,diversity

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('state',type=Path); ap.add_argument('screenshot',type=Path)
    ap.add_argument('-o','--out',type=Path,default=Path('vram_candidates'))
    ap.add_argument('--step',type=lambda x:int(x,0),default=0x10)
    ap.add_argument('--top',type=int,default=12)
    args=ap.parse_args(); raw=gzip.open(args.state,'rb').read(); wanted=screenshot_masks(args.screenshot)
    args.out.mkdir(parents=True,exist_ok=True)
    rows=[]
    for off in range(0,max(0,len(raw)-VRAM+1),args.step):
        s,e,x=score_window(raw,off,wanted); rows.append({'state_offset':off,'score':s,'exact_masks':e,'unique_tile_masks':x})
    rows.sort(key=lambda r:(r['score'],r['exact_masks']),reverse=True)
    candidates=[]
    for n,r in enumerate(rows[:args.top]):
        p=args.out/f'candidate_{n:02d}_{r["state_offset"]:06x}.vram'; p.write_bytes(raw[r['state_offset']:r['state_offset']+VRAM]); r['path']=str(p.resolve()); candidates.append(r)
    report={'state':str(args.state.resolve()),'state_size':len(raw),'state_sha256':hashlib.sha256(raw).hexdigest(),'screenshot':str(args.screenshot.resolve()),'screenshot_masks':len(wanted),'step':args.step,'candidates':candidates}
    (args.out/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report,indent=2))

if __name__=='__main__': main()
