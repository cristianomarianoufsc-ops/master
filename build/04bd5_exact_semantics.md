# 04BD5: semântica confirmada por disassembly

## Localização

Durante as chamadas de inicialização em `0x8AE6–0x8B04`, `FFFE=0x15` seleciona o banco físico 21 na janela `0x4000–0x7FFF`. Portanto, o endereço lógico `04BD5` corresponde ao offset `0x0BD5` do banco físico 21, que aparece no dump disassemblado como `0x8BD5`.

## Corpo da rotina

```asm
ld b,(hl)          ; count
inc hl
loop:
  ld e,(hl)        ; destination/source pointer, little endian
  inc hl
  ld d,(hl)
  inc hl
  ld a,(de)
  and (hl)
  jr z,no_match
  ld a,001h
no_match:
  exx
  ld (de),a
  inc de
  exx
  inc hl
  djnz loop
ret
```

A tabela começa com um contador e contém registros de três bytes: endereço de leitura, seguido de uma máscara. Para cada registro, a rotina lê o byte no endereço indicado, testa a máscara e produz `0x01` ou `0x00`. O resultado é gravado em um buffer sequencial apontado pelo `DE` do conjunto alternado de registradores. O `EXX` é essencial: o `DE` usado para ler os endereços da tabela e o `DE` usado para receber os resultados pertencem a conjuntos diferentes.

## Chamador

O chamador prepara sequências como:

```asm
ld de,0C032h
exx
ld hl,0AC47h
call 04BD5h
ld de,0C2B0h
exx
ld hl,0AC6Ch
call 04BD5h
```

Assim, não é seguro interpretar `DE` apenas pelo conjunto de registradores visível imediatamente antes do `call`. É necessário modelar o estado principal/alternado desde a entrada da rotina. A rotina `04BD5` não aplica diretamente máscaras em `D12x`; ela transforma testes de bits em bytes booleanos, que depois são consumidos por `04D16`.

## Consequência

A implementação de `04BD5` está resolvida no nível de instruções. A parte ainda pendente é reconstruir os valores iniciais dos dois conjuntos de `DE` no ponto `0x8ADF`, bem como a cadeia `04BBD -> 3954 -> RST 10h`, para gerar os buffers reais antes de executar `04D16`.
