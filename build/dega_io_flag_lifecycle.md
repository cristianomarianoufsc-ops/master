# Ciclo de vida dos flags de carregamento de cena

Fonte: `/tmp/dega-io.json`

## Resumo

- Registros de trace: 90704
- Escritas de `C008`: 6241
- Escritas de `C203`: 8

## Escritas de `0xC008`

| Ocorrências | Índices | Blocos | PC | Valor | FFFE | FFFF |
|---:|---|---|---|---:|---:|---:|
| 1 | 0 | 1 | 0x00AD | 0 | 1 | 130 |
| 3 | 9–7698 | 41–267 | 0x04E4 | 1 | 1 | 130 |
| 1 | 10 | 42 | 0x04E4 | 128 | 1 | 130 |
| 6191 | 11–7743 | 42–278 | 0x04E4 | 3 | 1 | 130 |
| 19 | 263–281 | 52 | 0x04E4 | 3 | 1 | 140 |
| 1 | 7669 | 265 | 0x01A1 | 0 | 1 | 130 |
| 1 | 7744 | 278 | 0x04E4 | 1 | 149 | 130 |
| 1 | 7745 | 285 | 0x40F5 | 2 | 149 | 12 |
| 2 | 40620–75566 | 527–789 | 0x01A1 | 0 | 149 | 130 |
| 1 | 40621 | 531 | 0x412A | 2 | 149 | 19 |
| 19 | 75567–75586 | 789 | 0x04E4 | 3 | 149 | 22 |
| 1 | 75588 | 789 | 0x403A | 2 | 149 | 22 |

## Escritas de `0xC203`

| Ocorrências | Índices | Blocos | PC | Valor | FFFE | FFFF |
|---:|---|---|---|---:|---:|---:|
| 1 | 2 | 1 | 0x00AD | 0 | 1 | 130 |
| 1 | 256 | 44 | 0x4939 | 0 | 1 | 130 |
| 1 | 7692 | 265 | 0x4496 | 0 | 1 | 130 |
| 1 | 7746 | 285 | 0x40FA | 1 | 149 | 12 |
| 1 | 40618 | 527 | 0x432F | 0 | 149 | 12 |
| 1 | 40622 | 531 | 0x412D | 2 | 149 | 19 |
| 1 | 75564 | 789 | 0x4352 | 0 | 149 | 22 |
| 1 | 75589 | 789 | 0x403F | 1 | 149 | 22 |

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

## Janelas locais das escritas

As janelas abaixo são contexto do trace, não prova de causalidade.

### Registro 0: run=1 pc=0x00AD 0xC008=0 banks=(1,130)

```text
0: run=1 pc=0x00AD 0xC008=0 banks=(1,130)
1: run=1 pc=0x00AD 0xC02C=0 banks=(1,130)
2: run=1 pc=0x00AD 0xC203=0 banks=(1,130)
```

### Registro 9: run=41 pc=0x04E4 0xC008=1 banks=(1,130) (3 ocorrências com a mesma assinatura)

```text
7: run=1 pc=0x00AD 0xC24B=0 banks=(1,130)
8: run=2 pc=0x0545 ?=0 banks=(1,130)
9: run=41 pc=0x04E4 0xC008=1 banks=(1,130)
10: run=42 pc=0x04E4 0xC008=128 banks=(1,130)
11: run=42 pc=0x04E4 0xC008=3 banks=(1,130)
```

### Registro 10: run=42 pc=0x04E4 0xC008=128 banks=(1,130)

```text
8: run=2 pc=0x0545 ?=0 banks=(1,130)
9: run=41 pc=0x04E4 0xC008=1 banks=(1,130)
10: run=42 pc=0x04E4 0xC008=128 banks=(1,130)
11: run=42 pc=0x04E4 0xC008=3 banks=(1,130)
12: run=42 pc=0x04E4 0xC008=3 banks=(1,130)
```

### Registro 11: run=42 pc=0x04E4 0xC008=3 banks=(1,130) (6191 ocorrências com a mesma assinatura)

```text
9: run=41 pc=0x04E4 0xC008=1 banks=(1,130)
10: run=42 pc=0x04E4 0xC008=128 banks=(1,130)
11: run=42 pc=0x04E4 0xC008=3 banks=(1,130)
12: run=42 pc=0x04E4 0xC008=3 banks=(1,130)
13: run=42 pc=0x04E4 0xC008=3 banks=(1,130)
```

