# Consolidated dialogue-resolution graph

This report separates executable handlers from pointer tables and scene bytecode.

## handlers: build/dialog_handler_candidates.md
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



## chains: build/chain_5c02_finals.txt
build/chain_5c02_af55.md:final=0xB018 bytes=0011ff00120413ff0015ff0016ff00160011ff001200130819341aff00110819341aff0c22001200110819ff00120011341aff00120013ff0012001100190022
build/chain_5c02_b228.md:final=0xB404 bytes=0eb416b4d6b3e0b31ab492c2368680c2f68680c234838fc2768680c20f8724b480c2088a2ab48bc2598a80c2758a38b43cb444b480c2868ab4c2c28d80c2e68b
build/chain_5c02_b9ea.md:final=0xBAAA bytes=ff001c331dff00370038ff75bb79bb81bb91bb95bb91bb91bb99bba5bba5bb91bbadbb91bb91bb91bb91bbb5bb91bbc1bbc5bbd1bbf1bbfdbb09bc11bc0dbc0d


## primary: build/dialog_pointer_af55_bank22.md
C205=0x00 table=0xAF55 ptr=0xB015 len=3 hex=0014ff
C205=0x01 table=0xAF57 ptr=0xB018 len=3 hex=0011ff
C205=0x02 table=0xAF59 ptr=0xB01B len=5 hex=00120413ff
C205=0x03 table=0xAF5B ptr=0xB020 len=3 hex=0015ff
C205=0x04 table=0xAF5D ptr=0xB023 len=3 hex=0016ff
C205=0x05 table=0xAF5F ptr=0xB026 len=5 hex=00160011ff
C205=0x06 table=0xAF61 ptr=0xB020 len=3 hex=0015ff
C205=0x07 table=0xAF63 ptr=0xB02B len=9 hex=001200130819341aff
C205=0x08 table=0xAF65 ptr=0xB034 len=7 hex=00110819341aff
C205=0x09 table=0xAF67 ptr=0xB03B len=9 hex=0c22001200110819ff
C205=0x0A table=0xAF69 ptr=0xB020 len=3 hex=0015ff
C205=0x0B table=0xAF6B ptr=0xB044 len=7 hex=00120011341aff
C205=0x0C table=0xAF6D ptr=0xB034 len=7 hex=00110819341aff
C205=0x0D table=0xAF6F ptr=0xB04B len=5 hex=00120013ff
C205=0x0E table=0xAF71 ptr=0xB050 len=9 hex=0012001100190022ff
C205=0x0F table=0xAF73 ptr=0xB020 len=3 hex=0015ff
C205=0x10 table=0xAF75 ptr=0xB059 len=9 hex=00110019001a0e20ff
C205=0x11 table=0xAF77 ptr=0xB062 len=3 hex=0012ff
C205=0x12 table=0xAF79 ptr=0xB065 len=3 hex=0023ff
C205=0x13 table=0xAF7B ptr=0xB068 len=9 hex=001200130019001aff
C205=0x14 table=0xAF7D ptr=0xB071 len=3 hex=0a24ff
C205=0x15 table=0xAF7F ptr=0xB074 len=3 hex=0025ff
C205=0x16 table=0xAF81 ptr=0xB077 len=7 hex=0024002a332bff
C205=0x17 table=0xAF83 ptr=0xB020 len=3 hex=0015ff
C205=0x18 table=0xAF85 ptr=0xB07E len=11 hex=002e002f003000310032ff
C205=0x19 table=0xAF87 ptr=0xB07E len=11 hex=002e002f003000310032ff
C205=0x1A table=0xAF89 ptr=0xB07E len=11 hex=002e002f003000310032ff
C205=0x1B table=0xAF8B ptr=0xB07E len=11 hex=002e002f003000310032ff
C205=0x1C table=0xAF8D ptr=0xB07E len=11 hex=002e002f003000310032ff
C205=0x1D table=0xAF8F ptr=0xB07E len=11 hex=002e002f003000310032ff
C205=0x1E table=0xAF91 ptr=0xB07E len=11 hex=002e002f003000310032ff
C205=0x1F table=0xAF93 ptr=0xB07E len=11 hex=002e002f003000310032ff
C205=0x20 table=0xAF95 ptr=0xB07E len=11 hex=002e002f003000310032ff
C205=0x21 table=0xAF97 ptr=0xB07E len=11 hex=002e002f003000310032ff
C205=0x22 table=0xAF99 ptr=0xB07E len=11 hex=002e002f003000310032ff
C205=0x23 table=0xAF9B ptr=0xB07E len=11 hex=002e002f003000310032ff
C205=0x24 table=0xAF9D ptr=0xB07E len=11 hex=002e002f003000310032ff
C205=0x25 table=0xAF9F ptr=0xB07E len=11 hex=002e002f003000310032ff
C205=0x26 table=0xAFA1 ptr=0xB07E len=11 hex=002e002f003000310032ff
C205=0x27 table=0xAFA3 ptr=0xB07E len=11 hex=002e002f003000310032ff
C205=0x28 table=0xAFA5 ptr=0xB07E len=11 hex=002e002f003000310032ff
C205=0x29 table=0xAFA7 ptr=0xB07E len=11 hex=002e002f003000310032ff
C205=0x2A table=0xAFA9 ptr=0xB07E len=11 hex=002e002f003000310032ff
C205=0x2B table=0xAFAB ptr=0xB07E len=11 hex=002e002f003000310032ff
C205=0x2C table=0xAFAD ptr=0xB07E len=11 hex=002e002f003000310032ff
C205=0x2D table=0xAFAF ptr=0xB07E len=11 hex=002e002f003000310032ff
C205=0x2E table=0xAFB1 ptr=0xB07E len=11 hex=002e002f003000310032ff
C205=0x2F table=0xAFB3 ptr=0xB07E len=11 hex=002e002f003000310032ff
C205=0x30 table=0xAFB5 ptr=0xB07E len=11 hex=002e002f003000310032ff
C205=0x31 table=0xAFB7 ptr=0xB074 len=3 hex=0025ff
C205=0x32 table=0xAFB9 ptr=0xB089 len=3 hex=002aff
C205=0x33 table=0xAFBB ptr=0xB08C len=3 hex=133aff
C205=0x34 table=0xAFBD ptr=0xB123 len=1 hex=ff
C205=0x35 table=0xAFBF ptr=0xB08F len=5 hex=0011063cff
C205=0x36 table=0xAFC1 ptr=0xB094 len=7 hex=00120013063cff
C205=0x37 table=0xAFC3 ptr=0xB09B len=5 hex=00160011ff
C205=0x38 table=0xAFC5 ptr=0xB0A0 len=3 hex=0115ff
C205=0x39 table=0xAFC7 ptr=0xB0A3 len=5 hex=05160511ff
C205=0x3A table=0xAFC9 ptr=0xB0A8 len=5 hex=00120011ff
C205=0x3B table=0xAFCB ptr=0xB0AD len=7 hex=09120911093dff
C205=0x3C table=0xAFCD ptr=0xB0B4 len=5 hex=0015133eff
C205=0x3D table=0xAFCF ptr=0xB020 len=3 hex=0015ff
C205=0x3E table=0xAFD1 ptr=0xB0B9 len=7 hex=00120011003cff
C205=0x3F table=0xAFD3 ptr=0xB0C0 len=9 hex=00120011003d1541ff
C205=0x40 table=0xAFD5 ptr=0xB0C9 len=5 hex=00420043ff


