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

## Avanço atual: 04BD5 reconstruído

A referência `04BD5` foi localizada no banco físico 21, no offset `0x0BD5`, quando `FFFE=0x15`; no endereço lógico ela aparece como `0x8BD5`. A rotina lê uma tabela com contador e registros de três bytes (`endereço little-endian` + `máscara`). Para cada registro, testa `(RAM[endereço] & máscara)` e grava `0x01` ou `0x00` em um buffer sequencial apontado pelo `DE` do conjunto alternado de registradores. O chamador usa `EXX`, portanto os papéis de leitura e escrita precisam ser modelados separadamente.

`tools/emulate_04bd5_exact.py` reproduz essa operação e foi validado com AC47. O relatório `build/04bd5_exact_semantics.md` registra o disassembly e a consequência para a cadeia de C280. Isso confirma que `04BD5` produz bytes booleanos para as fontes de `04D16`; ainda falta reconstruir a cadeia de valores de RAM que antecede essa etapa.

## Avanço atual: 04BBD confirmado

Com a ROM japonesa fornecida localmente, a rotina física em `0x4BBD` do banco 21 foi disassemblada e confirmada como produtora de máscaras compactadas. Ela lê uma tabela do banco 19 contendo registros `(endereço de RAM, máscara)`, testa cada registro e combina os resultados nos bits `0..7` de `A`, usando `EX AF,AF'` enquanto lê a RAM e `RLC C` para avançar a máscara de saída. Os chamadores em `0x4A8D–0x4B0D` gravam os resultados em `C022`, `C025–C028`, `C215`, `C205`, `C281` e `C251`.

A ferramenta `tools/emulate_04bbd_exact.py` reproduz essa semântica e exige os valores de RAM explicitamente. O relatório `build/04bbd_exact_semantics.md` registra o disassembly, o mapeamento das tabelas e a cadeia subsequente `04BD5 -> 04D16`. A ROM permanece em `input/`, ignorada pelo Git. Ainda falta obter um trace ou snapshot do estado de RAM no ponto `0x4A8D` para produzir o `C280` real; não se deve usar estado zerado como resultado final.

## Ferramenta de continuidade: inicialização em runtime

Foi adicionada `tools/emulate_runtime_initialization.py`, que reproduz em uma única execução as semânticas confirmadas de `04BBD`, `04BD5`, `04D16` e `04CFD` sobre a ordem de inicialização observada no banco 21. Ela aceita bytes de RAM por `--set ADDR=VALUE` ou `--ram-json`, lista endereços ausentes e grava os buffers/resultados em um relatório. O estado vazio e um vetor sintético foram executados com sucesso; o estado vazio não deve ser interpretado como o estado real do jogo.

A ROM local foi usada apenas como entrada. A próxima melhoria necessária é conectar um trace de emulador ou snapshot obtido no ponto `0x4A8D`, quando `D120–D135` já refletem o estado do jogo. Com esse snapshot, a ferramenta poderá produzir os valores reais de `C022`, `C025–C028`, `C205`, `C215`, `C251`, `C281` e os buffers consumidos pela construção de `C280`.

## Avanço atual: executor SMS instrumentado

Foi adicionada `tools/run_sms_capture.py`, um executor diagnóstico que usa uma CPU Z80 real, mapeia os 32 bancos da ROM e controla `FFFE`/`FFFF`, RAM SMS e breakpoints. O teste inicial revelou uma espera em `0x04E7` dependente do VDP; foi incluído um stub limitado e explícito para liberar essa espera. Com ciclos agrupados, o executor agora avança pelo boot até rotinas de inicialização em torno de `0x4912`/`0x3542`, embora ainda não alcance `0x4A8D`. O próximo trabalho é modelar as demais esperas de VDP/interrupção, validando cada uma por contexto, antes de aceitar qualquer snapshot como real.

## Recurso adicional: código-fonte do Dega 1.12

Foi fornecido `Dega-1.12.tar.gz` como recurso local de referência. O código contém um emulador SMS/Mark III real, com núcleo Z80 (`doze/`), memória e VDP (`mast/mem.cpp`), paginação SMS (`mast/map.cpp`) e temporização/interrupções (`mast/frame.cpp`). A implementação confirma que `FFFE`/`FFFD`/`FFFC`/`FFF8` são tratados como registradores de mapper, que a RAM ocupa `C000–DFFF` com espelho em `E000–FFFF`, e que as portas VDP `BE/BF` controlam VRAM, CRAM, status e auto-incremento.

O Dega 1.12 não oferece um debugger moderno pronto para o nosso uso e a compilação original depende de GCC, SDL 1.2 e NASM, ausentes no ambiente. O arquivo foi usado como referência local, não foi adicionado ao repositório. A adaptação em andamento é incorporar ao `tools/run_sms_capture.py` o comportamento necessário de VDP e interrupções para alcançar o breakpoint `0x4A8D` e capturar o estado de RAM.

## Reforço do protocolo de continuidade

