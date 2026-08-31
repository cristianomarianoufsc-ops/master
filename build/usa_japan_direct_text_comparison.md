# Inventário comparativo de fontes diretas de texto

O extrator `tools/extract_direct_text_sources.py` foi corrigido para aceitar tanto o formato antigo (`0C223h`) quanto o formato atual do disassembler (`0xc223`) e equivalentes para `C238`.

A execução em banco 21 encontrou seis candidatos em cada ROM. Os streams extraídos são idênticos byte a byte, embora seus endereços de origem mudem:

| Stream | Americana | Japonesa | Delta Japão–EUA | Tamanho até FF |
|---:|---:|---:|---:|---:|
| 1 | `0x542A` | `0x5434` | `+0x0A` | 13 bytes |
| 2 | `0x5A2D` | `0x5A58` | `+0x2B` | 5 bytes |
| 3 | `0x5F1A` | `0x5F45` | `+0x2B` | 7 bytes |
| 4 | `0x61E8` | `0x6213` | `+0x2B` | 15 bytes |
| 5 | `0x61F7` | `0x6222` | `+0x2B` | 9 bytes |
| 6 | `0x62DF` | `0x630A` | `+0x2B` | 19 bytes |

Os bytes dos seis streams são iguais, portanto eles representam dados compartilhados ou estruturas de texto não localizadas. Isso valida a correção do extrator e fornece âncoras confiáveis para o deslocamento entre as versões. Esses seis candidatos não são ainda o inventário completo de diálogos: o texto principal é carregado por estruturas/handlers paginados e precisa ser resolvido seguindo `05C16`, `C206`, `C223` e `C238` em runtime.

Arquivos brutos: `build/usa_direct_text_sources.md` e `build/japan_direct_text_sources.md`.