## external: build/bd55_external_ref_targets.txt
## 88c2
bank=22 cpu=0x88C2 file=0x0588C2 bytes=88c201029700020605100002980000060510000299000006051000fb16f660c4583c010005100002230300060510000224030d06051000fe89c2010296000006
## 85e5
bank=22 cpu=0x85E5 file=0x0585E5 bytes=0242000106051000fe88c2010245000106051000feb4c2010244000106051000feb3c201f151c21fff0904fc0e0306050400022c0300060510000104fc0f0308
## 8bc2
bank=22 cpu=0x8BC2 file=0x058BC2 bytes=0102ce000206051000010102d00000ee9705080006050400fb18051000fee4c2fdb2c20104fc18030d05100002d20000060510000104fc19030d05100002d200
## 81f4
bank=22 cpu=0x81F4 file=0x0581F4 bytes=021700010605100001022a00000605100001050400ff140225000006051000010238000206051000021900010605100001021800020605100002190001060510
## 8020
bank=22 cpu=0x8020 file=0x058020 bytes=c79b089d189d289d389d8f9dd29d209e4f9d509f629f729f909fa09fb89fc89feb9ffb9f0ba01ba02ba0b2a11fa237a247a259a228944e945fa3e1a547a657a6
## 97c2
bank=22 cpu=0x97C2 file=0x0597C2 bytes=9c070605100002150300060510000239010006051000fa06021f030006051000f2021603000605100002170302050400ee9b0706051000021803000605100002
## 8a97
bank=22 cpu=0x8A97 file=0x058A97 bytes=02b1000f060510000102b3000e060510000102b400000605100002b5000f06051000feb0c20102b600020605100002b700000605100002b800020605100002bb
## 8fc2
bank=22 cpu=0x8FC2 file=0x058FC2 bytes=03000605100002e200000605100002ea000006051000fa06f2021603000605100002170302050400ee9b0706051000021803000605100002e200000605100002
## 9380
bank=22 cpu=0x9380 file=0x059380 bytes=02010102060510000202010e060510000102030100060510000102ee000006050400eea30510000204010f060510000102050100060510000206010f06051000


