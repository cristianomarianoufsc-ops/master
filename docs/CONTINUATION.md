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

Antes de cada commit, executar `git status`, verificar se não há ROMs ou estados de emulador, revisar o diff e atualizar este manual ou um relatório específico. Usar mensagens no formato `area: descrição`, por exemplo `docs: document dual-slot mapper`, `feat: add exact 04cfd emulator` ou `analysis: classify dialogue pointer tables`. Após cada nova etapa técnica descoberta e validada, o agente deve publicar imediatamente o commit usando a autenticação GitHub conectada ao Manus: confirmar primeiro a identidade com `gh api user`, executar `git push origin main`, e verificar que o remoto recebeu o hash com `git status --short --branch` ou `git log --oneline --decorate -n 2`. Não considerar a etapa concluída enquanto o push não tiver sido confirmado. Se o push direto pelo Git falhar por falta de credenciais, não abandonar a publicação: usar o cliente GitHub autenticado pela conexão do Manus e repetir a verificação. Registrar no relatório o hash commitado e o hash efetivamente enviado.

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

A conexão GitHub habilitada no Manus deve ser usada para publicar o trabalho do projeto. A autenticação disponível para o cliente GitHub pode não aparecer como credencial configurada no transporte HTTPS do Git; por isso, o agente deve validar a conta com `gh api user` antes de publicar e não deve concluir que o acesso está indisponível apenas porque uma tentativa inicial de `git push` solicitou usuário e senha.

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

## Avanço atual: sequência de entradas no capturador

O executor `tools/run_sms_capture.py` agora aceita `--input-sequence`, uma lista separada por vírgulas de valores hexadecimais ou decimais para as portas de controle `DC/C0`. Cada valor é aplicado a um bloco nativo sucessivo; quando a execução ultrapassa o tamanho da lista, o último valor permanece ativo. O relatório JSON inclui a sequência configurada e os últimos valores efetivamente usados por bloco.

Essa mudança permite testar combinações de soltura, pressionamento e manutenção de botões sem alterar a ROM, mas não constitui ainda um modelo completo de eventos do jogo. A sequência atua apenas na fronteira entre chamadas `run()`; o estado de frames, VBlank e o retorno correto das IRQs continua sendo uma limitação documentada.

A alteração foi validada com `py_compile`, `--help` e uma ROM sintética temporária de 32 bancos, confirmando o parsing de `0xFE,0xFD` e seu registro no relatório. A dependência pública `z80==1.0.0` foi instalada no ambiente de execução; a ROM sintética e o relatório de teste permaneceram fora do repositório.

## Avanço atual: ROM japonesa e ordem de frame do Dega

A ROM japonesa foi recebida localmente como `input/KujakuOu_Japan.sms` e o pacote `Dega-1.12.tar.gz` foi extraído somente em área temporária para referência. Ambos permanecem fora do Git conforme a política do projeto.

A comparação com `mast/frame.cpp` confirmou que o Dega executa cada frame na ordem `MastY=192`, depois `193–261` e finalmente `0–191`, com `228` ciclos por linha em NTSC. O capturador recebeu a opção `--dega-frame-schedule` para reproduzir essa ordem, mantendo o modo anterior disponível para comparação. O processamento de H-interrupt foi alinhado ao contador `Reg[10]` e o VBlank continua condicionado a `Reg[1] & 0x20`.

Na captura real com a ROM (`120` blocos, `50.000` ticks por bloco, `--scanline-irq --dega-frame-schedule`, entrada `FF,FE,FF`), o executor chegou a `0x3591`, com `FFFF=0x84` e VRAM com `2626` bytes não nulos, mas ainda não alcançou `0x4A8D`; os campos `C022`, `C025–C028`, `C205`, `C215`, `C251`, `C280` e `C281` permaneceram zerados. Portanto, a captura ainda não deve ser usada como snapshot real. O próximo diagnóstico deve concentrar-se no loop principal em `0x34xx–0x3591`, no estado de entrada e na semântica de retorno/aceitação de IRQ, antes de ampliar o número de frames.

## Avanço atual: trace do loop e latch de IRQ

Foi criada `tools/analyze_capture_trace.py`, uma ferramenta independente que resume arquivos de trace, conta PCs e endereços recorrentes, separa leituras de controle e lista alterações de mapper. O capturador também passou a registrar `FFFE/FFFF` em cada evento detalhado, permitindo interpretar corretamente PCs nas janelas paginadas.

O trace revelou dois problemas no modelo experimental. Primeiro, o ciclo repetia principalmente `0x34DA`, `0x350C`, `0x3530`, `0x355E` e `0x48ED`, alternando escritas em `FFFF`; as leituras de controle ocorriam apenas durante a rotina inicial em `0x055F`, não no loop principal. Segundo, o injetor aceitava uma IRQ em toda chamada de agendamento mesmo sem uma solicitação pendente, causando centenas de entradas artificiais em `0x0038`.

Foi corrigido o segundo problema: IRQs agora são solicitadas por `request_irq()` e permanecem latched até que `IFF1` permita a aceitação. Após a correção, uma captura de 450 blocos com a ROM japonesa injetou apenas uma IRQ, não ficou presa no vetor `0x0038` e retornou ao ciclo de boot em `0x3537`; ainda não alcançou `0x4A8D`. O próximo passo é modelar o estado de frame/IRQ no ponto em que o jogo deixa o boot, mantendo o trace de bancos e investigando o estado de `C021` e das rotinas `0x43F2/0x48ED/0x4939`.

## Avanço atual: janela de amostragem do controle

O trace com valores de leitura mostrou que a primeira leitura da porta `DC` ocorre aproximadamente no bloco nativo `265`, dentro da rotina em `0x055F`; a entrada não é amostrada continuamente no ciclo `0x34xx`. Uma sequência que manteve `0xFF` até o bloco 260, aplicou `0xFE` por 30 blocos e depois liberou o controle alterou o fluxo: após duas passagens de VBlank, o executor terminou em `0x491C`, em vez de permanecer em `0x3537`. Isso confirma que a entrada precisa ser temporizada em relação ao avanço do boot, mas ainda não constitui uma transição válida para `0x4A8D`.

O trace foi aprimorado para registrar também o valor lido de cada endereço monitorado, em particular `C021`, e a instrumentação foi mantida como ferramenta diagnóstica. O próximo experimento deve testar cada máscara de botão na janela em torno do bloco 265, mantendo a mesma cadência de frames, e comparar as rotinas alcançadas em `0x491C`, `0x4939`, `0x4A8D` e seus retornos.

## Avanço atual: matriz de botões e espera em 0x406F

Foi criada `tools/run_input_matrix.py` para executar máscaras de controle temporizadas e comparar PC final, bancos ativos, IRQs e leituras da porta `DC`. A matriz manteve `0xFF` até o bloco 260, pressionou cada máscara por 30 blocos e depois liberou.

As máscaras `0xFE`, `0xFD`, `0xFB`, `0xF7`, `0xBF` e `0x7F` convergiram para `0x491C`, com duas IRQs observadas. As máscaras `0xEF` e `0xDF` seguiram um caminho diferente e ficaram em `0x406F/0x4073`, com `FFFE=0x95` e `FFFF=0x16` (valores crus do mapper). Nesse caminho, `C203` foi lido mais de cem mil vezes, indicando uma espera específica de estado de cena.

Foi testado liberar artificialmente a espera de `C008` também em `0x406F`; o fluxo continuou em `0x4073` e não alcançou `0x4A8D`. Por segurança, `0x406F` não faz parte da lista padrão de pontos liberados. A opção `--vdp-wait-pcs` permanece configurável para experimentos explícitos, mas nenhum valor obtido com esse desbloqueio deve ser tratado como snapshot real. O próximo passo é reconstruir a condição de `C203` e a rotina paginada do banco 21 antes de alterar a temporização novamente.

## Avanço atual: condição real do loop 0x406F

O trace foi ampliado para registrar `C008`, além dos registradores `A–L` do Z80. No caminho acionado por um pulso de `0xEF` no bloco 265, a execução entra no banco físico 21 com `FFFE=0x95` e `FFFF=0x16`, e permanece no ciclo `0x406F/0x4073`. Durante aproximadamente 25 mil leituras, `C008` permaneceu em `0x02` e `C203` em `0x01`; nos eventos observados, `B=0`, `C=1` e `A` alternou entre os valores usados pelo teste da condição.

Essa evidência confirma que a espera de `0x406F` não pode ser liberada simplesmente zerando `C008`: o estado de cena em `C203` também participa da condição, e a combinação atual representa uma operação de carregamento ainda pendente. A ferramenta não foi alterada para forçar essa transição. O próximo passo é mapear os escritores de `C008` e `C203` e comparar o caminho com uma execução real do Dega, antes de introduzir qualquer valor sintético.

## Avanço atual: VBlank periódico confirmado

O trace passou a distinguir `irq_requested`, `irq_injected` e `vblank_tick`. Uma execução sem registros repetitivos, usando `--trace-pc-range 0x0000-0x0000`, confirmou VBlanks nos blocos 2, 264 e 526. As solicitações e aceitações de IRQ ocorreram nos blocos 264 e 526, portanto a ausência aparente de VBlanks em traces anteriores era causada pelo limite do arquivo sendo consumido pelas leituras repetitivas de `C008/C203`, não por uma falha da cadência.

Mesmo com IRQs periódicas aceitas, o caminho do botão `0xEF` continua em `0x406F/0x4073`, com `C008=0x02` e `C203=0x01`. A hipótese de que bastaria gerar mais VBlanks foi descartada. A investigação deve agora acompanhar o handler em `0x0038` e os escritores de `C008/C203` depois da segunda IRQ, procurando a diferença entre o estado esperado pelo jogo e o estado produzido pelo modelo VDP.

## Gate contra falsos positivos

Foi criada `tools/audit_false_positives.py` para auditar relatórios e traces antes de aceitar uma conclusão. A ferramenta sinaliza, entre outros riscos, breakpoint não alcançado, trace saturado, erro de captura, configuração de temporização não referencial, ausência de leitura de controle, divergência entre IRQ solicitada e aceita, vetor de IRQ inválido, flags `C008/C203` presas e PC dominante indicando loop.

O auditor retorna `status=pass` apenas quando não encontra alertas, `status=review` quando há avisos que exigem análise humana e `status=risk` quando encontra risco crítico; nesse último caso o processo termina com código diferente de zero. O resultado não prova a correção do emulador: ele funciona como barreira contra aceitar evidência incompleta ou confundida com progresso.

Aplicado à captura longa do caminho `0xEF`, o auditor retornou `status=risk` e detectou corretamente `BREAKPOINT_NOT_REACHED` (`PC=0x4074`, alvo `0x4A8D`) e `TRACE_SATURATED` (`500000/500000` registros). Essa captura não deve ser usada como snapshot nem como prova de que o diálogo foi alcançado.

## Avanço atual: captura real e trace amostrado

A ROM japonesa fornecida pelo usuário foi instalada localmente como `input/KujakuOu_Japan.sms` e permanece ignorada pelo Git. O pacote `Dega-1.12.tar.gz` foi mantido somente em `/home/ubuntu/reference/`, também fora do repositório.

A captura-base com `--scanline-irq --dega-frame-schedule` e entrada `FF,FE,FF` não alcançou `0x4A8D`; o auditor classificou-a como `risk` por `BREAKPOINT_NOT_REACHED`. Uma reprodução da janela documentada, mantendo `0xFF` até o bloco 260 e aplicando `0xEF` por 30 blocos, convergiu para `0x406F/0x4073`, com `FFFE=0x95`, `FFFF=0x16`, `C008=0x02` e `C203=0x01`. A auditoria confirmou `BREAKPOINT_NOT_REACHED`, além de `FLAG_STUCK` e `DOMINANT_PC_LOOP`; a captura original também saturava o limite de trace.

