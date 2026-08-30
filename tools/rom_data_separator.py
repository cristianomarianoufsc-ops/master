#!/usr/bin/env python3
"""Heuristic analyzer for Sega Master System / Mark III ROMs.

It never modifies the input ROM. It identifies bank boundaries, padding, low/high
entropy regions, Z80-like code references, pointer tables, and 4bpp tile sheets.
All classifications are candidates and must be validated against emulator memory.
"""
from __future__ import annotations
import argparse, csv, hashlib, json, math, re
from pathlib import Path
from collections import Counter
from PIL import Image, ImageDraw

BANK = 0x4000
WINDOW = 0x400

def entropy(data: bytes) -> float:
    if not data: return 0.0
    n=len(data); c=Counter(data)
    return -sum((v/n)*math.log2(v/n) for v in c.values())

def runs(data: bytes, value: int, minimum: int = 64):
    out=[]; start=None
    for i,b in enumerate(data + bytes([value ^ 0xff])):
        if b == value and start is None: start=i
        elif b != value and start is not None:
            if i-start >= minimum: out.append((start,i-start,value))
            start=None
    return out

def z80_signatures(data: bytes):
    pats={
      'ld_hl_imm16': b'\x21', 'ld_de_imm16': b'\x11', 'ld_bc_imm16': b'\x01',
      'call': b'\xcd', 'bank_write_ffff': b'\x32\xff\xff',
      'vdp_data_out': b'\xd3\xbe', 'vdp_ctrl_out': b'\xd3\xbf',
      'rst_8': b'\xcf',
    }
    found={}
    for name,p in pats.items(): found[name]=[m.start() for m in re.finditer(re.escape(p),data)]
    # Decode common three-byte Z80 instructions into useful literal references.
    refs=[]; calls=[]
    for i in range(len(data)-2):
        op=data[i]
        if op in (0x01,0x11,0x21,0x31,0x22,0x2a,0x32,0x3a,0xcd):
            v=data[i+1] | (data[i+2]<<8)
            kind={0x01:'ld_bc',0x11:'ld_de',0x21:'ld_hl',0x31:'ld_sp',0x22:'ld_mem_hl',0x2a:'ld_hl_mem',0x32:'ld_mem_a',0x3a:'ld_a_mem',0xcd:'call'}[op]
            item={'file_offset':i,'opcode':op,'kind':kind,'value':v}
            if 0x4000 <= v <= 0xffff: refs.append(item)
            if op==0xcd: calls.append(item)
    found['literal_references']=refs
    found['call_targets']=calls
    return found

def pointer_tables(data: bytes, min_run=5):
    # Candidate little-endian pointer runs to SMS CPU windows 0x4000-0xffff.
    hits=[]
    for off in range(0,len(data)-2,2):
        count=0; vals=[]
        j=off
        while j+1<len(data):
            v=data[j] | (data[j+1]<<8)
            if 0x4000 <= v <= 0xffff:
                count += 1; vals.append(v); j += 2
            else: break
        if count >= min_run:
            hits.append({'offset':off,'length':count*2,'count':count,'values':vals[:16]})
    # merge overlapping/adjacent reports
    merged=[]
    for h in hits:
        if merged and h['offset'] <= merged[-1]['offset']+merged[-1]['length']:
            end=max(merged[-1]['offset']+merged[-1]['length'],h['offset']+h['length'])
            merged[-1]['length']=end-merged[-1]['offset']; merged[-1]['count']=max(merged[-1]['count'],h['count'])
        else: merged.append(h)
    return merged

def tile_score(data: bytes, off: int):
    # SMS 4bpp planar tile: four bytes per row, 8 rows.
    d=data[off:off+32]
    if len(d)<32: return 0.0
    nonzero=sum(x!=0 for x in d); nonff=sum(x!=255 for x in d)
    # Avoid all-empty/all-solid and score varied glyph-like tiles.
    colors=set()
    for y in range(8):
        for x in range(8):
            bit=7-x; v=sum(((d[y*4+p]>>bit)&1)<<p for p in range(4)); colors.add(v)
    return (len(colors)-1) * 2 + min(nonzero,32)/32 + min(nonff,32)/32