## findings: build/static_script_findings.md
# Descobertas estáticas — etapa de streams

O loop de exibição em `bank21.asm` nas rotinas `0x96CA–0x9779` usa `0xC238` como ponteiro inicial e `0xC223` como ponteiro de avanço. O byte `0xFF` encerra o stream. O byte `0x00` é ignorado como espaço/controle. Para outros bytes, a rotina consulta a tabela RAM `0xC280 + código`; se a entrada for zero, o código é pulado. Códigos aceitos são convertidos em um endereço de glifo por `código * 0x40` somado à base `lad0c`, e enviados a `0xC86E` via a rotina `0x5B3E`.

Os handlers do banco 21 selecionam dados em múltiplas tabelas. Em vários casos, o banco `0x16` é selecionado antes de acessar endereços CPU `0x5F40`, `0x5F7E`, `0x6046`, `0x61FB`, `0x6867`, `0x6A5B`, `0x6E33`, `0x6F47`, `0x70D3` e `0x789D`. No banco 22, a região `0x5F40` contém streams estruturados com comandos e parâmetros, com padrões frequentes `05 10 00`, `06 05 10 00`, `FC`, `FE`, `FB` e `EE`; portanto ela não deve ser tratada como texto plano.

A rotina `0x9E70` copia `0xA14` bytes de `0x5F7E` para RAM `0xCF00`, depois seleciona registros de quatro bytes a partir de `0x6046`, indexados por `0xC205`. Isso indica um bloco de scripts/objetos de cena, com dados de mensagem provavelmente referenciados por comandos ou subregistros.

A máscara `0xC280` é zerada em `0x8A73`; a inicialização seguinte preenche `0xC281` com uma faixa de códigos definida por dados em `0xAC0B`, e inicializa outras tabelas RAM em `0xC2B0`, `0xC2D0` e `0xC2E0`. As etiquetas `0xAC0B–0xACD5` são tabelas binárias, apesar do disassembler as mostrar como instruções.

O extrator `tools/extract_pair_streams.py` que tratava os dados como pares gerou muitos falsos candidatos porque os streams do banco 22 misturam comandos, ponteiros e parâmetros. O próximo extrator deve modelar os comandos (`FC/FE/FB/EE` e blocos `05 10 00`/`06 05 10 00`) antes de procurar caracteres.

## Mapeamento de paginação adicional

O relatório `build/bank_switch_contexts.md` encontrou 35 contextos de escrita no registrador `0xFFFF`. Em particular, o fluxo inicial alterna entre os bancos 12, 19, 22 e 23; durante a inicialização de tabelas em `0x8A0A–0x8B0A`, o banco 19 é selecionado antes de consultas a tabelas compactadas. Os endereços lógicos `0x5C02`, `0x5C16` e `0x5C21` não identificam uma única rotina física: os bytes variam conforme o banco paginado. O banco 22 contém scripts nessa faixa, enquanto o banco 1 apresenta código/tabelas auxiliares e o banco 19 apresenta dados compactados. Qualquer extrator definitivo deve carregar o banco físico indicado pelo último valor escrito em `0xFFFF` antes de interpretar um endereço CPU entre `0x4000` e `0x7FFF`.

