# IX+18 dispatch candidates

The fixed-bank dispatcher at 3954 loads IX+18, calls RST 10h, and jumps through HL.

## 1. line 792: ld (ix+018h),a		;0632	dd 77 18 	. w .
    jr nz,sub_0649h		;062b	20 1c 	  .
    bit 1,c		;062d	cb 49 	. I
    ret z			;062f	c8 	.
    ld a,001h		;0630	3e 01 	> .
    ld (ix+018h),a		;0632	dd 77 18 	. w .
    ld a,(ix+004h)		;0635	dd 7e 04 	. ~ .
    cp 0b0h		;0638	fe b0 	. .
    ret z			;063a	c8 	.
    ld a,010h		;063b	3e 10 	> .
    add a,(ix+004h)		;063d	dd 86 04 	. . .
    ld (ix+004h),a		;0640	dd 77 04 	. w .

## 2. line 804: ld (ix+018h),a		;064a	dd 77 18 	. w .
    ld (0dd04h),a		;0645	32 04 dd 	2 . .
    ret			;0648	c9 	.
    sub_0649h:
    xor a			;0649	af 	.
    ld (ix+018h),a		;064a	dd 77 18 	. w .
    ld a,(ix+004h)		;064d	dd 7e 04 	. ~ .
    cp 0a0h		;0650	fe a0 	. .
    ret z			;0652	c8 	.
    ld a,(ix+004h)		;0653	dd 7e 04 	. ~ .
    sub 010h		;0656	d6 10 	. .
    ld (ix+004h),a		;0658	dd 77 04 	. w .

## 3. line 1505: ld (ix+018h),001h		;0afa	dd 36 18 01 	. 6 . .
    ld a,(0c304h)		;0af1	3a 04 c3 	: . .
    add a,008h		;0af4	c6 08 	. .
    cp (ix+004h)		;0af6	dd be 04 	. . .
    ret nc			;0af9	d0 	.
    ld (ix+018h),001h		;0afa	dd 36 18 01 	. 6 . .
    ld (ix+010h),000h		;0afe	dd 36 10 00 	. 6 . .
    ret			;0b02	c9 	.
    ret			;0b03	c9 	.
    bit 0,(ix+007h)		;0b04	dd cb 07 46 	. . . F
    jr nz,l0b33h		;0b08	20 29 	  )
    ld hl,04b10h		;0b0a	21 10 4b 	! . K

## 4. line 1551: ld (ix+018h),a		;0b7a	dd 77 18 	. w .
    ld hl,09550h		;0b6d	21 50 95 	! P .
    call 03931h		;0b70	cd 31 39 	. 1 9
    ld (ix+00ah),004h		;0b73	dd 36 0a 04 	. 6 . .
    ld a,(ix+017h)		;0b77	dd 7e 17 	. ~ .
    ld (ix+018h),a		;0b7a	dd 77 18 	. w .
    ld a,002h		;0b7d	3e 02 	> .
    jp 03a3fh		;0b7f	c3 3f 3a 	. ? :
    l0b82h:
    ld hl,04b88h		;0b82	21 88 4b 	! . K
    jp 038d6h		;0b85	c3 d6 38 	. . 8
    ld de,l1a00h+1		;0b88	11 01 1a 	. . .

## 5. line 1587: ld (ix+018h),d		;0bd4	dd 72 18 	. r .
    sub_0bcdh:
    ld bc,0d030h		;0bcd	01 30 d0 	. 0 .
    call sub_3a69h		;0bd0	cd 69 3a 	. i :
    ret nc			;0bd3	d0 	.
    ld (ix+018h),d		;0bd4	dd 72 18 	. r .
    xor a			;0bd7	af 	.
    ld bc,l0107h+1		;0bd8	01 08 01 	. . .
    jp l3ac4h		;0bdb	c3 c4 3a 	. . :
    ld hl,04c65h		;0bde	21 65 4c 	! e L
    call sub_3aaah		;0be1	cd aa 3a 	. . :
    call 03759h		;0be4	cd 59 37 	. Y 7

## 6. line 1596: ld (ix+018h),000h		;0be8	dd 36 18 00 	. 6 . .
    call sub_3aaah		;0be1	cd aa 3a 	. . :
    call 03759h		;0be4	cd 59 37 	. Y 7
    ret c			;0be7	d8 	.
    l0be8h:
    ld (ix+018h),000h		;0be8	dd 36 18 00 	. 6 . .
    xor a			;0bec	af 	.
    ld bc,l0102h+2		;0bed	01 04 01 	. . .
    jp l3ac4h		;0bf0	c3 c4 3a 	. . :
    l0bf3h:
    ld (ix+010h),0fch		;0bf3	dd 36 10 fc 	. 6 . .
    l0bf7h:

## 7. line 1603: ld (ix+018h),003h		;0bf7	dd 36 18 03 	. 6 . .
    jp l3ac4h		;0bf0	c3 c4 3a 	. . :
    l0bf3h:
    ld (ix+010h),0fch		;0bf3	dd 36 10 fc 	. 6 . .
    l0bf7h:
    ld (ix+018h),003h		;0bf7	dd 36 18 03 	. 6 . .
    ld hl,04c6dh		;0bfb	21 6d 4c 	! m L
    call sub_3aaah		;0bfe	cd aa 3a 	. . :
    jp 03931h		;0c01	c3 31 39 	. 1 9
    ld d,004h		;0c04	16 04 	. .
    call 04bcdh		;0c06	cd cd 4b 	. . K
    l0c09h:

