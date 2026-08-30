from pathlib import Path
from PIL import Image,ImageDraw
rom=Path('/home/ubuntu/work/kujakuou_direct/work/kujaku_ou_jp_original.sms').read_bytes()
starts=[0x4d600,0x4d700,0x4a000,0x4a100]
def tile(off):
 d=rom[off:off+32]; pix=[]
 for y in range(8):
  row=[]
  for x in range(8):
   bit=7-x
   v=sum(((d[y*4+p]>>bit)&1)<<p for p in range(4))
   row.append(v)
  pix.append(row)
 return pix
W=4*8*12; H=len(starts)*8*12
im=Image.new('RGB',(W,H),'black'); dr=ImageDraw.Draw(im)
for r,s in enumerate(starts):
 for i in range(12):
  t=tile(s+i*32); ox=i*96; oy=r*96
  for y in range(8):
   for x in range(8):
    v=t[y][x]; c=(255,255,255) if v else (0,0,0)
    dr.rectangle((ox+x*12,oy+y*12,ox+x*12+11,oy+y*12+11),fill=c)
 dr.text((0,r*96+80),f'offset {s+i*32:#x}',fill=(255,255,0))
im.save('/home/ubuntu/work/kujakuou_direct/build/font_candidates.png')
