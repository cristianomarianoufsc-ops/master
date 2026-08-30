# Comando A0: tarefa DDD7 não armada

A captura focada em `DDD7–DDF6` foi executada com `FFFF=0x0C`, entrada `0x10` nos blocos 260–289 e dispatcher `0x8000–0x8D00`.

Foram observadas 26 escritas nessa faixa. Em todos os passes de inicialização (`0x8B8B–0x8B93`), o slot `DDD7` e os campos `DDEF–DDF2` foram escritos como zero. O dispatcher também leu `DDD7=0` no bloco 278 e não houve escrita posterior de `DDD7=0x80` nem chamada de handler ativo para esse grupo.

Isso confirma o roteamento do comando `0xA0` para o grupo iniciado em `DDD7`, mas mostra que o grupo não recebe a tarefa/dados necessários. O estado final permanece `0x406F` lendo `C203=1`. A causa deve ser procurada na origem da tabela usada por `sub_857C`/`sub_8536`, ou na condição que deveria fornecer a entrada não nula para o grupo DDD7.