Foi gerado também `build/scene_index_and_records.txt`, contendo os bytes da região `0x5F4C` e dos registros em `0x6046` no banco 22. A região não é uma tabela de ponteiros simples; sua interpretação depende da rotina paginada e do estado de cena.

## Verificação visual de lad0c

Foi gerada uma folha de 64 blocos de 64 bytes a partir de `lad0c` no banco 21 (`build/lad0c_glyphs.png`) e outra no banco 22 (`build/lad0c_bank22_glyphs.png`). Ambas aparecem como padrões densos e não como uma fonte japonesa reconhecível quando interpretadas diretamente em 4bpp planar. Isso indica que `lad0c` não deve ser tratado como uma folha de fonte ROM simples; pode ser uma região remapeada, uma tabela intermediária ou um formato de tiles diferente. O loop seleciona o banco 22 imediatamente antes do processamento, mas a comparação visual ainda não confirmou uma fonte nesse endereço.

## Rotina 05B3E

As chamadas `call 05B3Eh` aparecem no banco 21 durante a montagem de tiles, mas o endereço é paginado e não foi encontrado como rotina independente no banco fixo. A faixa equivalente no banco 1 contém handlers de estado, não uma cópia genérica de fonte. A operação deve ser resolvida junto com o valor vigente do registrador `0xFFFF` e com o dispatcher de objetos; interpretar `05B3E` como endereço fixo gera conclusões erradas.

## Banco físico da cópia de glifos

No loop `0x9726–0x9746`, o código calcula a origem `lad0c`, prepara o destino em `0xC86E` e, imediatamente antes de `call 05B3Eh`, escreve `0x13` em `0xFFFF`. Portanto, a origem `lad0c` nessa operação deve ser lida no banco 13, não nos bancos 21 ou 22. A folha correspondente foi gerada em `build/lad0c_bank13_glyphs.png`; a interpretação visual direta ainda não é suficiente para confirmar o formato, mas o banco físico correto está estabelecido.

## Parser refinado do stream de cena

A listagem `build/scene_stream_command_parse.csv` cobre `0x5F40–0x633F` no banco 22. A região apresenta padrões recorrentes como `FC xx yy`, `05 10 00`, `06 05 10 00` e marcadores `FB/FD/FE/FF`. Esses padrões indicam um bytecode de cena com comandos e parâmetros variáveis, não uma sequência de caracteres japonesa linear. O parser foi mantido conservador: ele classifica bytes sem substituir comandos por texto nem assumir comprimentos que ainda não foram validados.

## Banco 22 e C280

O disassembly automático do banco 22 contém referências a `0xC280`, mas muitos trechos próximos são identificados como instruções inválidas ou dados mistos. Isso é consistente com estruturas de cena compactadas intercaladas com pequenos handlers, e não com um bloco de código linear. O arquivo `build/bank22_c280_handlers.txt` preserva os contextos encontrados. Os vetores em `0x8000` continuam sendo os pontos de entrada confiáveis para uma análise dirigida.

## Vetores dirigidos do banco 22

A tabela em `0x8000` do banco 22 aponta para handlers em `0x8080`, `0x80BD`, `0x8236`, `0x82B6`, `0x9561`, `0x98CA`, `0x9910`, `0x9A01`, `0x9BC7`, `0x9D08–0x9E20` e `0x9F50–0x9FC8`. A faixa `0x9D08–0x9FC8` contém bytecode de cena com padrões `FC`, `FB`, `FD`, `FE`, `FF` e comandos `05 10 00`/`06 05 10 00`, não código Z80 linear. O relatório completo está em `build/vector_guided_bank22.md`.

## Candidatos de ativação de texto

A análise `build/scene_text_activation_candidates.txt` encontrou ocorrências recorrentes de `05 10 00` e `06 05 10 00`, além de padrões `F480C2` e transições `FB/FE/FD`. Esses bytes aparecem dentro de registros de cena e não foram tratados como caracteres. Eles são candidatos a comandos/índices que levam ao sistema de texto, mas ainda exigem confirmação pelo fluxo de execução e pelas variáveis `C223/C238`.