Para evitar que loops de espera saturem o trace, `tools/run_sms_capture.py` recebeu `--trace-every N`. A opção registra um evento correspondente a cada N eventos de trace, preservando eventos forçados de IRQ, VBlank e controle. Com `--trace-every 32`, a mesma captura não saturou o trace e confirmou, de forma mais limpa, que `C008` e `C203` permanecem constantes sem escritores observados durante a espera. O auditor continua retornando `risk` exclusivamente porque `0x4A8D` não foi alcançado, e `review` pelos flags presos, loop dominante e entrada variável.

Essa etapa não constitui snapshot válido de `C280`. A conclusão operacional é que o problema atual está na transição de cena/estado que antecede `0x406F`, não na falta de capacidade do trace. O próximo diagnóstico deve correlacionar os escritores estáticos de `C008/C203` encontrados na ROM com o trace dinâmico e investigar por que a rotina paginada de banco 21 não altera esses flags no caminho de entrada `0xEF`.

## Matriz de entradas após a captura real

Com a ROM real, a matriz temporizada manteve `0xFF` até o bloco 260, pressionou cada máscara por 30 blocos e liberou em seguida. As máscaras `0xFE`, `0xFD`, `0xFB`, `0xF7`, `0xBF` e `0x7F` terminaram em `0x3537` com `FFFF=0x84`; as máscaras `0xEF` e `0xDF` terminaram em `0x4073` com `FFFE=0x95` e `FFFF=0x0C`.

A leitura da porta de controle ocorreu no bloco 265, confirmando a janela temporal. Cada relatório principal foi submetido ao auditor e todos retornaram `risk` por não alcançarem `0x4A8D`; portanto, nenhum caminho da matriz foi aceito como evidência de diálogo. No caminho `0xEF/0xDF`, o trace estreito e amostrado confirmou repetição da espera em torno de `0x406F/0x4073`, com `C008=0x02` e `C203=0x01`, sem saturação após a introdução de `--trace-every`.

A filtragem correta dos relatórios também foi registrada operacionalmente: arquivos `*-trace.json` são artefatos auxiliares e não devem ser passados como relatório principal ao auditor. O próximo passo é instrumentar a correlação entre os escritores estáticos de `C008/C203` e os eventos dinâmicos, além de localizar a rotina paginada que deveria consumir ou alterar o estado de cena após `0x4073`.

## Probe diagnóstico do loop de cena

Foi adicionada a opção explicitamente experimental `--diagnostic-release-scene-wait` ao capturador. Quando combinada com `--vdp-wait-pcs 0x406F,0x4073`, ela limpa `C203` nos pontos de espera para revelar o caminho posterior, sem alterar o comportamento padrão e sem permitir que o resultado seja interpretado como snapshot real.

O probe com a janela `0xEF` não alcançou `0x4A8D`; após o desbloqueio artificial, a execução retornou a `0x04E7` e terminou com `BREAKPOINT_NOT_REACHED`. O auditor classificou o relatório como `risk`. Esse resultado é útil apenas como diagnóstico: liberar `C008/C203` não resolve a causa, mas desloca a execução para outra espera anterior do boot. A opção deve permanecer marcada como experimental e nunca ser usada para validar o estado de `C280`.

A análise estática confirmou que `0x406C` é um loop que só retorna quando `C203` e `C008` estão ambos zerados. No caminho testado, `0x40F5–0x40FA` grava `C008=2`, `C203=1` e `C204=1`; a IRQ em `0x01A1` limpa `C008`, mas não `C203`. A única referência direta encontrada a `HL=C203` está na rotina em torno de `0x433D`, que não foi alcançada pelo probe. O próximo passo é reconstruir a cadeia de carregamento que deveria chamar essa rotina, em vez de liberar flags sinteticamente.

## Probe completo após a publicação do diagnóstico

Após o commit do probe diagnóstico, foi repetido o experimento com os pontos de espera do boot (`0x04E7/0x04EA/0x04EB`) e da cena (`0x406F/0x4073`) configurados simultaneamente. A captura percorreu 650 blocos, observou três VBlanks e três IRQs aceitas, mas terminou em `0x4000` com `FFFF=0x82`, sem alcançar `0x4A8D`. O auditor retornou `risk` por `BREAKPOINT_NOT_REACHED`; a entrada variável foi registrada como advertência.

O trace não saturado registrou atividade nos PCs `0x4017`, `0x4065`, `0x406A`, `0x406F`, `0x4073`, `0x43F2`, `0x4496` e `0x4939`, mas a liberação artificial não produziu uma transição estável para o diálogo. Em vez disso, o fluxo voltou a rotinas de inicialização e alternância de banco. Isso reforça que limpar `C008/C203` não é um substituto para a operação de carregamento real; o probe serve somente para localizar dependências posteriores.

A partir desta etapa, não serão feitos novos desbloqueios sintéticos como tentativa de alcançar `0x4A8D`. A investigação deve se concentrar na causa do carregamento pendente: a rotina em `0x40F5–0x40FA` inicia a operação, o loop em `0x406C` aguarda ambos os flags zerarem, e as rotinas que deveriam consumir o estado precisam ser reproduzidas na ordem correta do jogo/emulador.

## Descoberta: 0x8B8B é um limpador incondicional de slots

A janela física de `0x8B80–0x8BCF` foi extraída do banco 2, ativo quando `FFFF=0x82`, e documentada em `build/a0_cleanup_routine.md`. A sequência em `0x8B81` inicializa `HL=DD17h`, zera `A`, executa dez iterações e grava zero em cinco campos por slot, avançando `0x20` bytes por iteração. O laço não testa `C203`, `DD97` nem o bit 7 dos slots; portanto, não há uma condição interna em `0x8B8B–0x8B93` que escolha desmontar a tarefa A0.

A correspondência entre `DD17` e `DDF7` ocorre na oitava iteração, com os campos associados em `DE0F–DE12`, exatamente os endereços observados no trace. A interpretação correta é que o chamador leva a execução ao limpador geral enquanto a operação A0 ainda está pendente. O próximo probe deve capturar o fluxo de entrada e o endereço de retorno imediatamente antes de `0x8B81`, correlacionando `DD03`, `DD97`, `DDB7` e `C203`. Nenhum desbloqueio sintético deve ser usado.

## Descoberta: variantes de timing mudam o bloqueio, mas não alcançam 0x4A8D

A mesma sequência causal foi testada com três modelos: baseline sem agendamento de scanlines, modelo Dega com `--scanline-irq` e `--dega-frame-schedule`, e modelo Dega com oito leituras antes de liberar a espera VDP. Os PCs finais foram, respectivamente, `0x3546`, `0x4070` e `0x4073`; nenhum alcançou `0x4A8D`. O relatório está em `build/a0_timing_variants.md`.

O modelo Dega com agendamento de scanlines continua sendo a referência, porque reproduz o fluxo de cena e o bloqueio A0/C203. O baseline é controle negativo; aumentar o limiar VDP altera o ponto do loop, mas não resolve a transição. Não será usado como correção um desbloqueio artificial de `C203`.

## Descoberta: matriz de duas janelas não alcança o diálogo

Foi criada `tools/run_two_window_matrix.py` para testar os valores `0x00`, `0x10`, `0x20` e `0x30` nas duas janelas reais de leitura do controle, nos blocos 265 e 527. As 16 combinações foram executadas com semântica de I/O do Dega até o bloco 900. Quinze combinações terminaram em `0x406C` com `FFFF=0x16`; a combinação sem entrada nas duas janelas terminou em `0x3548` com `FFFF=0x84`. Nenhuma alcançou `0x4A8D`.

A segunda leitura de controle, portanto, altera o caminho para a espera de cena, mas não é suficiente para disparar o diálogo. As execuções continuam sendo evidência diagnóstica, não snapshots válidos. O próximo probe deve correlacionar a leitura do bloco 527 com `C202`, `C206`, `DD03`, `DD97` e o pedido de tarefa associado a `C203`.

## Descoberta: dois chamadores distintos do limpador A0

A instrumentação passou a registrar `SP` e os dois bytes no topo da pilha em eventos de execução. O relatório `build/a0_cleanup_callers.md` confirma que o inicializador em `0x8B62` é alcançado por dois chamadores: o `CALL 0x8B62` em `0x0533`, com retorno `0x0536`, e o `CALL 0x8B62` em `0x4569`, com retorno `0x456C`. O bloco 267 usa o chamador fixo de `0x0533`; o bloco 277 usa o chamador paginado de `0x4569`; o bloco 278 volta ao chamador fixo com `FFFE=0x95`.

Essa descoberta separa duas causas possíveis para a limpeza de `DDF7`: a inicialização geral de boot e uma reentrada pelo caminho paginado de jogo. O próximo probe deve comparar `C203`, `DD03`, `DD97` e `DDF7–DE16` antes de cada chamador, em vez de atribuir a desmontagem diretamente ao dispatcher A0.

## Ferramenta específica para o ciclo da tarefa A0

Foi adicionada `tools/analyze_a0_task_lifecycle.py`, que resume eventos de armamento, limpeza e atividade do grupo `DDF7–DE16`, além de `C203`, `DD03` e `DD97`, a partir de uma captura JSON. A ferramenta é somente observacional: não libera esperas, não altera RAM e não interpreta a ausência do breakpoint como sucesso. O capturador e `tools/run_timed_capture.py` também aceitam `--trace-forced-addresses`, permitindo retirar `C008` do conjunto de eventos forçados e evitar que o loop diagnóstico de boot sature um trace focalizado.

A validação foi feita com a ROM local, sem alterar a ROM e sem publicar artefatos locais. Com `--trace-memory-range 0xDDF7-0xDE16`, `--trace-pc-range 0x8000-0x8D00` e `--trace-forced-addresses 0xC203`, a captura de 1.100 blocos terminou em `0x4070` e não alcançou `0x4A8D`, como esperado para uma evidência ainda não conclusiva. O trace focalizado registrou no bloco 265 a cópia da estrutura para `DDF7–DE06`, incluindo `DDF7=0xA8`; no bloco 267, `0x8B8B–0x8B93` escreveu `DDF7=0` e zerou `DE0F–DE12`; no bloco 285, `0x40FA` iniciou nova operação com `C203=1`. Isso reproduz e detalha a desmontagem prematura já observada, sem usar desbloqueio sintético.

## Correção incremental: limpeza do latch de IRQ pelo VDP

A comparação com `mast/mem.cpp` do Dega revelou que leituras do status VDP (`BF`) e escritas de controle VDP limpam o latch de interrupção. O capturador foi ajustado para limpar `pending_irq` nesses dois pontos, mantendo a solicitação de IRQ separada da aceitação pelo Z80.

A alteração passou por compilação e captura curta. Na captura real com a janela `0xEF`, o caminho continuou terminando em `0x4073`, sem alcançar `0x4A8D`. O auditor retornou `risk` por `BREAKPOINT_NOT_REACHED` e apontou uma divergência entre duas IRQs solicitadas e uma aceita, além de `C203=1` constante e PC dominante em `0x406F`. Portanto, a correção alinha o modelo a uma semântica documentada do Dega, mas não constitui avanço suficiente para declarar a transição de cena resolvida.

A hipótese atual permanece: o carregamento iniciado em `0x40F5–0x40FA` depende de uma cadeia de estado que não está sendo reproduzida pelo capturador; apenas ajustar o latch VDP não libera corretamente `C203`.

## Instrumentação: escritores dinâmicos de flags

O capturador passou a registrar escritas em `C008` e `C203` independentemente da faixa de PCs configurada para o trace. Isso evita perder produtores que executam em handlers de IRQ, no boot ou em bancos diferentes da rotina sob investigação. A opção não altera a execução; apenas garante que os eventos de escrita dos dois flags sejam preservados no relatório.

