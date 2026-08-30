# Probe focalizado da tarefa A0 — 2026-08-30

## Configuração

A captura usou `input/KujakuOu_Japan.sms`, semântica de I/O do Dega, agendamento de frame Dega, IRQ por scanline, controle padrão até o bloco 260 e pulso de `0x10` por 30 blocos. O trace registrou `DD00–DE37`, execução em `0x83D0–0x8BD0` e eventos críticos forçados para `C203`, `DD03`, `DD57`, `DD64`, `DD66`, `DD97`, `DDB7`, `DDF7` e `DE0F–DE12`.

## Resultado

A captura terminou em `0x4073` após 300 blocos e não alcançou `0x4A8D`. O auditor marcou `status=risk` exclusivamente por `BREAKPOINT_NOT_REACHED`; não houve saturação do trace nessa execução. Portanto, o resultado continua sendo diagnóstico, não um snapshot válido.

## Sequência observada

| Bloco | PC | Evidência |
|---:|---|---|
| 265 | `0x8540` | `DDF7=0xA8`, com a estrutura A0 sendo copiada para o grupo `DDF7–DE06`. |
| 265 | `0x874D` | `DDF7` permanece com o bit 7 ativo durante a verificação do dispatcher. |
| 267 | `0x4496` | `DDF7`, `DE0F–DE12`, `DDB7` e `DD97` são escritos com zero; a operação armada é desmontada antes de alcançar seu processamento normal. |
| 267 | `0x8B8B–0x8B93` | O limpador geral repete a zeragem dos slots e campos auxiliares. |
| 285 | `0x40FA` | Uma operação posterior grava `C203=1`, entrando no caminho de espera. |

Ao incluir os seletores no analisador, `DDB7` passou a ser reportado junto de `DD97`; ambos apresentaram nove escritas e valores observados `0` e `4`. Isso confirma que o estado auxiliar A0 participa do armamento, mas não identifica sozinho a causa do retorno ao limpador.

## Conclusão

A hipótese de tabela A0 nula foi descartada novamente. O trace mostra armamento real em `0x8540`, seguido de desmontagem pelo caminho que passa por `0x4496` e `0x8B8B`. A próxima investigação deve reconstruir o chamador de `0x4496`, os valores de retorno na pilha e a condição que decide retornar ao limpador, sem forçar `C203`, `DDB7`, `DD97` ou `DDF7`.
