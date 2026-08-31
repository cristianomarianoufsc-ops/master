# Janela causal anterior aos CALLs A0 — 2026-08-30

## Nova ferramenta

Foi criada `tools/compare_a0_call_windows.py`. Ela recebe os traces estreitos dos caminhos fixo e paginado, localiza as entradas em `0x8B62` pelos retornos `0x0536` e `0x456C`, e produz tabelas com PC, tipo de evento, registradores A/F, pares BC/DE/HL, IX/IY, SP e operações de memória imediatamente anteriores.

O capturador também passou a registrar `F`, `IX` e `IY` em cada evento, mantendo `getattr` para compatibilidade com implementações Z80 que não exponham algum registrador.

## Evidência causal

| Caminho | Entrada em `0x8B62` | Estado imediatamente antes do CALL | Operação distintiva |
|---|---|---|---|
| Fixo | retorno `0x0536`, bloco 41/46/267/278 | `A=0x82`, `F=0x80`, `BC=0x0000`, `DE=0x8900`, `HL=0xC73F`, `SP=0xDFEC` antes do CALL | escreve `0x82` em `FFFF` em `0x0533`; lê `C73E` e escreve `C73F` |
| Paginado | retorno `0x456C`, bloco 277 | `A=0x82`, `F=0x10`, `BC=0x0000`, `DE=0x0003`, `HL=0x4547`, `SP=0xDFEC` antes do CALL | escreve `0x82` em `FFFF` em `0x4569`; é precedido por escritas repetidas em `C008` no loop `0x04E4` |

O caminho fixo executa a sequência `0x0526–0x0534`, que transforma `HL` de `0xC73E` para `0xC73F`, atualiza `DE` para `0x8900` e chega com `F=0x80`. O caminho paginado passa por `0x4564–0x456A`, chega com `HL=0x4547`, `DE=0x0003` e `F=0x10`, após o loop de `0x04E4` escrever repetidamente `0x03` em `C008`.

## Interpretação

Esta é a primeira diferença concreta no estado de CPU imediatamente anterior aos dois `CALL`s. A distinção não está nos campos DDxx/C203 na entrada de `0x8B62`, que permanecem zerados, mas no contexto de execução que entrega os parâmetros à rotina: `HL`, `DE` e flags são completamente diferentes. O caminho paginado também está causalmente ligado ao loop VDP em `0x04E4`, que escreve `0x03` em `C008` antes de alcançar `0x4569`.

Ainda não é seguro afirmar qual registrador é a condição lógica final, pois o capturador é diagnóstico e o breakpoint `0x4A8D` não é alcançado. Entretanto, o próximo experimento agora pode ser focalizado: acompanhar como `0x8B62` usa `HL=0x4547`, `DE=0x0003`, `F=0x10` e o valor `C008=0x03` no caminho paginado, comparando com `HL=0xC73F`, `DE=0x8900`, `F=0x80` no caminho fixo.

## Estado de validação

As duas execuções foram de 300 blocos, terminaram em `0x4073` e não atingiram `0x4A8D`. Portanto, a descoberta é forte como diferença causal observada, mas ainda não constitui snapshot válido de `C280` nem autoriza alteração da ROM.