A validação com captura curta passou e o auditor retornou `risk` somente por breakpoint não alcançado, IRQ solicitada sem aceitação, ausência de leitura de controle na faixa escolhida e loop dominante em `0x04E4`. A nova instrumentação foi confirmada pelo registro das escritas em `C008` durante o boot, mesmo com trace restrito a outra faixa de PCs. Ela será usada no próximo experimento de correlação entre escritores e o loop de cena.

## Avanço atual: primeira conclusão real de carregamento

A captura padrão com a ROM real, sem liberar artificialmente `C008/C203`, foi estendida para 650 blocos usando a janela de entrada `0xEF` e a instrumentação de escritores forçados. O trace foi auditado e retornou `risk` porque `0x4A8D` ainda não foi alcançado, mas revelou uma transição real importante.

No bloco 305, a rotina em `0x40F5–0x40FA` iniciou o carregamento com `C008=2`, `C203=1` e `C204=1`. No bloco 527, após o VBlank/IRQ seguinte, `0x01A1` limpou `C008` e a rotina em `0x432F` limpou `C203`. Isso demonstra que o loop `0x406C` pode ser concluído pelo fluxo normal, sem desbloqueio sintético. Em seguida, no bloco 536, o programa iniciou uma segunda operação no banco `FFFF=0x13`, gravando `C008=2` e `C203=2` em `0x412A/0x412D`.

Esse resultado corrige a hipótese anterior de que o primeiro carregamento permanecia permanentemente preso. O capturador está reproduzindo pelo menos uma conclusão real de operação e avançando para um segundo carregamento, embora a captura de 650 blocos ainda termine sem `0x4A8D`. O próximo passo é estender a execução após o bloco 536 e rastrear essa segunda operação, preservando as escritas forçadas de `C008/C203` e usando o auditor antes de aceitar qualquer novo marco.


## Validação: semântica de I/O compatível com Dega

O código de referência do Dega foi extraído somente para `/home/ubuntu/reference/dega-1.12/`. A comparação com `mast/frame.cpp` e `mast/mem.cpp` identificou duas diferenças úteis para o diagnóstico: o valor do V-counter na porta `0x7E` e a conversão ativa-baixa das portas de controle `0xDC/0xC0`. O capturador recebeu a opção opcional `--dega-io-semantics`, preservando o comportamento histórico quando ela não é usada.

A captura com essa opção, 900 blocos, agendamento de frame do Dega e entrada interna `0x00, 0x10, 0x00` na janela já documentada, reproduziu o mesmo caminho: leitura `0xEF` no bloco 265, PC final `0x406C`, `FFFE=0x95`, `FFFF=0x16`, `C021=0x88`, `C022=1`, `C205=0` e `C280=0`. O auditor retornou `risk` por `BREAKPOINT_NOT_REACHED`, entrada variável e `C203=2` preso na espera.

A semântica de I/O do Dega, portanto, não é a causa principal do bloqueio da segunda operação. O próximo foco continua sendo a cadeia iniciada em `0x403A/0x403F` e a rotina paginada que deveria consumir o carregamento e limpar `C203`; não usar desbloqueios sintéticos nem esse resultado para declarar `C280` válido. O relatório detalhado está em `build/dega_io_semantics_validation.md`.

## Nova ferramenta: ciclo de vida dos flags de cena

Foi criada `tools/analyze_scene_flag_lifecycle.py`, que aceita uma captura ou trace JSON, normaliza endereços, agrupa escritas de `C008/C203` por PC, valor e bancos ativos, lista os blocos relevantes e mostra janelas locais de contexto. O relatório é observacional: não atribui causalidade a uma escrita e não libera flags sinteticamente.

Aplicada à captura Dega de 900 blocos, a ferramenta confirmou 8 escritas de `C203`: inicialização em `0x00AD`, limpeza em `0x4939`, início em `0x40FA`, limpeza em `0x432F`, segunda inicialização em `0x412D`, e eventos posteriores em `0x4352/0x403F`. Também confirmou a segunda operação em `0x412A/0x412D` no bloco 531 e o novo início em `0x403A/0x403F` no bloco 789, quando o executor permanece em `0x406C`. O relatório condensado está em `build/dega_io_flag_lifecycle.md`.

## Descoberta: segunda operação reinicia em ciclo

A nova ferramenta `tools/analyze_scene_flag_lifecycle.py` foi aplicada à captura compatível com Dega de 900 blocos. Além da segunda operação iniciada em `0x412A/0x412D` no bloco 531, o trace mostra nova tentativa em `0x403A/0x403F` no bloco 789, com `C008=2` e `C203=1`, seguida pelo loop `0x406C`. Isso indica que a segunda operação pode ser rearmada depois de uma passagem incompleta, e não deve ser modelada como uma única espera estática. O relatório agrupado está em `build/dega_io_flag_lifecycle.md`; a causa da ausência de limpeza de `C203` ainda não foi resolvida.

## Descoberta: consumidores de C203 passam pelo dispatcher de IRQ

A desassemblagem do banco físico 21 confirmou que `0x432F` e `0x4352` implementam os consumidores dos bits 0 e 1 de `C203`, respectivamente, usando também os bits correspondentes de `C204`. Eles não possuem chamadas diretas no banco 21. O handler de IRQ em `0x015D–0x01B4` grava `FFFF=0x82`, chama `0x8000` e só então limpa `C008`; a entrada `0x8000` do banco 2 percorre estruturas de tarefas em `DDxx`. A hipótese operacional atual é que a conclusão da segunda operação depende de uma tarefa/estado em `DDxx` que o capturador ainda não reproduz, e não simplesmente de mais IRQs. Essa conclusão foi obtida sem desbloqueio sintético.

## Descoberta: atividade de tarefas DDxx durante o segundo carregamento

O capturador recebeu `--trace-memory-range`, permitindo registrar leituras e escritas em intervalos como `DD00–DE37` sem ampliar indiscriminadamente o trace de PCs. Foi adicionada também `tools/summarize_ddxx_trace.py` para resumir esses eventos.

Na captura de 800 blocos com a semântica do Dega, foram observados 42 eventos DDxx, incluindo 28 escritas. Durante o caminho do segundo carregamento, no bloco 789, as rotinas `0x855E` e `0x8786` escreveram em `DD64` e `DD66`; outras atualizações ocorreram em `DD07`, `DD32`, `DD6F` e `DDB7`. O dispatcher de IRQ, portanto, está modificando registros de tarefas quando a execução termina em `0x4073`; a hipótese de que a cadeia não é executada foi descartada. O próximo passo é seguir o slot em torno de `DD57–DD76`, correlacionando o bit 7 do registro de tarefa com as chamadas `0x8585/0x85DB`.

## Correção de hipótese: segunda operação também conclui

O trace focado em `DD57–DD76` mostrou que, após a operação iniciada em `0x403A/0x403F` no bloco 789, o dispatcher prepara a tarefa em `DD57–DD66` e processa seus estados pelas rotinas `0x855E`, `0x8786`, `0x8CA6` e relacionadas. No bloco 1051, a rotina `0x432F` limpa `C203`; imediatamente depois, `0x4065/0x406A` inicia outra operação com `C008=2` e `C203=2`. A segunda operação, portanto, não fica permanentemente presa em `0x406C`; a captura anterior apenas terminou antes de sua conclusão. A investigação deve agora acompanhar as operações subsequentes até a transição de diálogo.

## Descoberta: ciclo periódico de carregamentos sem transição de diálogo

A captura estendida para 3.500 blocos confirmou um padrão periódico. Após a primeira conclusão em `0x432F`, as operações seguintes alternam entre `0x4065/0x406A` e `0x403A/0x403F` a cada 262 blocos aproximadamente. As conclusões passam por `0x432F` ou `0x4352`, mas o fluxo retorna ao carregamento e termina em `0x406F`. O problema atual não é uma operação individual permanentemente pendente; trata-se de uma espera/ciclo de cena que não dispara a transição para o diálogo.

O relatório completo está em `build/scene_3500_flag_lifecycle.md`, com o resumo DDxx em `build/scene_3500_ddxx_summary.txt`. O próximo experimento deve sincronizar pulsos de controle com esses ciclos, mantendo a auditoria e sem liberar flags artificialmente.

## Descoberta: pulsos tardios não são amostrados

A matriz de entradas com pulsos iniciados no bloco 1040 confirmou que o jogo não lê `DC/C0` nessa janela: as leituras permaneceram apenas nos blocos 265 e 527, com `0xFF`. Os casos `0xEF` e `0xDF` continuam no caminho `0x406F`; as demais máscaras retornam ao fluxo `0x3536`. O relatório está em `build/timed_input_matrix_1040.md`. Não se deve atribuir efeito causal aos pulsos tardios; o próximo teste deve alterar apenas a janela real de amostragem ou modelar a atualização de entrada por frame no emulador.

## Descoberta: entrada reconhecida, mas sem transição

A matriz na janela causal (blocos 240–299), agora com `--dega-io-semantics`, confirmou que as máscaras de controle são convertidas e reconhecidas: leituras no bloco 265 variaram entre `0xFE`, `0xFD`, `0xFB`, `0xF7`, `0xEF`, `0xDF` e `0xFF`. As máscaras `0x10` e `0x20` alteraram a cadência para uma IRQ e impediram a segunda leitura observada em 527, mas todos os caminhos terminaram em `0x406C` com `FFFF=0x16`. O relatório está em `build/input_window_240_dega.md`. A causa restante é estado/condição da cena, não ausência de amostragem do controle.

## Descoberta: combinações curtas também não mudam o caminho

Foram testadas combinações internas `0x03`, `0x0C`, `0x10`, `0x20`, `0x30` e `0x3F` por 1, 5 e 15 blocos na janela causal de entrada. Todos os casos terminaram em `0x4073`, sem alcançar `0x4A8D`; algumas combinações alteraram a segunda leitura no bloco 527 e a quantidade de IRQs, mas não a transição de cena. O relatório está em `build/input_short_combinations.md`. Foi adicionado `tools/summarize_input_matrix.py` para resumir matrizes sem depender de saída bruta.

## Descoberta: C202 participa do ponteiro C206

O probe determinístico de `C200–C20F` confirmou que a segunda operação em `0x412A/0x412D` calcula um valor em `C206` no bloco 531, após mudar `FFFF` para `0x16`: `C206=0x0080`, com a instrução em `0x4146`. O ciclo seguinte ainda conclui em `0x432F` e é rearmado em `0x406A`, mas retorna ao loop `0x4070`. Isso indica que o índice/estado em `C202` e o ponteiro em `C206` são candidatos mais promissores que os flags isolados para explicar a repetição da cena. Foram adicionados `tools/run_timed_capture.py` e `tools/summarize_memory_writes.py`; o relatório está em `build/c200_state_probe.md`.

## Descoberta: bloqueio localizado em 0x406F com FFFF=0x0C

O probe de acessos confirmou que o estado de bloqueio reproduzível começa no bloco 311: `0x406F` lê repetidamente `C203=1` enquanto `FFFF=0x0C`. Não há nova escrita de `C206` nem avanço ao breakpoint `0x4A8D`. O mesmo experimento também confirmou que outros ciclos alcançam `0x432F` e limpam `C203`, portanto o problema agora está restrito à cadeia do pedido associado ao banco `0x0C`/bit 0. O relatório está em `build/c206_block_state.md`; foi adicionado `tools/summarize_memory_accesses.py` para reproduzir a extração.

## Descoberta: tarefa DD57 não é armada no caminho FFFF=0x0C

A comparação direta do dispatcher no caminho bloqueado mostrou que ele executa, mas `DD57` permanece em `0` (escritas nos blocos 41, 46, 267, 277 e 278). No caminho que progride, `DD57` recebe `0x80` no bloco 789 e os handlers da tarefa são processados. O loop em `0x406F` ocorre porque `C203=1` aguarda essa tarefa sem que o bit 7 seja ativado. O diagnóstico está em `build/bank0c_task_block.md`; o resumidor `tools/summarize_memory_accesses.py` permite reproduzir a comparação.

