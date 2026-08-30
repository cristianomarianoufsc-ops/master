#!/usr/bin/env python3
from pathlib import Path
import argparse
p=argparse.ArgumentParser(description='Validate referenced text stream candidates')
p.add_argument('manifest');p.add_argument('--out',required=True);p.add_argument('--min-len',type=int,default=2)
a=p.parse_args();out=['# Structurally validated text candidates','']
for line in Path(a.manifest).read_text(errors='replace').splitlines():
 if 'hex=' not in line or 'ptr=0x' not in line: continue
 parts=dict(x.split('=',1) for x in line.split() if '=' in x); hx=parts.get('hex','')
 try: data=bytes.fromhex(hx)
 except ValueError: continue
 if len(data)<a.min_len or not data or data[-1]!=0xff: continue
 words=[data[i]|data[i+1]<<8 for i in range(0,len(data)-1,2)]
 pointer_words=sum(1 for w in words if 0x8000<=w<0xc000)
 controls=sum(1 for x in data if x in (0xee,0xfb,0xfc,0xfd,0xfe))
 score=len(data)-4*pointer_words-2*controls
 kind='candidate' if pointer_words==0 and score>=2 else 'state_or_pointer'
 out.append(f'{line} pointer_words={pointer_words} controls={controls} score={score} class={kind}')
Path(a.out).write_text('\n'.join(out)+'\n',encoding='utf-8');print(f'wrote {a.out}')
