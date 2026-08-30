# Matriz de duas janelas de entrada

Foi criada `tools/run_two_window_matrix.py` para testar, de forma reproduzível, os valores internos aplicados nas duas janelas em que a ROM lê o controle: blocos 265 e 527. Foram testados `0x00`, `0x10`, `0x20` e `0x30` em cada janela, com semântica de I/O do Dega e execução até o bloco 900.

| Primeira janela | Segunda janela | Leituras observadas | PC final | Banco FFFF final |
|---:|---:|---|---|---:|
| `0x00` | `0x00` | `0xFF`, `0xFF`, `0xFF` | `0x3548` | `0x84` |
| Qualquer valor testado | `0x10`, `0x20` ou `0x30` | Segunda leitura diferente de `0xFF` | `0x406C` | `0x16` |
| `0x10`, `0x20` ou `0x30` | `0x00` | Primeira leitura diferente de `0xFF` | `0x406C` | `0x16` |

Nenhuma das 16 combinações alcançou `0x4A8D`. O resultado é útil porque confirma que a segunda janela de leitura não é ignorada: ela muda o caminho para a espera de cena em `0x406C`, mas não basta para disparar o diálogo. A matriz também não fornece base para forçar flags ou alterar a ROM.

A auditoria causal deve continuar tratando essas execuções como evidência diagnóstica: o PC final é uma espera, e não uma transição válida. O próximo probe deve correlacionar o valor reconhecido em `0x527` com `C202`, `C206`, `DD03`, `DD97` e o pedido de tarefa que termina em `C203`.