## Descoberta: FFFF=0x0C executa, mas não arma DD57

A comparação do dispatcher confirmou que `FFFF=0x0C` não é banco ausente: `0x83E7` e os handlers de tarefa são executados. A diferença decisiva é que `DD57` permanece `0`, enquanto no caminho progressivo recebe `0x80`. O pedido chega a `0x406F` com `C203=1`, mas sem uma tarefa ativa para limpar o flag. O relatório está em `build/bank0c_dispatch_correlation.md`. O próximo diagnóstico deve comparar `DD03` e o índice de `sub_857C` entre os caminhos `0x0C` e `0x16`.

## Correção: comando A0 é roteado para DDD7, não DD57

A comparação de `DD03` revelou `DD03=0xA0` no bloco 265 no caminho bloqueado. Pela desassemblagem de `0x83E7`, o caso `0xA0` passa por `0x84D2` e seleciona `DE=DDD7` em `0x8504`; portanto, a hipótese anterior que tratava `DD57=0` como prova direta da tarefa pendente foi corrigida. O estado forte continua sendo `0x406F` lendo `C203=1` após `DD03=0xA0`. O próximo diagnóstico deve seguir `DDD7–DDF6`, não apenas `DD57–DD76`. Relatório: `build/command_a0_routing_correction.md`.

## Descoberta: comando A0 alcança DDD7, mas a tarefa permanece zerada

O probe `DDD7–DDF6` confirmou que o comando `0xA0` chega ao grupo correto, mas `DDD7` permanece zero. Nos passes de inicialização em `0x8B8B–0x8B93`, `DDD7` e `DDEF–DDF2` são zerados; o dispatcher lê `DDD7=0` e não chama handler ativo. Não houve escrita `DDD7=0x80`. O relatório está em `build/command_a0_unarmed_task.md`. O próximo diagnóstico deve seguir a tabela/dados fornecidos a `sub_857C` e `sub_8536`, procurando por que a entrada do grupo A0 é nula.

## Descoberta: tabelas do comando A0 têm ponteiros válidos

A resolução estática do índice `0x10` do comando `0xA0` encontrou ponteiros válidos em `l836D→0xAB5F`, `l833D→0xA2C7` e `l82DD→0xAB72`, todos com cabeçalhos estruturados. A hipótese de entrada nula na ROM foi descartada. O próximo passo é identificar a tabela efetivamente selecionada pelo estado `EX AF,AF'` e verificar em runtime até onde `sub_8536` copia a estrutura para `DDD7`.

## Correção runtime: A0 seleciona AB72 e o grupo DDF7/DD97

A extração de registradores nos eventos do dispatcher corrigiu a cadeia: com `DD03=0xA0`, `0x8536` usa o ponteiro `0xAB72`, trabalha com destino `DDF7` e sinaliza `DD97=4`; depois `0x857B` reduz `DD03` para `0x80`. Assim, o grupo efetivo do comando A0 é `DDF7–DE16`, com estado auxiliar em `DD97`, não `DDD7`. O relatório está em `build/command_a0_runtime_chain.md`, e foi adicionado `tools/extract_trace_pc.py`.

## Descoberta: tarefa A0 é armada e desmontada imediatamente

O trace do grupo correto `DDF7–DE16` mostrou que o comando `0xA0` é realmente armado no bloco 265: `DD97=4`, `DDF7=0xA8` (bit 7 ativo) e estrutura copiada para `DDF7–DE06`. No bloco 267, a rotina `0x8B8B–0x8B93` zera `DDF7` e `DDEF–DDF2`; depois o fluxo fica em `0x406F` lendo `C203=1`. A causa foi estreitada para desmontagem prematura da tarefa A0, não para tabela nula, banco ausente ou falta de IRQ. Relatório: `build/a0_task_lifecycle.md`.

## Reprodução local: ambiente preparado e caminho não conclusivo

A ROM fornecida foi instalada localmente como `input/KujakuOu_Japan.sms` e o código-fonte do Dega foi extraído somente para `/home/ubuntu/reference/dega-1.12/`; ambos permanecem fora do Git. Todos os scripts passaram por `python3 -m py_compile tools/*.py`. A captura com semântica de I/O do Dega, agendamento de frame, IRQ por scanline, pulso de controle na janela causal e trace amostrado terminou no PC `0x4070` após 1.100 blocos, sem alcançar `0x4A8D`.

O auditor retornou `status=risk`, com `BREAKPOINT_NOT_REACHED`, entrada variável e loop dominante em `0x04E4`. O analisador A0 encontrou cinco escritas em `DD97` (valores `0` e `4`), mas nenhuma escrita em `DDF7–DE16` nesta configuração; isso não substitui nem contradiz a captura de 3.500 blocos documentada anteriormente, pois os caminhos e a duração não são equivalentes. O relatório completo está em `build/local_reproduction_2026-08-30.md`. A próxima execução deve focalizar a janela que armou A0 e registrar também `DDB7` e o retorno imediatamente anterior a `0x8B81`, sem desbloqueios sintéticos.

## Probe focalizado: armamento A0 seguido de desmontagem

Uma captura focalizada com trace de `DD00–DE37` e execução em `0x83D0–0x8BD0` confirmou novamente o armamento real da tarefa A0. No bloco 265, `0x8540` gravou `DDF7=0xA8` e copiou a estrutura para `DDF7–DE06`; `0x874D` verificou o slot ainda armado. No bloco 267, o caminho em `0x4496` gravou zero em `DDF7`, `DE0F–DE12`, `DDB7` e `DD97`, seguido pela passagem do limpador geral em `0x8B8B–0x8B93`. O resultado terminou em `0x4073` após 300 blocos; o auditor marcou `risk` somente por `BREAKPOINT_NOT_REACHED`, sem saturação do trace.

O analisador A0 foi ampliado para acompanhar `DDB7` junto de `C203`, `DD03`, `DD97` e do grupo `DDF7–DE16`. No trace, `DDB7` e `DD97` tiveram nove escritas cada, com valores `0` e `4`, confirmando que ambos participam do estado auxiliar de armamento. A evidência não identifica ainda a causa do retorno ao limpador; o próximo passo é reconstruir o chamador de `0x4496`, os valores de retorno na pilha e a condição que leva à desmontagem, sem forçar os flags ou os slots. Relatório: `build/a0_dispatch_probe_2026-08-30.md`.

## Reprodução: contexto de retorno A0

Foi adicionada `tools/extract_a0_return_context.py`, ferramenta observacional que extrai dos traces os contextos de `0x4496`, `0x8B81`, `0x8B8B` e `0x8B93`, incluindo SP, bytes no topo da pilha, bancos ativos, registradores e eventos de memória. Ela não altera RAM, não libera esperas e não interpreta a ausência do breakpoint como sucesso.

A reprodução em 1.100 blocos, com semântica de I/O do Dega, agendamento de frame, IRQ por scanline, janela `0xFF` até o bloco 260 e pulso `0x10` por 30 blocos, terminou em `0x4070` sem alcançar `0x4A8D`. O auditor retornou `risk` por `BREAKPOINT_NOT_REACHED` e entrada variável. O trace confirmou `0x4496` no bloco 267 com SP `0xDFEE`, topo `0xEB/0x00` e escritas de limpeza em campos DDxx; também confirmou acessos posteriores ao limpador `0x8B81/0x8B8B`. O relatório detalhado está em `build/a0_resume_probe_2026-08-30.md`.

Essa reprodução não é snapshot válido de `C280` e não identifica sozinha a causa da desmontagem. O próximo experimento deve separar os chamadores conhecidos de `0x8B62` (`0x0533` e `0x4569`) com faixa de execução estreita e correlação de `DDB7`, `DD97`, `DDF7–DE12`, `DD03`, retorno na pilha e bancos ativos, sem desbloqueios sintéticos.

## Probe: duas janelas de chamada A0

Foram executadas duas capturas independentes com a mesma entrada e temporização, uma observando `0x0500–0x0540` e outra `0x4540–0x4580`, para tentar separar os contextos associados aos chamadores `0x0533` e `0x4569`. Ambas terminaram em `0x4073` após 300 blocos, com `FFFE=0x95`, `FFFF=0x0C`, sem alcançar `0x4A8D`, e foram classificadas como `risk` pelo auditor.

As duas capturas registraram o mesmo caminho de interesse: `0x4496` no bloco 267 com `SP=0xDFEE` e topo `0xEB/0x00`, seguido de limpeza em `DD03`, `DD97`, `DDB7`, `DDF7` e `DE0F–DE12`; o limpador `0x8B8B/0x8B93` foi observado com `SP=0xDFD4` e topo `0x00/0x00`. A restrição da faixa de PCs observados não separa os chamadores, pois não altera a execução e ambas as capturas convergem para o mesmo estado.

O relatório está em `build/a0_two_callers_probe_2026-08-30.md`. O próximo passo deve registrar explicitamente o endereço de retorno na entrada de `0x8B62`, usando um marcador de execução ou instrumentação específica das instruções `CALL` em `0x0533` e `0x4569`; não devem ser feitas novas inferências a partir de faixas de trace isoladas nem alterações na ROM.

## Instrumentação concluída: retornos reais de 0x8B62

O capturador recebeu `--trace-call-targets`, que registra a entrada em PCs de chamada selecionados e reconstrói o endereço de retorno diretamente dos dois bytes no topo da pilha. A captura focalizada em `0x8B60–0x8B90` observou dez entradas em `0x8B62` e separou os dois contextos em runtime: retorno `0x0536`, correspondente ao `CALL 0x8B62` em `0x0533`, nos blocos 41, 46, 265 e 278; e retorno `0x456C`, correspondente ao `CALL 0x8B62` em `0x4569`, no bloco 277. O banco `FFFF` era `0x82`; `FFFE` foi `0x01` ou `0x95` conforme o contexto.

A entrada em `0x8B81` também foi registrada, mas com topo de pilha `0x00/0x00`, confirmando que o ponto pertence ao fluxo interno de `0x8B62` e não deve ser usado para reconstruir o retorno. O relatório está em `build/a0_call_target_probe_2026-08-30.md`. A execução terminou em `0x4073` sem alcançar `0x4A8D`, portanto continua sendo evidência diagnóstica e não snapshot válido de `C280`.

A ambiguidade entre o chamador fixo e o paginado foi eliminada. O próximo probe deve comparar o estado `DD03`, `DD97`, `DDB7`, `DDF7–DE12`, `C203` e os bancos imediatamente antes das entradas com retorno `0x0536` e `0x456C`, priorizando a reentrada paginada do bloco 277.

## Comparação de estado na entrada de 0x8B62

Foi adicionado um snapshot atômico aos eventos `call_target`. Nos blocos 41, 46, 267 e 278, com retorno `0x0536` pelo caminho fixo, e no bloco 277, com retorno `0x456C` pelo caminho paginado, os campos monitorados `C203`, `DD03`, `DD57`, `DD64`, `DD66`, `DD97`, `DDB7`, `DDF7` e `DE0F–DE12` estavam todos em `0x00` na entrada de `0x8B62`. `FFFF` era `0x82` em todos os casos; `FFFE` era `0x01`, exceto no retorno fixo do bloco 278, quando já estava em `0x95`.

A diferença entre os caminhos, portanto, não aparece como valor residual nesses campos no instante da entrada. Isso não prova que eles sejam irrelevantes: podem ter sido consumidos e zerados antes da chamada. A próxima captura deve observar o intervalo imediatamente anterior aos `CALL`s em `0x0533` e `0x4569`, incluindo registradores, flags, leituras/escritas, HL/DE e endereços fora de DDxx. O relatório está em `build/a0_state_compare_probe_2026-08-30.md`.

