# 04BBD: produtor exato de máscaras de bits

## Localização e papel

Na ROM fornecida, a rotina está no banco físico 21, na janela de código `0x4000–0x7FFF`, no endereço lógico `0x4BBD`. O fluxo de inicialização chama essa rotina com `FFFF=0x13`, portanto as tabelas apontadas por `HL` estão no banco físico 19, na janela `0x8000–0xBFFF`.

A rotina é usada para converter tabelas de testes `(endereço de RAM, máscara)` em um único byte de flags. Ela não lê valores diretamente da ROM como se fossem flags: cada registro aponta para uma posição de RAM que precisa ser fornecida pelo estado de execução.

## Disassembly confirmado

```asm
4BBD  ld b,(hl)          ; número de registros
4BBE  inc hl
4BBF  xor a              ; acumulador de saída = 0
4BC0  ex af,af'
4BC1  ld c,01h           ; bit corrente = 1
4BC3  ld e,(hl)          ; endereço da RAM, little-endian
4BC4  inc hl
4BC5  ld d,(hl)
4BC6  inc hl
4BC7  ld a,(de)          ; lê RAM[endereço]
4BC8  and (hl)           ; testa a máscara do registro
4BCA  jr z,4BCEh
4BCB  ex af,af'
4BCC  or c               ; ativa o bit corrente
4BCD  ex af,af'
4BCE  inc hl              ; próximo registro
4BCF  rlc c               ; próximo bit: 1, 2, 4, ...
4BD1  djnz 4BC3h
4BD3  ex af,af'
4BD4  ret                 ; A = máscara compactada
```

O acumulador é protegido por `EX AF,AF'` enquanto `A` é usado para ler a RAM. O registrador `C` percorre os bits por `RLC C`. Portanto, para uma tabela com até oito registros, o registro `i` contribui com `1 << i` quando `(RAM[endereço] & máscara) != 0`.

## Chamadores relevantes

A inicialização em `0x4A8D–0x4B0D` faz as seguintes consultas, todas com tabelas no banco 19:

| Tabela | Destino | Função observada |
|---|---:|---|
| `AB89` | `DE`/comparação | produz a parcela baixa de uma assinatura de estado |
| `ABA2` | `DE`/comparação | produz a parcela alta e valida o estado |
| `ABBB` | `C022` | produz flag de banco/estado |
| `ABC5` | `C025` | produz flag de estado |
| `ABDE` | `C026` | produz flag de estado |
| `ABE5` | `C027` | produz flag de estado |
| `ABFE` | `C028` | produz flag de estado |
| `AC1E` | `C215` | produz flag de estado |
| `AC31` | `C205` | seleciona o índice de cena/tabela |
| `AC0B` | `C281[0..A-1]` | define a faixa inicial de códigos aceitos |
| `ACD5` | `C251` | produz flag de estado adicional |

A sequência de código relevante é:

```asm
4A8D  ld hl,ABBBh
4A90  call 04BBDh
4A93  ld (C022h),a
...
4AC3  ld hl,AC31h
4AC6  call 04BBDh
4AC9  ld (C205h),a
4ACC  ld hl,AC0Bh
4ACF  call 04BBDh
4AD2  ld hl,C281h
4AD5  ld b,a
4AD6  or a
4AD9  ld a,01h
4ADB  ld (hl),a
4ADC  inc hl
4ADD  djnz 4ADBh
```

Depois disso, `04BD5` transforma os testes das tabelas `AC47`, `AC6C`, `ACB5` e `ACBC` em buffers booleanos destinados a `C032`, `C2B0`, `C2D0` e `C2E0`. As rotinas `04CFD` e `04D16` então combinam esses buffers para construir as tabelas usadas pelo loop de texto.

## Limite atual

A semântica de `04BBD` está resolvida em nível de instrução e foi implementada em `tools/emulate_04bbd_exact.py`. Ainda não é correto declarar o `C280` final: os valores de `D120–D135` são produzidos pela sequência de entrada e pelo estado de jogo, e a ROM isolada não contém um snapshot universal desses bytes. O emulador aceita os valores de RAM explicitamente para evitar resultados inventados.

O próximo passo seguro é conectar um trace de execução ou um estado de RAM capturado no ponto `0x4A8D`; com esses bytes, o script pode reproduzir `C022`, `C025–C028`, `C205`, `C215`, `C251` e a construção completa de `C280`.