## 8. line 1624: ld (ix+018h),002h		;0c26	dd 36 18 02 	. 6 . .
    call sub_3aceh		;0c1d	cd ce 3a 	. . :
    ld a,(ix+017h)		;0c20	dd 7e 17 	. ~ .
    or a			;0c23	b7 	.
    jr z,l0be8h		;0c24	28 c2 	( .
    ld (ix+018h),002h		;0c26	dd 36 18 02 	. 6 . .
    jp 04bech		;0c2a	c3 ec 4b 	. . K
    ld hl,04c69h		;0c2d	21 69 4c 	! i L
    l0c30h:
    call sub_3aaah		;0c30	cd aa 3a 	. . :
    call 03759h		;0c33	cd 59 37 	. Y 7
    jr c,l0c09h		;0c36	38 d1 	8 .

## 9. line 1631: ld (ix+018h),003h		;0c38	dd 36 18 03 	. 6 . .
    l0c30h:
    call sub_3aaah		;0c30	cd aa 3a 	. . :
    call 03759h		;0c33	cd 59 37 	. Y 7
    jr c,l0c09h		;0c36	38 d1 	8 .
    ld (ix+018h),003h		;0c38	dd 36 18 03 	. 6 . .
    call 04bech		;0c3c	cd ec 4b 	. . K
    jp 04c09h		;0c3f	c3 09 4c 	. . L
    ld bc,0a050h		;0c42	01 50 a0 	. P .
    call sub_3a69h		;0c45	cd 69 3a 	. i :
    jp c,04bf3h		;0c48	da f3 4b 	. . K
    ld bc,0e008h		;0c4b	01 08 e0 	. . .

## 10. line 1691: ld (ix+018h),001h		;0cb9	dd 36 18 01 	. 6 . .
    jp 03954h		;0cae	c3 54 39 	. T 9
    dec (ix+019h)		;0cb1	dd 35 19 	. 5 .
    ret nz			;0cb4	c0 	.
    ld (ix+019h),030h		;0cb5	dd 36 19 30 	. 6 . 0
    ld (ix+018h),001h		;0cb9	dd 36 18 01 	. 6 . .
    xor a			;0cbd	af 	.
    ld bc,00404h		;0cbe	01 04 04 	. . .
    jp l3ac4h		;0cc1	c3 c4 3a 	. . :
    ld hl,04d18h		;0cc4	21 18 4d 	! . M
    call 03aa1h		;0cc7	cd a1 3a 	. . :
    call sub_3731h		;0cca	cd 31 37 	. 1 7

## 11. line 1703: ld (ix+018h),000h		;0cd7	dd 36 18 00 	. 6 . .
    cp 001h		;0cd0	fe 01 	. .
    jr z,l0ce4h		;0cd2	28 10 	( .
    cp 002h		;0cd4	fe 02 	. .
    ret nz			;0cd6	c0 	.
    ld (ix+018h),000h		;0cd7	dd 36 18 00 	. 6 . .
    ld hl,04d14h		;0cdb	21 14 4d 	! . M
    call 03aa1h		;0cde	cd a1 3a 	. . :
    jp 03931h		;0ce1	c3 31 39 	. 1 9
    l0ce4h:
    ld a,(ix+009h)		;0ce4	dd 7e 09 	. ~ .
    cp 003h		;0ce7	fe 03 	. .

## 12. line 1800: ld (ix+018h),001h		;0da9	dd 36 18 01 	. 6 . .
    ld c,003h		;0d9e	0e 03 	. .
    call 03a57h		;0da0	cd 57 3a 	. W :
    ld (ix+01ah),a		;0da3	dd 77 1a 	. w .
    ld (ix+010h),b		;0da6	dd 70 10 	. p .
    ld (ix+018h),001h		;0da9	dd 36 18 01 	. 6 . .
    ld hl,097d4h		;0dad	21 d4 97 	! . .
    jp 03931h		;0db0	c3 31 39 	. 1 9
    ld de,l0050h		;0db3	11 50 00 	. P .
    call sub_3946h		;0db6	cd 46 39 	. F 9
    bit 7,h		;0db9	cb 7c 	. |
    ret nz			;0dbb	c0 	.

## 13. line 1812: ld (ix+018h),002h		;0dc7	dd 36 18 02 	. 6 . .
    call 01040h		;0dbf	cd 40 10 	. @ .
    rlca			;0dc2	07 	.
    ret nc			;0dc3	d0 	.
    call sub_3aceh		;0dc4	cd ce 3a 	. . :
    ld (ix+018h),002h		;0dc7	dd 36 18 02 	. 6 . .
    call sub_3af4h		;0dcb	cd f4 3a 	. . :
    xor a			;0dce	af 	.
    ld bc,00106h		;0dcf	01 06 01 	. . .
    jp l3ac4h		;0dd2	c3 c4 3a 	. . :
    call sub_3af4h		;0dd5	cd f4 3a 	. . :
    dec (ix+019h)		;0dd8	dd 35 19 	. 5 .

## 14. line 1869: ld (ix+018h),001h		;0e5d	dd 36 18 01 	. 6 . .
    ld c,(hl)			;0e56	4e 	N
    ld h,d			;0e57	62 	b
    ld c,(hl)			;0e58	4e 	N
    ld (ix+010h),0fdh		;0e59	dd 36 10 fd 	. 6 . .
    ld (ix+018h),001h		;0e5d	dd 36 18 01 	. 6 . .
    ret			;0e61	c9 	.
    dec (ix+019h)		;0e62	dd 35 19 	. 5 .
    call z,04e87h		;0e65	cc 87 4e 	. . N
    ld de,00080h		;0e68	11 80 00 	. . .
    ld a,(ix+004h)		;0e6b	dd 7e 04 	. ~ .
    cp (ix+01ah)		;0e6e	dd be 1a 	. . .

## 15. line 2004: ld (ix+018h),001h		;0f8a	dd 36 18 01 	. 6 . .
    ld c,a			;0f82	4f 	O
    ld hl,09815h		;0f83	21 15 98 	! . .
    call 03759h		;0f86	cd 59 37 	. Y 7
    ret c			;0f89	d8 	.
    ld (ix+018h),001h		;0f8a	dd 36 18 01 	. 6 . .
    ret			;0f8e	c9 	.
    dec (ix+019h)		;0f8f	dd 35 19 	. 5 .
    ret nz			;0f92	c0 	.
    ld (ix+019h),050h		;0f93	dd 36 19 50 	. 6 . P
    ld (ix+018h),002h		;0f97	dd 36 18 02 	. 6 . .
    ld hl,0981eh		;0f9b	21 1e 98 	! . .

## 16. line 2009: ld (ix+018h),002h		;0f97	dd 36 18 02 	. 6 . .
    ret			;0f8e	c9 	.
    dec (ix+019h)		;0f8f	dd 35 19 	. 5 .
    ret nz			;0f92	c0 	.
    ld (ix+019h),050h		;0f93	dd 36 19 50 	. 6 . P
    ld (ix+018h),002h		;0f97	dd 36 18 02 	. 6 . .
    ld hl,0981eh		;0f9b	21 1e 98 	! . .
    call 03931h		;0f9e	cd 31 39 	. 1 9
    ld bc,04fceh		;0fa1	01 ce 4f 	. . O
    ld a,(0c022h)		;0fa4	3a 22 c0 	: " .
    cp 004h		;0fa7	fe 04 	. .
    ld de,l0200h		;0fa9	11 00 02 	. . .

## 17. line 2027: ld (ix+018h),001h		;0fc6	dd 36 18 01 	. 6 . .
    jp 04ea5h		;0fbb	c3 a5 4e 	. . N
    dec (ix+01ah)		;0fbe	dd 35 1a 	. 5 .
    ret nz			;0fc1	c0 	.
    ld (ix+01ah),005h		;0fc2	dd 36 1a 05 	. 6 . .
    ld (ix+018h),001h		;0fc6	dd 36 18 01 	. 6 . .
    ld hl,09832h		;0fca	21 32 98 	! 2 .
    jp 03931h		;0fcd	c3 31 39 	. 1 9
    call m,0fcfeh		;0fd0	fc fe fc 	. . .
    rst 38h			;0fd3	ff 	.
    call m,0fc00h		;0fd4	fc 00 fc 	. . .
    ld bc,002fch		;0fd7	01 fc 02 	. . .

## 18. line 2170: ld (ix+018h),001h		;111c	dd 36 18 01 	. 6 . .
    ld hl,05180h		;1113	21 80 51 	! . Q
    call 03abah		;1116	cd ba 3a 	. . :
    jp sub_3731h		;1119	c3 31 37 	. 1 7
    l111ch:
    ld (ix+018h),001h		;111c	dd 36 18 01 	. 6 . .
    ld (ix+010h),0fbh		;1120	dd 36 10 fb 	. 6 . .
    ret			;1124	c9 	.
    ld a,(ix+017h)		;1125	dd 7e 17 	. ~ .
    ld hl,051aah		;1128	21 aa 51 	! . Q
    call 03abah		;112b	cd ba 3a 	. . :
    ex de,hl			;112e	eb 	.

## 19. line 2209: ld (ix+018h),000h		;1175	dd 36 18 00 	. 6 . .
    ld de,00060h		;116c	11 60 00 	. ` .
    jp sub_3946h		;116f	c3 46 39 	. F 9
    l1172h:
    call sub_3aceh		;1172	cd ce 3a 	. . :
    ld (ix+018h),000h		;1175	dd 36 18 00 	. 6 . .
    xor a			;1179	af 	.
    ld bc,00106h		;117a	01 06 01 	. . .
    jp l3ac4h		;117d	c3 c4 3a 	. . :
    xor l			;1180	ad 	.
    sbc a,b			;1181	98 	.
    add a,(hl)			;1182	86 	.

## 20. line 2357: ld (ix+018h),001h		;1290	dd 36 18 01 	. 6 . .
    ld de,02308h		;1288	11 08 23 	. . #
    call 01040h		;128b	cd 40 10 	. @ .
    rlca			;128e	07 	.
    ret c			;128f	d8 	.
    ld (ix+018h),001h		;1290	dd 36 18 01 	. 6 . .
    ret			;1294	c9 	.
    l1295h:
    ld a,(ix+004h)		;1295	dd 7e 04 	. ~ .
    add a,0f8h		;1298	c6 f8 	. .
    ld (ix+004h),a		;129a	dd 77 04 	. w .
    ret			;129d	c9 	.

## 21. line 2378: ld (ix+018h),001h		;12c9	dd 36 18 01 	. 6 . .
    ld (ix+019h),a		;12bf	dd 77 19 	. w .
    ld a,(ix+017h)		;12c2	dd 7e 17 	. ~ .
    and 0f0h		;12c5	e6 f0 	. .
    jr nz,l12d1h		;12c7	20 08 	  .
    ld (ix+018h),001h		;12c9	dd 36 18 01 	. 6 . .
    ld a,002h		;12cd	3e 02 	> .
    jr l12d7h		;12cf	18 06 	. .
    l12d1h:
    rrca			;12d1	0f 	.
    rrca			;12d2	0f 	.
    rrca			;12d3	0f 	.

## 22. line 2423: ld (ix+018h),000h		;1330	dd 36 18 00 	. 6 . .
    jp sub_3946h		;1325	c3 46 39 	. F 9
    ld bc,0b050h		;1328	01 50 b0 	. P .
    call sub_3a69h		;132b	cd 69 3a 	. i :
    jr nc,l130bh		;132e	30 db 	0 .
    ld (ix+018h),000h		;1330	dd 36 18 00 	. 6 . .
    ld c,004h		;1334	0e 04 	. .
    call 03a57h		;1336	cd 57 3a 	. W :
    jp 0530bh		;1339	c3 0b 53 	. . S
    ld b,e			;133c	43 	C
    sbc a,c			;133d	99 	.
    ld l,099h		;133e	2e 99 	. .

## 23. line 2479: ld (ix+018h),001h		;13af	dd 36 18 01 	. 6 . .
    ld bc,0d030h		;13a4	01 30 d0 	. 0 .
    call sub_3a8fh		;13a7	cd 8f 3a 	. . :
    ret nc			;13aa	d0 	.
    ld (ix+010h),003h		;13ab	dd 36 10 03 	. 6 . .
    ld (ix+018h),001h		;13af	dd 36 18 01 	. 6 . .
    ret			;13b3	c9 	.
    ld de,l1008h		;13b4	11 08 10 	. . .
    call sub_3e26h		;13b7	cd 26 3e 	. & >
    call 01040h		;13ba	cd 40 10 	. @ .
    rlca			;13bd	07 	.
    ret nc			;13be	d0 	.

## 24. line 2487: ld (ix+018h),002h		;13c2	dd 36 18 02 	. 6 . .
    call 01040h		;13ba	cd 40 10 	. @ .
    rlca			;13bd	07 	.
    ret nc			;13be	d0 	.
    call sub_3aceh		;13bf	cd ce 3a 	. . :
    ld (ix+018h),002h		;13c2	dd 36 18 02 	. 6 . .
    ld c,003h		;13c6	0e 03 	. .
    jp 03a57h		;13c8	c3 57 3a 	. W :
    ld (ix+010h),000h		;13cb	dd 36 10 00 	. 6 . .
    ld hl,053f6h		;13cf	21 f6 53 	! . S
    call sub_3aaah		;13d2	cd aa 3a 	. . :
    ex de,hl			;13d5	eb 	.

## 25. line 2502: ld (ix+018h),003h		;13e8	dd 36 18 03 	. 6 . .
    ld de,l1208h		;13e0	11 08 12 	. . .
    call 01040h		;13e3	cd 40 10 	. @ .
    rlca			;13e6	07 	.
    ret c			;13e7	d8 	.
    ld (ix+018h),003h		;13e8	dd 36 18 03 	. 6 . .
    ret			;13ec	c9 	.
    ld de,00040h		;13ed	11 40 00 	. @ .
    call sub_3946h		;13f0	cd 46 39 	. F 9
    jp 0539fh		;13f3	c3 9f 53 	. . S
    djnz $+14		;13f6	10 0c 	. .
    nop			;13f8	00 	.

## 26. line 2590: ld (ix+018h),001h		;14b2	dd 36 18 01 	. 6 . .
    ld d,h			;14ab	54 	T
    cp 054h		;14ac	fe 54 	. T
    dec (ix+019h)		;14ae	dd 35 19 	. 5 .
    ret nz			;14b1	c0 	.
    ld (ix+018h),001h		;14b2	dd 36 18 01 	. 6 . .
    call sub_3af4h		;14b6	cd f4 3a 	. . :
    ld (ix+010h),002h		;14b9	dd 36 10 02 	. 6 . .
    ret			;14bd	c9 	.
    ld de,l1008h		;14be	11 08 10 	. . .
    call sub_3e26h		;14c1	cd 26 3e 	. & >
    call 01040h		;14c4	cd 40 10 	. @ .

## 27. line 2600: ld (ix+018h),002h		;14cc	dd 36 18 02 	. 6 . .
    call 01040h		;14c4	cd 40 10 	. @ .
    rlca			;14c7	07 	.
    ret nc			;14c8	d0 	.
    call sub_3aceh		;14c9	cd ce 3a 	. . :
    ld (ix+018h),002h		;14cc	dd 36 18 02 	. 6 . .
    ret			;14d0	c9 	.
    ld (ix+010h),000h		;14d1	dd 36 10 00 	. 6 . .
    ld bc,0d030h		;14d5	01 30 d0 	. 0 .
    call sub_3a8fh		;14d8	cd 8f 3a 	. . :
    ret nc			;14db	d0 	.
    ld (ix+018h),003h		;14dc	dd 36 18 03 	. 6 . .

## 28. line 2606: ld (ix+018h),003h		;14dc	dd 36 18 03 	. 6 . .
    ld (ix+010h),000h		;14d1	dd 36 10 00 	. 6 . .
    ld bc,0d030h		;14d5	01 30 d0 	. 0 .
    call sub_3a8fh		;14d8	cd 8f 3a 	. . :
    ret nc			;14db	d0 	.
    ld (ix+018h),003h		;14dc	dd 36 18 03 	. 6 . .
    ld hl,09977h		;14e0	21 77 99 	! w .
    call 03931h		;14e3	cd 31 39 	. 1 9
    ld hl,05505h		;14e6	21 05 55 	! . U
    call 03aa1h		;14e9	cd a1 3a 	. . :
    ld de,l0202h		;14ec	11 02 02 	. . .
    exx			;14ef	d9 	.

## 29. line 2726: ld (ix+018h),001h		;15f7	dd 36 18 01 	. 6 . .
    call 05600h		;15eb	cd 00 56 	. . V
    ret nz			;15ee	c0 	.
    ld (ix+01ah),008h		;15ef	dd 36 1a 08 	. 6 . .
    ld (ix+000h),07ch		;15f3	dd 36 00 7c 	. 6 . |
    ld (ix+018h),001h		;15f7	dd 36 18 01 	. 6 . .
    ld (ix+013h),000h		;15fb	dd 36 13 00 	. 6 . .
    ret			;15ff	c9 	.
    inc (ix+019h)		;1600	dd 34 19 	. 4 .
    bit 0,(ix+019h)		;1603	dd cb 19 46 	. . . F
    jr z,l160eh		;1607	28 05 	( .
    ld (ix+013h),001h		;1609	dd 36 13 01 	. 6 . .

## 30. line 2741: ld (ix+018h),003h		;161e	dd 36 18 03 	. 6 . .
    ret			;1615	c9 	.
    call 05600h		;1616	cd 00 56 	. . V
    ret nz			;1619	c0 	.
    ld (ix+01ah),008h		;161a	dd 36 1a 08 	. 6 . .
    ld (ix+018h),003h		;161e	dd 36 18 03 	. 6 . .
    ld (ix+014h),001h		;1622	dd 36 14 01 	. 6 . .
    ld (ix+013h),001h		;1626	dd 36 13 01 	. 6 . .
    ret			;162a	c9 	.
    dec (ix+01ch)		;162b	dd 35 1c 	. 5 .
    ret nz			;162e	c0 	.
    ld (ix+01ch),010h		;162f	dd 36 1c 10 	. 6 . .

## 31. line 2749: ld (ix+018h),000h		;1637	dd 36 18 00 	. 6 . .
    dec (ix+01ch)		;162b	dd 35 1c 	. 5 .
    ret nz			;162e	c0 	.
    ld (ix+01ch),010h		;162f	dd 36 1c 10 	. 6 . .
    ld (ix+014h),000h		;1633	dd 36 14 00 	. 6 . .
    ld (ix+018h),000h		;1637	dd 36 18 00 	. 6 . .
    jp 055a0h		;163b	c3 a0 55 	. . U
    ld (hl),h			;163e	74 	t
    sbc a,d			;163f	9a 	.
    ld (hl),09ah		;1640	36 9a 	6 .
    and b			;1642	a0 	.
    jr nz,$-62		;1643	20 c0 	  .

## 32. line 2775: ld (ix+018h),002h		;166d	dd 36 18 02 	. 6 . .
    ld (ix+013h),000h		;1661	dd 36 13 00 	. 6 . .
    dec (ix+01bh)		;1665	dd 35 1b 	. 5 .
    ret nz			;1668	c0 	.
    ld (ix+01bh),00dh		;1669	dd 36 1b 0d 	. 6 . .
    ld (ix+018h),002h		;166d	dd 36 18 02 	. 6 . .
    ld (ix+000h),07bh		;1671	dd 36 00 7b 	. 6 . {
    ld hl,0569bh		;1675	21 9b 56 	! . V
    call 03aa1h		;1678	cd a1 3a 	. . :
    call 03931h		;167b	cd 31 39 	. 1 9
    ld hl,l0000h		;167e	21 00 00 	! . .
    ld de,00404h		;1681	11 04 04 	. . .

## 33. line 2862: ld (ix+018h),001h		;1739	dd 36 18 01 	. 6 . .
    cp 020h		;1730	fe 20 	.
    ret nz			;1732	c0 	.
    ld a,(ix+002h)		;1733	dd 7e 02 	. ~ .
    ld (ix+01ah),a		;1736	dd 77 1a 	. w .
    ld (ix+018h),001h		;1739	dd 36 18 01 	. 6 . .
    ld a,(ix+00eh)		;173d	dd 7e 0e 	. ~ .
    ld (ix+01ch),a		;1740	dd 77 1c 	. w .
    ld (ix+00eh),000h		;1743	dd 36 0e 00 	. 6 . .
    ld (ix+010h),001h		;1747	dd 36 10 01 	. 6 . .
    ret			;174b	c9 	.
    l174ch:

## 34. line 3080: ld (ix+018h),002h		;18c7	dd 36 18 02 	. 6 . .
    ld a,(ix+017h)		;18bb	dd 7e 17 	. ~ .
    ld hl,058f5h		;18be	21 f5 58 	! . X
    call sub_3e32h		;18c1	cd 32 3e 	. 2 >
    ld (ix+012h),a		;18c4	dd 77 12 	. w .
    ld (ix+018h),002h		;18c7	dd 36 18 02 	. 6 . .
    ld (ix+010h),001h		;18cb	dd 36 10 01 	. 6 . .
    ld (ix+014h),000h		;18cf	dd 36 14 00 	. 6 . .
    ret			;18d3	c9 	.
    ld a,(ix+017h)		;18d4	dd 7e 17 	. ~ .
    ld hl,058fah		;18d7	21 fa 58 	! . X
    call sub_3e32h		;18da	cd 32 3e 	. 2 >

## 35. line 3161: ld (ix+018h),001h		;1987	dd 36 18 01 	. 6 . .
    or (hl)			;1980	b6 	.
    jp nz,0369eh		;1981	c2 9e 36 	. . 6
    add hl,de			;1984	19 	.
    djnz l197fh		;1985	10 f8 	. .
    ld (ix+018h),001h		;1987	dd 36 18 01 	. 6 . .
    ld (ix+000h),081h		;198b	dd 36 00 81 	. 6 . .
    ld (ix+013h),000h		;198f	dd 36 13 00 	. 6 . .
    ld a,0b5h		;1993	3e b5 	> .
    ld (0dd04h),a		;1995	32 04 dd 	2 . .
    bit 0,(ix+017h)		;1998	dd cb 17 46 	. . . F
    ld a,003h		;199c	3e 03 	> .

## 36. line 3339: ld (ix+018h),001h		;1af5	dd 36 18 01 	. 6 . .
    ld a,(ix+019h)		;1aee	dd 7e 19 	. ~ .
    inc a			;1af1	3c 	<
    jp 059fbh		;1af2	c3 fb 59 	. . Y
    l1af5h:
    ld (ix+018h),001h		;1af5	dd 36 18 01 	. 6 . .
    jp sub_3af4h		;1af9	c3 f4 3a 	. . :
    ld hl,05b02h		;1afc	21 02 5b 	! . [
    jp 038d6h		;1aff	c3 d6 38 	. . 8
    ld a,(0c460h)		;1b02	3a 60 c4 	: ` .
    or a			;1b05	b7 	.
    jp z,0369eh		;1b06	ca 9e 36 	. . 6

## 37. line 3378: ld (ix+018h),001h		;1b5c	dd 36 18 01 	. 6 . .
    ld e,e			;1b54	5b 	[
    ld bc,0d030h		;1b55	01 30 d0 	. 0 .
    call sub_3a8fh		;1b58	cd 8f 3a 	. . :
    ret nc			;1b5b	d0 	.
    ld (ix+018h),001h		;1b5c	dd 36 18 01 	. 6 . .
    ret			;1b60	c9 	.
    dec (ix+017h)		;1b61	dd 35 17 	. 5 .
    ret nz			;1b64	c0 	.
    ld a,005h		;1b65	3e 05 	> .
    jp l3a4bh		;1b67	c3 4b 3a 	. K :
    bit 0,(ix+007h)		;1b6a	dd cb 07 46 	. . . F

## 38. line 3453: ld (ix+018h),002h		;1c1f	dd 36 18 02 	. 6 . .
    ld e,h			;1c16	5c 	\
    l1c17h:
    res 6,(ix+007h)		;1c17	dd cb 07 b6 	. . . .
    ld (ix+000h),088h		;1c1b	dd 36 00 88 	. 6 . .
    ld (ix+018h),002h		;1c1f	dd 36 18 02 	. 6 . .
    xor a			;1c23	af 	.
    ld bc,l0102h		;1c24	01 02 01 	. . .
    jp l3ac4h		;1c27	c3 c4 3a 	. . :
    ld bc,0c040h		;1c2a	01 40 c0 	. @ .
    call sub_3a8fh		;1c2d	cd 8f 3a 	. . :
    jr nc,l1c37h		;1c30	30 05 	0 .

## 39. line 3460: ld (ix+018h),001h		;1c32	dd 36 18 01 	. 6 . .
    jp l3ac4h		;1c27	c3 c4 3a 	. . :
    ld bc,0c040h		;1c2a	01 40 c0 	. @ .
    call sub_3a8fh		;1c2d	cd 8f 3a 	. . :
    jr nc,l1c37h		;1c30	30 05 	0 .
    ld (ix+018h),001h		;1c32	dd 36 18 01 	. 6 . .
    ret			;1c36	c9 	.
    l1c37h:
    ld a,(ix+019h)		;1c37	dd 7e 19 	. ~ .
    l1c3ah:
    cp (ix+004h)		;1c3a	dd be 04 	. . .
    ld de,00040h		;1c3d	11 40 00 	. @ .

## 40. line 3499: ld (ix+018h),003h		;1c7a	dd 36 18 03 	. 6 . .
    jr nz,l1c7ah		;1c73	20 05 	  .
    ld a,(0c304h)		;1c75	3a 04 c3 	: . .
    jr l1c3ah		;1c78	18 c0 	. .
    l1c7ah:
    ld (ix+018h),003h		;1c7a	dd 36 18 03 	. 6 . .
    jp 05bb4h		;1c7e	c3 b4 5b 	. . [
    ld hl,09b9ah		;1c81	21 9a 9b 	! . .
    call 03759h		;1c84	cd 59 37 	. Y 7
    jr c,l1c5bh		;1c87	38 d2 	8 .
    ld (ix+000h),087h		;1c89	dd 36 00 87 	. 6 . .
    ld (ix+018h),001h		;1c8d	dd 36 18 01 	. 6 . .

## 41. line 3505: ld (ix+018h),001h		;1c8d	dd 36 18 01 	. 6 . .
    ld hl,09b9ah		;1c81	21 9a 9b 	! . .
    call 03759h		;1c84	cd 59 37 	. Y 7
    jr c,l1c5bh		;1c87	38 d2 	8 .
    ld (ix+000h),087h		;1c89	dd 36 00 87 	. 6 . .
    ld (ix+018h),001h		;1c8d	dd 36 18 01 	. 6 . .
    jr l1c5bh		;1c91	18 c8 	. .
    ret			;1c93	c9 	.
    bit 0,(ix+007h)		;1c94	dd cb 07 46 	. . . F
    jr nz,l1cc4h		;1c98	20 2a 	  *
    ld hl,05ca0h		;1c9a	21 a0 5c 	! . \
    jp 03963h		;1c9d	c3 63 39 	. c 9

## 42. line 3542: ld (ix+018h),001h		;1cf3	dd 36 18 01 	. 6 . .
    l1ceah:
    ld a,0b5h		;1cea	3e b5 	> .
    ld (0dd04h),a		;1cec	32 04 dd 	2 . .
    ld (ix+019h),030h		;1cef	dd 36 19 30 	. 6 . 0
    ld (ix+018h),001h		;1cf3	dd 36 18 01 	. 6 . .
    ld a,(ix+00eh)		;1cf7	dd 7e 0e 	. ~ .
    ld (ix+01ah),a		;1cfa	dd 77 1a 	. w .
    xor a			;1cfd	af 	.
    ld bc,l0102h+1		;1cfe	01 03 01 	. . .
    call l3ac4h		;1d01	cd c4 3a 	. . :
    jp sub_3af4h		;1d04	c3 f4 3a 	. . :

## 43. line 3558: ld (ix+018h),000h		;1d17	dd 36 18 00 	. 6 . .
    l1d13h:
    call 03759h		;1d13	cd 59 37 	. Y 7
    ret c			;1d16	d8 	.
    l1d17h:
    ld (ix+018h),000h		;1d17	dd 36 18 00 	. 6 . .
    ld a,(ix+01ah)		;1d1b	dd 7e 1a 	. ~ .
    ld (ix+00eh),a		;1d1e	dd 77 0e 	. w .
    ret			;1d21	c9 	.
    bit 0,(ix+007h)		;1d22	dd cb 07 46 	. . . F
    jr nz,l1d49h		;1d26	20 21 	  !
    ld hl,05d2eh		;1d28	21 2e 5d 	! . ]

## 44. line 3598: ld (ix+018h),001h		;1d81	dd 36 18 01 	. 6 . .
    call sub_3731h		;1d77	cd 31 37 	. 1 7
    ld bc,0d828h		;1d7a	01 28 d8 	. ( .
    call sub_3a8fh		;1d7d	cd 8f 3a 	. . :
    ret nc			;1d80	d0 	.
    ld (ix+018h),001h		;1d81	dd 36 18 01 	. 6 . .
    ld (ix+000h),08bh		;1d85	dd 36 00 8b 	. 6 . .
    ld hl,05dcch		;1d89	21 cc 5d 	! . ]
    call sub_3aaah		;1d8c	cd aa 3a 	. . :
    call 03931h		;1d8f	cd 31 39 	. 1 9
    jp sub_3af4h		;1d92	c3 f4 3a 	. . :
    dec (ix+019h)		;1d95	dd 35 19 	. 5 .

## 45. line 3680: ld (ix+018h),001h		;1e4d	dd 36 18 01 	. 6 . .
    ld e,(hl)			;1e45	5e 	^
    ld bc,0c040h		;1e46	01 40 c0 	. @ .
    call sub_3a8fh		;1e49	cd 8f 3a 	. . :
    ret nc			;1e4c	d0 	.
    ld (ix+018h),001h		;1e4d	dd 36 18 01 	. 6 . .
    ld (ix+000h),08dh		;1e51	dd 36 00 8d 	. 6 . .
    ld (ix+00ch),0ffh		;1e55	dd 36 0c ff 	. 6 . .
    ld (ix+004h),090h		;1e59	dd 36 04 90 	. 6 . .
    ld (ix+010h),001h		;1e5d	dd 36 10 01 	. 6 . .
    ld (ix+013h),000h		;1e61	dd 36 13 00 	. 6 . .
    ret			;1e65	c9 	.

## 46. line 3693: ld (ix+018h),002h		;1e73	dd 36 18 02 	. 6 . .
    jr nc,l1e73h		;1e6b	30 06 	0 .
    ld de,00060h		;1e6d	11 60 00 	. ` .
    jp sub_3946h		;1e70	c3 46 39 	. F 9
    l1e73h:
    ld (ix+018h),002h		;1e73	dd 36 18 02 	. 6 . .
    ld (ix+004h),080h		;1e77	dd 36 04 80 	. 6 . .
    jp sub_3af4h		;1e7b	c3 f4 3a 	. . :
    ld a,(0c08ch)		;1e7e	3a 8c c0 	: . .
    or a			;1e81	b7 	.
    ret nz			;1e82	c0 	.
    dec (ix+019h)		;1e83	dd 35 19 	. 5 .

## 47. line 3913: ld (ix+018h),001h		;206d	dd 36 18 01 	. 6 . .
    ld h,b			;2065	60 	`
    ld bc,0d030h		;2066	01 30 d0 	. 0 .
    call sub_3a8fh		;2069	cd 8f 3a 	. . :
    ret nc			;206c	d0 	.
    ld (ix+018h),001h		;206d	dd 36 18 01 	. 6 . .
    push ix		;2071	dd e5 	. .
    pop iy		;2073	fd e1 	. .
    ld e,(ix+002h)		;2075	dd 5e 02 	. ^ .
    ld d,(ix+004h)		;2078	dd 56 04 	. V .
    ld a,012h		;207b	3e 12 	> .
    ld (0c180h),a		;207d	32 80 c1 	2 . .

## 48. line 3929: ld (ix+018h),002h		;2099	dd 36 18 02 	. 6 . .
    cp (ix+004h)		;208e	dd be 04 	. . .
    ret nc			;2091	d0 	.
    call sub_3af4h		;2092	cd f4 3a 	. . :
    ld (ix+010h),0fdh		;2095	dd 36 10 fd 	. 6 . .
    ld (ix+018h),002h		;2099	dd 36 18 02 	. 6 . .
    ret			;209d	c9 	.
    ld a,(ix+004h)		;209e	dd 7e 04 	. ~ .
    cp 020h		;20a1	fe 20 	.
    jr c,l20a9h		;20a3	38 04 	8 .
    dec (ix+019h)		;20a5	dd 35 19 	. 5 .
    ret nz			;20a8	c0 	.

## 49. line 3938: ld (ix+018h),003h		;20ad	dd 36 18 03 	. 6 . .
    dec (ix+019h)		;20a5	dd 35 19 	. 5 .
    ret nz			;20a8	c0 	.
    l20a9h:
    ld (ix+019h),018h		;20a9	dd 36 19 18 	. 6 . .
    ld (ix+018h),003h		;20ad	dd 36 18 03 	. 6 . .
    jp sub_3af4h		;20b1	c3 f4 3a 	. . :
    dec (ix+01ah)		;20b4	dd 35 1a 	. 5 .
    ret nz			;20b7	c0 	.
    ld (ix+01ah),020h		;20b8	dd 36 1a 20 	. 6 .
    jp 0606dh		;20bc	c3 6d 60 	. m `
    bit 0,(ix+007h)		;20bf	dd cb 07 46 	. . . F

## 50. line 3992: ld (ix+018h),001h		;2143	dd 36 18 01 	. 6 . .
    ld h,c			;213a	61 	a
    l213bh:
    res 6,(ix+007h)		;213b	dd cb 07 b6 	. . . .
    ld (ix+000h),094h		;213f	dd 36 00 94 	. 6 . .
    ld (ix+018h),001h		;2143	dd 36 18 01 	. 6 . .
    ld (ix+015h),006h		;2147	dd 36 15 06 	. 6 . .
    ret			;214b	c9 	.
    ld hl,06161h		;214c	21 61 61 	! a a
    l214fh:
    call sub_3aaah		;214f	cd aa 3a 	. . :
    ld bc,09909h		;2152	01 09 99 	. . .

## 51. line 4076: ld (ix+018h),001h		;220f	dd 36 18 01 	. 6 . .
    call sub_3aaah		;2206	cd aa 3a 	. . :
    ld bc,0ae00h		;2209	01 00 ae 	. . .
    jp 02fb3h		;220c	c3 b3 2f 	. . /
    l220fh:
    ld (ix+018h),001h		;220f	dd 36 18 01 	. 6 . .
    call sub_3af4h		;2213	cd f4 3a 	. . :
    ld bc,sub_0303h		;2216	01 03 03 	. . .
    jp l3ac4h		;2219	c3 c4 3a 	. . :
    ld hl,06241h		;221c	21 41 62 	! A b
    call 03aa1h		;221f	cd a1 3a 	. . :
    ld bc,0ae00h		;2222	01 00 ae 	. . .

## 52. line 4085: ld (ix+018h),000h		;2229	dd 36 18 00 	. 6 . .
    call 03aa1h		;221f	cd a1 3a 	. . :
    ld bc,0ae00h		;2222	01 00 ae 	. . .
    call 02f9eh		;2225	cd 9e 2f 	. . /
    ret c			;2228	d8 	.
    ld (ix+018h),000h		;2229	dd 36 18 00 	. 6 . .
    xor a			;222d	af 	.
    ld bc,l0102h+2		;222e	01 04 01 	. . .
    call l3ac4h		;2231	cd c4 3a 	. . :
    ld c,002h		;2234	0e 02 	. .
    jp 03a57h		;2236	c3 57 3a 	. W :
    ld b,b			;2239	40 	@

## 53. line 4215: ld (ix+018h),001h		;2336	dd 36 18 01 	. 6 . .
    ld h,e			;232d	63 	c
    dec (ix+019h)		;232e	dd 35 19 	. 5 .
    ret nz			;2331	c0 	.
    ld (ix+019h),020h		;2332	dd 36 19 20 	. 6 .
    ld (ix+018h),001h		;2336	dd 36 18 01 	. 6 . .
    ld a,(ix+00eh)		;233a	dd 7e 0e 	. ~ .
    ld (ix+01ch),a		;233d	dd 77 1c 	. w .
    ld (ix+00eh),000h		;2340	dd 36 0e 00 	. 6 . .
    ld a,(ix+004h)		;2344	dd 7e 04 	. ~ .
    cp 098h		;2347	fe 98 	. .
    jr nc,l2352h		;2349	30 07 	0 .

## 54. line 4237: ld (ix+018h),002h		;2368	dd 36 18 02 	. 6 . .
    dec (ix+01ah)		;235c	dd 35 1a 	. 5 .
    ret nz			;235f	c0 	.
    ld (ix+01ah),010h		;2360	dd 36 1a 10 	. 6 . .
    ld (ix+010h),000h		;2364	dd 36 10 00 	. 6 . .
    ld (ix+018h),002h		;2368	dd 36 18 02 	. 6 . .
    ld hl,l0000h		;236c	21 00 00 	! . .
    ld de,l0412h		;236f	11 12 04 	. . .
    exx			;2372	d9 	.
    ld c,052h		;2373	0e 52 	. R
    ld hl,004fch		;2375	21 fc 04 	! . .
    call 039b0h		;2378	cd b0 39 	. . 9

## 55. line 4251: ld (ix+018h),000h		;238a	dd 36 18 00 	. 6 . .
    ret			;2381	c9 	.
    dec (ix+01bh)		;2382	dd 35 1b 	. 5 .
    ret nz			;2385	c0 	.
    ld (ix+01bh),010h		;2386	dd 36 1b 10 	. 6 . .
    ld (ix+018h),000h		;238a	dd 36 18 00 	. 6 . .
    ld a,(ix+01ch)		;238e	dd 7e 1c 	. ~ .
    ld (ix+00eh),a		;2391	dd 77 0e 	. w .
    ret			;2394	c9 	.
    bit 0,(ix+007h)		;2395	dd cb 07 46 	. . . F
    jr nz,l23bfh		;2399	20 24 	  $
    ld hl,063a1h		;239b	21 a1 63 	! . c

## 56. line 4297: ld (ix+018h),001h		;2406	dd 36 18 01 	. 6 . .
    call nc,sub_3adch		;23fb	d4 dc 3a 	. . :
    dec (ix+019h)		;23fe	dd 35 19 	. 5 .
    ret nz			;2401	c0 	.
    ld (ix+019h),010h		;2402	dd 36 19 10 	. 6 . .
    ld (ix+018h),001h		;2406	dd 36 18 01 	. 6 . .
    call sub_3af4h		;240a	cd f4 3a 	. . :
    ld bc,l0201h		;240d	01 01 02 	. . .
    jp l3ac4h		;2410	c3 c4 3a 	. . :
    ld hl,06466h		;2413	21 66 64 	! f d
    call 03aa1h		;2416	cd a1 3a 	. . :
    call 03759h		;2419	cd 59 37 	. Y 7

## 57. line 4305: ld (ix+018h),002h		;241d	dd 36 18 02 	. 6 . .
    ld hl,06466h		;2413	21 66 64 	! f d
    call 03aa1h		;2416	cd a1 3a 	. . :
    call 03759h		;2419	cd 59 37 	. Y 7
    ret c			;241c	d8 	.
    ld (ix+018h),002h		;241d	dd 36 18 02 	. 6 . .
    ld (ix+010h),0fbh		;2421	dd 36 10 fb 	. 6 . .
    ld c,002h		;2425	0e 02 	. .
    call 03a57h		;2427	cd 57 3a 	. W :
    ld hl,0646ah		;242a	21 6a 64 	! j d
    call sub_3aaah		;242d	cd aa 3a 	. . :
    jp 03931h		;2430	c3 31 39 	. 1 9

## 58. line 4322: ld (ix+018h),000h		;244a	dd 36 18 00 	. 6 . .
    call 01040h		;2442	cd 40 10 	. @ .
    rlca			;2445	07 	.
    ret nc			;2446	d0 	.
    call sub_3aceh		;2447	cd ce 3a 	. . :
    ld (ix+018h),000h		;244a	dd 36 18 00 	. 6 . .
    ld a,r		;244e	ed 5f 	. _
    and 001h		;2450	e6 01 	. .
    ld a,002h		;2452	3e 02 	> .
    jr nz,l2458h		;2454	20 02 	  .
    neg		;2456	ed 44 	. D
    l2458h:

## 59. line 4420: ld (ix+018h),001h		;2541	dd 36 18 01 	. 6 . .
    ld e,h			;253a	5c 	\
    inc d			;253b	14 	.
    ld h,(hl)			;253c	66 	f
    res 6,(ix+007h)		;253d	dd cb 07 b6 	. . . .
    ld (ix+018h),001h		;2541	dd 36 18 01 	. 6 . .
    ld (ix+01bh),001h		;2545	dd 36 1b 01 	. 6 . .
    ld c,004h		;2549	0e 04 	. .
    call 03a57h		;254b	cd 57 3a 	. W :
    jp 064e6h		;254e	c3 e6 64 	. . d
    ld a,(ix+019h)		;2551	dd 7e 19 	. ~ .
    inc a			;2554	3c 	<

## 60. line 4437: ld (ix+018h),002h		;256d	dd 36 18 02 	. 6 . .
    cp 007h		;2564	fe 07 	. .
    call z,065b0h		;2566	cc b0 65 	. . e
    cp 020h		;2569	fe 20 	.
    jr nz,l2572h		;256b	20 05 	  .
    ld (ix+018h),002h		;256d	dd 36 18 02 	. 6 . .
    xor a			;2571	af 	.
    l2572h:
    ld (ix+019h),a		;2572	dd 77 19 	. w .
    ld hl,065bfh		;2575	21 bf 65 	! . e
    call sub_3e32h		;2578	cd 32 3e 	. 2 >
    ld b,a			;257b	47 	G

## 61. line 4540: ld (ix+018h),004h		;263c	dd 36 18 04 	. 6 . .
    ld a,(0c464h)		;2630	3a 64 c4 	: d .
    ld (ix+004h),a		;2633	dd 77 04 	. w .
    ld a,(0c46eh)		;2636	3a 6e c4 	: n .
    ld (ix+00eh),a		;2639	dd 77 0e 	. w .
    ld (ix+018h),004h		;263c	dd 36 18 04 	. 6 . .
    ld a,(ix+017h)		;2640	dd 7e 17 	. ~ .
    ld hl,06673h		;2643	21 73 66 	! s f
    call 03abah		;2646	cd ba 3a 	. . :
    ld b,h			;2649	44 	D
    ld c,l			;264a	4d 	M
    ld iy,0c460h		;264b	fd 21 60 c4 	. ! ` .

## 62. line 4722: ld (ix+018h),001h		;27e8	dd 36 18 01 	. 6 . .
    ld (ix+01ah),020h		;27de	dd 36 1a 20 	. 6 .
    ld a,(ix+004h)		;27e2	dd 7e 04 	. ~ .
    cp 040h		;27e5	fe 40 	. @
    ret nc			;27e7	d0 	.
    ld (ix+018h),001h		;27e8	dd 36 18 01 	. 6 . .
    ld l,(ix+00dh)		;27ec	dd 6e 0d 	. n .
    ld h,(ix+00eh)		;27ef	dd 66 0e 	. f .
    ld (0c1adh),hl		;27f2	22 ad c1 	" . .
    ld l,(ix+00fh)		;27f5	dd 6e 0f 	. n .
    ld h,(ix+010h)		;27f8	dd 66 10 	. f .
    ld (0c1afh),hl		;27fb	22 af c1 	" . .

## 63. line 4733: ld (ix+018h),000h		;2809	dd 36 18 00 	. 6 . .
    jp sub_3af4h		;27fe	c3 f4 3a 	. . :
    dec (ix+01bh)		;2801	dd 35 1b 	. 5 .
    ret nz			;2804	c0 	.
    ld (ix+01bh),018h		;2805	dd 36 1b 18 	. 6 . .
    ld (ix+018h),000h		;2809	dd 36 18 00 	. 6 . .
    ld hl,(0c1adh)		;280d	2a ad c1 	* . .
    call 0393fh		;2810	cd 3f 39 	. ? 9
    ld hl,(0c1afh)		;2813	2a af c1 	* . .
    call l394ch+1		;2816	cd 4d 39 	. M 9
    ld bc,0684bh		;2819	01 4b 68 	. K h
    ld de,l0612h		;281c	11 12 06 	. . .

## 64. line 4751: ld (ix+018h),000h		;283b	dd 36 18 00 	. 6 . .
    jp 067cfh		;2830	c3 cf 67 	. . g
    dec (ix+01bh)		;2833	dd 35 1b 	. 5 .
    ret nz			;2836	c0 	.
    ld (ix+01bh),018h		;2837	dd 36 1b 18 	. 6 . .
    ld (ix+018h),000h		;283b	dd 36 18 00 	. 6 . .
    ld a,002h		;283f	3e 02 	> .
    call 03a3fh		;2841	cd 3f 3a 	. ? :
    ld hl,(0c1afh)		;2844	2a af c1 	* . .
    call l394ch+1		;2847	cd 4d 39 	. M 9
    jp 067cfh		;284a	c3 cf 67 	. . g
    inc bc			;284d	03 	.

## 65. line 4922: ld (ix+018h),003h		;29db	dd 36 18 03 	. 6 . .
    dec (ix+019h)		;29d2	dd 35 19 	. 5 .
    ret nz			;29d5	c0 	.
    ld a,(ix+018h)		;29d6	dd 7e 18 	. ~ .
    cp 000h		;29d9	fe 00 	. .
    ld (ix+018h),003h		;29db	dd 36 18 03 	. 6 . .
    jr z,l29e5h		;29df	28 04 	( .
    ld (ix+018h),004h		;29e1	dd 36 18 04 	. 6 . .
    l29e5h:
    ld (ix+019h),040h		;29e5	dd 36 19 40 	. 6 . @
    ld hl,06ac0h		;29e9	21 c0 6a 	! . j
    ld a,(ix+018h)		;29ec	dd 7e 18 	. ~ .

## 66. line 4924: ld (ix+018h),004h		;29e1	dd 36 18 04 	. 6 . .
    ld a,(ix+018h)		;29d6	dd 7e 18 	. ~ .
    cp 000h		;29d9	fe 00 	. .
    ld (ix+018h),003h		;29db	dd 36 18 03 	. 6 . .
    jr z,l29e5h		;29df	28 04 	( .
    ld (ix+018h),004h		;29e1	dd 36 18 04 	. 6 . .
    l29e5h:
    ld (ix+019h),040h		;29e5	dd 36 19 40 	. 6 . @
    ld hl,06ac0h		;29e9	21 c0 6a 	! . j
    ld a,(ix+018h)		;29ec	dd 7e 18 	. ~ .
    call sub_3ab1h		;29ef	cd b1 3a 	. . :
    call 03931h		;29f2	cd 31 39 	. 1 9

## 67. line 4944: ld (ix+018h),001h		;2a11	dd 36 18 01 	. 6 . .
    ld a,09eh		;2a0b	3e 9e 	> .
    ld (0dd04h),a		;2a0d	32 04 dd 	2 . .
    ret			;2a10	c9 	.
    l2a11h:
    ld (ix+018h),001h		;2a11	dd 36 18 01 	. 6 . .
    ld (ix+01bh),006h		;2a15	dd 36 1b 06 	. 6 . .
    ld (ix+01ch),001h		;2a19	dd 36 1c 01 	. 6 . .
    ret			;2a1d	c9 	.
    dec (ix+017h)		;2a1e	dd 35 17 	. 5 .
    jp nz,069b5h		;2a21	c2 b5 69 	. . i
    ld (ix+017h),008h		;2a24	dd 36 17 08 	. 6 . .

## 68. line 4951: ld (ix+018h),000h		;2a28	dd 36 18 00 	. 6 . .
    ret			;2a1d	c9 	.
    dec (ix+017h)		;2a1e	dd 35 17 	. 5 .
    jp nz,069b5h		;2a21	c2 b5 69 	. . i
    ld (ix+017h),008h		;2a24	dd 36 17 08 	. 6 . .
    ld (ix+018h),000h		;2a28	dd 36 18 00 	. 6 . .
    ret			;2a2c	c9 	.
    ld hl,06ab8h		;2a2d	21 b8 6a 	! . j
    call 03aa1h		;2a30	cd a1 3a 	. . :
    call sub_3731h		;2a33	cd 31 37 	. 1 7
    dec (ix+01bh)		;2a36	dd 35 1b 	. 5 .
    ret nz			;2a39	c0 	.

## 69. line 4961: ld (ix+018h),000h		;2a40	dd 36 18 00 	. 6 . .
    ret nz			;2a39	c0 	.
    ld a,(ix+01ch)		;2a3a	dd 7e 1c 	. ~ .
    or a			;2a3d	b7 	.
    jr nz,l2a45h		;2a3e	20 05 	  .
    ld (ix+018h),000h		;2a40	dd 36 18 00 	. 6 . .
    ret			;2a44	c9 	.
    l2a45h:
    ld (ix+01ah),080h		;2a45	dd 36 1a 80 	. 6 . .
    ld (ix+018h),002h		;2a49	dd 36 18 02 	. 6 . .
    ld c,003h		;2a4d	0e 03 	. .
    call 03a57h		;2a4f	cd 57 3a 	. W :

## 70. line 4965: ld (ix+018h),002h		;2a49	dd 36 18 02 	. 6 . .
    ld (ix+018h),000h		;2a40	dd 36 18 00 	. 6 . .
    ret			;2a44	c9 	.
    l2a45h:
    ld (ix+01ah),080h		;2a45	dd 36 1a 80 	. 6 . .
    ld (ix+018h),002h		;2a49	dd 36 18 02 	. 6 . .
    ld c,003h		;2a4d	0e 03 	. .
    call 03a57h		;2a4f	cd 57 3a 	. W :
    ld a,r		;2a52	ed 5f 	. _
    and 003h		;2a54	e6 03 	. .
    ld c,a			;2a56	4f 	O
    ld b,000h		;2a57	06 00 	. .

## 71. line 4993: ld (ix+018h),002h		;2a90	dd 36 18 02 	. 6 . .
    jp sub_3946h		;2a83	c3 46 39 	. F 9
    dec (ix+017h)		;2a86	dd 35 17 	. 5 .
    jp nz,06a6dh		;2a89	c2 6d 6a 	. m j
    ld (ix+017h),008h		;2a8c	dd 36 17 08 	. 6 . .
    ld (ix+018h),002h		;2a90	dd 36 18 02 	. 6 . .
    ret			;2a94	c9 	.
    l2a95h:
    ld (ix+004h),080h		;2a95	dd 36 04 80 	. 6 . .
    ld (ix+003h),000h		;2a99	dd 36 03 00 	. 6 . .
    ld (ix+01bh),010h		;2a9d	dd 36 1b 10 	. 6 . .
    ld (ix+018h),001h		;2aa1	dd 36 18 01 	. 6 . .

## 72. line 4999: ld (ix+018h),001h		;2aa1	dd 36 18 01 	. 6 . .
    l2a95h:
    ld (ix+004h),080h		;2a95	dd 36 04 80 	. 6 . .
    ld (ix+003h),000h		;2a99	dd 36 03 00 	. 6 . .
    ld (ix+01bh),010h		;2a9d	dd 36 1b 10 	. 6 . .
    ld (ix+018h),001h		;2aa1	dd 36 18 01 	. 6 . .
    ld (ix+01ch),000h		;2aa5	dd 36 1c 00 	. 6 . .
    jp sub_3af4h		;2aa9	c3 f4 3a 	. . :
    call m,0fafbh		;2aac	fc fb fa 	. . .
    ld sp,hl			;2aaf	f9 	.
    nop			;2ab0	00 	.
    djnz l2ab3h		;2ab1	10 00 	. .

## 73. line 5149: ld (ix+018h),001h		;2be1	dd 36 18 01 	. 6 . .
    rrca			;2bd9	0f 	.
    and 003h		;2bda	e6 03 	. .
    ret			;2bdc	c9 	.
    ld (ix+01ah),050h		;2bdd	dd 36 1a 50 	. 6 . P
    ld (ix+018h),001h		;2be1	dd 36 18 01 	. 6 . .
    ld a,(ix+00eh)		;2be5	dd 7e 0e 	. ~ .
    ld (ix+01ch),a		;2be8	dd 77 1c 	. w .
    ld a,(ix+010h)		;2beb	dd 7e 10 	. ~ .
    ld (ix+01dh),a		;2bee	dd 77 1d 	. w .
    call sub_3af4h		;2bf1	cd f4 3a 	. . :
    ld bc,06c46h		;2bf4	01 46 6c 	. F l

## 74. line 5168: ld (ix+018h),000h		;2c13	dd 36 18 00 	. 6 . .
    jp 04ea9h		;2c08	c3 a9 4e 	. . N
    dec (ix+01bh)		;2c0b	dd 35 1b 	. 5 .
    ret nz			;2c0e	c0 	.
    ld (ix+01bh),008h		;2c0f	dd 36 1b 08 	. 6 . .
    ld (ix+018h),000h		;2c13	dd 36 18 00 	. 6 . .
    ld a,(ix+01ch)		;2c17	dd 7e 1c 	. ~ .
    ld (ix+00eh),a		;2c1a	dd 77 0e 	. w .
    ld a,(ix+01dh)		;2c1d	dd 7e 1d 	. ~ .
    ld (ix+010h),a		;2c20	dd 77 10 	. w .
    ret			;2c23	c9 	.
    inc l			;2c24	2c 	,

## 75. line 5283: ld (ix+018h),002h		;2d10	dd 36 18 02 	. 6 . .
    ld a,(ix+015h)		;2d05	dd 7e 15 	. ~ .
    cp 014h		;2d08	fe 14 	. .
    jr nc,l2d17h		;2d0a	30 0b 	0 .
    ld (ix+012h),001h		;2d0c	dd 36 12 01 	. 6 . .
    ld (ix+018h),002h		;2d10	dd 36 18 02 	. 6 . .
    call sub_3af4h		;2d14	cd f4 3a 	. . :
    l2d17h:
    ld hl,06d1dh		;2d17	21 1d 6d 	! . m
    jp 03954h		;2d1a	c3 54 39 	. T 9
    dec hl			;2d1d	2b 	+
    ld l,l			;2d1e	6d 	m

## 76. line 5320: ld (ix+018h),c		;2d5c	dd 71 18 	. q .
    or (hl)			;2d57	b6 	.
    ret nz			;2d58	c0 	.
    add hl,de			;2d59	19 	.
    djnz l2d56h		;2d5a	10 fa 	. .
    ld (ix+018h),c		;2d5c	dd 71 18 	. q .
    xor a			;2d5f	af 	.
    ld bc,l1010h		;2d60	01 10 10 	. . .
    call l3ac4h		;2d63	cd c4 3a 	. . :
    ld hl,(0c46dh)		;2d66	2a 6d c4 	* m .
    ld (0c1a3h),hl		;2d69	22 a3 c1 	" . .
    ld hl,(0c46fh)		;2d6c	2a 6f c4 	* o .

## 77. line 5349: ld (ix+018h),000h		;2da0	dd 36 18 00 	. 6 . .
    cp 00fh		;2d9b	fe 0f 	. .
    jr z,l2db1h		;2d9d	28 12 	( .
    ret			;2d9f	c9 	.
    l2da0h:
    ld (ix+018h),000h		;2da0	dd 36 18 00 	. 6 . .
    ld hl,(0c1a3h)		;2da4	2a a3 c1 	* . .
    ld (0c46dh),hl		;2da7	22 6d c4 	" m .
    ld hl,(0c1a5h)		;2daa	2a a5 c1 	* . .
    ld (0c46fh),hl		;2dad	22 6f c4 	" o .
    ret			;2db0	c9 	.
    l2db1h:

## 78. line 5372: ld (ix+018h),003h		;2dd7	dd 36 18 03 	. 6 . .
    ld a,003h		;2dce	3e 03 	> .
    jp 04ea9h		;2dd0	c3 a9 4e 	. . N
    dec (ix+01ah)		;2dd3	dd 35 1a 	. 5 .
    ret nz			;2dd6	c0 	.
    ld (ix+018h),003h		;2dd7	dd 36 18 03 	. 6 . .
    ld (ix+010h),0fch		;2ddb	dd 36 10 fc 	. 6 . .
    ld hl,l0000h		;2ddf	21 00 00 	! . .
    ld (0c1a3h),hl		;2de2	22 a3 c1 	" . .
    ld (0c1a5h),hl		;2de5	22 a5 c1 	" . .
    ret			;2de8	c9 	.
    ld bc,0e808h		;2de9	01 08 e8 	. . .

## 79. line 5391: ld (ix+018h),004h		;2e09	dd 36 18 04 	. 6 . .
    ld de,00060h		;2dff	11 60 00 	. ` .
    jp sub_3946h		;2e02	c3 46 39 	. F 9
    l2e05h:
    ld (ix+004h),080h		;2e05	dd 36 04 80 	. 6 . .
    ld (ix+018h),004h		;2e09	dd 36 18 04 	. 6 . .
    jp sub_3af4h		;2e0d	c3 f4 3a 	. . :
    ld c,006h		;2e10	0e 06 	. .
    call 06d4eh		;2e12	cd 4e 6d 	. N m
    ret z			;2e15	c8 	.
    ld hl,06e68h		;2e16	21 68 6e 	! h n
    call 03aa1h		;2e19	cd a1 3a 	. . :

## 80. line 5402: ld (ix+018h),005h		;2e27	dd 36 18 05 	. 6 . .
    call 03931h		;2e1c	cd 31 39 	. 1 9
    dec (ix+01bh)		;2e1f	dd 35 1b 	. 5 .
    ret nz			;2e22	c0 	.
    ld (ix+01bh),018h		;2e23	dd 36 1b 18 	. 6 . .
    ld (ix+018h),005h		;2e27	dd 36 18 05 	. 6 . .
    ld a,r		;2e2b	ed 5f 	. _
    and 003h		;2e2d	e6 03 	. .
    ld hl,06e6ch		;2e2f	21 6c 6e 	! l n
    rst 10h			;2e32	d7 	.
    ld (ix+010h),l		;2e33	dd 75 10 	. u .
    ld hl,06e4ch		;2e36	21 4c 6e 	! L n

## 81. line 5470: ld (ix+018h),001h		;2eaf	dd 36 18 01 	. 6 . .
    call po,sub_3a6eh		;2ea7	e4 6e 3a 	. n :
    ld (hl),d			;2eaa	72 	r
    call nz,028b7h		;2eab	c4 b7 28 	. . (
    inc b			;2eae	04 	.
    ld (ix+018h),001h		;2eaf	dd 36 18 01 	. 6 . .
    ld de,l0010h		;2eb3	11 10 00 	. . .
    ld l,(ix+01bh)		;2eb6	dd 6e 1b 	. n .
    ld h,(ix+01ch)		;2eb9	dd 66 1c 	. f .
    or a			;2ebc	b7 	.
    sbc hl,de		;2ebd	ed 52 	. R
    ld (ix+01bh),l		;2ebf	dd 75 1b 	. u .

## 82. line 5608: ld (ix+018h),001h		;3007	dd 36 18 01 	. 6 . .
    add hl,de			;3003	19 	.
    djnz l2fffh		;3004	10 f9 	. .
    ret			;3006	c9 	.
    l3007h:
    ld (ix+018h),001h		;3007	dd 36 18 01 	. 6 . .
    xor a			;300b	af 	.
    ld bc,l0a06h		;300c	01 06 0a 	. . .
    jp l3ac4h		;300f	c3 c4 3a 	. . :
    l3012h:
    ld (ix+018h),002h		;3012	dd 36 18 02 	. 6 . .
    ld (ix+000h),067h		;3016	dd 36 00 67 	. 6 . g

## 83. line 5613: ld (ix+018h),002h		;3012	dd 36 18 02 	. 6 . .
    xor a			;300b	af 	.
    ld bc,l0a06h		;300c	01 06 0a 	. . .
    jp l3ac4h		;300f	c3 c4 3a 	. . :
    l3012h:
    ld (ix+018h),002h		;3012	dd 36 18 02 	. 6 . .
    ld (ix+000h),067h		;3016	dd 36 00 67 	. 6 . g
    res 6,(ix+007h)		;301a	dd cb 07 b6 	. . . .
    ld hl,07105h		;301e	21 05 71 	! . q
    call 03aa1h		;3021	cd a1 3a 	. . :
    call 06f8eh		;3024	cd 8e 6f 	. . o
    ld bc,0e808h		;3027	01 08 e8 	. . .

## 84. line 5634: ld (ix+018h),004h		;3047	dd 36 18 04 	. 6 . .
    jp z,07163h		;303f	ca 63 71 	. c q
    ld a,(0c580h)		;3042	3a 80 c5 	: . .
    or a			;3045	b7 	.
    ret nz			;3046	c0 	.
    ld (ix+018h),004h		;3047	dd 36 18 04 	. 6 . .
    ld (ix+000h),067h		;304b	dd 36 00 67 	. 6 . g
    res 0,(ix+012h)		;304f	dd cb 12 86 	. . . .
    xor a			;3053	af 	.
    ld bc,02006h		;3054	01 06 20 	. .
    call l3ac4h		;3057	cd c4 3a 	. . :
    ld hl,l0000h		;305a	21 00 00 	! . .

## 85. line 5664: ld (ix+018h),000h		;3094	dd 36 18 00 	. 6 . .
    cp 005h		;308e	fe 05 	. .
    jp z,07099h		;3090	ca 99 70 	. . p
    ret			;3093	c9 	.
    l3094h:
    ld (ix+018h),000h		;3094	dd 36 18 00 	. 6 . .
    ret			;3098	c9 	.
    ld hl,070f5h		;3099	21 f5 70 	! . p
    call 03aa1h		;309c	cd a1 3a 	. . :
    ld de,l0200h		;309f	11 00 02 	. . .
    exx			;30a2	d9 	.
    ld hl,070f9h		;30a3	21 f9 70 	! . p

## 86. line 5695: ld (ix+018h),000h		;30e3	dd 36 18 00 	. 6 . .
    ld a,(ix+004h)		;30d9	dd 7e 04 	. ~ .
    cp 078h		;30dc	fe 78 	. x
    ret c			;30de	d8 	.
    res 6,(ix+007h)		;30df	dd cb 07 b6 	. . . .
    ld (ix+018h),000h		;30e3	dd 36 18 00 	. 6 . .
    ld (ix+003h),000h		;30e7	dd 36 03 00 	. 6 . .
    ld (ix+004h),078h		;30eb	dd 36 04 78 	. 6 . x
    call sub_3af4h		;30ef	cd f4 3a 	. . :
    jp 0700bh		;30f2	c3 0b 70 	. . p
    nop			;30f5	00 	.
    ld bc,0ff00h		;30f6	01 00 ff 	. . .

## 87. line 5749: ld (ix+018h),003h		;3163	dd 36 18 03 	. 6 . .
    dec (ix+01bh)		;315b	dd 35 1b 	. 5 .
    ret nz			;315e	c0 	.
    l315fh:
    ld (ix+01bh),003h		;315f	dd 36 1b 03 	. 6 . .
    ld (ix+018h),003h		;3163	dd 36 18 03 	. 6 . .
    ld (ix+000h),065h		;3167	dd 36 00 65 	. 6 . e
    ld a,r		;316b	ed 5f 	. _
    and 001h		;316d	e6 01 	. .
    ld hl,071f1h		;316f	21 f1 71 	! . q
    rst 10h			;3172	d7 	.
    ld (ix+010h),l		;3173	dd 75 10 	. u .

## 88. line 5989: ld (ix+018h),001h		;336a	dd 36 18 01 	. 6 . .
    ld (ix+004h),a		;3362	dd 77 04 	. w .
    ret			;3365	c9 	.
    l3366h:
    ld (ix+01ah),020h		;3366	dd 36 1a 20 	. 6 .
    ld (ix+018h),001h		;336a	dd 36 18 01 	. 6 . .
    ld (ix+000h),06dh		;336e	dd 36 00 6d 	. 6 . m
    xor a			;3372	af 	.
    ld bc,l0110h		;3373	01 10 01 	. . .
    call l3ac4h		;3376	cd c4 3a 	. . :
    jp 07343h		;3379	c3 43 73 	. C s
    ld hl,07427h		;337c	21 27 74 	! ' t

## 89. line 6007: ld (ix+018h),000h		;3397	dd 36 18 00 	. 6 . .
    cp 00fh		;3390	fe 0f 	. .
    jr z,l33a2h		;3392	28 0e 	( .
    jp 07343h		;3394	c3 43 73 	. C s
    l3397h:
    ld (ix+018h),000h		;3397	dd 36 18 00 	. 6 . .
    ld (ix+000h),06bh		;339b	dd 36 00 6b 	. 6 . k
    jp 07343h		;339f	c3 43 73 	. C s
    l33a2h:
    call 07343h		;33a2	cd 43 73 	. C s
    ld hl,l0000h		;33a5	21 00 00 	! . .
    ld de,00404h		;33a8	11 04 04 	. . .

## 90. line 6144: ld (ix+018h),001h		;3481	dd 36 18 01 	. 6 . .
    ld (hl),h			;3478	74 	t
    ld a,(0c460h)		;3479	3a 60 c4 	: ` .
    cp 05ch		;347c	fe 5c 	. \
    jp nz,07334h		;347e	c2 34 73 	. 4 s
    ld (ix+018h),001h		;3481	dd 36 18 01 	. 6 . .
    ld b,000h		;3485	06 00 	. .
    ld c,(ix+017h)		;3487	dd 4e 17 	. N .
    ld hl,074a2h		;348a	21 a2 74 	! . t
    add hl,bc			;348d	09 	.
    ld a,(hl)			;348e	7e 	~
    ld (ix+01bh),a		;348f	dd 77 1b 	. w .

## 91. line 6202: ld (ix+018h),a		;3504	dd 77 18 	. w .
    ld a,d			;34fe	7a 	z
    ld hl,0762fh		;34ff	21 2f 76 	! / v
    rst 10h			;3502	d7 	.
    ld a,(hl)			;3503	7e 	~
    ld (ix+018h),a		;3504	dd 77 18 	. w .
    inc hl			;3507	23 	#
    ld a,(hl)			;3508	7e 	~
    ld (ix+00ch),a		;3509	dd 77 0c 	. w .
    inc hl			;350c	23 	#
    sub_350dh:
    ld a,(hl)			;350d	7e 	~

## 92. line 6305: ld (ix+018h),002h		;35de	dd 36 18 02 	. 6 . .
    ld a,(ix+010h)		;35d2	dd 7e 10 	. ~ .
    ld (ix+01ah),a		;35d5	dd 77 1a 	. w .
    ld a,(ix+018h)		;35d8	dd 7e 18 	. ~ .
    ld (ix+01bh),a		;35db	dd 77 1b 	. w .
    ld (ix+018h),002h		;35de	dd 36 18 02 	. 6 . .
    jp sub_3af4h		;35e2	c3 f4 3a 	. . :
    l35e5h:
    ld bc,07657h		;35e5	01 57 76 	. W v
    ld de,l0400h+2		;35e8	11 02 04 	. . .
    exx			;35eb	d9 	.
    ld iy,0c480h		;35ec	fd 21 80 c4 	. ! . .

## 93. line 6321: ld (ix+018h),a		;3608	dd 77 18 	. w .
    ld (ix+019h),010h		;35fb	dd 36 19 10 	. 6 . .
    ld a,(ix+01ah)		;35ff	dd 7e 1a 	. ~ .
    ld (ix+010h),a		;3602	dd 77 10 	. w .
    ld a,(ix+01bh)		;3605	dd 7e 1b 	. ~ .
    ld (ix+018h),a		;3608	dd 77 18 	. w .
    ret			;360b	c9 	.
    ld hl,0ad12h		;360c	21 12 ad 	! . .
    call sub_3731h		;360f	cd 31 37 	. 1 7
    inc (ix+01ch)		;3612	dd 34 1c 	. 4 .
    ld a,(ix+01ch)		;3615	dd 7e 1c 	. ~ .
    cp 008h		;3618	fe 08 	. .

## 94. line 6502: ld (ix+018h),a		;378d	dd 77 18 	. w .
    set 0,(ix+007h)		;3780	dd cb 07 c6 	. . . .
    ld hl,l0808h		;3784	21 08 08 	! . .
    ld (0c469h),hl		;3787	22 69 c4 	" i .
    ld a,(ix+004h)		;378a	dd 7e 04 	. ~ .
    ld (ix+018h),a		;378d	dd 77 18 	. w .
    jp 0783ch		;3790	c3 3c 78 	. < x
    l3793h:
    bit 3,(ix+012h)		;3793	dd cb 12 5e 	. . . ^
    jr z,l37c8h		;3797	28 2f 	( /
    ld a,(ix+00ch)		;3799	dd 7e 0c 	. ~ .
    or a			;379c	b7 	.

## 95. line 6603: ld (ix+018h),a		;387a	dd 77 18 	. w .
    ld b,(hl)			;3870	46 	F
    jr nz,l388eh		;3871	20 1b 	  .
    set 0,(ix+007h)		;3873	dd cb 07 c6 	. . . .
    ld a,(ix+004h)		;3877	dd 7e 04 	. ~ .
    ld (ix+018h),a		;387a	dd 77 18 	. w .
    ld (ix+01ah),023h		;387d	dd 36 1a 23 	. 6 . #
    ld hl,02001h		;3881	21 01 20 	! .
    ld (0c469h),hl		;3884	22 69 c4 	" i .
    ld hl,08671h		;3887	21 71 86 	! q .
    ld (0c465h),hl		;388a	22 65 c4 	" e .
    ret			;388d	c9 	.
