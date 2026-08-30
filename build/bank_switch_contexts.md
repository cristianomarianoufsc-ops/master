# Bank-switch contexts

## 1. line 77 bank=12
    jr l809fh		;809d
    l809fh:
    out (0bfh),a		;809f
    ei			;80a1
    ld a,00ch		;80a2
    ld (0ffffh),a		;80a4
    ld hl,l981bh+2		;80a7
    ld de,04000h		;80aa
    call 0033dh		;80ad
    ld hl,048b4h		;80b0
    ld de,0c800h		;80b3
    ld bc,00113h		;80b6
    ld a,000h		;80b9

## 2. line 112 bank=19
    ld a,001h		;80f5
    ld (0c203h),a		;80f7
    ld (0c204h),a		;80fa
    call 0406ch		;80fd
    ld a,013h		;8100
    ld (0ffffh),a		;8102
    ld hl,l9e70h+2		;8105
    ld de,05200h		;8108
    call 0033dh		;810b
    ld hl,09d82h		;810e
    ld de,0cba8h		;8111
    ld bc,00a18h		;8114
    call 05ad9h		;8117

## 3. line 129 bank=22
    ld a,002h		;8125
    ld (0c008h),a		;8127
    ld (0c203h),a		;812a
    ld (0c204h),a		;812d
    ld a,016h		;8130
    ld (0ffffh),a		;8132
    ld hl,(0c202h)		;8135
    ld h,000h		;8138
    add hl,hl			;813a
    ld de,l8000h		;813b
    add hl,de			;813e
    ld a,(hl)			;813f
    inc hl			;8140

## 4. line 1171 bank=12
    ld de,0d101h		;88ea
    ld bc,0003fh		;88ed
    ld (hl),000h		;88f0
    ldir		;88f2
    ld a,00ch		;88f4
    ld (0ffffh),a		;88f6
    ld hl,04160h		;88f9
    ld de,0c0e0h		;88fc
    ld bc,00020h		;88ff
    ldir		;8902
    ld hl,l981bh+2		;8904
    ld de,04000h		;8907
    call 0033dh		;890a

## 5. line 1181 bank=19
    ld hl,l981bh+2		;8904
    ld de,04000h		;8907
    call 0033dh		;890a
    ld a,013h		;890d
    l890fh:
    ld (0ffffh),a		;890f
    ld hl,la894h		;8912
    ld de,04000h		;8915
    call 0033dh		;8918
    ld hl,0a7d2h		;891b
    ld de,07a80h		;891e
    l8921h:
    call 0033dh		;8921

## 6. line 1307 bank=19
    ld c,(hl)			;8a05
    inc hl			;8a06
    inc de			;8a07
    djnz l8a00h		;8a08
    ld a,013h		;8a0a
    ld (0ffffh),a		;8a0c
    ld hl,lab89h		;8a0f
    call 04bbdh		;8a12
    ld e,a			;8a15
    push de			;8a16
    ld hl,laba2h		;8a17
    call 04bbdh		;8a1a
    pop de			;8a1d

## 7. line 1491 bank=22
    ld a,001h		;8b5d
    ld (0c2e8h),a		;8b5f
    ld a,003h		;8b62
    ld (0c2e9h),a		;8b64
    ld a,016h		;8b67
    ld (0ffffh),a		;8b69
    ld hl,l9420h		;8b6c
    ld de,0c258h		;8b6f
    ld bc,0000ch		;8b72
    ldir		;8b75
    ld a,(0c205h)		;8b77
    ld (0c259h),a		;8b7a
    ld a,(0c215h)		;8b7d

## 8. line 1581 bank=19
    exx			;8be4
    inc hl			;8be5
    djnz l8bd7h		;8be6
    ret			;8be8
    ld a,013h		;8be9
    ld (0ffffh),a		;8beb
    ld hl,0d120h		;8bee
    ld de,0d121h		;8bf1
    ld bc,0001fh		;8bf4
    ld (hl),000h		;8bf7
    ldir		;8bf9
    ld hl,lab89h		;8bfb
    ld b,(hl)			;8bfe

