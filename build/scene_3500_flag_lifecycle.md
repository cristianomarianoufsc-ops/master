# Ciclo de vida dos flags de carregamento de cena

Fonte: `/tmp/scene-3500.json`

## Resumo

- Registros de trace: 115764
- Escritas de `C008`: 6261
- Escritas de `C203`: 28

## Escritas de `0xC008`

| Ocorrências | Índices | Blocos | PC | Valor | FFFE | FFFF |
|---:|---|---|---|---:|---:|---:|
| 1 | 0 | 1 | 0x00AD | 0 | 1 | 130 |
| 3 | 10–6580 | 41–267 | 0x04E4 | 1 | 1 | 130 |
| 1 | 11 | 42 | 0x04E4 | 128 | 1 | 130 |
| 6191 | 12–6623 | 42–278 | 0x04E4 | 3 | 1 | 130 |
| 19 | 250–268 | 52 | 0x04E4 | 3 | 1 | 140 |
| 1 | 6551 | 265 | 0x01A1 | 0 | 1 | 130 |
| 1 | 6625 | 278 | 0x04E4 | 1 | 149 | 130 |
| 1 | 6626 | 285 | 0x40F5 | 2 | 149 | 12 |
| 12 | 14851–112638 | 527–3409 | 0x01A1 | 0 | 149 | 130 |
| 1 | 14852 | 531 | 0x412A | 2 | 149 | 19 |
| 19 | 23597–23615 | 789 | 0x04E4 | 3 | 149 | 22 |
| 1 | 23616 | 789 | 0x403A | 2 | 149 | 22 |
| 5 | 32499–103735 | 1051–3147 | 0x4065 | 2 | 149 | 130 |
| 5 | 41402–112640 | 1313–3409 | 0x403A | 2 | 149 | 130 |

## Escritas de `0xC203`

| Ocorrências | Índices | Blocos | PC | Valor | FFFE | FFFF |
|---:|---|---|---|---:|---:|---:|
| 1 | 1 | 1 | 0x00AD | 0 | 1 | 130 |
| 1 | 242 | 44 | 0x4939 | 0 | 1 | 130 |
| 1 | 6572 | 265 | 0x4496 | 0 | 1 | 130 |
| 1 | 6627 | 285 | 0x40FA | 1 | 149 | 12 |
| 1 | 14848 | 527 | 0x432F | 0 | 149 | 12 |
| 1 | 14853 | 531 | 0x412D | 2 | 149 | 19 |
| 1 | 23591 | 789 | 0x4352 | 0 | 149 | 22 |
| 1 | 23617 | 789 | 0x403F | 1 | 149 | 22 |
| 1 | 32495 | 1051 | 0x432F | 0 | 149 | 22 |
| 5 | 32500–103736 | 1051–3147 | 0x406A | 2 | 149 | 130 |
| 5 | 41399–112636 | 1313–3409 | 0x4352 | 0 | 149 | 130 |
| 5 | 41403–112641 | 1313–3409 | 0x403F | 1 | 149 | 130 |
| 4 | 50303–103731 | 1575–3147 | 0x432F | 0 | 149 | 130 |

## Escritas agrupadas por bloco

