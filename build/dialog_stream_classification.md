# Extração e classificação de streams de diálogo

## Método

`tools/extract_dialog_streams.py` resolveu 260 entradas em quatro tabelas intermediárias (`B124`, `B228`, `B9EA` e `BAB5`) no banco 22 de cada ROM. Cada entrada foi seguida até `FF` ou até 512 bytes. A classificação usa presença de marcadores de bytecode (`FB`, `FC`, `FD`, `FE`, `EE`), pares que parecem endereços CPU e densidade de bytes baixos.

## Resultado

| Classe | Americana | Japonesa | Interpretação |
|---|---:|---:|---|
| `bytecode_or_structure` | 195 | 195 | registros, ponteiros ou comandos; não editar como texto plano |
| `mixed_or_unknown` | 63 | 63 | requer correlação com handler e runtime |
| `text_or_glyph_stream` | 2 | 2 | streams curtos de códigos baixos, ainda não narrativos |

Os dois candidatos classificados como texto são idênticos nas duas ROMs: `00 1C 33 1D FF` e `00 37 00 38 FF`, provenientes de `B9EA[8]` e `B9EA[49]`. Pelo tamanho e conteúdo, parecem tabelas curtas de parâmetros/códigos, não diálogos narrativos.

## Blocos narrativos candidatos

A análise estática anterior e a extração atual convergem para os seguintes blocos, que contêm a cadeia narrativa, mas não são streams de texto plano isolados:

- `0x5F7E` no banco 22: base copiada para `CF00` pelo handler `0x9E70`;
- `0x6046` no banco 22: estrutura referenciada durante a preparação de objetos;
- `0x61FB` e regiões vizinhas: tabelas/streams que alimentam handlers e apresentam terminadores `FF`;
- tabelas deslocadas apontadas pelos pares `0x6603→0x662E` e `0x6463→0x648E`.

Esses blocos são bytecode/estruturas de cena com chamadas, parâmetros e ponteiros; o texto narrativo só aparece depois que os handlers resolvem sub-registros para `C223/C238`. Portanto, não foi identificado ainda um bloco que possa ser classificado com segurança como diálogo narrativo plano. A próxima extração deve seguir cada entrada de `5F7E` pelos handlers `05C16/05BEB`, capturando o ponteiro final de `C223/C238` em runtime.

## ROMs

A estrutura e a classificação foram executadas separadamente nas ROMs japonesa e americana. As diferenças de offsets permanecem, mas a quantidade por classe é igual, reforçando que a tabela intermediária é compartilhada e que a localização regional ocorre em níveis posteriores.
