# Consumidor de C0E0 após a transição A0 — 2026-08-30

A análise pós-`0x4589` e a desmontagem Z80 localizaram um consumidor relevante do bloco copiado para `C0E0`: a rotina em `0x078A`.

```asm
078A  LD   DE,C0E0h
078D  LD   BC,0020h
0790  LDIR
0792  POP  DE
0793  LD   HL,C0A1h
0796  LD   A,04h
0798  LD   (HL),A
0799  LD   (C0A0h),A
079C  LD   HL,C0E0h
079F  LD   B,20h
07A1  XOR  A
07A2  RLD
07A4  SUB  D
07A5  JR   NC,07AAh
07A7  XOR  A
07A8  RRD
07AA  RRD
...
07CD  DJNZ 07A2h
```

O código copia 32 bytes a partir de `C0E0`, restaura DE, define o estado `C0A0=4` e processa os bytes de `C0E0` com `RLD/RRD`, máscaras e subtrações dependentes de D. Isso indica que a tabela instalada por `0x4569` não é texto diretamente; é um bloco intermediário consumido por uma transformação de dados.

O trace pós-cópia mostrou escritas em `C0E0/C0E1/C0FF` por PCs `0x0718`, `0x071F`, `0x0721`, `0x0743`, `0x0792`, `0x07A4` e outros, além de mudanças de `C0A0` para `4`. Esses PCs devem ser tratados como a cadeia de processamento seguinte, não como ruído de memória.

A hipótese atual é que `C0E0` contém uma estrutura codificada ou parâmetros para o próximo estado de cena, e `0x0792` é um decodificador/normalizador que prepara os dados para o renderizador. O próximo probe deve capturar `0x078A–0x07D0`, o valor de D usado nas subtrações e o destino final após o laço.
