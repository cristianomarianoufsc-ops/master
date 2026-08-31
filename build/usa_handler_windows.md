# Dialogue resolver windows

count=15

## candidate 1 pc=0x5C24 line=3881

5C18: 5c         ld e, h
5C19: 5f         ld e, a
5C1A: 5c         ld e, h
5C1B: 9f         sbc a, a
5C1C: 5c         ld e, h
5C1D: d45cd4     call nc, 0xd45c
5C20: 5c         ld e, h
5C21: 1155af     ld de, 0xaf55
5C24: cdeb5b     call 0x5beb
5C27: ed5323c2   ld (0xc223), de
5C2B: ed5338c2   ld (0xc238), de
5C2F: 2100c2     ld hl, 0xc200
5C32: cbfe       set 0x7, (hl)
5C34: 2142c2     ld hl, 0xc242
5C37: 34         inc (hl)
5C38: c9         ret
5C39: 3a22c2     ld a, (0xc222)

## candidate 2 pc=0x5C4D line=3898

5C3C: feff       cp 0xff
5C3E: 2805       jr z, 0x5c45
5C40: 2142c2     ld hl, 0xc242
5C43: 34         inc (hl)
5C44: c9         ret
5C45: 2100c2     ld hl, 0xc200
5C48: cb86       res 0x0, (hl)
5C4A: 1124b1     ld de, 0xb124
5C4D: cdeb5b     call 0x5beb
5C50: eb         ex de, hl
5C51: cdd75b     call 0x5bd7
5C54: 2206c2     ld (0xc206), hl
5C57: af         xor a
5C58: 3241c2     ld (0xc241), a
5C5B: 3242c2     ld (0xc242), a
5C5E: c9         ret
5C5F: 3e04       ld a, 0x4

## candidate 3 pc=0x5CA2 line=3936

5C8E: af         xor a
5C8F: 32a0c3     ld (0xc3a0), a
5C92: 32a7c3     ld (0xc3a7), a
5C95: 32c0c3     ld (0xc3c0), a
5C98: 3242c2     ld (0xc242), a
5C9B: 3241c2     ld (0xc241), a
5C9E: c9         ret
5C9F: 1128b2     ld de, 0xb228
5CA2: cdeb5b     call 0x5beb
5CA5: d5         push de
5CA6: 2ab5c3     ld hl, (0xc3b5)
5CA9: 2600       ld h, 0x0
5CAB: 1126c2     ld de, 0xc226
5CAE: 19         add hl, de
5CAF: 6e         ld l, (hl)
5CB0: 2600       ld h, 0x0
5CB2: 29         add hl, hl

## candidate 4 pc=0x5CF7 line=3981

5CED: 5d         ld e, l
5CEE: 33         inc sp
5CEF: 5d         ld e, l
5CF0: 66         ld h, (hl)
5CF1: 5d         ld e, l
5CF2: 8d         adc a, l
5CF3: 5d         ld e, l
5CF4: 11eab9     ld de, 0xb9ea
5CF7: cdeb5b     call 0x5beb
5CFA: ed5323c2   ld (0xc223), de
5CFE: 2100c2     ld hl, 0xc200
5D01: cbfe       set 0x7, (hl)
5D03: 2142c2     ld hl, 0xc242
5D06: 34         inc (hl)
5D07: c9         ret
5D08: 3a22c2     ld a, (0xc222)
5D0B: feff       cp 0xff

## candidate 5 pc=0x5D21 line=3999

5D0F: 3e04       ld a, 0x4
5D11: 32a0c3     ld (0xc3a0), a
5D14: 2142c2     ld hl, 0xc242
5D17: 34         inc (hl)
5D18: c9         ret
5D19: 2100c2     ld hl, 0xc200
5D1C: cb86       res 0x0, (hl)
5D1E: 11b5ba     ld de, 0xbab5
5D21: cdeb5b     call 0x5beb
5D24: eb         ex de, hl
5D25: cdd75b     call 0x5bd7
5D28: 2206c2     ld (0xc206), hl
5D2B: af         xor a
5D2C: 3241c2     ld (0xc241), a
5D2F: 3242c2     ld (0xc242), a
5D32: c9         ret
5D33: 3a05c0     ld a, (0xc005)