### Registro 263: run=52 pc=0x04E4 0xC008=3 banks=(1,140) (19 ocorrências com a mesma assinatura)

```text
261: run=44 pc=0x4939 0xC249=0 banks=(1,130)
262: run=46 pc=0x04E4 0xC008=1 banks=(1,130)
263: run=52 pc=0x04E4 0xC008=3 banks=(1,140)
264: run=52 pc=0x04E4 0xC008=3 banks=(1,140)
265: run=52 pc=0x04E4 0xC008=3 banks=(1,140)
```

### Registro 7669: run=265 pc=0x01A1 0xC008=0 banks=(1,130)

```text
7667: run=264 pc=0x0038 ?=? banks=(1,132)
7668: run=265 pc=0x055F 0x00DC=239 banks=(1,132)
7669: run=265 pc=0x01A1 0xC008=0 banks=(1,130)
7670: run=265 pc=0x04E4 0xC008=3 banks=(1,130)
7671: run=265 pc=0x04E4 0xC008=3 banks=(1,130)
```

### Registro 7744: run=278 pc=0x04E4 0xC008=1 banks=(149,130)

```text
7742: run=278 pc=0x04E4 0xC008=3 banks=(1,130)
7743: run=278 pc=0x04E4 0xC008=3 banks=(1,130)
7744: run=278 pc=0x04E4 0xC008=1 banks=(149,130)
7745: run=285 pc=0x40F5 0xC008=2 banks=(149,12)
7746: run=285 pc=0x40FA 0xC203=1 banks=(149,12)
```

### Registro 7745: run=285 pc=0x40F5 0xC008=2 banks=(149,12)

```text
7743: run=278 pc=0x04E4 0xC008=3 banks=(1,130)
7744: run=278 pc=0x04E4 0xC008=1 banks=(149,130)
7745: run=285 pc=0x40F5 0xC008=2 banks=(149,12)
7746: run=285 pc=0x40FA 0xC203=1 banks=(149,12)
7747: run=285 pc=0x4073 0xC008=2 banks=(149,12)
```

### Registro 40620: run=527 pc=0x01A1 0xC008=0 banks=(149,130) (2 ocorrências com a mesma assinatura)

```text
40618: run=527 pc=0x432F 0xC203=0 banks=(149,12)
40619: run=527 pc=0x0577 0x00DC=255 banks=(149,12)
40620: run=527 pc=0x01A1 0xC008=0 banks=(149,130)
40621: run=531 pc=0x412A 0xC008=2 banks=(149,19)
40622: run=531 pc=0x412D 0xC203=2 banks=(149,19)
```

### Registro 40621: run=531 pc=0x412A 0xC008=2 banks=(149,19)

```text
40619: run=527 pc=0x0577 0x00DC=255 banks=(149,12)
40620: run=527 pc=0x01A1 0xC008=0 banks=(149,130)
40621: run=531 pc=0x412A 0xC008=2 banks=(149,19)
40622: run=531 pc=0x412D 0xC203=2 banks=(149,19)
40623: run=531 pc=0x4146 0xC206=128 banks=(149,22)
```

### Registro 75567: run=789 pc=0x04E4 0xC008=3 banks=(149,22) (19 ocorrências com a mesma assinatura)

```text
75565: run=789 pc=0x0577 0x00DC=255 banks=(149,22)
75566: run=789 pc=0x01A1 0xC008=0 banks=(149,130)
75567: run=789 pc=0x04E4 0xC008=3 banks=(149,22)
75568: run=789 pc=0x04E4 0xC008=3 banks=(149,22)
75569: run=789 pc=0x04E4 0xC008=3 banks=(149,22)
```

### Registro 75588: run=789 pc=0x403A 0xC008=2 banks=(149,22)

```text
75586: run=789 pc=0x04E4 0xC008=3 banks=(149,22)
75587: run=789 pc=0x4015 0xC200=16 banks=(149,22)
75588: run=789 pc=0x403A 0xC008=2 banks=(149,22)
75589: run=789 pc=0x403F 0xC203=1 banks=(149,22)
75590: run=789 pc=0x4073 0xC008=2 banks=(149,22)
```