## Janela causal anterior aos CALLs A0

Foi criada `tools/compare_a0_call_windows.py` para comparar traces estreitos e foram adicionados `F`, `IX` e `IY` aos registros do capturador. A comparação encontrou a primeira diferença concreta imediatamente antes dos dois CALLs.

O caminho fixo (`0x0533 → 0x0536`) chega à entrada com `A=0x82`, `F=0x80`, `DE=0x8900`, `HL=0xC73F` e `SP=0xDFEC` antes do empilhamento. O caminho paginado (`0x4569 → 0x456C`) chega com `A=0x82`, `F=0x10`, `DE=0x0003`, `HL=0x4547` e o mesmo SP. O caminho fixo passa por `0x0526–0x0534`, lê `C73E`, escreve `C73F` e atualiza `DE`; o caminho paginado passa por `0x4564–0x456A` e é precedido por escritas repetidas de `0x03` em `C008` no loop `0x04E4`.

A diferença não está nos campos DDxx/C203 na entrada de `0x8B62`, que permanecem zerados, mas nos parâmetros e flags entregues à rotina. O próximo probe deve acompanhar como `0x8B62` consome `HL=0x4547`, `DE=0x0003`, `F=0x10` e `C008=0x03`, comparando com `HL=0xC73F`, `DE=0x8900`, `F=0x80` do caminho fixo. O relatório está em `build/a0_causal_window_probe_2026-08-30.md`.

## Dependências internas de 0x8B62

Foi criada `tools/analyze_a0_routine_dependencies.py` e foram executadas capturas cobrindo `0x8B60–0x8BD0`. Os caminhos fixo (`0x0536`) e paginado (`0x456C`) percorrem o mesmo conjunto de PCs, de `0x8B62` a `0x8B98`, e realizam o mesmo conjunto de leituras `DD03–DD0C` e escritas nos campos DDxx monitorados. A diferença permanece na entrada: o caminho fixo chega com `F=0x80`, `DE=0x8900`, `HL=0xC73F`; o paginado chega com `F=0x10`, `DE=0x0003`, `HL=0x4547`.

A rotina não mostrou, nesta janela, um ramo interno diferente selecionado pelos campos DDxx. A hipótese prioritária agora é que a condição relevante esteja antes do CALL ou nos dados apontados por DE/HL. O próximo probe deve comparar os bytes lidos a partir de `HL=0xC73F` versus `HL=0x4547` e `DE=0x8900` versus `DE=0x0003`, registrando também flags depois de cada leitura. O relatório está em `build/a0_routine_dependency_probe_2026-08-30.md`.

## Dependência de operandos dentro de 0x8B62

Foi adicionada a opção `--trace-memory-pcs`, que força o registro de toda leitura/escrita enquanto o PC está em uma faixa escolhida, e o wrapper temporizado passou a encaminhá-la corretamente. O probe em `0x8B62–0x8BD0` registrou cinco entradas, quatro pelo retorno `0x0536` e uma pelo retorno `0x456C`.

Dentro da rotina, os dois contextos apresentam o mesmo conjunto de fetches de opcode `0x8B62–0x8B98`, leituras `DD03–DD0C` e escritas DDxx, sem leituras de dados nos endereços apontados pelos valores de HL ou DE (`C73F/4547` e `8900/0003`). A hipótese de dereferência direta de HL/DE não é sustentada. Esses registradores parecem ser valores de estado/parâmetros, enquanto DDxx é a estrutura de destino.

O próximo passo deve ser a desmontagem semântica de `0x8B62–0x8B98`, correlacionando opcodes, efeitos nas flags e instruções que escrevem DDxx. Não é necessário criar outra ferramenta de captura neste ciclo. O relatório está em `build/a0_operand_dependency_probe_2026-08-30.md`.

## Desmontagem semântica de A0

A rotina `0x8B62` foi desmontada no banco efetivo 2. Ela salva HL/DE/BC, zera/copía campos fixos de DDxx com `LDI`, executa um laço incondicional que zera dez grupos de cinco bytes e grava `0xE4` em `DD08`, restaurando os registradores ao final. Logo, não dereferencia os valores recebidos em HL/DE e não possui ramo interno que diferencie os chamadores.

O chamador fixo `0x0533` executa `CALL 0x8B62`, depois `EI`, chama `0x04E1` e retorna a `0x0201`. O chamador paginado `0x4569` executa o mesmo `CALL` e, no retorno em `0x456C`, lê `C119`, compara com `4` e, se diferente, atualiza `C119`, `C0A0`, `C11D` e copia 32 bytes de `0x46C0` para `C0E0`. O novo relatório está em `build/a0_semantic_disassembly_2026-08-30.md`.

A investigação deve agora concentrar-se no valor de `C119` antes de `0x4569` e no efeito do teste em `0x456C–0x4571`, pois esse é o primeiro ponto condicional real após a limpeza comum.

## Branch C119 após a limpeza A0

No bloco 277, o caminho paginado chega a `0x4569` com `C119=0x01`, instalado explicitamente por `0x4530`. Após o retorno de `0x8B62` em `0x456C`, o código lê `C119=1`, compara com `4` e não toma o salto condicional. Em seguida instala `C119=5`, `C0A0=5`, `C11D=1` e copia 32 bytes de `0x46C0` para `C0E0`.

A condição contra `4` não bloqueia o caminho nesta reprodução; ela seleciona a transição para o estado `5`. O próximo gargalo está depois de `0x4589`, em quem consome `C0E0` e os estados `C0A0/C11D`, ou na condição especial que produziria `C119=4`. O relatório está em `build/a0_c119_branch_probe_2026-08-30.md`.

## Consumidor de C0E0 e transição para C0A0=4

A desmontagem pós-`0x4589` localizou a rotina `0x078A–0x07CD`: ela copia 32 bytes a partir de `C0E0`, restaura DE, define `C0A0=4` e transforma os bytes de `C0E0` com `RLD/RRD`, máscaras e subtrações dependentes de D. Portanto, o bloco instalado pelo caminho `0x4569` é uma estrutura intermediária codificada, não texto direto.

O trace também mostrou escritas em `C0E0/C0E1/C0FF` por `0x0718`, `0x071F`, `0x0721`, `0x0743`, `0x0792` e `0x07A4`, além da mudança de `C0A0` para `4`. O próximo probe deve capturar `0x078A–0x07D0`, o valor de D usado nas subtrações e o destino após o laço, seguindo a cadeia até o renderizador.

## Gate VDP e ordenação temporal da máquina A0

O trace de 1.100 passos confirmou que a máquina `0x078A–0x07F2` completa cinco ciclos e então zera `C0A0`, `C0A2` e `C113`, marcando `C0A4=1`. Depois, o scheduler `0x06CE` é executado após `C080=0`, mas lê `C0A0=0` e retorna; o caminho `0x06D8–0x06E4`, que transferiria `C0E0` para `C000` via `RST 30h`, não é tomado.

Isso aponta para uma condição de ordenação temporal entre a conclusão da máquina, o IRQ/VDP e o scheduler. A próxima investigação deve comparar a ordem de `0x07E5–0x07F2`, `0x180E` e `0x06CE`, verificando se a cadência de IRQ do emulador está atrasando a avaliação de `C0A0`. Não deve haver desbloqueio artificial de `C0A0`. O relatório está em `build/a0_vdp_gate_probe_2026-08-30.md`.

### Correção do handler IRQ/VDP

A desmontagem de `0x1809–0x185F` corrigiu a interpretação temporal anterior: `0x1809–0x180C` limpa `C080`; `0x180E` lê `C112`; se `C112=2` e os contadores `C081/C082` mudaram, `0x181C–0x181F` reativa `C080=1`. O scheduler `0x06CE` continua retornando porque encontra `C0A0=0` após a conclusão da máquina, e não porque `0x180E` escreva `C080`.

A próxima captura deve correlacionar quando `0x06CE` é chamado em relação aos quatro ciclos intermediários e ao handler `0x1809–0x181F`, sem liberar artificialmente `C0A0`.

## Xrefs do scheduler e do handler VDP

A nova ferramenta `tools/find_z80_call_xrefs.py` localizou o xref fixo `0x0DA6`, que chama `0x06CE` somente quando `C080=0` (`0x0D9C–0x0DA0`). O handler em `0x0179` chama separadamente `0x1809`; esse handler limpa `C080` e pode reativá-lo conforme `C112` e `C081/C082`.

A cadeia correta é, portanto, `0x0179 → 0x1809` para o estado VDP, seguida de `0x0D9C → 0x0DA6 → 0x06CE` quando o gate `C080` está livre. O scheduler ainda possui sua própria guarda: retorna se `C0A0=0` e só então transfere `C0E0` para `C000`. A hipótese de simples atraso de IRQ foi refinada para uma interação entre as guardas explícitas `C080` e `C0A0`. O relatório está em `build/a0_scheduler_xref_probe_2026-08-30.md`.

## Comparação com a ROM americana SpellCaster

Foi recebida localmente a ROM `SpellCaster(USA,Europe).sms`, com 524288 bytes e 32 bancos de 16 KiB. Ela permanece em `input/`, fora do Git. A análise estrutural encontrou 5179 regiões candidatas a tabelas de ponteiros e 454 regiões candidatas a tiles, portanto a organização geral é comparável à ROM japonesa.

A versão americana contém texto inglês verificável em ASCII, incluindo `NEW GAME`, `PASSWORD!`, `PUSH START BUTTON` e a mensagem final `THE EVIL LORD AND HIS ARMIES HAVE BEEN DEFEATED...`. Isso a torna uma ROM-oráculo muito valiosa para associar códigos internos, mensagens, fluxo de menus e significado de tabelas. Porém, ela não é um substituto direto da japonesa: as tabelas foram deslocadas e alguns endereços diferem. Na região equivalente de banco 21, a cadeia japonesa usa referências como `AB89`, `ABA2`, `ABBB`, `ABC5`, enquanto a americana usa regiões deslocadas como `AAFB`, `AB14`, `AB2D`, `AB37`; a rotina equivalente de leitura de máscaras aparece em `0x4BCB`/`0x4D0B` em vez de `0x4BBD`/`0x4CFD`. O padrão de lógica, contudo, é reconhecível: limpeza de `C280`, chamadas de resolução de máscaras e posterior construção de estado.

Conclusão: a ROM americana torna a engenharia reversa significativamente mais fácil para identificar textos, formato de mensagens, fonte e semântica de menus, mas o trabalho de mapeamento paginado e validação dinâmica continua necessário para a versão japonesa. A prioridade passa a ser alinhar regiões equivalentes entre as duas ROMs e usar a americana para construir um mapa código→glifo, sem copiar offsets cegamente.

## Ferramenta de alinhamento entre versões

Foi criada `tools/align_rom_versions.py` para comparar a ROM americana de referência com a japonesa sem assumir offsets idênticos. A ferramenta procura assinaturas binárias locais por banco de 16 KiB e, se necessário, globalmente; informa hits, delta de offsets, banco físico, janela de CPU e unicidade. Também lista sequências ASCII da ROM de referência para transformar mensagens inglesas em âncoras de alinhamento.

A ferramenta foi validada com a ROM americana contra si mesma usando assinaturas em `0x46500` e `0x4A81`; os matches foram únicos e os deltas foram zero. Quando a ROM japonesa for fornecida novamente, os próximos testes devem usar assinaturas de rotinas estáveis e tabelas, não apenas texto, pois traduções e reorganizações podem alterar as sequências ASCII.

## Resultado quantitativo: ROM japonesa versus americana