| Bloco | C008 (valores) | C203 (valores) | PCs envolvidos |
|---:|---|---|---|
| 1 | 0 | 0 | 0x00AD |
| 41 | 1 | — | 0x04E4 |
| 42 | 128, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3 | — | 0x04E4 |
| 44 | 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3 | 0 | 0x04E4, 0x4939 |
| 46 | 1 | — | 0x04E4 |
| 265 | 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3 | 0 | 0x01A1, 0x04E4, 0x4496 |
| 267 | 1 | — | 0x04E4 |
| 278 | 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1 | — | 0x04E4 |
| 285 | 2 | 1 | 0x40F5, 0x40FA |
| 527 | 0 | 0 | 0x01A1, 0x432F |
| 531 | 2 | 2 | 0x412A, 0x412D |
| 789 | 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2 | 0, 1 | 0x01A1, 0x04E4, 0x403A, 0x403F, 0x4352 |
| 1051 | 0, 2 | 0, 2 | 0x01A1, 0x4065, 0x406A, 0x432F |
| 1313 | 0, 2 | 0, 1 | 0x01A1, 0x403A, 0x403F, 0x4352 |
| 1575 | 0, 2 | 0, 2 | 0x01A1, 0x4065, 0x406A, 0x432F |
| 1837 | 0, 2 | 0, 1 | 0x01A1, 0x403A, 0x403F, 0x4352 |
| 2099 | 0, 2 | 0, 2 | 0x01A1, 0x4065, 0x406A, 0x432F |
| 2361 | 0, 2 | 0, 1 | 0x01A1, 0x403A, 0x403F, 0x4352 |
| 2623 | 0, 2 | 0, 2 | 0x01A1, 0x4065, 0x406A, 0x432F |
| 2885 | 0, 2 | 0, 1 | 0x01A1, 0x403A, 0x403F, 0x4352 |
| 3147 | 0, 2 | 0, 2 | 0x01A1, 0x4065, 0x406A, 0x432F |
| 3409 | 0, 2 | 0, 1 | 0x01A1, 0x403A, 0x403F, 0x4352 |

## Janelas locais das escritas

As janelas abaixo são contexto do trace, não prova de causalidade.

### Registro 0: run=1 pc=0x00AD 0xC008=0 banks=(1,130)

```text
0: run=1 pc=0x00AD 0xC008=0 banks=(1,130)
1: run=1 pc=0x00AD 0xC203=0 banks=(1,130)
2: run=1 pc=0x00AD 0xC22B=0 banks=(1,130)
```

### Registro 10: run=41 pc=0x04E4 0xC008=1 banks=(1,130) (3 ocorrências com a mesma assinatura)

```text
8: run=2 pc=0x0545 ?=0 banks=(1,130)
9: run=41 pc=0x8B8F 0xDE10=0 banks=(1,130)
10: run=41 pc=0x04E4 0xC008=1 banks=(1,130)
11: run=42 pc=0x04E4 0xC008=128 banks=(1,130)
12: run=42 pc=0x04E4 0xC008=3 banks=(1,130)
```

### Registro 11: run=42 pc=0x04E4 0xC008=128 banks=(1,130)

```text
9: run=41 pc=0x8B8F 0xDE10=0 banks=(1,130)
10: run=41 pc=0x04E4 0xC008=1 banks=(1,130)
11: run=42 pc=0x04E4 0xC008=128 banks=(1,130)
12: run=42 pc=0x04E4 0xC008=3 banks=(1,130)
13: run=42 pc=0x04E4 0xC008=3 banks=(1,130)
```

### Registro 12: run=42 pc=0x04E4 0xC008=3 banks=(1,130) (6191 ocorrências com a mesma assinatura)

```text
10: run=41 pc=0x04E4 0xC008=1 banks=(1,130)
11: run=42 pc=0x04E4 0xC008=128 banks=(1,130)
12: run=42 pc=0x04E4 0xC008=3 banks=(1,130)
13: run=42 pc=0x04E4 0xC008=3 banks=(1,130)
14: run=42 pc=0x04E4 0xC008=3 banks=(1,130)
```

### Registro 250: run=52 pc=0x04E4 0xC008=3 banks=(1,140) (19 ocorrências com a mesma assinatura)

```text
248: run=45 pc=0x4939 0xDE2D=0 banks=(1,130)
249: run=46 pc=0x04E4 0xC008=1 banks=(1,130)
250: run=52 pc=0x04E4 0xC008=3 banks=(1,140)
251: run=52 pc=0x04E4 0xC008=3 banks=(1,140)
252: run=52 pc=0x04E4 0xC008=3 banks=(1,140)
```