## 9. line 1925 bank=19
    add hl,hl			;8dda
    add hl,de			;8ddb
    ld de,0ace8h		;8ddc
    add hl,de			;8ddf
    ld a,013h		;8de0
    ld (0ffffh),a		;8de2
    ld c,(hl)			;8de5
    inc hl			;8de6
    ld b,(hl)			;8de7
    inc hl			;8de8
    ld e,(hl)			;8de9
    inc hl			;8dea
    ld d,(hl)			;8deb

## 10. line 1968 bank=19
    l8e1dh:
    add hl,de			;8e1d
    ld de,04e58h		;8e1e
    add hl,de			;8e21
    ld a,(hl)			;8e22
    ld (0ffffh),a		;8e23
    inc hl			;8e26
    ld e,(hl)			;8e27
    inc hl			;8e28
    ld d,(hl)			;8e29
    inc hl			;8e2a
    push hl			;8e2b
    ex de,hl			;8e2c

## 11. line 1998 bank=23
    inc hl			;8e44
    ld h,(hl)			;8e45
    ld l,a			;8e46
    ld de,0cf00h		;8e47
    ld a,017h		;8e4a
    ld (0ffffh),a		;8e4c
    call 05b12h		;8e4f
    ld a,001h		;8e52
    ld (0c0a0h),a		;8e54
    ret			;8e57
    jr $-74		;8e58
    l8e5ah:
    add a,d			;8e5a

## 12. line 2308 bank=19
    add hl,hl			;8fe0
    add hl,de			;8fe1
    ld de,0ace8h		;8fe2
    add hl,de			;8fe5
    ld a,013h		;8fe6
    ld (0ffffh),a		;8fe8
    ld c,(hl)			;8feb
    inc hl			;8fec
    ld b,(hl)			;8fed
    inc hl			;8fee
    ld e,(hl)			;8fef
    inc hl			;8ff0
    ld d,(hl)			;8ff1

## 13. line 2336 bank=22
    ld (0c216h),a		;9009
    ld hl,0c200h		;900c
    res 3,(hl)		;900f
    ret			;9011
    ld a,016h		;9012
    ld (0ffffh),a		;9014
    ld hl,(0c206h)		;9017
    ld a,(hl)			;901a
    ld d,a			;901b
    inc hl			;901c
    inc a			;901d
    jp z,05146h		;901e
    inc a			;9021

## 14. line 2957 bank=31
    jr c,l947fh		;9478
    ld (0c208h),hl		;947a
    ld a,01fh		;947d
    l947fh:
    ld (0c20eh),a		;947f
    ld (0ffffh),a		;9482
    ld hl,(0c208h)		;9485
    add hl,hl			;9488
    l9489h:
    ld de,l8000h		;9489
    add hl,de			;948c
    ld a,(hl)			;948d
    inc hl			;948e

## 15. line 2977 bank=19
    ld h,000h		;9498
    ld de,lb28ch		;949a
    l949dh:
    add hl,de			;949d
    ld a,013h		;949e
    ld (0ffffh),a		;94a0
    ld a,(hl)			;94a3
    inc hl			;94a4
    ld h,(hl)			;94a5
    ld l,a			;94a6
    ld b,002h		;94a7
    ld c,(hl)			;94a9
    inc hl			;94aa

## 16. line 3004 bank=16
    jr z,l94cfh		;94cb
    dec (hl)			;94cd
    ret			;94ce
    l94cfh:
    ld a,(0c20eh)		;94cf
    ld (0ffffh),a		;94d2
    ld hl,(0c20ch)		;94d5
    ld a,(hl)			;94d8
    l94d9h:
    inc a			;94d9
    jp z,05514h		;94da
    inc a			;94dd
    jp z,05514h		;94de

## 17. line 3179 bank=24
    ld de,l8000h		;9618
    add hl,de			;961b
    ld bc,00202h		;961c
    pop de			;961f
    ld a,018h		;9620
    ld (0ffffh),a		;9622
    jp 05ad9h		;9625
    ld hl,0c200h		;9628
    bit 5,(hl)		;962b
    ret z			;962d
    ld a,(0c21ch)		;962e
    or a			;9631
    jr nz,l963ah		;9632

