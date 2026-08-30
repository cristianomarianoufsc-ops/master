#!/usr/bin/env python3
from pathlib import Path
import argparse
p=argparse.ArgumentParser(description='Filter only handler-referenced streams')
p.add_argument('manifest');p.add_argument('--out',required=True);p.add_argument('--max-bytes',type=int,default=128)
a=p.parse_args(); lines=Path(a.manifest).read_text(errors='replace').splitlines(); out=['# Referenced text-stream candidates','']
for line in lines:
 if 'ptr=0x' not in line or ('raw=' not in line and 'hex=' not in line): continue
 parts=dict(x.split('=',1) for x in line.split() if '=' in x)
 raw=parts.get('raw', parts.get('hex',''));
 if not raw: continue
 data=bytes.fromhex(raw[:a.max_bytes*2]); nonzero=[x for x in data if x not in (0,0xff,0xfb,0xfc,0xfd,0xfe,0xee)]
 ratio=len(nonzero)/max(1,len(data))
 out.append(f"{line} candidate_ratio={ratio:.3f} glyph_like={'yes' if ratio>=0.35 else 'no'}")
Path(a.out).write_text('\n'.join(out)+'\n',encoding='utf-8'); print(f'wrote {a.out}')