A partir desta etapa, toda descoberta ou alteração técnica significativa deve ser registrada imediatamente em `docs/CONTINUATION.md` ou em um relatório específico, validada com testes, revisada com `git diff --check`, commitada com mensagem no formato `area: descrição` e enviada com `git push origin main`. Antes de cada commit deve ser confirmado que ROMs, save states, dumps completos e outros artefatos locais permanecem ignorados e fora do Git. O último estado enviado inclui o executor SMS instrumentado no commit `d4d137f`; esta atualização registra o Dega e o plano de integração.

## Etapa concluída: modelo VDP no capturador

O `tools/run_sms_capture.py` agora contém um modelo VDP baseado em `mast/mem.cpp` do Dega: portas `BE/BF`, latch de comando de dois bytes, endereço de 14 bits, modos VRAM/CRAM, auto-incremento, registradores VDP e leitura de status. O relatório passou a incluir endereço, modo, status, registradores e contagem de bytes não nulos em VRAM/CRAM.

A validação com a ROM foi bem-sucedida: o boot executou escritas VDP e produziu VRAM não vazia (`2626` bytes não nulos no teste), confirmando que a camada não está mais sendo simplesmente ignorada. O executor ainda não alcança `0x4A8D`; o ponto atual é uma rotina de espera/coordenação de hardware em torno de `0x04E4`, que depende do atendimento correto de VBlank/H-interrupt. A próxima etapa é modelar o agendamento e a aceitação de IRQ pelo núcleo Z80, sem transformar o stub de VDP em um valor artificial de RAM.

## Etapa experimental: injeção de IRQ IM1

O capturador recebeu `--irq-every-runs` e uma injeção controlada de IRQ modo IM1 entre blocos nativos. Como o binding Python do núcleo Z80 expõe `IFF` apenas para leitura e não possui uma API pública de latch de IRQ, a implementação usa o `state_view()` gravável para empilhar o PC, limpar IFF1/IFF2 e saltar para `0038h`. Isso é útil para diagnóstico, mas ainda não é considerado um modelo final de temporização.

Os testes confirmaram que o vetor de IRQ é alcançado, porém o retorno/coordenação do handler ainda não está correto: com IRQ frequente o PC pode permanecer em `0038h`/rotinas de serviço e `D120–D135` continuam zerados. Não usar os valores obtidos nessa fase como snapshot real. A próxima correção deve reproduzir a cadência por scanline do Dega e preservar o estado de interrupção/retorno com a mesma semântica do hardware, ou então compilar um harness nativo do núcleo Doze sem depender da GUI SDL.

## Teste de cadência por scanline

Foi adicionado `--scanline-irq` ao `tools/run_sms_capture.py`. O modo avança uma linha NTSC por execução nativa (`228` ciclos), marca VBlank na linha 193 e considera H-interrupt conforme os bits dos registradores VDP `Reg[0]` e `Reg[10]`, seguindo a estrutura de `frame.cpp` do Dega.

O teste de 12.000 linhas/execuções compilou e terminou rapidamente, mas ficou em `0x0545` com os registradores VDP ainda zerados e sem alcançar `0x4A8D`. Isso mostra que a cadência não deve ser aplicada desde o reset sem modelar o restante do protocolo de frame; não há snapshot válido nesta etapa. O próximo passo é inicializar o frame/VDP no ponto correto e tratar a espera em `0x0545` por seu contexto, em vez de liberar loops genericamente.

## Correção de diagnóstico: 0545 é atraso, não espera VDP

A disassemblagem de `0x053F–0x054D` confirmou que `0x0545` apenas executa um atraso aninhado (`BC=0x1999`, `B=0x14`) e retorna. O bloqueio aparente observado nessa faixa não era uma espera de hardware. Com o modelo VDP atual, a execução passa por esse atraso e chega ao loop principal em `0x34xx`, com escritas reais em VRAM e troca do banco `FFFF` para `0x84`.

A busca por `CALL 0545` não encontrou chamadas diretas porque a rotina é alcançada por `CALL 053F`/outros caminhos. O breakpoint `0x4A8D` não ocorre no boot inicial: a execução precisa avançar por uma transição de jogo/cena e por entrada de usuário para chegar à inicialização de diálogo. Portanto, o próximo passo não é liberar mais um loop de VDP, mas modelar o estado de entrada/frames ou localizar um ponto de entrada de cena que leve ao código em `0x4A8D`.

## Entrada de controle configurável

O capturador recebeu `--input-value`, usado nas portas SMS `DC/C0`, para permitir testes reproduzíveis de ações sem alterar o código. A varredura dos valores ativos comuns (`FF`, `FE`, `FD`, `FB`, `F7`, `EF`, `DF`, `BF`, `7F`) produziu o mesmo fluxo: `step_limit` em `0x3546` após 500 execuções nativas, com banco `FFFF=0x84`. Portanto, uma entrada fixa isolada não avança a cena; o loop principal depende também do estado de frame/rotinas de jogo e possivelmente de transições temporais. Não foi obtido snapshot válido.