## Carregamento de C280

A inicialização em `0x8C5E–0x8CA9` usa `04CFD` e `04D16` para processar as tabelas `AC31`, `AC0B`, `AC6C`, `ACB5`, `ACBC` e `ACD5`, escrevendo resultados em RAM (`C280`, `C2B0`, `C2D0`, `C2E0` e outras áreas). As implementações não aparecem diretamente no banco 1 nos offsets homônimos; são chamadas paginadas/trampolines dependentes da janela ativa. Portanto, C280 é uma tabela construída em tempo de execução, e não um bloco ROM simples.

## Rotinas de reconstrução AC0B/AC31

O trecho do banco 21 em `0x8CFD–0x8D2D` lê entradas de dois bytes, acessa endereços derivados e combina máscaras por rota (`OR`, `CPL`, `AND`) para escrever resultados de volta na memória. Isso é compatível com a construção de tabelas filtradas em RAM, não com uma simples cópia linear. As chamadas `04CFD` e `04D16` devem ser analisadas como entradas paginadas para esse tipo de transformação.

## Separação correta dos slots SMS

A arquitetura de paginação usa registradores distintos: `FFFE` controla a janela CPU `0x4000–0x7FFF`, onde ficam as rotinas chamadas por endereços como `04CFD`, `04D16`, `04BBD` e `05B3E`; `FFFF` controla a janela `0x8000–0xBFFF`, onde o loop acessa `lad0c` e os dados do banco 13. Assim, a rotina de cópia e a fonte podem estar em bancos físicos diferentes simultaneamente. A implementação anterior de `map_dual_slots.py` precisa ser estendida para rastrear `C20E/FFFE` e `FFFF` separadamente por fluxo.

## Resolução dual-slot das chamadas

O relatório `build/dual_slot_call_resolution.md` encontrou 33 chamadas relevantes no banco 21. Nas rotinas de inicialização, `FFFF=0x19` acompanha as chamadas `04BBD`, `04CFD` e `04D16`, confirmando que esse registrador seleciona a janela de dados em `0x8000–0xBFFF`. Durante a montagem de glifos, `FFFF=0x19` também está ativo antes de `05B3E`; a origem `lad0c` foi calculada enquanto `FFFF=0x16` em uma etapa anterior, indicando que o acesso é restaurado/trocado entre etapas. O rastreador não consegue inferir FFFE apenas de escritas no banco 21 porque seu valor é atualizado pelo loop principal e por interrupções; esse é o próximo dado a resolver.

## Fontes de C02B/FFFE

`sub_1014` seleciona temporariamente `FFFF=0x92`, consulta uma tabela via `RST 10h` e obtém o valor de banco em `C02B/C02C`; mais tarde esse valor é aplicado a `FFFE`. Outros estados fixos atribuem `C02B=0x95`. Assim, o slot de código `0x4000–0x7FFF` durante `05B3E` pode ser `0x92`, `0x95` ou um valor derivado da tabela, não necessariamente banco 1. O contexto de execução em `0x9746` ainda precisa ser conectado ao estado imediatamente anterior do loop.

## Descoberta decisiva: 05B3E no banco físico 0x15

Como `C02B=0x95` corresponde ao banco físico `0x15` sob a máscara de 5 bits do mapper, o endereço CPU `0x5B3E` foi localizado no banco 21. A rotina em `0x5B3E` executa cinco iterações: preserva `BC/DE`, usa `LDI` para consumir bytes de `HL`, grava o byte alternando com `EX AF,AF'`, incrementa `DE`, e depois avança a origem em `0x40` bytes. Em termos funcionais, ela copia uma coluna/linha de cada glifo de 64 bytes para um buffer intercalado, exatamente a transformação esperada antes da VRAM. O trecho confirmado é `0x5B3E–0x5B58`; os dados seguintes começam em `0x5B59`.

A fonte `lad0c` está, portanto, organizada em blocos de `0x40` bytes, e o destino `C86E+offset` recebe a forma intercalada. Esta é a primeira confirmação direta do formato de glifo usado pelo jogo.

