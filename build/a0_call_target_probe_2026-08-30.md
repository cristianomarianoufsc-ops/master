# Entrada instrumentada em 0x8B62 — 2026-08-30

## Configuração

O capturador foi ampliado com `--trace-call-targets`, que registra a entrada em PCs de chamada selecionados e reconstrói o endereço de retorno a partir dos dois bytes no topo da pilha. O alvo padrão é `0x8B62`; a opção aceita múltiplos PCs separados por vírgula. A captura usou a ROM local, semântica de I/O do Dega, agendamento de frame, IRQ por scanline, entrada `0xFF` até o bloco 260 e pulso `0x10` por 30 blocos. Nenhum flag ou slot foi liberado artificialmente.

Para evitar saturação, o trace foi restrito à janela `0x8B60–0x8B90`, com 300 blocos e rastreamento DDxx forçado.

## Resultado

A entrada em `0x8B62` foi observada dez vezes. O endereço de retorno reconstruído separa claramente os dois contextos previamente conhecidos:

| Bloco(s) | Banco FFFE | Retorno | Chamador | Interpretação |
|---:|---:|---:|---|---|
| 41, 46, 265, 278 | `0x01` ou `0x95` | `0x0536` | `CALL 0x8B62` em `0x0533` | Caminho fixo de inicialização/limpeza |
| 277 | `0x01` | `0x456C` | `CALL 0x8B62` em `0x4569` | Reentrada pelo caminho paginado |

Em todos os casos, `FFFF=0x82`. A entrada em `0x8B81` também foi registrada, mas seu topo de pilha era `0x00/0x00`, pois esse ponto é alcançado dentro do fluxo de `0x8B62`, não por uma nova chamada; portanto, o retorno deve ser lido na entrada de `0x8B62`.

O capturador terminou em `0x4073` após 300 blocos e não alcançou `0x4A8D`. Essa limitação mantém a captura como evidência diagnóstica de fluxo A0, não como snapshot válido de `C280`.

## Conclusão

A instrumentação confirmou em runtime os dois chamadores de `0x8B62` e eliminou a ambiguidade da inferência por faixa de PCs. O retorno `0x0536` identifica o caminho fixo, enquanto `0x456C` identifica a reentrada paginada. O próximo diagnóstico deve comparar o estado `DD03`, `DD97`, `DDB7`, `DDF7–DE12`, `C203` e os bancos imediatamente antes dessas duas entradas, priorizando a diferença no contexto de `0x4569` que arma e desmonta a tarefa A0.
