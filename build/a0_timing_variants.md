# Variantes de timing, IRQ e semântica Dega

A mesma sequência causal (`0x00` nos primeiros 260 blocos, `0x10` nos blocos 260–289 e `0x00` depois) foi executada até 1.100 blocos com três configurações do capturador base.

| Variante | Configuração | PC final | FFFE/FFFF | Interpretação |
|---|---|---|---|---|
| Baseline | Sem `--scanline-irq`, sem `--dega-frame-schedule`, `vdp_wait_reads=2` | `0x3546` | `0x01/0x84` | Não reproduz o fluxo de cena esperado |
| Scanline Dega | `--scanline-irq`, `--dega-frame-schedule`, I/O Dega, `vdp_wait_reads=2` | `0x4070` | `0x95/0x82` | Reproduz o bloqueio A0/C203 |
| VDP mais lento | Mesmo modelo Dega, `vdp_wait_reads=8` | `0x4073` | `0x95/0x82` | Altera o ponto do loop, mas não alcança o diálogo |

Nenhuma configuração alcançou `0x4A8D`. O resultado demonstra que o timing e a ordem de IRQs alteram o caminho observado, mas não constituem, isoladamente, a causa final da transição de cena. O modo de referência continua sendo o modelo Dega com `--scanline-irq` e `--dega-frame-schedule`; o baseline deve ser tratado apenas como controle negativo.

O bloqueio permanece associado a estados internos posteriores ao armamento A0. Não foram usados desbloqueios artificiais de `C203`.