A ROM japonesa recém-recebida foi comparada byte a byte com `SpellCaster(USA,Europe)`. Ambas têm 524288 bytes e 32 bancos. O resultado é favorável: os bancos 6–11, 13, 15–16, 22, 25–27 e 29 são 100% idênticos; o banco 23 é 99,7% idêntico e o banco 5 é 96,6% idêntico. Isso fornece uma base direta para validar código comum, mapper, VDP e rotinas compartilhadas.

As diferenças estão concentradas nos bancos regionais/localizados. O banco 21 tem somente 16,1% de igualdade byte a byte, explicando por que assinaturas literais de 32 bytes não alinharam as tabelas de diálogo. Ainda assim, as rotinas homólogas foram identificadas: a leitura americana equivalente a `04BBD` está em `0x4BCB` e a equivalente a `04CFD` em `0x4D0B`, contra `0x4BBD` e `0x4CFD` na japonesa. O relatório detalhado está em `build/usa_japan_comparison.md`.

Conclusão operacional: a ROM americana é uma referência muito valiosa e torna o projeto mais fácil, mas o alinhamento do banco 21 deve usar assinaturas de opcode/controle de fluxo com operandos mascarados, não comparação literal. Nenhuma ROM foi modificada.

## Alinhamento estrutural Z80 entre versões

Foi criada `tools/align_z80_signatures.py`, que decodifica rotinas Z80 e compara fingerprints formados por primeiro opcode e tamanho da instrução, ignorando operandos regionais como endereços, imediatos e deslocamentos. A ferramenta é apropriada para localizar código homólogo quando a comparação literal de bytes falha; seus resultados continuam sendo candidatos e precisam de revisão.

Aplicação no banco 21: a rotina americana em `0x4BCB–0x4C00` foi comparada com a japonesa em `0x4BBD–0x4BF5`, usando janelas de 10 instruções. Foram decodificadas 41 instruções americanas e 42 japonesas; 32 janelas tiveram correspondência única. O relatório está em `build/z80_b21_alignment_usa_japan.json`. Isso confirma automaticamente o deslocamento estrutural da rotina equivalente a `04BBD` e valida a estratégia de ignorar operandos variáveis.

O próximo passo é aplicar a ferramenta a blocos maiores do banco 21, incluindo a rotina equivalente a `04CFD`, os chamadores de `C022/C205/C215/C251` e as regiões de mensagens. As correspondências únicas devem ser usadas para mapear funções e tabelas; não devem ainda ser usadas para gerar patch sem confirmação dinâmica.

## Alinhamento estrutural ampliado: 04CFD e C280

A ferramenta `align_z80_signatures.py` foi aplicada à rotina americana equivalente a `04CFD` (`0x4D0B–0x4D70`) contra a japonesa (`0x4CFD–0x4D62`). Em janelas de 10 instruções, foram encontradas 82 correspondências, sendo 74 únicas, entre 91 instruções de cada lado. Isso confirma que a semântica de `04CFD` é compartilhada apesar do deslocamento de 14 bytes.

O bloco de limpeza/construção de `C280` também alinhou: o início americano em `0x4A81` corresponde ao japonês em `0x4A73`, com 7 janelas únicas de 8 instruções. A busca literal localiza o ponto japonês `0x4A8D` em torno de `0x4A9B` na americana, indicando que o breakpoint equivalente americano é `0x4A9B`, não `0x4A8D`.

Os relatórios estão em `build/z80_04cfd_alignment_usa_japan.json` e `build/z80_c280_alignment_usa_japan.json`. A versão americana agora pode ser usada para estudar o fluxo homólogo no breakpoint `0x4A9B` e identificar quais valores de estado precedem a resolução de C280, sem confundir offsets entre versões.

## Teste do breakpoint homólogo na ROM americana

O capturador foi executado contra `SpellCaster(USA,Europe).sms` usando o breakpoint regionalmente correto `0x4A9B` e a janela temporizada de entrada documentada. A execução não alcançou o alvo e terminou em `0x051F`, com `FFFF=0x8C`/`0x84` dependendo da configuração e campos `C022/C025–C028/C205/C215/C251/C280/C281` zerados. Isso não é um snapshot válido.

A causa operacional é que `tools/run_sms_capture.py` ainda contém pontos de espera e fluxo específicos derivados da ROM japonesa; ele não pode ser usado diretamente na americana apenas trocando o endereço do breakpoint. O valor da ROM americana nesta etapa é estrutural: os alinhamentos Z80 confirmam que `0x4A9B` corresponde ao `0x4A8D` japonês e que `04CFD`/`04BBD` são homólogos. O próximo passo deve separar a configuração regional do capturador ou executar um harness com pontos de espera descobertos na versão americana, sem transportar os offsets japoneses.

## Trace focalizado: ordenação C080/C0A0

Foi executado um trace focalizado da região `0x06C0–0x07F5`, com acessos a `C080–C11F`, alvos de chamada `0x06CE` e `0x1809`, sem desbloqueios sintéticos. A captura japonesa com agendamento de frame/IRQ do Dega e entrada variável terminou em `0x4070` após 1200 blocos, com `FFFE=0x95` e `FFFF=0x82`, sem alcançar `0x4A8D`.

O resultado confirma que a instrumentação atual é suficiente para acompanhar o scheduler, mas não resolve a transição: a execução continua no caminho A0/C203 antes de chegar à construção de `C280`. O wrapper `run_timed_capture.py` não aceita os parâmetros modernos de frame/IRQ; para novos probes, usar diretamente `run_sms_capture.py` ou atualizar o wrapper antes de reutilizá-lo. Nenhum desbloqueio ou valor sintético foi aplicado nesta etapa e nenhum snapshot foi aceito.

## Entrega final obrigatória

Além do patch PT-BR distribuível, o objetivo inclui gerar uma cópia privada da ROM fornecida pelo usuário com a tradução aplicada, para uso pessoal do próprio usuário. A cópia modificada completa e a ROM original nunca devem ser adicionadas ao GitHub, aos commits ou aos relatórios versionados; devem permanecer em diretório local ignorado e ser entregues separadamente apenas ao usuário quando a tradução estiver validada. O patch deve continuar sendo o artefato reproduzível principal, aplicado sobre a ROM original correspondente.

A cópia traduzida só deve ser gerada depois de validar fontes, ponteiros, limites de mensagens, comandos especiais, bancos e checksum da ROM. Não considerar uma ROM com textos parcialmente substituídos ou com snapshot dinâmico não validado como entrega final.

## Primeiro inventário comparativo de streams de texto

O extrator `tools/extract_direct_text_sources.py` foi corrigido para reconhecer o formato atual do disassembler (`0xc223`/`0xc238`) além do formato legado. Executado nas duas ROMs, ele encontrou seis candidatos diretos em cada banco 21. Os seis streams são byte a byte idênticos entre as versões, com deslocamentos Japão–EUA de `+0x0A` no primeiro e `+0x2B` nos demais: `0x542A→0x5434`, `0x5A2D→0x5A58`, `0x5F1A→0x5F45`, `0x61E8→0x6213`, `0x61F7→0x6222` e `0x62DF→0x630A`.

Isso valida o extrator e fornece âncoras precisas para o alinhamento. Esses seis candidatos ainda não são o diálogo principal; os streams narrativos são carregados por handlers paginados e devem ser resolvidos acompanhando `05C16`, `C206`, `C223` e `C238` em runtime. O relatório está em `build/usa_japan_direct_text_comparison.md`, com os dumps em `build/usa_direct_text_sources.md` e `build/japan_direct_text_sources.md`.

## Mapa inicial dos resolvedores narrativos

A ferramenta `tools/extract_handler_windows.py` foi criada para extrair janelas do disassembly atual ao redor das chamadas que resolvem ponteiros de diálogo. A primeira execução revelou uma diferença importante: a ROM japonesa chama o resolvedor em `0x5C16`, enquanto a americana usa o resolvedor homólogo em `0x5BEB`. O extrator foi ajustado para reconhecer ambos.

Foram encontrados 15 candidatos japoneses e 15 candidatos americanos no banco 21. Isso confirma que o conjunto de handlers narrativos é estruturalmente paralelo, mas não é seguro procurar somente pelo endereço japonês. Os relatórios estão em `build/japan_handler_windows.md` e `build/usa_handler_windows.md`.

Os candidatos americanos incluem chamadas que gravam `C223/C238` e chamam `0x5BEB`, enquanto os japoneses fazem o equivalente com `0x5C16`. O próximo passo é alinhar esses 15 candidatos por fingerprints Z80 e extrair os ponteiros de origem (`DE/HL`) de cada handler, começando pelos pares `0x5C4F↔0x5C24` e `0x5D22↔0x5C4D`.

## Mapa automático dos handlers de diálogo

Foi criada `tools/map_dialog_handlers.py` para parear chamadas aos resolvedores regionais e extrair os valores imediatos de `HL/DE` próximos a cada chamada. Aplicada ao banco 21, a ferramenta encontrou 15 chamadas americanas ao resolvedor `0x5BEB` e 15 chamadas japonesas ao resolvedor `0x5C16`; todas as 15 possuem pelo menos um match estrutural, e 7 foram matches únicos com janela de 12 instruções.

Entre os matches únicos, foram confirmados os pares `0x5C4D→0x5C78`, `0x5CA2→0x5CCD`, `0x5CF7→0x5D22`, `0x5D21→0x5D4C`, `0x5EA4→0x5ECF`, `0x6323→0x634E` e `0x6371→0x639C`. Os quatro primeiros preservam ponteiros de origem idênticos (`B124`, `B228`, `B9EA`, `BAB5`), enquanto os três últimos mostram deslocamentos consistentes de `+0x2B` (`6A30→6A5B`, `6603→662E`, `6463→648E`). Isso separa dados compartilhados de regiões deslocadas e é a primeira base automatizada para construir o mapa código→stream.

O relatório completo está em `build/dialog_handler_map_usa_japan.json`; as janelas de contexto estão em `build/usa_handler_windows.md` e `build/japan_handler_windows.md`. O próximo passo é extrair os streams apontados por esses pares, classificar terminadores/comandos e localizar quais são narrativos antes de editar qualquer byte.

## Extração de streams: separação entre bytecode e texto

Foi criada `tools/extract_dialog_streams.py` para resolver entradas das tabelas `B124`, `B228`, `B9EA` e `BAB5` no banco 22, seguir cada ponteiro até `FF`/limite e classificar o resultado. Em cada ROM foram examinadas 260 entradas: 195 foram classificadas como `bytecode_or_structure`, 63 como `mixed_or_unknown` e apenas 2 como `text_or_glyph_stream`. Os dois streams curtos (`00 1C 33 1D FF` e `00 37 00 38 FF`) são idênticos e não têm características de diálogo narrativo.

A conclusão importante é que os ponteiros dos handlers levam principalmente a registros/bytecode. Os blocos narrativos candidatos continuam sendo `5F7E`, `6046`, `61FB` e as tabelas deslocadas em torno de `6603/662E` e `6463/648E`, mas o texto só se materializa depois da resolução dinâmica para `C223/C238`. Não foi classificado nenhum bloco como diálogo narrativo plano com segurança; isso evita corromper bytecode no primeiro patch. O relatório está em `build/dialog_stream_classification.md`, com os dumps completos em `build/usa_dialog_streams.json` e `build/japan_dialog_streams.json`.

## Probe dinâmico dos ponteiros finais de diálogo

Foi executado trace forçado de `C206`, `C223` e `C238` durante 3500 blocos da ROM japonesa, com IRQ por scanline, frame do Dega e semântica de I/O ativa-baixa. A execução terminou em `0x406C`, com `FFFE=0x95` e `FFFF=0x82`, sem alcançar `0x4A8D` ou os handlers narrativos. Os únicos eventos nesses campos foram inicializações/limpezas em `0x00AD`, `0x4939` e `0x4496`, todos com valor zero; nenhum ponteiro não nulo foi observado.