### Registro 6551: run=265 pc=0x01A1 0xC008=0 banks=(1,130)

```text
6549: run=265 pc=0x055F 0x00DC=239 banks=(1,132)
6550: run=265 pc=0x8CE2 0xDDF7=168 banks=(1,130)
6551: run=265 pc=0x01A1 0xC008=0 banks=(1,130)
6552: run=265 pc=0x04E4 0xC008=3 banks=(1,130)
6553: run=265 pc=0x04E4 0xC008=3 banks=(1,130)
```

### Registro 6625: run=278 pc=0x04E4 0xC008=1 banks=(149,130)

```text
6623: run=278 pc=0x04E4 0xC008=3 banks=(1,130)
6624: run=278 pc=0x8B93 0xDD32=0 banks=(149,130)
6625: run=278 pc=0x04E4 0xC008=1 banks=(149,130)
6626: run=285 pc=0x40F5 0xC008=2 banks=(149,12)
6627: run=285 pc=0x40FA 0xC203=1 banks=(149,12)
```

### Registro 6626: run=285 pc=0x40F5 0xC008=2 banks=(149,12)

```text
6624: run=278 pc=0x8B93 0xDD32=0 banks=(149,130)
6625: run=278 pc=0x04E4 0xC008=1 banks=(149,130)
6626: run=285 pc=0x40F5 0xC008=2 banks=(149,12)
6627: run=285 pc=0x40FA 0xC203=1 banks=(149,12)
6628: run=285 pc=0x4073 0xC008=2 banks=(149,12)
```

### Registro 14851: run=527 pc=0x01A1 0xC008=0 banks=(149,130) (12 ocorrências com a mesma assinatura)

```text
14849: run=527 pc=0x0577 0x00DC=255 banks=(149,12)
14850: run=527 pc=0x8090 0xDE17=0 banks=(149,130)
14851: run=527 pc=0x01A1 0xC008=0 banks=(149,130)
14852: run=531 pc=0x412A 0xC008=2 banks=(149,19)
14853: run=531 pc=0x412D 0xC203=2 banks=(149,19)
```

### Registro 14852: run=531 pc=0x412A 0xC008=2 banks=(149,19)

```text
14850: run=527 pc=0x8090 0xDE17=0 banks=(149,130)
14851: run=527 pc=0x01A1 0xC008=0 banks=(149,130)
14852: run=531 pc=0x412A 0xC008=2 banks=(149,19)
14853: run=531 pc=0x412D 0xC203=2 banks=(149,19)
14854: run=531 pc=0x4073 0xC008=2 banks=(149,22)
```

### Registro 23597: run=789 pc=0x04E4 0xC008=3 banks=(149,22) (19 ocorrências com a mesma assinatura)

```text
23595: run=789 pc=0x8C9F 0xDDB7=192 banks=(149,130)
23596: run=789 pc=0x01A1 0xC008=0 banks=(149,130)
23597: run=789 pc=0x04E4 0xC008=3 banks=(149,22)
23598: run=789 pc=0x04E4 0xC008=3 banks=(149,22)
23599: run=789 pc=0x04E4 0xC008=3 banks=(149,22)
```

### Registro 23616: run=789 pc=0x403A 0xC008=2 banks=(149,22)

```text
23614: run=789 pc=0x04E4 0xC008=3 banks=(149,22)
23615: run=789 pc=0x04E4 0xC008=3 banks=(149,22)
23616: run=789 pc=0x403A 0xC008=2 banks=(149,22)
23617: run=789 pc=0x403F 0xC203=1 banks=(149,22)
23618: run=789 pc=0x406F 0xC203=1 banks=(149,22)
```

### Registro 32499: run=1051 pc=0x4065 0xC008=2 banks=(149,130) (5 ocorrências com a mesma assinatura)