def render_tiles(data: bytes, start: int, count: int, out: Path, scale=3):
    cols=16; rows=(count+cols-1)//cols
    im=Image.new('RGB',(cols*8*scale,rows*8*scale),'black')
    for n in range(count):
        off=start+n*32; d=data[off:off+32]
        if len(d)<32: break
        for y in range(8):
            for x in range(8):
                bit=7-x; v=sum(((d[y*4+p]>>bit)&1)<<p for p in range(4))
                c=255 if v else 0
                for yy in range(scale):
                    for xx in range(scale): im.putpixel(( (n%cols)*8*scale+x*scale+xx, (n//cols)*8*scale+y*scale+yy),(c,c,c))
    im.save(out)

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('rom',type=Path); ap.add_argument('-o','--out',type=Path,default=Path('rom_analysis'))
    ap.add_argument('--dump-regions',action='store_true'); ap.add_argument('--tile-sheets',action='store_true')
    args=ap.parse_args(); data=args.rom.read_bytes(); args.out.mkdir(parents=True,exist_ok=True)
    report={'input':str(args.rom.resolve()),'size':len(data),'sha256':hashlib.sha256(data).hexdigest(),'bank_size':BANK,'banks':[]}
    for n in range((len(data)+BANK-1)//BANK):
        s=n*BANK; chunk=data[s:s+BANK]
        report['banks'].append({'bank':n,'file_offset':s,'size':len(chunk),'entropy':round(entropy(chunk),4),'zero_bytes':chunk.count(0),'ff_bytes':chunk.count(255),'unique_bytes':len(set(chunk))})
    report['padding_runs']=[{'offset':s,'length':length,'value':v} for s,length,v in runs(data,0xff)+runs(data,0)]
    report['pointer_tables']=pointer_tables(data)
    sig=z80_signatures(data)
    report['z80_signatures']={k:{'count':len(v),'offsets':v[:200]} for k,v in sig.items()}
    # Sliding entropy candidates, excluding obvious fill.
    windows=[]
    for s in range(0,len(data),WINDOW):
        c=data[s:s+WINDOW]; e=entropy(c)
        if len(c)==WINDOW and c.count(0xff)<WINDOW*.8 and c.count(0)<WINDOW*.8:
            windows.append({'offset':s,'entropy':round(e,4),'unique_bytes':len(set(c)),'zero_bytes':c.count(0),'ff_bytes':c.count(255)})
    report['windows_low_entropy']=sorted(windows,key=lambda x:x['entropy'])[:200]
    # Candidate tile-rich windows: number of varied 4bpp tiles.
    tile_regions=[]
    for s in range(0,len(data)-0x400,0x400):
        scores=[tile_score(data,s+i*32) for i in range(32)]
        good=sum(x>=4 for x in scores)
        if good>=12: tile_regions.append({'offset':s,'good_tiles':good,'mean_score':round(sum(scores)/len(scores),3)})
    report['tile_regions']=tile_regions
    (args.out/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    with (args.out/'banks.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=report['banks'][0].keys()); w.writeheader(); w.writerows(report['banks'])
    with (args.out/'regions.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['offset','entropy','unique_bytes','zero_bytes','ff_bytes']); w.writeheader(); w.writerows(report['windows_low_entropy'])
    if args.dump_regions:
        for i,r in enumerate(report['windows_low_entropy'][:64]):
            s=r['offset']; (args.out/f'region_{s:06x}_{s+WINDOW:06x}.bin').write_bytes(data[s:s+WINDOW])
    if args.tile_sheets:
        for r in report['tile_regions'][:32]:
            s=r['offset']; render_tiles(data,s,64,args.out/f'tiles_{s:06x}.png')
    print(json.dumps({'rom':str(args.rom),'size':len(data),'banks':len(report['banks']),'padding_runs':len(report['padding_runs']),'pointer_tables':len(report['pointer_tables']),'tile_regions':len(tile_regions),'report':str((args.out/'report.json').resolve())},indent=2))

if __name__=='__main__': main()
