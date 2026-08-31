# Dependência de operandos em 0x8B62 — 2026-08-30

## Instrumentação

Foi adicionada a opção `--trace-memory-pcs`, encaminhada também pelo wrapper temporizado. Ela força o registro de toda leitura e escrita de memória enquanto o PC está em uma faixa selecionada. A opção foi necessária porque a instrumentação anterior só registrava faixas DDxx/Cxxx e não permitia distinguir fetches de opcode de operandos em ROM/RAM.

Também foi corrigido o wrapper `tools/run_timed_capture.py`, que agora encaminha corretamente `--trace-memory-pcs` sem modificar a sequência de entrada.

## Probe

A captura usou `--trace-memory-pcs 0x8B62-0x8BD0`, `--trace-exec-range 0x8B60-0x8BD0`, a janela de entrada `0xFF` até o bloco 260 e `0x10` por 30 blocos, sem desbloqueios sintéticos. Foram observadas cinco entradas em `0x8B62`: quatro com retorno `0x0536` e uma com retorno `0x456C`.

A ferramenta de análise encontrou, em ambas as classes de entrada, o mesmo conjunto de leituras de memória dentro da rotina: fetches dos opcodes `0x8B62–0x8B98` e leituras de `DD03–DD0C`. Não foram observadas leituras de dados nos endereços apontados pelos valores de `HL` (`0xC73F` no caminho fixo e `0x4547` no paginado) nem por `DE` (`0x8900` e `0x0003`, respectivamente). As escritas permaneceram no conjunto DDxx e em alguns bytes da pilha `DFE4–DFE9`.

## Conclusão

A hipótese de que `0x8B62` dereferencia diretamente `HL` ou `DE` não é sustentada por este trace. Esses registradores parecem funcionar como valores de estado ou parâmetros consumidos por instruções aritméticas/transferências, enquanto a rotina usa DDxx como estrutura de destino. O caminho fixo e o paginado continuam atravessando o mesmo corpo de rotina; a diferença chega pronta em `F`, `DE` e `HL`.

O próximo foco deve ser a desmontagem semântica do intervalo `0x8B62–0x8B98`, correlacionando opcode, efeitos em flags e instruções que escrevem os campos DDxx, em vez de criar outra ferramenta de captura. A execução terminou em `0x4073` sem alcançar `0x4A8D`; portanto, a ROM continua sem alteração.
