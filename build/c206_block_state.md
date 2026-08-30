# Estado de bloqueio em 0x406F

O probe focalizado de `C202`, `C203`, `C204` e `C206` foi executado com entrada `0x10` nos blocos 260–289, usando a semântica do Dega e trace de PCs `0x4000–0x43FF`.

A sequência relevante termina assim:

| Bloco | PC | Estado observado |
|---:|---|---|
| 285 | `0x40FA` | `C203=1`, início da operação com banco `FFFF=0x0C` |
| 527 | `0x432F` | `C203=0`, conclusão de uma operação posterior |
| 531 | `0x412D` | `C203=2`, novo ciclo |
| 531 | `0x4146` | `C206=0x0080`, ponteiro calculado |
| 789 | `0x403F` | `C203=1`, novo pedido de operação |
| 1051 | `0x432F` | `C203=0`, conclusão observada |
| 1051 | `0x406A` | `C203=2`, rearmamento |

Na execução com `max_steps=1100`, o PC final foi `0x4070`. A partir do bloco 311, o trace mostra repetidas leituras de `C203=1` em `0x406F`, com `FFFF=0x0C`, sem nova escrita de `C206` e sem alcançar `0x4A8D`. Esse é o primeiro estado de bloqueio reproduzível e localizado: um pedido de operação em banco `0x0C` aguarda o bit 0, mas não há evidência de que seu consumidor seja chamado nessa configuração.

A conclusão é observacional: o próximo teste deve comparar a cadeia de IRQ quando `FFFF=0x0C` com a cadeia que alcança `0x432F`, verificando se a tabela/rotina do banco `0x0C` está sendo mapeada corretamente. Não foi alterada RAM nem liberado flag artificialmente.
