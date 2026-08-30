# Ciclo de vida da tarefa A0 em DDF7

O trace `DDD7–DE16` foi corrigido para seguir o grupo efetivamente selecionado em runtime, `DDF7–DE16`, e o flag auxiliar `DD97`.

No bloco 265, o dispatcher executa a cadeia do comando `0xA0`: `DDB7=4`, `DD97=4`, e `0x8536` copia uma estrutura para `DDF7–DE06`, começando com `DDF7=0xA8` (bit 7 ativo). O grupo contém dados não nulos, incluindo ponteiro/atributos e campos de controle.

No bloco 267, a rotina de inicialização `0x8B8B–0x8B93` escreve `DDF7=0` e zera `DDEF–DDF2`; em seguida, o estado entra no loop `0x406F` com `C203=1`. Assim, a tarefa é armada e recebe dados, mas é desmontada no passe seguinte antes que `C203` seja consumido. Essa é a causa localizada atual; o próximo passo é identificar a condição de limpeza em `0x8B8B` e por que ela ocorre imediatamente após o comando A0.