## 18. line 3261 bank=22
    bit 7,(hl)		;96af
    ret z			;96b1
    bit 6,(hl)		;96b2
    ret nz			;96b4
    ld a,016h		;96b5
    ld (0ffffh),a		;96b7
    ld a,(0c221h)		;96ba
    or a			;96bd
    jp nz,056f7h		;96be
    ld de,(0c238h)		;96c1
    ld hl,0c226h		;96c5
    ld b,000h		;96c8
    l96cah:

## 19. line 3348 bank=19
    add hl,de			;9739
    ex de,hl			;973a
    ld bc,00208h		;973b
    pop hl			;973e
    ld a,013h		;973f
    ld (0ffffh),a		;9741
    ld a,000h		;9744
    call 05b3eh		;9746
    ld hl,0c204h		;9749
    set 0,(hl)		;974c
    ld hl,0c222h		;974e
    inc (hl)			;9751
    ld a,(hl)			;9752

## 20. line 3589 bank=19
    ret z			;98e6
    ld a,(0c200h)		;98e7
    and 00ch		;98ea
    ret nz			;98ec
    ld a,013h		;98ed
    ld (0ffffh),a		;98ef
    ld a,(0c247h)		;98f2
    inc a			;98f5
    ld (0c247h),a		;98f6
    cp (hl)			;98f9
    ret nz			;98fa
    xor a			;98fb
    ld (0c247h),a		;98fc

## 21. line 3636 bank=19
    ret z			;992f
    ld a,(0c200h)		;9930
    and 00ch		;9933
    ret nz			;9935
    ld a,013h		;9936
    ld (0ffffh),a		;9938
    ld a,(0c24bh)		;993b
    inc a			;993e
    ld (0c24bh),a		;993f
    cp (hl)			;9942
    ret nz			;9943
    xor a			;9944
    ld (0c24bh),a		;9945

## 22. line 3805 bank=19
    or a			;9a66
    jr nz,l9aa2h		;9a67
    inc a			;9a69
    ld (0c20ah),a		;9a6a
    ld a,013h		;9a6d
    ld (0ffffh),a		;9a6f
    ld hl,la894h		;9a72
    ld de,04000h		;9a75
    call 0033dh		;9a78
    call 04be9h		;9a7b
    ld hl,0d100h		;9a7e
    ld de,0cc48h		;9a81
    ld b,002h		;9a84

## 23. line 3851 bank=12
    l9abch:
    ld a,(0c200h)		;9abc
    or a			;9abf
    ret nz			;9ac0
    ld a,00ch		;9ac1
    ld (0ffffh),a		;9ac3
    ld hl,l981bh+2		;9ac6
    ld de,04000h		;9ac9
    call 0033dh		;9acc
    xor a			;9acf
    ld (0c20ah),a		;9ad0
    ld hl,0c201h		;9ad3
    res 3,(hl)		;9ad6

## 24. line 3962 bank=19
    ld h,000h		;9b5a
    add hl,hl			;9b5c
    ld de,l8000h		;9b5d
    add hl,de			;9b60
    ld a,013h		;9b61
    ld (0ffffh),a		;9b63
    ld a,(hl)			;9b66
    inc hl			;9b67
    ld h,(hl)			;9b68
    ld l,a			;9b69
    ld e,(hl)			;9b6a
    inc hl			;9b6b
    ld d,(hl)			;9b6c

## 25. line 3982 bank=19
    ld h,(hl)			;9b74
    ld l,a			;9b75
    ret			;9b76
    ret			;9b77
    ld a,013h		;9b78
    ld (0ffffh),a		;9b7a
    ld hl,(0c23ah)		;9b7d
    ld h,000h		;9b80
    add hl,hl			;9b82
    ld de,lba8eh		;9b83
    add hl,de			;9b86
    ld a,(hl)			;9b87
    inc hl			;9b88

## 26. line 4004 bank=19
    ld (0c23fh),a		;9b98
    inc hl			;9b9b
    ld (0c23bh),hl		;9b9c
    ret			;9b9f
    ld a,013h		;9ba0
    ld (0ffffh),a		;9ba2
    xor a			;9ba5
    ld (0c23dh),a		;9ba6
    ld (0c23fh),a		;9ba9
    jp 05bbfh		;9bac
    l9bafh:
    ld a,013h		;9baf
    ld (0ffffh),a		;9bb1

