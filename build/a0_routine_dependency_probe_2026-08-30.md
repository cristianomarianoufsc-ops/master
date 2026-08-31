# Dependências observadas dentro de 0x8B62 — 2026-08-30

## Ferramenta criada

Foi criada `tools/analyze_a0_routine_dependencies.py`, que agrupa o trace por entrada em `0x8B62`, lista os PCs visitados, as leituras e escritas de memória e a evolução dos registradores. O capturador passou a registrar `F`, `IX` e `IY` além de A–L, SP e bancos.

## Resultado comparativo

As capturas foram executadas com a janela de PCs `0x8B60–0x8BD0`, entrada `0xFF` até o bloco 260 e `0x10` por 30 blocos, sem desbloqueios sintéticos.

| Caminho | Entradas | A/F na entrada | DE | HL | PCs observados | Acessos principais |
|---|---:|---|---|---|---|---|
| Fixo, retorno `0x0536` | 4 | `0x82/0x80` | `0x8900` | `0xC73F` | `0x8B62–0x8B98` com os mesmos saltos | Leituras `DD03–DD0C`; escritas em `DD03–DD0D`, `DD17`, `DD2F–DD32`, `DD37`, `DD4F–DD52`, `DD57`, `DD6F–DD72`, `DD77`, `DD8F–DD92`, `DD97`, `DDAF–DDB2` |
| Paginado, retorno `0x456C` | 1 | `0x82/0x10` | `0x0003` | `0x4547` | Mesmo conjunto `0x8B62–0x8B98` | Mesmo conjunto de leituras e escritas DDxx |

A rotina `0x8B62` percorreu o mesmo caminho interno e tocou o mesmo conjunto de campos nos dois contextos. A diferença observável já existia na entrada: flags `F`, ponteiros `DE/HL` e o banco `FFFE` quando ocorre a reentrada fixa posterior. O caminho paginado também foi precedido pelo loop `0x04E4`, que escreve `0x03` em `C008`.

## Conclusão

Não há evidência, neste probe, de que a rotina `0x8B62` escolha um ramo interno diferente com base somente nos campos DDxx monitorados. Ela executa a mesma sequência de limpeza para os dois retornos. A condição que diferencia o comportamento provavelmente está antes da chamada, ou em dados apontados pelos parâmetros `DE/HL`, não na seleção de um ramo interno observável nesta janela.

O próximo experimento deve seguir os ponteiros dos dois contextos: comparar os bytes lidos a partir de `HL=0xC73F` versus `HL=0x4547`, e `DE=0x8900` versus `DE=0x0003`, além de registrar flags após cada leitura dentro de `0x8B62`. O resultado continua diagnóstico: ambas as execuções terminam em `0x4073` sem atingir `0x4A8D`, portanto não há autorização para modificar a ROM.
