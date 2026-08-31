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

Mais tarde, o handler em `0x1809–0x181F` foi executado: `0x1809–0x180C` escreve `C080=0`, `0x180E` lê `C112`, e, se `C112=2` e os contadores `C081/C082` mudaram, `0x181C–0x181F` volta a escrever `C080=1`. Na ocorrência observada, o scheduler em `0x06CE` encontrou `C0A0=0` em `0x06D1` e retornou imediatamente. Assim, o caminho `06D8–06E4`, que limparia `C0A0` e transferiria 32 bytes de `C0E0` para `C000`, não foi tomado.

## Interpretação

A reprodução mostra que a máquina de transformação finaliza e zera `C0A0` antes da avaliação do scheduler. O handler de IRQ/VDP controla `C080` separadamente: ele o limpa no início e pode reativá-lo conforme `C112` e `C081/C082`. Portanto, o bloqueio observado é primariamente `C0A0=0`, não uma escrita de `C080` em `0x180E`.

A próxima etapa deve correlacionar a chamada de `0x06CE` com a janela em que `C0A0` fica ativo e com o handler `0x1809–0x181F`. Não se deve liberar artificialmente `C0A0`, pois isso mudaria a semântica do emulador. O objetivo é determinar se o scheduler precisa ser chamado durante os quatro ciclos intermediários, ou se a execução real deveria alcançar outro consumidor antes de zerar `C0A0`.
