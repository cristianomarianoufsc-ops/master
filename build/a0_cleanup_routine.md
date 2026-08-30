# Rotina de limpeza de slots em 0x8B81–0x8B99

A janela física correspondente a `0x8B80–0x8BCF` foi extraída do banco 2, que é o banco ativo quando `FFFF=0x82`. A sequência de bytes em `0x8B81` é:

```text
21 17 DD AF 06 0A 11 18 00 77 19 77 23 77 23 77 23 77 11 05 00 19 10 EE
```

A decodificação Z80 é:

| Endereço | Instrução | Efeito |
|---|---|---|
| `0x8B81` | `LD HL,DD17h` | Seleciona o início da tabela de slots |
| `0x8B84` | `XOR A` | Define o valor de limpeza como zero |
| `0x8B85` | `LD B,0Ah` | Executa dez iterações |
| `0x8B87` | `LD DE,0018h` | Define o deslocamento entre o primeiro e o segundo campo |
| `0x8B8A` | `LD (HL),A` | Zera o primeiro byte do slot |
| `0x8B8B` | `ADD HL,DE` | Avança `0x18` bytes |
| `0x8B8C` | `LD (HL),A` | Zera o segundo campo |
| `0x8B8D` | `INC HL` | Avança um byte |
| `0x8B8E` | `LD (HL),A` | Zera o terceiro campo |
| `0x8B8F` | `INC HL` | Avança um byte |
| `0x8B90` | `LD (HL),A` | Zera o quarto campo |
| `0x8B91` | `INC HL` | Avança um byte |
| `0x8B92` | `LD (HL),A` | Zera o quinto campo |
| `0x8B93` | `LD DE,0005h` | Avança até o próximo slot lógico |
| `0x8B96` | `ADD HL,DE` | Completa o passo de `0x20` bytes |
| `0x8B97` | `DJNZ 8B87h` | Repete sem testar flags de tarefa |

Nos traces do capturador, o callback de escrita registra o PC já avançado após a instrução. Por isso, uma escrita executada por `LD (HL),A` em `0x8B8A` pode aparecer associada ao PC `0x8B8B`.

O primeiro campo de cada slot começa em `DD17` e os slots seguintes começam a cada `0x20` bytes. Assim, uma iteração posterior alcança `DDF7`, seguida pelos campos `DE0F–DE12`, exatamente como observado no trace dinâmico.

## Consequência para a investigação

A hipótese anterior deve ser refinada: a tarefa A0 é armada no bloco 265, mas o laço de inicialização entra posteriormente no limpador geral de slots. A causa a localizar não está em uma decisão interna de `0x8B8B`; está no chamador ou no estado de despacho que leva a execução a essa rotina enquanto `C203=1` ainda depende da tarefa.

O próximo probe deve capturar o endereço de retorno e as instruções imediatamente anteriores à entrada em `0x8B81`, além de `DD03`, `DD97`, `DDB7` e do slot A0. Esta análise é estática e compatível com o trace dinâmico já observado. Ela não altera flags, não libera esperas e não constitui evidência de que o breakpoint `0x4A8D` foi alcançado.
