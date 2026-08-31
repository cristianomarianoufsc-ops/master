# Comparação do estado A0 na entrada de 0x8B62 — 2026-08-30

## Resultado principal

A instrumentação agora captura, na própria entrada de `0x8B62`, o endereço de retorno, os bancos ativos, a pilha e um snapshot dos campos `C203`, `DD03`, `DD57`, `DD64`, `DD66`, `DD97`, `DDB7`, `DDF7` e `DE0F–DE12`.

| Bloco | Retorno | Chamador | FFFE | FFFF | Estado A0 observado |
|---:|---|---|---:|---:|---|
| 41 | `0x0536` | fixo (`0x0533`) | `0x01` | `0x82` | Todos os campos observados = `0x00` |
| 46 | `0x0536` | fixo (`0x0533`) | `0x01` | `0x82` | Todos os campos observados = `0x00` |
| 267 | `0x0536` | fixo (`0x0533`) | `0x01` | `0x82` | Todos os campos observados = `0x00` |
| 277 | `0x456C` | paginado (`0x4569`) | `0x01` | `0x82` | Todos os campos observados = `0x00` |
| 278 | `0x0536` | fixo (`0x0533`) | `0x95` | `0x82` | Todos os campos observados = `0x00` |

## Interpretação

A comparação elimina uma hipótese simples: a reentrada paginada no bloco 277 não é diferenciada, na entrada de `0x8B62`, por valores residuais nos campos DDxx/C203 monitorados. O retorno `0x456C` é a diferença observável mais forte; a outra diferença é temporal e de banco, pois o retorno fixo do bloco 278 ocorre depois da troca de `FFFE` para `0x95`.

Isso não prova que esses campos sejam irrelevantes para a decisão anterior. Eles podem ser consumidos e zerados pelo próprio caminho que leva à chamada, ou a condição relevante pode estar em outro endereço, em flags de CPU, no conteúdo apontado por HL/DE ou no estado de VDP/IRQ. Também não é válido concluir que A0 esteja corretamente armada apenas porque a entrada acontece.

## Conclusão operacional

O próximo probe deve capturar o intervalo imediatamente anterior à instrução `CALL` em `0x4569`, incluindo escritas e leituras de memória, registradores e flags, e comparar esse intervalo com o `CALL` em `0x0533`. A prioridade deixou de ser a leitura de DDxx na entrada da rotina; passou a ser localizar a operação que produz o retorno `0x456C` e verificar se o caminho paginado altera HL/DE, flags ou um endereço fora da faixa DDxx monitorada.

A execução continua terminando em `0x4073`, sem alcançar `0x4A8D`; portanto, o achado é diagnóstico e ainda não autoriza alteração da ROM.
