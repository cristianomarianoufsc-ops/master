# Desmontagem semântica de A0 e dos chamadores — 2026-08-30

## Rotina `0x8B62`

A rotina foi desmontada no banco efetivo `FFFF=0x82` (banco físico 2):

```asm
8B62  PUSH HL
8B63  PUSH DE
8B64  PUSH BC
8B65  LD   HL,DD03h
8B68  LD   DE,DD04h
8B6B  LD   (HL),00h
8B6D  LDI
8B6F  LDI
8B71  LDI
8B73  LDI
8B75  LDI
8B77  LDI
8B79  LDI
8B7B  LDI
8B7D  LDI
8B7F  LDI
8B81  LD   HL,DD17h
8B84  XOR  A
8B85  LD   B,0Ah
8B87  LD   DE,0018h
8B8A  LD   (HL),A
8B8B  ADD  HL,DE
8B8C  LD   (HL),A
8B8D  INC  HL
8B8E  LD   (HL),A
8B8F  INC  HL
8B90  LD   (HL),A
8B91  INC  HL
8B92  LD   (HL),A
8B93  LD   DE,0005h
8B96  ADD  HL,DE
8B97  DJNZ 8B8Ah
8B99  LD   A,E4h
8B9B  LD   (DD08h),A
8B9E  POP  BC
8B9F  POP  DE
8BA0  POP  HL
```

A rotina salva os valores recebidos de HL/DE/BC e os substitui por endereços constantes. Portanto, os valores `HL=0xC73F`/`0x4547` e `DE=0x8900`/`0x0003` não são operandos dereferenciados pela rotina. A limpeza também não contém salto condicional: ela é incondicional e termina restaurando os registradores salvos.

O `LDI` copia nove bytes a partir de `DD04` para `DD05–DD0D`, após zerar `DD03`. O segundo laço zera dez grupos de cinco bytes, avançando 24 bytes entre grupos, e depois grava `0xE4` em `DD08`.

## Chamador fixo

No banco fixo, `0x0533` é:

```asm
052E  LD   A,82h
0530  LD   (FFFFh),A
0533  CALL 8B62h
0536  EI
0537  LD   A,01h
0539  CALL 04E1h
053C  JP   0201h
```

## Chamador paginado

No banco ativo em `FFFE=0x01`, `0x4569` é:

```asm
4564  LD   A,82h
4566  LD   (FFFFh),A
4569  CALL 8B62h
456C  LD   A,(C119h)
456F  CP   04h
4571  JR   Z,4592h
4573  LD   A,05h
4575  LD   (C119h),A
4578  LD   (C0A0h),A
457B  LD   A,01h
457D  LD   (C11Dh),A
4580  LD   HL,46C0h
4583  LD   DE,C0E0h
4586  LD   BC,0020h
4589  LDIR
458B  RET
```

## Conclusão operacional

A desmontagem elimina a hipótese de que `0x8B62` decide entre os dois caminhos com base em HL/DE ou em um ramo interno. A rotina é um limpador comum chamado por dois contextos. A diferença funcional deve estar no código que vem depois do retorno: o caminho fixo habilita interrupções, chama `0x04E1` e volta a `0x0201`; o caminho paginado lê `C119`, compara com `4` e, se diferente, instala um novo estado em `C119`, `C0A0`, `C11D` e copia 32 bytes de `46C0` para `C0E0`.

Esse é o novo ponto de investigação para obter progresso funcional: descobrir qual valor de `C119` existe na entrada de `0x4569` e se o teste em `0x456C` é a condição que impede a transição esperada. Ainda não há base para alterar a ROM.
