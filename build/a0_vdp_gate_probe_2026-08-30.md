# Gate do scheduler VDP após a máquina A0 — 2026-08-30

## Observação

Foi rastreado o scheduler em `0x06CE–0x0708` durante 1.100 passos, com os estados `C0A0–C0A4`, `C080`, `C0E0`, `C112` e `C113` monitorados.

O scheduler possui esta lógica:

```asm
06CE  LD A,(C0A0h)
06D1  OR A
06D2  RET Z
06D3  LD A,(C080h)
06D6  OR A
06D7  RET NZ
06D8  XOR A
06D9  LD (C0A0h),A
06DC  LD HL,C0E0h
06DF  LD DE,C000h
06E2  LD B,20h
06E4  RST 30h
06E5  RET
```

## Resultado observado

No bloco 52, a máquina de estado em `0x078A–0x07F2` percorreu os cinco ciclos previstos. Ao completar o quinto ciclo, escreveu `C0A4=1`, `C0A2=0`, `C0A0=0` e `C113=0` em `0x07E5–0x07F2`.

Mais tarde, o scheduler foi executado em `0x06CE` após uma escrita de `C080=0` por `0x180E`, mas encontrou `C0A0=0` em `0x06D1` e retornou imediatamente. Assim, o caminho `06D8–06E4`, que limparia `C0A0` e transferiria 32 bytes de `C0E0` para `C000`, não foi tomado.

## Interpretação

A reprodução mostra uma possível corrida/ordenação entre a máquina de transformação e o scheduler VDP: o estado ativo é finalizado e `C0A0` é zerado antes de o scheduler avaliá-lo. Isso explica por que a cópia final para `C000` não aparece e por que o breakpoint de cena continua não sendo alcançado.

A hipótese deve ser testada comparando a cadência de IRQ/VDP e o ponto em que `0x06CE` é chamado. Não se deve liberar artificialmente `C0A0`, pois isso mudaria a semântica do emulador. O próximo passo é instrumentar a ordem temporal entre `0x07E5–0x07F2`, `0x180E` e `0x06CE`, e verificar se a implementação de IRQ está atrasando o scheduler em relação ao hardware.
