# Dialogue handler candidates

bank=21

## handler 0x9C4F
	ld e,h			;9c43
	adc a,d			;9c44
	ld e,h			;9c45
	jp z,0ff5ch		;9c46
	ld e,h			;9c49
	rst 38h			;9c4a
	ld e,h			;9c4b
	ld de,laf55h		;9c4c
	call 05c16h		;9c4f
	ld (0c223h),de		;9c52
	ld (0c238h),de		;9c56
	ld hl,0c200h		;9c5a
	set 7,(hl)		;9c5d
	ld hl,0c242h		;9c5f
	inc (hl)			;9c62
	ret			;9c63
	ld a,(0c222h)		;9c64
	cp 0ffh		;9c67
	jr z,l9c70h		;9c69
	ld hl,0c242h		;9c6b
	inc (hl)			;9c6e
l9c6fh:
	ret			;9c6f
l9c70h:

## handler 0x9C78
	ld hl,0c242h		;9c6b
	inc (hl)			;9c6e
l9c6fh:
	ret			;9c6f
l9c70h:
	ld hl,0c200h		;9c70
	res 0,(hl)		;9c73
	ld de,lb124h		;9c75
	call 05c16h		;9c78
	ex de,hl			;9c7b
	call 05c02h		;9c7c
	ld (0c206h),hl		;9c7f
	xor a			;9c82
	ld (0c241h),a		;9c83
	ld (0c242h),a		;9c86
	ret			;9c89
	ld a,004h		;9c8a
	ld (0c3a0h),a		;9c8c
	ld a,(0c3a7h)		;9c8f
	or a			;9c92
	ret z			;9c93
	ld a,(0c005h)		;9c94
	bit 4,a		;9c97
l9c99h:

## handler 0x9D22
	ld e,l			;9d18
	ld e,(hl)			;9d19
	ld e,l			;9d1a
	sub c			;9d1b
	ld e,l			;9d1c
	cp b			;9d1d
	ld e,l			;9d1e
	ld de,lb9eah		;9d1f
	call 05c16h		;9d22
	ld (0c223h),de		;9d25
	ld hl,0c200h		;9d29
	set 7,(hl)		;9d2c
	ld hl,0c242h		;9d2e
	inc (hl)			;9d31
	ret			;9d32
	ld a,(0c222h)		;9d33
	cp 0ffh		;9d36
	jr z,l9d44h		;9d38
	ld a,004h		;9d3a
	ld (0c3a0h),a		;9d3c
	ld hl,0c242h		;9d3f
	inc (hl)			;9d42
	ret			;9d43
l9d44h:

## handler 0x9D4C
	ld (0c3a0h),a		;9d3c
	ld hl,0c242h		;9d3f
	inc (hl)			;9d42
	ret			;9d43
l9d44h:
	ld hl,0c200h		;9d44
	res 0,(hl)		;9d47
	ld de,0bab5h		;9d49
	call 05c16h		;9d4c
	ex de,hl			;9d4f
	call 05c02h		;9d50
	ld (0c206h),hl		;9d53
	xor a			;9d56
	ld (0c241h),a		;9d57
	ld (0c242h),a		;9d5a
	ret			;9d5d
	ld a,(0c005h)		;9d5e
	bit 4,a		;9d61
	jr nz,l9d7eh		;9d63
	bit 5,a		;9d65
	ret z			;9d67
	ld a,0b8h		;9d68
	ld (0dd04h),a		;9d6a
	ld hl,0c200h		;9d6d

## handler 0x9D94
	xor a			;9d83
l9d84h:
	ld (0c3a0h),a		;9d84
	ld (0c3a7h),a		;9d87
	ld (0c242h),a		;9d8a
	ld (0c241h),a		;9d8d
	ret			;9d90
	ld de,lbd55h		;9d91
	call 05c16h		;9d94
	ld a,(0c3b5h)		;9d97
	call 05c21h		;9d9a
	call 05c02h		;9d9d
	ld (0c206h),hl		;9da0
	ld hl,0c200h		;9da3
	res 0,(hl)		;9da6
	set 4,(hl)		;9da8
	ld hl,00008h		;9daa
	ld (0c218h),hl		;9dad
	xor a			;9db0
	ld (0c241h),a		;9db1
	ld (0c242h),a		;9db4
	ret			;9db7
	ret			;9db8
	ld hl,0c200h		;9db9

## handler 0x9E3E
	ld a,003h		;9e31
	ld (0c380h),a		;9e33
	ld hl,0c242h		;9e36
	inc (hl)			;9e39
	ret			;9e3a
l9e3bh:
	ld de,06867h		;9e3b
l9e3eh:
	call 05c16h		;9e3e
	ex de,hl			;9e41
	call 05c02h		;9e42
	ld (0c206h),hl		;9e45
	ld hl,0c200h		;9e48
	res 0,(hl)		;9e4b
	set 4,(hl)		;9e4d
	ld hl,00008h		;9e4f
	ld (0c218h),hl		;9e52
	xor a			;9e55
	ld (0c241h),a		;9e56
	ld (0c242h),a		;9e59
	ret			;9e5c
l9e5dh:
	ld hl,0c200h		;9e5d
	set 6,(hl)		;9e60

## handler 0x9ECF
	ld a,000h		;9ebf
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
	res 0,(hl)		;9edf
	set 4,(hl)		;9ee1
	ld hl,00008h		;9ee3
	ld (0c218h),hl		;9ee6
	xor a			;9ee9
	ld (0c241h),a		;9eea
	ld (0c242h),a		;9eed
	ret			;9ef0
	ret			;9ef1
l9ef2h:

## handler 0xA070
	add a,l			;a065
	ld h,b			;a066
	or e			;a067
	ld h,b			;a068
	ret p			;a069
	ld h,b			;a06a
	jr nz,$+99		;a06b
	ld de,06e33h		;a06d
	call 05c16h		;a070
	ld (0c223h),de		;a073
	ld (0c238h),de		;a077
	ld hl,0c200h		;a07b
	set 7,(hl)		;a07e
	ld hl,0c242h		;a080
	inc (hl)			;a083
la084h:
	ret			;a084
	ld a,(0c222h)		;a085
	cp 0ffh		;a088
	jr z,la091h		;a08a
	ld hl,0c242h		;a08c
	inc (hl)			;a08f
la090h:
	ret			;a090

## handler 0xA094
	cp 0ffh		;a088
	jr z,la091h		;a08a
	ld hl,0c242h		;a08c
	inc (hl)			;a08f
la090h:
	ret			;a090
la091h:
	ld de,06f47h		;a091
	call 05c16h		;a094
	ex de,hl			;a097
	call 05c02h		;a098
	ld (0c206h),hl		;a09b
	ld hl,0c200h		;a09e
	res 0,(hl)		;a0a1
	set 4,(hl)		;a0a3
	ld hl,00008h		;a0a5
	ld (0c218h),hl		;a0a8
	xor a			;a0ab
	ld (0c241h),a		;a0ac
	ld (0c242h),a		;a0af
	ret			;a0b2
	ld a,004h		;a0b3
	ld (0c3a0h),a		;a0b5
	ld a,(0c3a7h)		;a0b8
