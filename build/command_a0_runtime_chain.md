# Cadeia runtime do comando A0

A extração de eventos do trace em `0x83E7–0x857B` corrigiu a inferência baseada apenas nos saltos estáticos. No bloco 265, `0x83EA` lê `DD03=0xA0`. Em seguida, `0x8536` opera com o ponteiro `0xAB72` (registradores `B:C=0xAB72`) e com destino `DDF7`; a mesma rotina sinaliza `DD97=4` e copia dados para o grupo iniciado em `DDF7`. Em `0x857B`, `DD03` é reduzido a `0x80`.

A cadeia observada é, portanto, `DD03=A0 → tabela/ponteiro AB72 → grupo DDF7/DD97`, e não `DDD7` como inferido anteriormente. O estado bloqueado em `0x406F` deve ser investigado seguindo `DDF7–DE16` e o flag de `DD97`. Nenhum flag foi forçado.
