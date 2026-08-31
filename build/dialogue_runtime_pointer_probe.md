# Probe dinâmico de C206/C223/C238

## Configuração

A ROM japonesa foi executada com o capturador instrumentado até 3500 blocos, usando IRQ por scanline, agendamento de frame do Dega, semântica de I/O ativa-baixa e entrada `FF,EF,FF`. O trace cobriu `C200–C23F`, com registros forçados para `C206`, `C223` e `C238`, e chamadas ao resolvedor `0x5C16`.

## Resultado

A execução terminou em `0x406C`, com `FFFE=0x95` e `FFFF=0x82`, sem alcançar `0x4A8D` e sem entrar nos handlers narrativos do banco 21. O trace acumulou muitos acessos repetitivos de `C008`, mas somente os seguintes eventos relevantes foram registrados para os ponteiros:

| Bloco | PC | Evento | Campo |
|---:|---:|---|---|
| 1 | `0x00AD` | escrita de inicialização | `C206/C223/C238=0` |
| 87 | `0x4939` | limpeza/leitura | `C206/C223/C238=0` |
| 266 | `0x4496` | escrita de limpeza | `C206/C223/C238=0` |

Não houve ponteiro não nulo em `C206`, `C223` ou `C238` nesta execução. Portanto, o probe não identifica ainda um diálogo narrativo, mas confirma que o caminho testado permanece preso antes da resolução de streams. O arquivo bruto permaneceu em `/tmp/dialogue_runtime_trace.json` e não foi versionado por ser um trace de diagnóstico grande e inconclusivo.

## Decisão

Não se deve extrair texto narrativo a partir desses zeros nem gerar patch com este estado. O próximo experimento deve usar a janela de execução que realmente alcança o armamento A0 e o caminho posterior documentado nos probes de 3500 blocos, ou corrigir o modelo da tarefa/VDP antes de repetir a captura. A análise estática já separa os candidatos de bytecode; falta obter um estado dinâmico válido em que `C223/C238` recebam ponteiros.
