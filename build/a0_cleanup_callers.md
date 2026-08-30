# Chamadores do inicializador A0 em 0x8B62

A instrumentação de execução passou a registrar `SP`, `stack0` e `stack1` nos eventos de opcode. Na entrada em `0x8B62`, os bytes no topo da pilha formam o endereço de retorno em little-endian.

| Bloco | PC de entrada | SP | Bytes no topo | Retorno reconstruído | Bancos FFFE/FFFF |
|---:|---|---|---|---|---|
| 41 | `0x8B62` | `0xDF2A` | `36 05` | `0x0536` | `0x01/0x82` |
| 46 | `0x8B62` | `0xDF2A` | `36 05` | `0x0536` | `0x01/0x82` |
| 267 | `0x8B62` | `0xDF2A` | `36 05` | `0x0536` | `0x01/0x82` |
| 277 | `0x8B62` | `0xDF2A` | `6C 45` | `0x456C` | `0x01/0x82` |
| 278 | `0x8B62` | `0xDF2A` | `36 05` | `0x0536` | `0x95/0x82` |

A janela fixa em `0x0530` confirma o primeiro chamador:

```text
32 FF FF CD 62 8B FB 3E 01 CD E1 04 C3 01 02
```

O `CALL 0x8B62` ocorre em `0x0533`; a execução retorna para `0x0536`. A janela paginada no banco 1 confirma o segundo chamador:

```text
32 20 C0 C9 3E 82 32 FF FF CD 62 8B 3A 19 C1 FE 04
```

Nesse caso, o `CALL 0x8B62` ocorre em `0x4569`; a execução retorna para `0x456C`. Portanto, a limpeza observada após o armamento A0 pode ocorrer por dois contextos diferentes: o inicializador fixo de boot (`0x0533`) ou o caminho paginado de jogo (`0x4569`). O bloco 267 usa o primeiro; o bloco 277 usa o segundo; o bloco 278 volta ao primeiro com `FFFE=0x95`.

## Consequência

O próximo diagnóstico deve separar os dois chamadores e acompanhar o estado de `C203`, `DD03`, `DD97` e `DDF7–DE16` antes de cada `CALL 0x8B62`. Não é seguro atribuir a desmontagem exclusivamente ao dispatcher A0: o mesmo limpador é reutilizado por uma rotina fixa e por uma rotina paginada.
