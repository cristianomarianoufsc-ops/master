# Reprodução do probe de retorno A0 — 2026-08-30

## Configuração

A ROM local `input/KujakuOu_Japan.sms` foi extraída do arquivo fornecido pelo usuário e permaneceu fora do Git. A execução usou semântica de I/O compatível com Dega, agendamento de frame Dega, IRQ por scanline, janela de controle com `0xFF` até o bloco 260, `0x10` por 30 blocos e `0xFF` depois. O capturador executou 1.100 blocos, com `--trace-every 32`, faixa de memória `DD00–DE37`, faixa de PCs `4400–8BD0` e faixa de execução `83D0–8BD0`. Não foi usado desbloqueio sintético de `C008`, `C203`, `DDB7`, `DD97` ou `DDF7`.

O novo extrator `tools/extract_a0_return_context.py` reuniu contextos dos PCs `4496`, `8B81`, `8B8B` e `8B93`, incluindo SP, bytes no topo da pilha, bancos ativos, registradores e eventos de memória.

## Resultado da execução

| Campo | Resultado |
|---|---|
| Blocos executados | `1100` |
| PC final | `0x4070` |
| Breakpoint esperado | `0x4A8D` |
| Registros no trace | `9892` |
| Saturação do trace | Não observada no limite configurado |
| Auditoria | `risk`, por `BREAKPOINT_NOT_REACHED` e entrada variável |

A captura não é um snapshot válido de `C280` nem prova de transição para diálogo. O resultado só é usado para caracterizar o caminho de diagnóstico.

## Evidência observada

A execução confirmou a presença do chamador em `0x4496` no bloco 267. Nesse ponto, o SP era `0xDFEE` e os bytes observados no topo da pilha eram `0xEB/0x00`, enquanto a rotina gravava zeros em campos de estruturas de tarefa, incluindo `DD03`, `DD57`, `DD64` e `DD66`. O trace também registrou o acesso ao limpador `0x8B81`/`0x8B8B` em blocos posteriores, com SP `0xDFD4` e topo `0x00/0x00`.

A instrumentação confirma que o caminho de limpeza é alcançado em mais de um contexto e que a pilha precisa ser interpretada junto com os bancos ativos. Contudo, nesta reprodução específica a amostragem de eventos não fornece, sozinha, um retorno confiável para atribuir a causa da desmontagem: o trace termina no caminho `0x4070`, e a auditoria rejeita a captura como evidência conclusiva.

## Conclusão operacional

O extrator é útil como ferramenta observacional para o próximo experimento, mas não altera a semântica do capturador e não libera esperas. A próxima investigação deve comparar os dois chamadores conhecidos de `0x8B62` (`0x0533` e `0x4569`) usando uma captura com faixa de execução estreita, eventos forçados para `DDB7`, `DD97`, `DDF7–DE12`, `DD03` e registro do endereço de retorno imediatamente antes de `0x8B81`. Nenhuma alteração de ROM deve ser feita até que essa correlação seja reproduzida sem `BREAKPOINT_NOT_REACHED`.
