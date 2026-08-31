# Dialogue resolver windows

count=15

## candidate 1 pc=0x5C4F line=3916

5C43: 5c         ld e, h
5C44: 8a         adc a, d
5C45: 5c         ld e, h
5C46: ca5cff     jp z, 0xff5c
5C49: 5c         ld e, h
5C4A: ff         rst 0x38
5C4B: 5c         ld e, h
5C4C: 1155af     ld de, 0xaf55
5C4F: cd165c     call 0x5c16
5C52: ed5323c2   ld (0xc223), de
5C56: ed5338c2   ld (0xc238), de
5C5A: 2100c2     ld hl, 0xc200
5C5D: cbfe       set 0x7, (hl)
5C5F: 2142c2     ld hl, 0xc242
5C62: 34         inc (hl)
5C63: c9         ret
5C64: 3a22c2     ld a, (0xc222)

## candidate 2 pc=0x5C78 line=3933

5C67: feff       cp 0xff
5C69: 2805       jr z, 0x5c70
5C6B: 2142c2     ld hl, 0xc242
5C6E: 34         inc (hl)
5C6F: c9         ret
5C70: 2100c2     ld hl, 0xc200
5C73: cb86       res 0x0, (hl)
5C75: 1124b1     ld de, 0xb124
5C78: cd165c     call 0x5c16
5C7B: eb         ex de, hl
5C7C: cd025c     call 0x5c02
5C7F: 2206c2     ld (0xc206), hl
5C82: af         xor a
5C83: 3241c2     ld (0xc241), a
5C86: 3242c2     ld (0xc242), a
5C89: c9         ret
5C8A: 3e04       ld a, 0x4

## candidate 3 pc=0x5CCD line=3971

5CB9: af         xor a
5CBA: 32a0c3     ld (0xc3a0), a
5CBD: 32a7c3     ld (0xc3a7), a
5CC0: 32c0c3     ld (0xc3c0), a
5CC3: 3242c2     ld (0xc242), a
5CC6: 3241c2     ld (0xc241), a
5CC9: c9         ret
5CCA: 1128b2     ld de, 0xb228
5CCD: cd165c     call 0x5c16
5CD0: d5         push de
5CD1: 2ab5c3     ld hl, (0xc3b5)
5CD4: 2600       ld h, 0x0
5CD6: 1126c2     ld de, 0xc226
5CD9: 19         add hl, de
5CDA: 6e         ld l, (hl)
5CDB: 2600       ld h, 0x0
5CDD: 29         add hl, hl

## candidate 4 pc=0x5D22 line=4018

5D18: 5d         ld e, l
5D19: 5e         ld e, (hl)
5D1A: 5d         ld e, l
5D1B: 91         sub c
5D1C: 5d         ld e, l
5D1D: b8         cp b
5D1E: 5d         ld e, l
5D1F: 11eab9     ld de, 0xb9ea
5D22: cd165c     call 0x5c16
5D25: ed5323c2   ld (0xc223), de
5D29: 2100c2     ld hl, 0xc200
5D2C: cbfe       set 0x7, (hl)
5D2E: 2142c2     ld hl, 0xc242
5D31: 34         inc (hl)
5D32: c9         ret
5D33: 3a22c2     ld a, (0xc222)
5D36: feff       cp 0xff

## candidate 5 pc=0x5D4C line=4036

5D3A: 3e04       ld a, 0x4
5D3C: 32a0c3     ld (0xc3a0), a
5D3F: 2142c2     ld hl, 0xc242
5D42: 34         inc (hl)
5D43: c9         ret
5D44: 2100c2     ld hl, 0xc200
5D47: cb86       res 0x0, (hl)
5D49: 11b5ba     ld de, 0xbab5
5D4C: cd165c     call 0x5c16
5D4F: eb         ex de, hl
5D50: cd025c     call 0x5c02
5D53: 2206c2     ld (0xc206), hl
5D56: af         xor a
5D57: 3241c2     ld (0xc241), a
5D5A: 3242c2     ld (0xc242), a
5D5D: c9         ret
5D5E: 3a05c0     ld a, (0xc005)

