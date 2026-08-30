# Probe dos dois contextos de chamada A0 — 2026-08-30

## Configuração

Foram executadas duas capturas independentes sobre `input/KujakuOu_Japan.sms`, sem desbloqueios sintéticos. Ambas usaram semântica de I/O do Dega, agendamento de frame Dega, IRQ por scanline, entrada `0xFF` até o bloco 260 e pulso `0x10` por 30 blocos. A primeira restringiu a execução observada à janela fixa `0x0500–0x0540`; a segunda, à janela paginada `0x4540–0x4580`. O estado A0 foi rastreado em `DD00–DE37`, com `DD03`, `DD57`, `DD64`, `DD66`, `DD97`, `DDB7`, `DDF7` e `DE0F–DE12` forçados no trace.

## Resultados

| Captura | Blocos | PC final | Banco FFFE | Banco FFFF | Breakpoint |
|---|---:|---|---:|---:|---|
| Fixa | 300 | `0x4073` | `0x95` | `0x0C` | Não alcançado |
| Paginada | 300 | `0x4073` | `0x95` | `0x0C` | Não alcançado |

As duas execuções registraram 37 ocorrências dos PCs de interesse no extrator. O caminho observado contém `0x4496` no bloco 267, com `SP=0xDFEE` e topo da pilha `0xEB/0x00`, seguido por escritas de limpeza em `DD03`, `DD97`, `DDB7`, `DDF7` e `DE0F–DE12`. Os acessos ao limpador `0x8B8B/0x8B93` ocorreram com `SP=0xDFD4` e topo `0x00/0x00` nos blocos 267, 277 e 278, além das passagens de inicialização nos blocos 41 e 46.

## Auditoria e interpretação

As duas capturas foram classificadas como `risk`: o breakpoint `0x4A8D` não foi atingido e o PC `0x04E4` dominou o trace. Portanto, nenhuma delas constitui snapshot válido de `C280` ou prova de transição para diálogo.

A comparação também mostrou que restringir a faixa de PCs observados não separa, por si só, os dois chamadores: ambas as execuções percorrem o mesmo caminho até `0x4073`, e os hashes diferem apenas por conteúdo de trace/configuração. O próximo experimento deve usar marcadores de execução específicos para os endereços de retorno dos `CALL` em `0x0533` e `0x4569`, ou uma captura que registre explicitamente a instrução anterior e o endereço de retorno no momento de cada entrada em `0x8B62`. Não há base para alterar a ROM nesta etapa.