```text
32497: run=1051 pc=0x8BE8 0xDDC2=0 banks=(149,130)
32498: run=1051 pc=0x01A1 0xC008=0 banks=(149,130)
32499: run=1051 pc=0x4065 0xC008=2 banks=(149,130)
32500: run=1051 pc=0x406A 0xC203=2 banks=(149,130)
32501: run=1051 pc=0x4073 0xC008=2 banks=(149,130)
```

### Registro 41402: run=1313 pc=0x403A 0xC008=2 banks=(149,130) (5 ocorrências com a mesma assinatura)

```text
41400: run=1313 pc=0x0577 0x00DC=239 banks=(149,130)
41401: run=1313 pc=0x01A1 0xC008=0 banks=(149,130)
41402: run=1313 pc=0x403A 0xC008=2 banks=(149,130)
41403: run=1313 pc=0x403F 0xC203=1 banks=(149,130)
41404: run=1313 pc=0x406F 0xC203=1 banks=(149,130)
```

### Registro 1: run=1 pc=0x00AD 0xC203=0 banks=(1,130)

```text
0: run=1 pc=0x00AD 0xC008=0 banks=(1,130)
1: run=1 pc=0x00AD 0xC203=0 banks=(1,130)
2: run=1 pc=0x00AD 0xC22B=0 banks=(1,130)
3: run=2 pc=0x00AD 0xDD19=0 banks=(1,130)
```

### Registro 242: run=44 pc=0x4939 0xC203=0 banks=(1,130)

```text
240: run=44 pc=0x04E4 0xC008=3 banks=(1,130)
241: run=44 pc=0x492C 0xC021=5 banks=(1,130)
242: run=44 pc=0x4939 0xC203=0 banks=(1,130)
243: run=44 pc=0x4939 0xC23F=0 banks=(1,130)
244: run=45 pc=0x4939 0xDD2D=0 banks=(1,130)
```

### Registro 6572: run=265 pc=0x4496 0xC203=0 banks=(1,130)

```text
6570: run=265 pc=0x04E4 0xC008=3 banks=(1,130)
6571: run=265 pc=0x04E4 0xC008=3 banks=(1,130)
6572: run=265 pc=0x4496 0xC203=0 banks=(1,130)
6573: run=265 pc=0x4496 0xC21A=0 banks=(1,130)
6574: run=267 pc=0x4496 0xDD08=0 banks=(1,130)
```

### Registro 6627: run=285 pc=0x40FA 0xC203=1 banks=(149,12)

```text
6625: run=278 pc=0x04E4 0xC008=1 banks=(149,130)
6626: run=285 pc=0x40F5 0xC008=2 banks=(149,12)
6627: run=285 pc=0x40FA 0xC203=1 banks=(149,12)
6628: run=285 pc=0x4073 0xC008=2 banks=(149,12)
6629: run=285 pc=0x4073 0xC008=2 banks=(149,12)
```

### Registro 14848: run=527 pc=0x432F 0xC203=0 banks=(149,12)

```text
14846: run=526 pc=0x406C ?=? banks=(149,12)
14847: run=526 pc=0x0038 ?=? banks=(149,12)
14848: run=527 pc=0x432F 0xC203=0 banks=(149,12)
14849: run=527 pc=0x0577 0x00DC=255 banks=(149,12)
14850: run=527 pc=0x8090 0xDE17=0 banks=(149,130)
```

### Registro 14853: run=531 pc=0x412D 0xC203=2 banks=(149,19)

```text
14851: run=527 pc=0x01A1 0xC008=0 banks=(149,130)
14852: run=531 pc=0x412A 0xC008=2 banks=(149,19)
14853: run=531 pc=0x412D 0xC203=2 banks=(149,19)
14854: run=531 pc=0x4073 0xC008=2 banks=(149,22)
14855: run=531 pc=0x4073 0xC008=2 banks=(149,22)
```

### Registro 23591: run=789 pc=0x4352 0xC203=0 banks=(149,22)

