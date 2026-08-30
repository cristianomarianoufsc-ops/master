# Análise do dispatcher de IRQ da cena

A análise local da ROM japonesa foi feita com `z80dasm`; o desassembly completo não é publicado para evitar distribuir dumps derivados de bancos da ROM.

## Caminho confirmado

O handler fixo de IRQ em `0x015D–0x01B4` lê o status VDP, preserva os registradores, força `FFFF=0x82`, chama `0x8000` e depois grava `C008=0`. A entrada `0x8000` do banco 2 executa um dispatcher que percorre estruturas em `DDxx`, incluindo grupos iniciados em `DD17` e `DD57`, e chama handlers conforme o bit 7 dos registros de tarefa.

No banco 21, `0x432F` consome o bit 0 de `C203` e usa o bit 0 de `C204`; `0x4352` consome o bit 1 de `C203` e usa o bit 1 de `C204`. Esses consumidores não são chamados diretamente pelo fluxo principal do banco 21. O trace observacional mostrou `0x432F` limpando `C203` no primeiro carregamento e `0x4352` limpando-o antes da nova operação observada no bloco 789.

## Consequência

A segunda operação depende da ativação e progressão de uma tarefa em `DDxx`. O capturador atual modela RAM e IRQ, mas ainda não expõe um relatório específico dos registros `DD00–DE37` nem consegue provar que o dispatcher percorreu o mesmo estado do hardware. O próximo instrumento deve registrar leituras/escritas desse intervalo e chamadas à janela `0x8000`, mantendo o gate contra falsos positivos.