## Emulação de 05B3E e stride da fonte

O loop em `0x9720–0x9726` multiplica o código por `0x10`, portanto cada entrada inicial em `lad0c` ocupa 16 bytes, não 64. A rotina `05B3E` consome dois grupos de oito bytes, escreve cada byte com espaçamento de dois e separa as passagens por `0x40` no destino. A emulação foi corrigida para stride `0x10`; a renderização ainda não é legível, indicando ordem de planos/linhas diferente da interpretação preliminar.

## Teste de lad0c no banco físico 19

Como `FFFF=0x13` está ativo antes de `05B3E`, foram testadas as entradas de `lad0c` no banco físico 19, usando stride `0x10` e a transformação da rotina confirmada. A renderização (`build/lad0c_bank19_transformed.png`) mostra padrões regulares, mas não glifos legíveis. Isso sugere que `lad0c` pode ser uma tabela intermediária/índices ou que ainda falta a ordem final de planos usada pela rotina de VRAM. Os testes anteriores no banco 13 também foram preservados para comparação.

## Comparação com a fonte comprimida em 0x3181D

O stream em `0x3181D` começa com dados gráficos densos (`09 00 C2 20 7C...`), enquanto `lad0c` no banco físico 19 começa com registros esparsos e muitos zeros (`00 34 00 00...`, `02 14 03...`, `1A 15 0D...`). Portanto, `lad0c` não é uma cópia direta do stream comprimido da fonte. Ele provavelmente é uma tabela de índices/descritores ou uma estrutura específica de cena que aponta para glifos/recursos. A fonte comprimida identificada anteriormente continua sendo o candidato para a fonte gráfica final.

## Fonte comprimida e transferência para VRAM

`sub_0303` e `sub_033D` não constroem a tabela `lad0c`; são rotinas de transferência para o VDP. Em `0x44DE–0x44E9`, o jogo seleciona `FFFF=0x8C`, usa `HL=0x981D` e transfere o stream comprimido da fonte para o destino VDP associado a `DE=0x6380`. A rotina lê comandos RLE/VDP e escreve os bytes diretamente no porto de dados. Isso confirma que o stream em ROM `0x3181D` é uma fonte gráfica carregada diretamente à VRAM, enquanto `lad0c` é uma estrutura posterior/alternativa usada pelo fluxo de glifos.

## Semântica confirmada do loop de texto

Em `0x96CA–0x96E6`, cada byte do stream em `C238` é consultado em `C280[byte]`; bytes com entrada zero não são copiados para o buffer de índices, enquanto bytes aceitos incrementam o contador `B`. Em `0x96F7–0x9719`, o mesmo filtro é aplicado ao stream em `C223`: quando `C280[byte]` é não zero, o byte é usado como índice de glifo; quando é zero, o cursor avança e o byte é descartado. `FF` encerra o stream. O código de glifo usado em `0x9720` é exatamente o byte aceito, multiplicado por `0x10` para indexar a estrutura apontada por `lad0c`.

## Implementação exata de 04CFD/04D16

A rotina física foi localizada no banco 21 em `0x4CFD`/`0x4D16`. `04CFD` lê o contador de entradas em `(HL)`, percorre pares de endereços `(DE)` e aplica uma máscara selecionada por `C`, usando `OR` ou `CPL/AND`, gravando o resultado de volta em cada endereço. `04D16` percorre uma estrutura semelhante, alterna para o banco/registradores auxiliares e extrai valores para RAM. A inicialização em `0x4C5E–0x4C7A` chama essas rotinas sobre `AC31` e `AC0B`, e a tabela resultante em `C280` é usada pelo loop de texto para distinguir glifos de comandos.

## Primeiro emulador de tabelas de máscaras

`emulate_c280_tables.py` foi executado sobre `AC31` com estado inicial zerado e gerou `build/emulated_c280_state.txt`. O resultado valida a leitura de registros e a aplicação de máscaras, mas não representa ainda o `C280` real do jogo: as tabelas dependem de valores de runtime como `C205`, `C215`, `C225` e de estruturas auxiliares `AC0B/AC31`. O emulador será usado como base para uma versão que receba esses estados reais.

## Relação entre C205 e streams de cena

