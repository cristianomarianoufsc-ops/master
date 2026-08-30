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