## candidate 6 pc=0x5D69 line=4031

5D56: cbf6       set 0x6, (hl)
5D58: af         xor a
5D59: 32a0c3     ld (0xc3a0), a
5D5C: 32a7c3     ld (0xc3a7), a
5D5F: 3242c2     ld (0xc242), a
5D62: 3241c2     ld (0xc241), a
5D65: c9         ret
5D66: 1155bd     ld de, 0xbd55
5D69: cdeb5b     call 0x5beb
5D6C: 3ab5c3     ld a, (0xc3b5)
5D6F: cdf65b     call 0x5bf6
5D72: cdd75b     call 0x5bd7
5D75: 2206c2     ld (0xc206), hl
5D78: 2100c2     ld hl, 0xc200
5D7B: cb86       res 0x0, (hl)
5D7D: cbe6       set 0x4, (hl)
5D7F: 210800     ld hl, 0x8

## candidate 7 pc=0x5E13 line=4110

5E02: fe02       cp 0x2
5E04: 283f       jr z, 0x5e45
5E06: 3e03       ld a, 0x3
5E08: 3280c3     ld (0xc380), a
5E0B: 2142c2     ld hl, 0xc242
5E0E: 34         inc (hl)
5E0F: c9         ret
5E10: 113c68     ld de, 0x683c
5E13: cdeb5b     call 0x5beb
5E16: eb         ex de, hl
5E17: cdd75b     call 0x5bd7
5E1A: 2206c2     ld (0xc206), hl
5E1D: 2100c2     ld hl, 0xc200
5E20: cb86       res 0x0, (hl)
5E22: cbe6       set 0x4, (hl)
5E24: 210800     ld hl, 0x8
5E27: 2218c2     ld (0xc218), hl

## candidate 8 pc=0x5EA4 line=4176

5E91: cd0463     call 0x6304
5E94: 3e00       ld a, 0x0
5E96: 3803       jr c, 0x5e9b
5E98: fd7e16     ld a, (iy + 0x16)
5E9B: f5         push af
5E9C: 3e16       ld a, 0x16
5E9E: 32ffff     ld (0xffff), a
5EA1: 11306a     ld de, 0x6a30
5EA4: cdeb5b     call 0x5beb
5EA7: f1         pop af
5EA8: cdf65b     call 0x5bf6
5EAB: cdd75b     call 0x5bd7
5EAE: 2206c2     ld (0xc206), hl
5EB1: 2100c2     ld hl, 0xc200
5EB4: cb86       res 0x0, (hl)
5EB6: cbe6       set 0x4, (hl)
5EB8: 210800     ld hl, 0x8

## candidate 9 pc=0x6045 line=4461

603B: 60         ld h, b
603C: 88         adc a, b
603D: 60         ld h, b
603E: c5         push bc
603F: 60         ld h, b
6040: f5         push af
6041: 60         ld h, b
6042: 11086e     ld de, 0x6e08
6045: cdeb5b     call 0x5beb
6048: ed5323c2   ld (0xc223), de
604C: ed5338c2   ld (0xc238), de
6050: 2100c2     ld hl, 0xc200
6053: cbfe       set 0x7, (hl)
6055: 2142c2     ld hl, 0xc242
6058: 34         inc (hl)
6059: c9         ret
605A: 3a22c2     ld a, (0xc222)

## candidate 10 pc=0x6069 line=4476

6059: c9         ret
605A: 3a22c2     ld a, (0xc222)
605D: feff       cp 0xff
605F: 2805       jr z, 0x6066
6061: 2142c2     ld hl, 0xc242
6064: 34         inc (hl)
6065: c9         ret
6066: 111c6f     ld de, 0x6f1c
6069: cdeb5b     call 0x5beb
606C: eb         ex de, hl
606D: cdd75b     call 0x5bd7
6070: 2206c2     ld (0xc206), hl
6073: 2100c2     ld hl, 0xc200
6076: cb86       res 0x0, (hl)
6078: cbe6       set 0x4, (hl)
607A: 210800     ld hl, 0x8
607D: 2218c2     ld (0xc218), hl

