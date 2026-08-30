# Validação da semântica de I/O do Dega

## Escopo

O código de referência `Dega-1.12` foi mantido fora do repositório em `/home/ubuntu/reference/dega-1.12/`. A comparação de `mast/frame.cpp` e `mast/mem.cpp` mostrou duas diferenças relevantes no capturador: o contador V do VDP na porta `0x7E` e a conversão ativa-baixa das portas de controle `0xDC/0xC0`.

O capturador recebeu a opção experimental `--dega-io-semantics`. Sem essa opção, os testes históricos continuam usando os valores diretamente retornados pelas portas. Com a opção, os valores de entrada representam o estado interno de `MastInput[0]`, limitado aos seis bits baixos e convertido para leitura ativa-baixa, e a porta `0x7E` retorna o contador de linha compatível com o Dega.

## Execução

A ROM local foi executada com 900 blocos, `--scanline-irq`, `--dega-frame-schedule`, `--irq-every-runs 0`, a janela `0x00` até o bloco 260, `0x10` por 30 blocos e `0x00` depois, além de `--dega-io-semantics`. A ROM permaneceu fora do Git.

## Resultado

| Campo | Resultado |
|---|---:|
| Blocos executados | 900 |
| Breakpoint | `0x4A8D` |
| PC final | `0x406C` |
| `FFFE` final | `0x95` |
| `FFFF` final | `0x16` |
| Leitura de controle no bloco 265 | `0xEF` |
| Leituras seguintes | `0xFF`, `0xFF` |
| `C021` | `0x88` |
| `C022` | `0x01` |
| `C205` | `0x00` |
| `C280` | `0x00` |
| `C281` | `0x00` |
| Auditoria | `risk` |

O auditor apontou `BREAKPOINT_NOT_REACHED`, `INPUT_NOT_STABLE` e `FLAG_STUCK` para `C203`, que permaneceu em `2` durante a espera.

## Conclusão

A semântica de controle e V-counter do Dega não altera o caminho observado: a execução continua presa em `0x406C`, aguardando a segunda operação de cena. Portanto, a diferença de I/O não é a causa principal do bloqueio atual. Não há base para aceitar `C280` ou qualquer snapshot como válido.

O próximo foco deve ser a cadeia de consumo da operação iniciada em `0x403A/0x403F`, incluindo a rotina que deveria limpar `C203` após o carregamento, correlacionando os escritores dinâmicos com a rotina paginada do banco 21. Desbloqueios sintéticos continuam proibidos como método de validação.