O resultado é inconclusivo para texto, mas útil como controle negativo: não é válido interpretar zeros como streams nem gerar patch. O relatório está em `build/dialogue_runtime_pointer_probe.md`. A próxima execução precisa reproduzir a janela que alcança o armamento A0 e depois o scheduler, ou corrigir o modelo dessa tarefa antes de tentar capturar novamente `C223/C238`.

## Auditoria do pacote ROMPROJECT do Zed

Foi recebido o pacote `ROMPROJECT.tar.gz` e inspecionado somente quanto às ferramentas Python, ignorando ROMs, emuladores e objetos compilados. O pacote contém extratores baseados em Shift-JIS/ASCII, scripts de templates e injetores preliminares.

A ideia de agrupamento de ponteiros de `extrair_textos_ponteiros.py` é útil, mas já foi substituída no projeto por `extract_dialog_streams.py`, que respeita bancos SMS, terminadores `FF` e classificação de bytecode. `extract_japanese_text.py` pode servir como triagem, mas não como decodificador: os resultados corrompidos confirmam que o jogo usa um código de glifo próprio ou uma camada de transformação. `injetar_traducao_v2.py` tem uma rotina de checksum potencialmente reaproveitável, porém seu injetor é inseguro porque assume Shift-JIS, procura ponteiros em faixas amplas e não conhece os handlers paginados.

Os templates do pacote incluem tentativas preliminares como `004739: INICIAR`, mas não foram tratados como mapa validado. Nenhuma ferramenta de injeção, ROM, emulador ou objeto compilado foi incorporado. O relatório está em `build/zed_tools_audit.md`. O próximo passo permanece o mapeamento do código de glifos e dos streams finais `C223/C238`; só depois deve ser implementado o injetor seguro e a cópia privada traduzida.

## Confirmação da fonte compartilhada após 05B3E

Foi executada `tools/transform_lad0c_05b3e.py` nas ROMs japonesa e americana, com banco físico 13, origem `AD0C`, stride `0x10` e 64 glifos. Cada saída tem 8192 bytes e ambas possuem o mesmo SHA-256: `ee4b13597f6f23eb3dfd3bb462c95d5ef1c79c170cbd55b2b3a564351b9a872a`. A fonte/grupo de glifos dessa etapa é, portanto, idêntico nas duas versões; a tradução deve alterar códigos/streams, não essa fonte.

Foram gerados `build/japan_glyph_map_05b3e.png` e `build/usa_glyph_map_05b3e.png`, mapas visuais 8x16 de 64 glifos. O relatório está em `build/glyph_map_05b3e_report.md`. A próxima tarefa é transformar os valores não nulos de `C280` em uma tabela código→índice de glifo e cruzá-la com os streams finais.

## Mapa runtime de C280 e cruzamento com streams

A ROM japonesa fornecida localmente foi colocada em `input/kujaku_ou_jp_original.sms`, diretório ignorado pelo Git. O código-fonte do Dega 1.12 foi extraído apenas como referência em `/home/ubuntu/reference/dega-1.12`; nenhum binário ou ROM foi incorporado ao repositório.

O capturador `tools/run_sms_capture.py` passou a registrar a região completa `C280–C37F` (256 bytes), além da lista de códigos não nulos. A execução com `--scanline-irq --dega-frame-schedule --dega-io-semantics`, por 3500 blocos, terminou em `PC=0x406F` com `FFFE=0x95`, `FFFF=0x82` e `result=step_limit`, sem alcançar o breakpoint `0x4A8D`. Ainda assim, a captura produziu 20 entradas não nulas de C280: `40–4F`, `89`, `A9`, `C9` e `E9`, todas com valor `0x01`.

Foi criada `tools/build_runtime_glyph_map.py`, que converte a captura em um mapa auditável código→glifo e cruza os códigos aceitos com os 260 streams do relatório `build/japan_dialog_streams.json`. O resultado está em `build/runtime_c280_glyph_map.md`: os códigos são usados como o próprio índice de glifo pelo loop de texto, com offsets `code*0x10` na origem `AD0C` do banco 13 e `code*0x80` após a transformação modelada de `05B3E`. O cruzamento encontrou 2189 ocorrências de códigos aceitos.

Este resultado é uma fotografia do caminho de execução atual, não o mapa final do jogo. A execução ainda não entrou no fluxo narrativo nem alcançou `0x4A8D`; portanto, os streams continuam sendo referências estruturais e as contagens não comprovam texto narrativo. O próximo passo seguro é obter uma captura que arme a transição de cena/dialogue, ou integrar um snapshot/trace real nesse ponto, antes de preparar qualquer patch.

## Rastreamento dedicado de ponteiros de cena

A instrumentação do capturador foi ampliada em `tools/run_sms_capture.py` com uma lista dedicada de escritas em `C205–C208`, `C223–C224` e `C238–C239`, independente do limite geral do trace. O snapshot final também passou a incluir os bytes baixos e altos de `C206`, `C223` e `C238`.

Na execução com sequência de entrada `FF,FE,FD,FB,F7,EF,DF,BF,7F`, cadência de scanline do Dega e semântica de I/O ativa-baixa, foram registradas 26 escritas nesses campos. As inicializações em `0x00AD`, `0x4939` e `0x4496` escreveram apenas zeros. O primeiro valor não nulo apareceu em `PC=0x4146`: `C206=C207=0x80`, com `FFFE=0x95` e `FFFF=0x16`. `C223/C238` permaneceram nulos, e a execução terminou em `0x4073` por limite de blocos.

A conclusão é que não é necessária uma nova ferramenta pós-processadora neste momento. O problema era a ausência de um monitor dedicado no capturador; a alteração atual já identifica o primeiro estado não nulo e o banco ativo. O próximo ajuste deve seguir a cadeia a partir de `0x4146`, reproduzir a transição que transforma `C206` em ponteiro de objeto e determinar qual evento de cena habilita as escritas posteriores em `C223/C238`.

## Trace dedicado após C206=0x8080

O capturador recebeu um segundo canal de trace, `--trace-exec-limit`, que preserva buscas de opcode no intervalo solicitado independentemente do limite geral de eventos de memória. Isso foi necessário porque o trace anterior era saturado por acessos de hardware antes de registrar a região de interesse.

Com o intervalo `0x4000–0x4A90`, a execução confirmou que a passagem por `0x4146` ocorre nos primeiros runs e grava `C206=C207=0x80` enquanto `FFFE=0x95` e `FFFF=0x16`. Depois da transição, o executor alcança repetidamente `0x4937/0x4938` no banco paginado do slot `FFFE`; os bytes físicos correspondentes começam por `14 02 CD 26 02 AF 32 6C C2...`. Esse caminho retorna ao scheduler sem produzir escritas não nulas em `C223/C238`, e a captura termina em `0x4073` por limite de blocos.

A instrumentação atual é suficiente para continuar; não foi criada uma ferramenta independente. O próximo passo é modelar ou verificar o estado consumido pelo scheduler em `0x4937`, especialmente a chamada `0x0226`, a escrita de `C26C` e as condições de entrada que levam de `C206` ao dispatcher de cena. Não se deve liberar esse laço genericamente, pois isso poderia fabricar um estado de diálogo inexistente.

## Comparação causal do scheduler A0

O resolvedor existente `tools/find_z80_call_xrefs.py` confirmou quatro referências a `0x06CE` no banco fixo/paginado, mas somente o xref fixo em `0x0DA6` é o chamador direto do scheduler no fluxo principal. A cadeia é `0x0D9C → 0x0DA6 → 0x06CE`, condicionada por `C080=0`; o probe direto do scheduler não encontrou `0x06CE` na execução atual porque o caminho permanece no ciclo paginado de `0x4937`.

Foi executada a ferramenta já existente `tools/compare_a0_call_windows.py` com traces separados. O caminho fixo encontrou duas entradas em `0x8B62` com retorno `0x0536`, precedidas por `0x0533` escrevendo `0x82` em `FFFF`. O caminho paginado encontrou uma entrada em `0x8B62` com retorno `0x456C`, precedida por `0x4569` escrevendo `0x82` em `FFFF` após repetidas escritas de `0x03` em `C008` pelo loop `0x04E4`.

O relatório atual está em `build/a0_call_windows_current.md`. A diferença confirma que os dois caminhos chegam ao mesmo dispatcher com contextos de CPU e pilha distintos; ela não justifica liberar `C0A0`, `C080` ou qualquer espera artificialmente. Não foi necessária uma nova ferramenta: o conjunto de xrefs, o trace dedicado e o comparador existente já isolam o próximo ponto de investigação, que é reproduzir a transição do caminho paginado `0x4569 → 0x8B62` até o chamador fixo `0x0DA6`, acompanhando `C080`, `C0A0`, `C112` e `C113`.

## Inventário do pacote de referência e âncoras ASCII

O pacote `ROMSEEMULADOR.tar.gz` fornecido pelo usuário foi preservado em `input/reference-ROMSEEMULADOR/`, fora do Git. Ele contém `Kujaku Ou (Japan).sms`, `SpellCaster (USA, Europe).sms` e `Dega-1.12.tar.gz`. A ROM japonesa do pacote tem SHA-256 `bfc5514e173113508d05721b3b45a70bb7a11d42d4e1ff0ff410460f1caa0a51`, idêntico à ROM já usada no projeto. A ROM americana tem 524288 bytes e é uma referência regional adicional; nenhuma ROM original foi modificada.

Foi adicionada `tools/list_ascii_runs.py` para listar sequências ASCII com offsets físicos, banco e janela de CPU. A comparação confirmou as âncoras de menu `NEW GAME`, `PASSWORD!` e `PUSH START BUTTON` nas duas versões, com deslocamento regional (`0x45FB/0x4654` na americana e `0x4670/0x46EF` na japonesa). Essas sequências são úteis para alinhamento, mas não devem ser tratadas como prova de que os streams narrativos foram localizados: os diálogos principais continuam dependentes da resolução paginada e da tabela de glyphs.

O alinhamento estrutural Z80 da rotina equivalente em `0x4BCB`/`0x4BBD` produziu 53 janelas, 49 únicas, confirmando a correspondência de código sem assumir offsets idênticos. A busca literal de 32 bytes não encontrou correspondência, portanto a estratégia correta permanece fingerprint de opcode/tamanho e validação dinâmica.

## Probe do gate `0x48D5–0x4970`

Foi criado `tools/analyze_dialog_state_gate.py` para resumir os PCs do gate de cena, estados C004/C005/C020/C02B/C26C e o resultado do auditor. A captura japonesa com semântica de I/O do Dega, frame por scanline e entrada na janela causal terminou em `0x406F` após 3500 blocos; o auditor retornou `risk` por `BREAKPOINT_NOT_REACHED`.

O trace preservou 7.871 passagens por `0x4937`, 26 chamadas de `0x4939`, uma passagem por `0x494A`, uma por `0x4970` e uma chamada a `0x4988`. Isso confirma que o caminho alternativo de `0x4970` chega a ser visitado, mas não se torna uma transição estável para `0x4A8D`. As escritas observadas em `C020` ocorreram em `0x4414`, `0x4911` e `0x45E4`; não houve escritas observadas em `C004`, `C005`, `C02B` ou `C26C` nesta janela focalizada. A captura não foi aceita como snapshot e nenhum valor foi forçado.

A desassemblagem mostra que `0x4937` carrega dados para VRAM por `0x0226`, zera `C26C`, aguarda `0x406C` e retorna ao scheduler; o ramo `0x4970` só prossegue para o resolvedor em `0x4B94` quando as guardas de `C005` e `C004` permitem. O próximo probe deve preservar esses estados fora do limite focalizado e correlacionar a entrada em `0x48D5` com as escritas do scheduler/VDP, sem tratar a simples passagem por `0x4970` como diálogo alcançado.

## Correção do monitor do gate de diálogo