## candidate 11 pc=0x60C8 line=4518

60B5: cbf6       set 0x6, (hl)
60B7: af         xor a
60B8: 32a0c3     ld (0xc3a0), a
60BB: 32a7c3     ld (0xc3a7), a
60BE: 3242c2     ld (0xc242), a
60C1: 3241c2     ld (0xc241), a
60C4: c9         ret
60C5: 11a870     ld de, 0x70a8
60C8: cdeb5b     call 0x5beb
60CB: d5         push de
60CC: 2ab5c3     ld hl, (0xc3b5)
60CF: 2600       ld h, 0x0
60D1: 1126c2     ld de, 0xc226
60D4: 19         add hl, de
60D5: 7e         ld a, (hl)
60D6: d1         pop de
60D7: cdf65b     call 0x5bf6

## candidate 12 pc=0x61AA line=4623

6197: cbf6       set 0x6, (hl)
6199: af         xor a
619A: 32a0c3     ld (0xc3a0), a
619D: 32a7c3     ld (0xc3a7), a
61A0: 3242c2     ld (0xc242), a
61A3: 3241c2     ld (0xc241), a
61A6: c9         ret
61A7: 110e72     ld de, 0x720e
61AA: cdeb5b     call 0x5beb
61AD: d5         push de
61AE: 2ab5c3     ld hl, (0xc3b5)
61B1: 2600       ld h, 0x0
61B3: 1126c2     ld de, 0xc226
61B6: 19         add hl, de
61B7: 7e         ld a, (hl)
61B8: d1         pop de
61B9: cdf65b     call 0x5bf6

## candidate 13 pc=0x62A7 line=4759

6297: 21f262     ld hl, 0x62f2
629A: 19         add hl, de
629B: 5e         ld e, (hl)
629C: 2a27c0     ld hl, (0xc027)
629F: b7         or a
62A0: ed52       sbc hl, de
62A2: 3827       jr c, 0x62cb
62A4: 117278     ld de, 0x7872
62A7: cdeb5b     call 0x5beb
62AA: 3a43c2     ld a, (0xc243)
62AD: cdf65b     call 0x5bf6
62B0: cdd75b     call 0x5bd7
62B3: 2206c2     ld (0xc206), hl
62B6: 2100c2     ld hl, 0xc200
62B9: cb86       res 0x0, (hl)
62BB: cbe6       set 0x4, (hl)
62BD: 210800     ld hl, 0x8

## candidate 14 pc=0x6323 line=4825

6312: d0         ret nc
6313: 112000     ld de, 0x20
6316: fd19       add iy, de
6318: 10f5       djnz 0x630f
631A: 37         scf
631B: c9         ret
631C: fd2160c4   ld iy, 0xc460
6320: 110366     ld de, 0x6603
6323: cdeb5b     call 0x5beb
6326: eb         ex de, hl
6327: 7e         ld a, (hl)
6328: b7         or a
6329: c8         ret z
632A: 47         ld b, a
632B: 23         inc hl
632C: 7e         ld a, (hl)
632D: 23         inc hl

## candidate 15 pc=0x6371 line=4871

6362: fd19       add iy, de
6364: 10c6       djnz 0x632c
6366: c9         ret
6367: 110500     ld de, 0x5
636A: 19         add hl, de
636B: 10bf       djnz 0x632c
636D: c9         ret
636E: 116364     ld de, 0x6463
6371: cdeb5b     call 0x5beb
6374: eb         ex de, hl
6375: 7e         ld a, (hl)
6376: b7         or a
6377: c8         ret z
6378: 47         ld b, a
6379: 23         inc hl
637A: c5         push bc
637B: 5e         ld e, (hl)
