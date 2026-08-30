# Manual de continuidade para o próximo agente

## Objetivo

Produzir um patch direto PT-BR para a versão japonesa de *Kujaku Ō* no Sega Master System/Mark III, modificando dados internos da ROM por meio de um patch IPS/BPS distribuível. A ROM original deve permanecer apenas no ambiente local do usuário.

## Descobertas confirmadas

| Item | Resultado confirmado |
|---|---|
| Fonte comprimida | Stream localizado em `0x3181D`, banco físico `0x8C` |
| Descompressão inicial | `sub_0303/sub_033D` envia a fonte para VRAM em `0x6380` |
| Slots SMS | `FFFE` controla `0x4000–0x7FFF`; `FFFF` controla `0x8000–0xBFFF` |
| Dispatcher | `RST 10h` usa tabela de vetores e salta via `JP (HL)` |
| Resolver por índice | `05C16` usa `C205*2` como índice em uma tabela passada em `DE` |
| Resolver de listas | `05C02` percorre pares de ponteiros até encontrar alvo cujo primeiro byte é zero |
| Loop de texto | `0x96CA–0x9779`; `FF` encerra; `C280[código] != 0` aceita glifo |
| Máscaras | `04CFD` em `0x8D03` aplica `RRC C` e máscaras de endereço; `04D16` processa outra classe via registradores alternados |
| Handler de cena | `0x9E70` copia `0x0A14` bytes de `0x5F7E` para `CF00` e aplica registros selecionados por `0x5F4C` |
| Origem de glifos | `FFFF=0x13` é selecionado antes de `05B3E`; `HL=lad0c`, `DE=C86E+offset`, `BC=0x0208` |
| Rotina 05B3E | Banco físico `0x15` quando `C02B=0x95`; reorganiza blocos de glifos antes do buffer |

## O que não deve ser assumido

`lad0c` não é uma fonte 4bpp direta. Testes 2bpp, 4bpp e 8x16 produziram imagens ilegíveis; a região é uma estrutura intermediária ou usa uma ordem de planos ainda não reconstruída. As regiões `AF55`, `B9EA`, `BD55`, `B228` e `BAAA` não são, por si só, diálogos contínuos: elas contêm registros, parâmetros, bytecode ou listas de ponteiros.

A densidade de bytes baixos não é evidência suficiente de texto. Qualquer candidato deve satisfazer simultaneamente o formato do terminador, a ausência de palavras de ponteiro e o consumo efetivo pelo loop que lê `C223/C238`.

## Próxima sequência técnica

Primeiro, completar a emulação de `04CFD/04D16` na ordem de inicialização observada em `0x8C20–0x8CA9`, usando os valores de runtime `C022`, `C025`, `C026`, `C027`, `C028`, `C215` e `C205`. Segundo, reconstruir a tabela `C280` de 256 entradas e verificar os códigos dos streams retornados por `05C16/05C02`. Terceiro, localizar uma mensagem japonesa verificável, renderizar seus códigos usando a fonte real e registrar o mapa código→glifo. Quarto, criar uma fonte latina com os mesmos requisitos de tile e implementar uma etapa de reinserção que preserve comandos e ponteiros. Quinto, gerar primeiro um patch mínimo de uma mensagem, testar no emulador e só depois ampliar para menus e diálogos.

## Ferramentas principais

`tools/resolve_paged_refs.py` resolve bancos físicos para chamadas paginadas. `tools/map_dual_slots.py` separa `FFFE` e `FFFF`. `tools/extract_dialog_pointer_tables.py` segue `05C16`. `tools/resolve_5c02_pointer_chain.py` modela `05C02`. `tools/extract_dialog_handler_candidates.py` reúne handlers que escrevem em `C223/C238`. `tools/emulate_04cfd_exact.py` reproduz `04CFD`. Os demais scripts de renderização devem ser tratados como experimentais até que o formato final seja validado.

## Protocolo de commits

Antes de cada commit, executar `git status`, verificar se não há ROMs ou estados de emulador, revisar o diff e atualizar este manual ou um relatório específico. Usar mensagens no formato `area: descrição`, por exemplo `docs: document dual-slot mapper`, `feat: add exact 04cfd emulator` ou `analysis: classify dialogue pointer tables`. Após o commit, executar `git push origin main` e registrar no relatório o hash enviado.

## Artefatos locais necessários

O próximo agente precisa receber a ROM japonesa por meio de um arquivo local fora do Git. Os scripts aceitam o caminho da ROM como argumento; não assumir que ela estará disponível no clone. Não publicar ROM, dumps completos de bancos, save states ou a ROM modificada completa.

## Avanço posterior: emulação exata de 04CFD

A rotina `04CFD` foi reconstruída a partir do código em `0x8D03`. O algoritmo lê uma contagem, percorre entradas de endereço+máscara, executa `RRC C` e liga ou desliga cada máscara conforme o carry. `tools/emulate_04cfd_exact.py` reproduz essa operação; `build/exact_c205_mask_sweep.csv` contém a varredura de `C205=0x00–0x40`. Essa tabela é evidência de classificação de estado, não ainda o mapa final de C280, que depende da ordem completa de inicialização e de `04D16`.

A tabela `AC0B` está confirmada no banco 19, com grupos de 6, 6, 7 e 12 registros sobre `D125–D133`. `AC31` também está no banco 19. Os scripts `tools/expand_c280_code_map.py` e `tools/emulate_c280_tables.py` são auxiliares; o primeiro ainda é heurístico e não deve ser usado para patch. O próximo agente deve priorizar a implementação completa de `04D16` e a expansão real de C280 antes de modificar qualquer stream.

## Avanço atual: 04D16 confirmado

A rotina física em `0x8D16` do banco ROM 21 foi confirmada como a implementação de `04D16` quando `FFFE=0x15`. Seu formato é `count` seguido de registros de três bytes (`destino little-endian`, `máscara`); para cada registro, ela lê o byte da fonte apontada por BC, avança BC, e aplica `destino |= máscara` somente quando o byte da fonte é diferente de zero. Não há rotação nem limpeza de bits nessa rotina.

O emulador `tools/emulate_04d16_exact.py` reproduz essa semântica. Com todas as fontes ativas, os tamanhos confirmados foram: AC47 = 12 registros, AC6C = 24, ACB5 = 2 e ACBC = 8. Os relatórios `build/exact_04d16_ac47.md`, `build/exact_04d16_ac6c.md`, `build/exact_04d16_acb5.md` e `build/exact_04d16_acbc.md` registram os destinos e máscaras. Isso elimina uma ambiguidade importante: AC47/AC6C/ACB5/ACBC não devem ser tratados como tabelas de 04CFD.

Ainda falta emular o produtor `04BD5` e a rotina `04BBD -> 3954 -> RST 10h`, que fornecem os bytes de C032/C2B0/C2D0/C2E0 e os valores de C022/C025–C028/C215/C205/C251. Só depois dessa etapa será seguro declarar C280 completo.
