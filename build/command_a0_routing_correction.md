# Correção do roteamento do comando A0

A comparação dos traces mostrou que, no caminho bloqueado, `DD03` recebe `0xA0` no bloco 265 e depois `0x80` em `0x857B`. A desassemblagem do dispatcher em `0x83E7–0x850C` separa comandos por faixa: para o caso `0xA0`, o fluxo passa por `0x84D2`, seleciona `DE=DDD7` em `0x8504` e prepara esse grupo, enquanto `DD57` é usado por outros casos.

Assim, a observação de que `DD57` permanece zero não prova, por si só, que ele seja a tarefa pendente de `C203=1`. A hipótese anterior foi corrigida. O dado forte que permanece é o loop em `0x406F` com `C203=1`, após `DD03=0xA0`; o próximo probe deve acompanhar `DDD7–DDF6` e identificar qual bit 7/handler corresponde ao comando A0.
