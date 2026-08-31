# Xrefs do scheduler A0 e do handler VDP — 2026-08-30

## Xrefs localizados

Foi criada `tools/find_z80_call_xrefs.py` para localizar referências literais Z80 a alvos em todos os bancos da ROM. O mapeamento foi corrigido para exibir `bank 0` no espaço fixo `0x0000–0x3FFF` e os demais bancos no espaço paginado `0x4000–0x7FFF`.

## Cadeia do scheduler

O xref fixo `0x0DA6` pertence à rotina:

```asm
0D9C  LD   A,(C080h)
0D9F  OR   A
0DA0  JP   NZ,0DA9h
0DA3  CALL 012B7h
0DA6  CALL 006CEh
0DA9  CALL 00A56h
0DAC  JP   00569h
```

Assim, `0x06CE` não é chamado diretamente por qualquer ponto arbitrário: ele é chamado por `0x0DA6` apenas quando `C080=0`. O handler relacionado ao VDP em `0x0179` é separado:

```asm
0171  LD   A,(C008h)
0174  CP   80h
0176  JP   Z,0195h
0179  CALL 01809h
017C  CALL 030D4h
...
```

A rotina `0x1809–0x181F` limpa `C080` e pode reativá-lo conforme `C112` e `C081/C082`. Portanto, a ordem relevante é: o handler determina se `C080` está livre; depois `0x0DA6` chama `0x06CE`; o scheduler verifica `C0A0` e, se ativo, transfere `C0E0` para `C000`.

## Conclusão

A falha observada não deve ser tratada como simples atraso de IRQ. O scheduler tem uma guarda explícita de `C080` no chamador `0x0D9C–0x0DA6`, e a rotina `0x06CE` tem uma guarda independente de `C0A0`. O próximo probe deve capturar a sequência completa `0x0179 → 0x1809`, `0x0D9C → 0x06CE` e a máquina `0x078A–0x07F2`, incluindo `C008`, `C080`, `C112` e `C0A0`, para descobrir qual estado impede a transferência.

Ainda não há justificativa para alterar a ROM ou o modelo de IRQ.
