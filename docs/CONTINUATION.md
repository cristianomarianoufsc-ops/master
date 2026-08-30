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