O handler `0x9E70` usa `C205-0x18`, multiplica por dois e consulta a tabela `0x5F4C`; em seguida usa o valor como deslocamento relativo a `0x6046` e copia `0x0A14` bytes para `0xCF00`. Para `C205` entre `0x18` e `0x30`, o handler `0x9DED` escolhe `0x5F45` como origem alternativa; caso contrário, usa `0x5F40`. Isso confirma que os streams de cena são carregados para RAM antes do processamento, e que o texto deve ser extraído do buffer copiado em `CF00/C223/C238`, não apenas da tabela ROM original.

## Diferenças entre buffers CF00 por C205

A comparação dos 25 buffers mostrou que todos compartilham a mesma base de `0x0A14` bytes. As diferenças estão somente em oito ou dez posições dentro dos primeiros `0xC2` bytes, onde os registros `8A18 8A1A` e `8A1C 8A1E` são escritos em destinos `CF00+offset` e `CF10+offset`. Logo, `C205` reposiciona registros de parâmetros dentro de uma estrutura comum; não seleciona diretamente um diálogo diferente. O texto/bytecode principal permanece na base copiada de `5F7E`.

## Estrutura interna de 5F7E/CF00

A região copiada por `0x9E70` contém uma estrutura de objetos/handlers: há chamadas a `5C16`, `5C21`, `5C02` e `5B59`, além de tabelas de ponteiros em `0x6200–0x6800` e entradas associadas a `C280/C2xx` em torno de `0x654E`. Portanto, o bloco CF00 é bytecode e dados de objetos, não um stream de diálogo isolado. A extração textual deve seguir os handlers internos até o ponto em que eles configuram `C223/C238`.

## Handlers de diálogo identificados

O cruzamento de `5Cxx` mostrou que os candidatos mais fortes são `0x9C4F`, `0x9D22`, `0x9D94`, `0x9E3E`, `0xA070` e rotinas vizinhas. `0x9C4F` e `0x9D22` chamam `05C16` e gravam diretamente o resultado em `C223/C238`; `0x9C78`, `0x9D4C`, `0x9D94`, `0x9E3E`, `0x9ECF` e `0xA094` chamam `05C16` seguido de `05C02`, preparando ponteiros em `C206`. Esses endereços são os pontos de entrada prioritários para resolver streams de diálogo.

## Estrutura encadeada de BD55

O stream `BD55` selecionado por `05C16` contém 37 bytes e termina em `FF`. As palavras `BE19`, `BE25`, `BE31` e `BE35` apontam para offsets internos do próprio bloco; outras palavras apontam para tabelas/handlers em `0x8000–0xBFFF`. Portanto, `BD55` é uma lista de sub-registros encadeados, não uma sequência de caracteres. O relatório detalhado está em `build/bd55_internal_refs.md`.

## Verificação dos sub-registros BD55

A inspeção física de `0xBE15–0xBE45` confirmou que `BE19`, `BE25`, `BE31` e `BE35` são referências internas ao mesmo bloco de parâmetros; após `0xBE3A` há uma sequência de `FF`. Assim, BD55 representa um registro curto de configuração/estado, e não um stream de diálogo. O candidato de texto precisa ser buscado nas tabelas apontadas pelos words `0x88C2`, `0x85E5`, `0x8BC2`, `0x81F4` e similares.

## Opcode dos alvos BD55

A faixa `0x81F4–0x97C2` no banco 22 contém 64 ocorrências de `EE`, 27 de `FB`, 80 de `FC`, 31 de `FD`, 75 de `FE` e 18 de `FF`. Os contextos mostram bytecode de comandos com parâmetros e referências a `C2xx`, não strings de caracteres. Os handlers de diálogo continuam sendo os pontos do banco 21 que resolvem ponteiros via `05C16`; os alvos BD55 externos são bytecode de estado/objeto.

## Tabela BAAA

`BAAA` não é uma tabela de pares compatível diretamente com `05C02`: começa com registros de bytecode (`FF`, `001C331DFF`, `00370038FF`) e depois contém ponteiros para handlers em `BBxx/BCxx`. O resolvedor de `05C02` deve ser aplicado apenas às tabelas que começam com listas de ponteiros; BAAA requer o dispatcher próprio.