A auditoria do trace revelou que C004, C005, C02B e C26C não faziam parte das faixas de memória sempre preservadas pelo capturador; portanto, a ausência anterior desses endereços no relatório não podia ser usada como evidência de que não eram lidos. O capturador foi corrigido para registrar leituras e escritas nesses quatro endereços independentemente da faixa focalizada.

Na reprodução de 1.200 blocos com a ROM japonesa e semântica de I/O do Dega, foram observadas uma passagem por `0x4970` e uma chamada a `0x4B94`, mas o fluxo terminou em `0x4073` sem alcançar `0x4A8D`. O novo monitor registrou `C004=0` e `C005=0` nas leituras preservadas, `C02B` inicializado em `0` e depois `1`, e `C26C` zerado em `0x00AD` e `0x4939`. Essa evidência é mais forte que a ausência anterior, mas ainda não prova a causa do retorno ao carregamento: a auditoria continua classificando a captura como `risk` por breakpoint não alcançado.

Foi criado `tools/analyze_dialog_state_gate.py` para consolidar esses estados, os PCs do gate e o resultado da auditoria. O próximo diagnóstico deve acompanhar a segunda chamada a `0x4B94` e os dados retornados por ela, sem forçar C004/C005/C26C nem aceitar a primeira visita a `0x4970` como transição de diálogo.

## Início do pipeline de tradução PT-BR

Foi criada `tools/apply_exact_patches.py`, um aplicador conservador que nunca modifica a ROM de entrada: exige bytes originais exatos, exige que a substituição tenha o mesmo tamanho, preserva o tamanho total da ROM e gera um manifesto ao lado da cópia de saída. O manifesto `build/ptbr_menu_patch.json` contém o primeiro patch validado: na ROM japonesa, `NEW GAME ` em `0x4672` foi substituído por `NOVO JOGO` usando o espaço de preenchimento existente.

A cópia de trabalho foi gerada como `input/kujaku_ou_ptbr_working.sms`, permanece ignorada pelo Git e tem 524288 bytes. A ROM original manteve SHA-256 `bfc5514e173113508d05721b3b45a70bb7a11d42d4e1ff0ff410460f1caa0a51`; a cópia privada modificada tem SHA-256 diferente e exibe `NOVO JOGO` no offset validado. Este é somente o primeiro patch de menu, não uma tradução final: os streams narrativos, ponteiros, comandos especiais, limites, checksum e validação visual ainda precisam ser resolvidos antes da entrega da cópia traduzida.

## Primeira tela PT-BR ampliada

O manifesto `build/ptbr_menu_patch.json` foi ampliado para três substituições ASCII exatas na ROM japonesa: `NEW GAME `→`NOVO JOGO`, `PASSWORD!`→`SENHA!!! ` e `PUSH START BUTTON`→`APERTE START` seguido de cinco espaços. Todas as substituições preservam o comprimento original e foram verificadas contra os bytes da ROM antes da aplicação.

A cópia privada `input/kujaku_ou_ptbr_working.sms` foi regenerada a partir da ROM original, manteve 524288 bytes e contém os três rótulos nas posições `0x4672`, `0x4686` e `0x46F0`. A ROM original não foi modificada nem incluída no Git. Esses patches traduzem somente a tela inicial; a tradução narrativa continua bloqueada até os streams finais e seus comandos serem validados.

## Smoke test da cópia PT-BR

A cópia privada `input/kujaku_ou_ptbr_working.sms` foi executada no mesmo capturador e com a mesma configuração da ROM original. Após 300 blocos, ambas terminaram em `PC=0x4073`, `SP=0xDFEC`, `FFFE=0x95`, `FFFF=0x0C` e `C280` com 20 entradas não nulas. O resultado `step_limit` é esperado neste smoke test, pois o breakpoint narrativo `0x4A8D` não é objetivo desta verificação. A igualdade dos estados de execução confirma que os patches da tela inicial não alteraram o fluxo de boot; a cópia ainda não é uma tradução completa.

## Captura limpa estendida da cadeia narrativa

Uma execução de 5000 blocos foi repetida com trace mínimo, `--trace-every 128` e monitor dedicado de `C200–C26F`, evitando a saturação causada por registrar cada opcode. Foram observados 20 VBlanks, 19 solicitações e 19 aceitações de IRQ, além de 19 leituras do controle; portanto, a cadeia periódica de interrupção permanece estável nessa configuração.

O ciclo de `C203` foi observado repetidamente: as rotinas `0x432F` e `0x4352` continuam limpando o estado, enquanto `0x406A` e `0x403F` rearmam operações. Além da escrita inicial `C206=0x80` em `0x4146`, apareceu uma escrita posterior `C206=0x82` e `C207=0x80` em `0x5275`, no bloco 4981. `C223`, `C238`, `C205`, `C215` e `C251` permaneceram apenas com as inicializações zeradas; o breakpoint `0x4A8D` não foi alcançado.

O auditor classificou o relatório como `risk` somente por `BREAKPOINT_NOT_REACHED`, loop dominante e entrada variável. A ausência de saturação torna esta evidência mais confiável para o ciclo de estado, mas não permite declarar diálogo ou snapshot de `C280`. O próximo probe deve acompanhar o banco e a rotina em torno de `0x5275`, correlacionando a nova escrita de `C206/C207` com a entrada do dispatcher e com a futura criação de `C223/C238`.

## Descoberta: 0x5275 prepara, mas não constrói o diálogo

A desassemblagem da rotina em `0x5270–0x5292`, alcançada no bloco 4981 com `C206=0x82` e `C207=0x80`, mostrou que `0x5275` grava `C022` a partir do byte apontado por HL, limpa `C280–C2BF` e inicializa `C2C0–C2CF` com `1`. Portanto, essa rotina é uma preparação de estado/objeto e não a construção final da tabela de glyphs.

A captura dedicada confirmou uma passagem completa por `0x5270–0x5292`, com `C022=1`, quatro eventos de limpeza em `C280` e quinze em `C281`/região de inicialização, mas não houve entrada em `0x4A73` ou `0x4A8D`. O auditor manteve `status=risk` por `BREAKPOINT_NOT_REACHED`; nenhum snapshot foi aceito. A distinção é importante: `C206/C207` não nulos indicam progresso no dispatcher, mas não significam que o diálogo foi resolvido.

O próximo passo é seguir o retorno de `0x5270` e o consumidor posterior de `C022`, identificando qual condição deveria selecionar a rotina `0x4A73` que chama `0x4BBD` para preencher `C022/C025–C028`, sem forçar a tabela C280.

## Mapa estático dos consumidores de C022

Foi criada `tools/find_ram_xrefs.py` para localizar referências absolutas Z80 a endereços de RAM, distinguindo leituras/escritas de byte e de palavra. Aplicada à ROM japonesa, a ferramenta encontrou leitores de `C022` em `0x4CF0`, `0x4E8E`, `0x4F20`, `0x4FA4`, `0x506F`, `0x4C1C` e `0x520F`, e escritas em `0x4A93`, `0x5275` e `0x4B3A`.

O resultado confirma que `0x5275` é apenas um produtor intermediário: ele instala `C022` e limpa `C280`. A construção final de C280 começa em `0x4A73`, grava os campos em `0x4A93–0x4AC9` e usa os valores em `0x4C1C–0x4C68` para resolver máscaras e streams. Na captura real, `C022=1` foi observado em `0x5275`, mas não houve entrada em `0x4A73`; portanto, esse valor isolado não pode ser tratado como diálogo pronto.

Os consumidores de `C022` agora formam uma lista concreta para o próximo trace, especialmente `0x4C1C`, `0x520F` e os chamadores que podem selecionar `0x4A73`. Nenhum patch narrativo será gerado a partir de referências estáticas sem validação dinâmica.

## Cadeia A0: C206 aponta para tabela de comandos

A rotina condicional `0x5012` foi desassemblada. Ela seleciona o banco `FFFF=0x16`, lê o ponteiro de `C206` e despacha pelo byte apontado para `0x5146`, `0x51A0`, `0x51AB`, `0x51B5`, `0x51BE`, `0x51CF`, `0x51EB`, `0x520C`, `0x5234`, `0x5270`, `0x5293`, `0x52B6`, `0x52D9` ou `0x52FE`. A captura dinâmica mostrou `C206=0x8380`, `C207=0x80` e chamada a `0x520F` com retorno para `0x401A`.

A região física correspondente do banco 22, em `0x58380`, contém uma tabela de registros compactados com códigos como `0x23`, `0x3B`, `0x3C`, `0x3D`, `0x3E`, `0x37`, `0x3F`, `0x46`, `0x47`, `0x48` e `0x49`, intercalados com parâmetros de tarefa. Isso confirma que o ponteiro de C206 está no dispatcher de tarefas A0, não em um stream de texto. O próximo passo deve identificar qual registro/código gera o comando que alimenta o produtor de C022/C280, acompanhando a progressão de C206 e os retornos ao `0x401A`.

## Consumidor dinâmico de C022 em 0x520F

A captura de 9000 blocos registrou uma chamada real a `0x520F` no bloco 5505, com retorno `0x401A`, `C022=1`, `C206=0x8383` e `C207=0x80`. A rotina lê `C022`, usa-o como índice na tabela local `0x5222` e grava o par correspondente em `C025`; para o índice `1`, o resultado é `C025=0x0020`. Em seguida, retorna ao dispatcher principal.

Essa passagem confirma que C022 é um índice de estado usado para selecionar parâmetros de tarefa, não um ponteiro direto para texto. O retorno para `0x401A` também explica por que o fluxo continua no dispatcher sem entrar em `0x4A73`: o caminho A0 está consumindo e rearmando tarefas, enquanto a rotina de construção final permanece não selecionada. O próximo probe deve correlacionar o valor do byte em `C206` antes de cada chamada a `0x5012`, `0x520F` e `0x5270`, para identificar o código de tarefa que deveria conduzir à entrada `0x4A73`.

## Progressão dinâmica do dispatcher A0

O trace de 9000 blocos mostrou três ciclos relevantes do dispatcher em `0x5012`: nos blocos 4981, 5505 e 6029, sempre com retorno para `0x401A`. No bloco 4981, `0x5012` despachou para `0x5270`; no bloco 5505, despachou para `0x520F`; nos demais ciclos seguintes não houve entrada em `0x4A73` nem em `0x4A8D`.

A chamada a `0x520F` ocorreu com `C022=1`, `C206=0x8383`, `C207=0x80` e `C203=0`; a rotina selecionou o parâmetro `0x0020` na tabela `0x5222` e gravou `C025=0x0020`. A sequência confirma que o dispatcher está consumindo tarefas A0 e avançando o ponteiro, mas a condição que seleciona a inicialização final de diálogo ainda não foi atingida. O auditor continua classificando a captura como `risk` por breakpoint não alcançado, portanto nenhum estado foi promovido a snapshot válido.

## Sequência de handlers A0 observada

Com o trace de destinos completo, a sequência dinâmica foi identificada sem inferência: em `C206=0x8080`, o byte `0xCB` levou a `0x5270`; em `C206=0x8082`, o byte `0x08` levou a `0x520C`; em `C206=0x8083`, o byte `0xC9` levou a `0x52FE`; e em `C206=0x8087`, o byte `0xDD` levou a `0x50FD`. Todos os handlers retornaram para `0x401A`, sem entrada em `0x4A73`/`0x4A8D`.

Essa sequência delimita o próximo ponto de investigação: os handlers `0x52FE` e `0x50FD` são os únicos destinos novos ainda não interpretados nesse trecho e podem atualizar o estado que habilita a construção final. O byte `0x08` não chama `0x520F` diretamente; ele cai em `0x520C`, que prepara o ponteiro C206 antes do retorno, enquanto `0x520F` é alcançado por uma chamada subsequente do dispatcher. A distinção foi registrada para evitar atribuir o efeito ao handler errado.