## candidate 6 pc=0x5D94 line=4068

5D81: cbf6       set 0x6, (hl)
5D83: af         xor a
5D84: 32a0c3     ld (0xc3a0), a
5D87: 32a7c3     ld (0xc3a7), a
5D8A: 3242c2     ld (0xc242), a
5D8D: 3241c2     ld (0xc241), a
5D90: c9         ret
5D91: 1155bd     ld de, 0xbd55
5D94: cd165c     call 0x5c16
5D97: 3ab5c3     ld a, (0xc3b5)
5D9A: cd215c     call 0x5c21
5D9D: cd025c     call 0x5c02
5DA0: 2206c2     ld (0xc206), hl
5DA3: 2100c2     ld hl, 0xc200
5DA6: cb86       res 0x0, (hl)
5DA8: cbe6       set 0x4, (hl)
5DAA: 210800     ld hl, 0x8

## candidate 7 pc=0x5E3E line=4149

5E2D: fe02       cp 0x2
5E2F: 283f       jr z, 0x5e70
5E31: 3e03       ld a, 0x3
5E33: 3280c3     ld (0xc380), a
5E36: 2142c2     ld hl, 0xc242
5E39: 34         inc (hl)
5E3A: c9         ret
5E3B: 116768     ld de, 0x6867
5E3E: cd165c     call 0x5c16
5E41: eb         ex de, hl
5E42: cd025c     call 0x5c02
5E45: 2206c2     ld (0xc206), hl
5E48: 2100c2     ld hl, 0xc200
5E4B: cb86       res 0x0, (hl)
5E4D: cbe6       set 0x4, (hl)
5E4F: 210800     ld hl, 0x8
5E52: 2218c2     ld (0xc218), hl

## candidate 8 pc=0x5ECF line=4215

5EBC: cd2f63     call 0x632f
5EBF: 3e00       ld a, 0x0
5EC1: 3803       jr c, 0x5ec6
5EC3: fd7e16     ld a, (iy + 0x16)
5EC6: f5         push af
5EC7: 3e16       ld a, 0x16
5EC9: 32ffff     ld (0xffff), a
5ECC: 115b6a     ld de, 0x6a5b
5ECF: cd165c     call 0x5c16
5ED2: f1         pop af
5ED3: cd215c     call 0x5c21
5ED6: cd025c     call 0x5c02
5ED9: 2206c2     ld (0xc206), hl
5EDC: 2100c2     ld hl, 0xc200
5EDF: cb86       res 0x0, (hl)
5EE1: cbe6       set 0x4, (hl)
5EE3: 210800     ld hl, 0x8

## candidate 9 pc=0x6070 line=4499

6065: 85         add a, l
6066: 60         ld h, b
6067: b3         or e
6068: 60         ld h, b
6069: f0         ret p
606A: 60         ld h, b
606B: 2061       jr nz, 0x60ce
606D: 11336e     ld de, 0x6e33
6070: cd165c     call 0x5c16
6073: ed5323c2   ld (0xc223), de
6077: ed5338c2   ld (0xc238), de
607B: 2100c2     ld hl, 0xc200
607E: cbfe       set 0x7, (hl)
6080: 2142c2     ld hl, 0xc242
6083: 34         inc (hl)
6084: c9         ret
6085: 3a22c2     ld a, (0xc222)

## candidate 10 pc=0x6094 line=4514

6084: c9         ret
6085: 3a22c2     ld a, (0xc222)
6088: feff       cp 0xff
608A: 2805       jr z, 0x6091
608C: 2142c2     ld hl, 0xc242
608F: 34         inc (hl)
6090: c9         ret
6091: 11476f     ld de, 0x6f47
6094: cd165c     call 0x5c16
6097: eb         ex de, hl
6098: cd025c     call 0x5c02
609B: 2206c2     ld (0xc206), hl
609E: 2100c2     ld hl, 0xc200
60A1: cb86       res 0x0, (hl)
60A3: cbe6       set 0x4, (hl)
60A5: 210800     ld hl, 0x8
60A8: 2218c2     ld (0xc218), hl