### Registro 2: run=1 pc=0x00AD 0xC203=0 banks=(1,130)

```text
0: run=1 pc=0x00AD 0xC008=0 banks=(1,130)
1: run=1 pc=0x00AD 0xC02C=0 banks=(1,130)
2: run=1 pc=0x00AD 0xC203=0 banks=(1,130)
3: run=1 pc=0x00AD 0xC20B=0 banks=(1,130)
4: run=1 pc=0x00AD 0xC21B=0 banks=(1,130)
```

### Registro 256: run=44 pc=0x4939 0xC203=0 banks=(1,130)

```text
254: run=44 pc=0x04E4 0xC008=3 banks=(1,130)
255: run=44 pc=0x04E4 0xC008=3 banks=(1,130)
256: run=44 pc=0x4939 0xC203=0 banks=(1,130)
257: run=44 pc=0x4939 0xC209=0 banks=(1,130)
258: run=44 pc=0x4939 0xC219=0 banks=(1,130)
```

### Registro 7692: run=265 pc=0x4496 0xC203=0 banks=(1,130)

```text
7690: run=265 pc=0x04E4 0xC008=3 banks=(1,130)
7691: run=265 pc=0x00E5 0xFFFE=1 banks=(1,130)
7692: run=265 pc=0x4496 0xC203=0 banks=(1,130)
7693: run=265 pc=0x4496 0xC20A=0 banks=(1,130)
7694: run=265 pc=0x4496 0xC21A=0 banks=(1,130)
```

### Registro 7746: run=285 pc=0x40FA 0xC203=1 banks=(149,12)

```text
7744: run=278 pc=0x04E4 0xC008=1 banks=(149,130)
7745: run=285 pc=0x40F5 0xC008=2 banks=(149,12)
7746: run=285 pc=0x40FA 0xC203=1 banks=(149,12)
7747: run=285 pc=0x4073 0xC008=2 banks=(149,12)
7748: run=285 pc=0x4073 0xC008=2 banks=(149,12)
```

### Registro 40618: run=527 pc=0x432F 0xC203=0 banks=(149,12)

```text
40616: run=526 pc=0x406C ?=? banks=(149,12)
40617: run=526 pc=0x0038 ?=? banks=(149,12)
40618: run=527 pc=0x432F 0xC203=0 banks=(149,12)
40619: run=527 pc=0x0577 0x00DC=255 banks=(149,12)
40620: run=527 pc=0x01A1 0xC008=0 banks=(149,130)
```

### Registro 40622: run=531 pc=0x412D 0xC203=2 banks=(149,19)

```text
40620: run=527 pc=0x01A1 0xC008=0 banks=(149,130)
40621: run=531 pc=0x412A 0xC008=2 banks=(149,19)
40622: run=531 pc=0x412D 0xC203=2 banks=(149,19)
40623: run=531 pc=0x4146 0xC206=128 banks=(149,22)
40624: run=531 pc=0x406F 0xC203=2 banks=(149,22)
```

### Registro 75564: run=789 pc=0x4352 0xC203=0 banks=(149,22)

```text
75562: run=788 pc=0x4073 ?=? banks=(149,22)
75563: run=788 pc=0x0038 ?=? banks=(149,22)
75564: run=789 pc=0x4352 0xC203=0 banks=(149,22)
75565: run=789 pc=0x0577 0x00DC=255 banks=(149,22)
75566: run=789 pc=0x01A1 0xC008=0 banks=(149,130)
```

### Registro 75589: run=789 pc=0x403F 0xC203=1 banks=(149,22)

```text
75587: run=789 pc=0x4015 0xC200=16 banks=(149,22)
75588: run=789 pc=0x403A 0xC008=2 banks=(149,22)
75589: run=789 pc=0x403F 0xC203=1 banks=(149,22)
75590: run=789 pc=0x4073 0xC008=2 banks=(149,22)
75591: run=789 pc=0x4073 0xC008=2 banks=(149,22)
```

## Interpretação operacional

Use este relatório para correlacionar os escritores dinâmicos com as rotinas paginadas e os bancos ativos. Um flag constante ou uma escrita repetida não deve ser tratado como conclusão de carregamento sem confirmar a rotina consumidora e a progressão normal do jogo.
