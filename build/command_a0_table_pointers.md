# Ponteiros das tabelas do comando A0

O utilitário `tools/resolve_z80_table.py` foi corrigido para tratar bancos paginados na janela `0x8000–0xBFFF`. Para o índice `0x10`, correspondente ao comando `0xA0` após a redução em `0x83E7`, as tabelas candidatas apontam para estruturas não nulas:

| Tabela | Ponteiro resolvido |
|---|---:|
| `l836D` | `0xAB5F` |
| `l833D` | `0xA2C7` |
| `l82DD` | `0xAB72` |

Os cabeçalhos nos três endereços contêm dados estruturados, e não preenchimento zero. Portanto, a ausência de tarefa em `DDD7` não é explicada por uma entrada inexistente na ROM. A questão restante é a tabela efetivamente selecionada pelo estado alternado de `AF` e o ponto em que a cópia de `sub_8536` deixa de armar o slot.