## 27. line 4011 bank=19
    ld (0c23dh),a		;9ba6
    ld (0c23fh),a		;9ba9
    jp 05bbfh		;9bac
    l9bafh:
    ld a,013h		;9baf
    ld (0ffffh),a		;9bb1
    ld a,(0c23fh)		;9bb4
    or a			;9bb7
    l9bb8h:
    jr z,l9bbfh		;9bb8
    dec a			;9bba
    ld (0c23fh),a		;9bbb
    ret			;9bbe

## 28. line 4106 bank=22
    ld hl,0c200h		;9c2b
    ld a,(hl)			;9c2e
    and 0feh		;9c2f
    ret nz			;9c31
    ld a,016h		;9c32
    ld (0ffffh),a		;9c34
    ld a,(0c242h)		;9c37
    ld hl,05c40h		;9c3a
    jp 00020h		;9c3d
    l9c40h:
    ld c,h			;9c40
    ld e,h			;9c41
    ld h,h			;9c42

## 29. line 4213 bank=22
    ld hl,0c200h		;9d00
    ld a,(hl)			;9d03
    and 0feh		;9d04
    ret nz			;9d06
    ld a,016h		;9d07
    ld (0ffffh),a		;9d09
    ld a,(0c242h)		;9d0c
    ld hl,05d15h		;9d0f
    jp 00020h		;9d12
    rra			;9d15
    ld e,l			;9d16
    inc sp			;9d17
    ld e,l			;9d18

## 30. line 4301 bank=22
    ld hl,0c200h		;9db9
    ld a,(hl)			;9dbc
    and 0feh		;9dbd
    ret nz			;9dbf
    ld a,016h		;9dc0
    ld (0ffffh),a		;9dc2
    ld a,(0c242h)		;9dc5
    ld hl,05dceh		;9dc8
    jp 00020h		;9dcb
    call c,0fd5dh		;9dce
    ld e,l			;9dd1
    daa			;9dd2
    ld e,(hl)			;9dd3

## 31. line 4435 bank=22
    jr c,l9ec6h		;9ec1
    ld a,(iy+016h)		;9ec3
    l9ec6h:
    push af			;9ec6
    ld a,016h		;9ec7
    ld (0ffffh),a		;9ec9
    ld de,06a5bh		;9ecc
    call 05c16h		;9ecf
    pop af			;9ed2
    call 05c21h		;9ed3
    call 05c02h		;9ed6
    ld (0c206h),hl		;9ed9
    ld hl,0c200h		;9edc

## 32. line 4734 bank=22
    ld e,021h		;a04d
    nop			;a04f
    jp nz,0e67eh		;a050
    cp 0c0h		;a053
    ld a,016h		;a055
    ld (0ffffh),a		;a057
    ld a,(0c242h)		;a05a
    ld hl,06063h		;a05d
    jp 00020h		;a060
    ld l,l			;a063
    ld h,b			;a064
    add a,l			;a065
    ld h,b			;a066

## 33. line 4836 bank=22
    ld hl,0c200h		;a121
    ld a,(hl)			;a124
    and 0feh		;a125
    ret nz			;a127
    ld a,016h		;a128
    ld (0ffffh),a		;a12a
    ld a,(0c242h)		;a12d
    ld hl,06136h		;a130
    jp 00020h		;a133
    ld b,b			;a136
    ld h,c			;a137
    ld l,e			;a138
    ld h,c			;a139

## 34. line 4983 bank=22
    ld hl,0c200h		;a22b
    ld a,(hl)			;a22e
    and 0feh		;a22f
    ret nz			;a231
    ld a,016h		;a232
    ld (0ffffh),a		;a234
    ld a,(0c242h)		;a237
    ld hl,06240h		;a23a
    jp 00020h		;a23d
    ld c,d			;a240
    ld h,d			;a241
    ld e,l			;a242
    ld h,d			;a243

## 35. line 5121 bank=132
    jr nz,la32dh		;a32b
    la32dh:
    jr nc,la32fh		;a32d
    la32fh:
    ld a,084h		;a32f
    ld (0ffffh),a		;a331
    ld iy,0c460h		;a334
    ld b,005h		;a338
    la33ah:
    call 010a7h		;a33a
    ret nc			;a33d
    ld de,00020h		;a33e
    add iy,de		;a341