## candidate 11 pc=0x60F3 line=4556

60E0: cbf6       set 0x6, (hl)
60E2: af         xor a
60E3: 32a0c3     ld (0xc3a0), a
60E6: 32a7c3     ld (0xc3a7), a
60E9: 3242c2     ld (0xc242), a
60EC: 3241c2     ld (0xc241), a
60EF: c9         ret
60F0: 11d370     ld de, 0x70d3
60F3: cd165c     call 0x5c16
60F6: d5         push de
60F7: 2ab5c3     ld hl, (0xc3b5)
60FA: 2600       ld h, 0x0
60FC: 1126c2     ld de, 0xc226
60FF: 19         add hl, de
6100: 7e         ld a, (hl)
6101: d1         pop de
6102: cd215c     call 0x5c21

## candidate 12 pc=0x61D5 line=4659

61C2: cbf6       set 0x6, (hl)
61C4: af         xor a
61C5: 32a0c3     ld (0xc3a0), a
61C8: 32a7c3     ld (0xc3a7), a
61CB: 3242c2     ld (0xc242), a
61CE: 3241c2     ld (0xc241), a
61D1: c9         ret
61D2: 113972     ld de, 0x7239
61D5: cd165c     call 0x5c16
61D8: d5         push de
61D9: 2ab5c3     ld hl, (0xc3b5)
61DC: 2600       ld h, 0x0
61DE: 1126c2     ld de, 0xc226
61E1: 19         add hl, de
61E2: 7e         ld a, (hl)
61E3: d1         pop de
61E4: cd215c     call 0x5c21

## candidate 13 pc=0x62D2 line=4798

62C2: 211d63     ld hl, 0x631d
62C5: 19         add hl, de
62C6: 5e         ld e, (hl)
62C7: 2a27c0     ld hl, (0xc027)
62CA: b7         or a
62CB: ed52       sbc hl, de
62CD: 3827       jr c, 0x62f6
62CF: 119d78     ld de, 0x789d
62D2: cd165c     call 0x5c16
62D5: 3a43c2     ld a, (0xc243)
62D8: cd215c     call 0x5c21
62DB: cd025c     call 0x5c02
62DE: 2206c2     ld (0xc206), hl
62E1: 2100c2     ld hl, 0xc200
62E4: cb86       res 0x0, (hl)
62E6: cbe6       set 0x4, (hl)
62E8: 210800     ld hl, 0x8

## candidate 14 pc=0x634E line=4864

633D: d0         ret nc
633E: 112000     ld de, 0x20
6341: fd19       add iy, de
6343: 10f5       djnz 0x633a
6345: 37         scf
6346: c9         ret
6347: fd2160c4   ld iy, 0xc460
634B: 112e66     ld de, 0x662e
634E: cd165c     call 0x5c16
6351: eb         ex de, hl
6352: 7e         ld a, (hl)
6353: b7         or a
6354: c8         ret z
6355: 47         ld b, a
6356: 23         inc hl
6357: 7e         ld a, (hl)
6358: 23         inc hl

## candidate 15 pc=0x639C line=4910

638D: fd19       add iy, de
638F: 10c6       djnz 0x6357
6391: c9         ret
6392: 110500     ld de, 0x5
6395: 19         add hl, de
6396: 10bf       djnz 0x6357
6398: c9         ret
6399: 118e64     ld de, 0x648e
639C: cd165c     call 0x5c16
639F: eb         ex de, hl
63A0: 7e         ld a, (hl)
63A1: b7         or a
63A2: c8         ret z
63A3: 47         ld b, a
63A4: 23         inc hl
63A5: c5         push bc
63A6: 5e         ld e, (hl)
