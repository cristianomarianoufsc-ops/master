from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
raw=Path('/home/ubuntu/work/kujakuou_direct/build/interleaved_981d/patterns.vram').read_bytes()
scale=3; cell=8*scale; cols=16; rows=(len(raw)//32+cols-1)//cols
im=Image.new('RGB',(cols*cell,rows*cell),'black'); d=ImageDraw.Draw(im)
for i in range(len(raw)//32):
 off=i*32
 for y in range(8):
  for x in range(8):
   bit=7-x; v=sum(((raw[off+y*4+p]>>bit)&1)<<p for p in range(4)); c=(v*17,)*3
   for yy in range(scale):
    for xx in range(scale): im.putpixel(((i%cols)*cell+x*scale+xx,(i//cols)*cell+y*scale+yy),c)
 d.rectangle(((i%cols)*cell,(i//cols)*cell,(i%cols)*cell+11,(i//cols)*cell+8),fill=(0,0,0))
 d.text(((i%cols)*cell,(i//cols)*cell),f'{i:02X}',fill='red')
im.save('/home/ubuntu/work/kujakuou_direct/build/font_981d_labeled.png')
print('tiles',len(raw)//32)
