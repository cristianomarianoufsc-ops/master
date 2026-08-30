# Probe do estado C200–C20F

A captura determinística foi executada com 1.100 blocos, entrada `0x10` na janela 260–289, sem desbloqueio sintético, usando trace de `C200–C20F`.

O ciclo observado foi:

| Bloco | PC | Escrita | Interpretação observacional |
|---:|---|---|---|
| 285 | `0x40FA` | `C203=1` | início da primeira operação desse caminho |
| 527 | `0x432F` | `C203=0` | conclusão pelo consumidor do bit 0 |
| 531 | `0x412D` | `C203=2` | início da operação seguinte |
| 531 | `0x4146` | `C206=0x0080` | ponteiro calculado após a troca para `FFFF=0x16` |
| 789 | `0x403F` | `C203=1` | nova operação/rearme |
| 1051 | `0x432F` | `C203=0` | conclusão normal |
| 1051 | `0x406A` | `C203=2` | novo ciclo iniciado |

A captura terminou em `0x4070`, sem alcançar `0x4A8D`. O resultado não é snapshot válido de `C280`. A evidência nova é que `C202` participa do cálculo de `C206` durante a segunda operação; o próximo diagnóstico deve correlacionar o índice em `C202`, o ponteiro em `C206` e os dados carregados antes do próximo ciclo.
