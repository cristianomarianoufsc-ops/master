# Diagnóstico do bloqueio da tarefa em FFFF=0x0C

A captura foi executada até 340 blocos com `FFFF=0x0C` no caminho bloqueado, usando trace completo do dispatcher `0x8000–0x8D00` e memória `DD00–DE37`.

O dispatcher executou normalmente, com 415 eventos DDxx, 326 escritas e 89 leituras. Entretanto, o slot de tarefa iniciado em `DD57` nunca foi armado: as escritas observadas foram `DD57=0` nos blocos 41, 46, 267, 277 e 278. No caminho que progride, o mesmo slot recebe `DD57=0x80` no bloco 789, permitindo que o dispatcher entre nos handlers associados.

Assim, o estado em `0x406F` é explicado por `C203=1` aguardando uma tarefa cujo bit 7 não foi ativado. O próximo ponto de análise é a rotina que deveria escrever `DD57=0x80` para o pedido do banco `0x0C`; a comparação deve ser feita no ponto de chamada, sem forçar o bit no emulador.