```text
23589: run=788 pc=0x4073 ?=? banks=(149,22)
23590: run=788 pc=0x0038 ?=? banks=(149,22)
23591: run=789 pc=0x4352 0xC203=0 banks=(149,22)
23592: run=789 pc=0x0577 0x00DC=239 banks=(149,22)
23593: run=789 pc=0x8B81 0xDD0C=0 banks=(149,130)
```

### Registro 23617: run=789 pc=0x403F 0xC203=1 banks=(149,22)

```text
23615: run=789 pc=0x04E4 0xC008=3 banks=(149,22)
23616: run=789 pc=0x403A 0xC008=2 banks=(149,22)
23617: run=789 pc=0x403F 0xC203=1 banks=(149,22)
23618: run=789 pc=0x406F 0xC203=1 banks=(149,22)
23619: run=789 pc=0x406F 0xC203=1 banks=(149,22)
```

### Registro 32495: run=1051 pc=0x432F 0xC203=0 banks=(149,22)

```text
32493: run=1050 pc=0x406C ?=? banks=(149,22)
32494: run=1050 pc=0x0038 ?=? banks=(149,22)
32495: run=1051 pc=0x432F 0xC203=0 banks=(149,22)
32496: run=1051 pc=0x0577 0x00DC=255 banks=(149,22)
32497: run=1051 pc=0x8BE8 0xDDC2=0 banks=(149,130)
```

### Registro 32500: run=1051 pc=0x406A 0xC203=2 banks=(149,130) (5 ocorrências com a mesma assinatura)

```text
32498: run=1051 pc=0x01A1 0xC008=0 banks=(149,130)
32499: run=1051 pc=0x4065 0xC008=2 banks=(149,130)
32500: run=1051 pc=0x406A 0xC203=2 banks=(149,130)
32501: run=1051 pc=0x4073 0xC008=2 banks=(149,130)
32502: run=1051 pc=0x4073 0xC008=2 banks=(149,130)
```

### Registro 41399: run=1313 pc=0x4352 0xC203=0 banks=(149,130) (5 ocorrências com a mesma assinatura)

```text
41397: run=1312 pc=0x406C ?=? banks=(149,130)
41398: run=1312 pc=0x0038 ?=? banks=(149,130)
41399: run=1313 pc=0x4352 0xC203=0 banks=(149,130)
41400: run=1313 pc=0x0577 0x00DC=239 banks=(149,130)
41401: run=1313 pc=0x01A1 0xC008=0 banks=(149,130)
```

### Registro 41403: run=1313 pc=0x403F 0xC203=1 banks=(149,130) (5 ocorrências com a mesma assinatura)

```text
41401: run=1313 pc=0x01A1 0xC008=0 banks=(149,130)
41402: run=1313 pc=0x403A 0xC008=2 banks=(149,130)
41403: run=1313 pc=0x403F 0xC203=1 banks=(149,130)
41404: run=1313 pc=0x406F 0xC203=1 banks=(149,130)
41405: run=1313 pc=0x406F 0xC203=1 banks=(149,130)
```

### Registro 50303: run=1575 pc=0x432F 0xC203=0 banks=(149,130) (4 ocorrências com a mesma assinatura)

```text
50301: run=1574 pc=0x406F ?=? banks=(149,130)
50302: run=1574 pc=0x0038 ?=? banks=(149,130)
50303: run=1575 pc=0x432F 0xC203=0 banks=(149,130)
50304: run=1575 pc=0x0577 0x00DC=255 banks=(149,130)
50305: run=1575 pc=0x80CD 0xDDA1=13 banks=(149,130)
```

## Interpretação operacional

Use este relatório para correlacionar os escritores dinâmicos com as rotinas paginadas e os bancos ativos. Um flag constante ou uma escrita repetida não deve ser tratado como conclusão de carregamento sem confirmar a rotina consumidora e a progressão normal do jogo.
