from pathlib import Path
import json
rom=Path('/home/ubuntu/work/kujakuou_direct/work/kujaku_ou_jp_original.sms').read_bytes()
base=19*0x4000+(0xACE8-0x8000)
rows=[]
for i in range(64):
 b=rom[base+i*6:base+i*6+6]
 if len(b)<6: break
 src=b[0]|b[1]<<8; p2=b[2]|b[3]<<8; ram=b[4]|b[5]<<8
 rows.append({'index':i,'file_offset':base+i*6,'word0':hex(src),'word1':hex(p2),'ram_target':hex(ram),'raw':b.hex()})
Path('/home/ubuntu/work/kujakuou_direct/build/event_records.json').write_text(json.dumps(rows,indent=2))
print(json.dumps(rows[:20],indent=2))
