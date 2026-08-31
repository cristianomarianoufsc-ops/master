# Comparação ROM japonesa × americana

## Entradas

A ROM japonesa `KujakuOu(Japan).sms` e a ROM americana `SpellCaster(USA,Europe).sms` têm **524.288 bytes**, equivalentes a **32 bancos de 16 KiB**. Ambas foram mantidas apenas localmente em `input/` e não foram adicionadas ao Git.

## Similaridade byte a byte por banco

A comparação foi feita na mesma posição física de cada banco.

| Banco | Bytes idênticos | Percentual |
|---:|---:|---:|
| 0 | 10.164 | 62,0% |
| 1 | 2.319 | 14,2% |
| 2 | 4.132 | 25,2% |
| 3 | 2.822 | 17,2% |
| 4 | 5.339 | 32,6% |
| 5 | 15.823 | 96,6% |
| 6 | 16.384 | 100,0% |
| 7 | 16.384 | 100,0% |
| 8 | 16.384 | 100,0% |
| 9 | 16.384 | 100,0% |
| 10 | 16.384 | 100,0% |
| 11 | 16.384 | 100,0% |
| 12 | 1.071 | 6,5% |
| 13 | 16.384 | 100,0% |
| 14 | 5.785 | 35,3% |
| 15 | 16.384 | 100,0% |
| 16 | 16.384 | 100,0% |
| 17 | 3.107 | 19,0% |
| 18 | 3.603 | 22,0% |
| 19 | 8.115 | 49,5% |
| 20 | 8.893 | 54,3% |
| 21 | 2.640 | 16,1% |
| 22 | 16.384 | 100,0% |
| 23 | 16.341 | 99,7% |
| 24 | 1.310 | 8,0% |
| 25 | 16.384 | 100,0% |
| 26 | 16.384 | 100,0% |
| 27 | 16.384 | 100,0% |
| 28 | 6.745 | 41,2% |
| 29 | 16.384 | 100,0% |
| 30 | 357 | 2,2% |
| 31 | 516 | 3,1% |

## Interpretação

O resultado é melhor do que a hipótese de duas ROMs completamente diferentes. **Dezessete bancos estão integralmente idênticos ou praticamente idênticos**: 6–11, 13, 15–16, 22–23 e 25–29. Esses bancos podem ser usados como referência direta para código compartilhado, rotinas comuns, gráficos e estruturas de dados. Os bancos 5 e 23 também são praticamente idênticos.

Os bancos com baixa similaridade concentram as diferenças de localização, textos, tabelas e/ou conteúdo específico regional. O banco 21, que contém a cadeia dinâmica de diálogo estudada, tem apenas 16,1% de bytes iguais; por isso os offsets das tabelas não podem ser copiados cegamente. Mesmo assim, a disassemblagem mostrou lógica homóloga: o equivalente americano de `04BBD` aparece em `0x4BCB`, e o equivalente de `04CFD` em `0x4D0B`, enquanto na japonesa aparecem em `0x4BBD` e `0x4CFD`.

A tentativa inicial de alinhar janelas binárias de 32 bytes nos pontos de texto e banco 21 não encontrou correspondências exatas. Isso é esperado para regiões localizadas. A estratégia correta passa a ser: usar bancos 100% idênticos para validar o executor e as rotinas comuns; comparar o código do banco 21 por assinaturas de instruções com operandos mascarados; e usar as mensagens ASCII americanas como âncoras sem presumir que suas posições físicas existam na japonesa.

## Conclusão operacional

A versão americana torna o projeto **consideravelmente mais fácil**, sobretudo como oráculo de texto e para validar o comportamento de bancos compartilhados. Ela não resolve sozinha o estado dinâmico japonês, mas reduz muito o espaço de busca. O próximo passo recomendado é implementar alinhamento por assinatura de opcode/controle de fluxo no banco 21 e localizar na japonesa as mensagens equivalentes aos textos ingleses, antes de criar qualquer patch.

## Integridade

Nenhuma ROM foi modificada. Nenhum dump completo ou save state foi publicado. O relatório registra somente metadados e resultados agregados da comparação.
