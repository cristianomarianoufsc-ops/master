# Ciclo de vida dos flags de carregamento de cena

Fonte: `/tmp/ddxx.json`

## Resumo

- Registros de trace: 41732
- Escritas de `C008`: 6241
- Escritas de `C203`: 8

## Escritas de `0xC008`

| Ocorrências | Índices | Blocos | PC | Valor | FFFE | FFFF |
|---:|---|---|---|---:|---:|---:|
| 1 | 0 | 1 | 0x00AD | 0 | 1 | 130 |
| 3 | 17–6975 | 41–267 | 0x04E4 | 1 | 1 | 130 |
| 1 | 18 | 42 | 0x04E4 | 128 | 1 | 130 |
| 6191 | 19–7019 | 42–278 | 0x04E4 | 3 | 1 | 130 |
| 19 | 270–288 | 52 | 0x04E4 | 3 | 1 | 140 |
| 1 | 6939 | 265 | 0x01A1 | 0 | 1 | 130 |
| 1 | 7021 | 278 | 0x04E4 | 1 | 149 | 130 |
| 1 | 7022 | 285 | 0x40F5 | 2 | 149 | 12 |
| 2 | 23465–40946 | 527–789 | 0x01A1 | 0 | 149 | 130 |
| 1 | 23466 | 531 | 0x412A | 2 | 149 | 19 |
| 19 | 40947–40965 | 789 | 0x04E4 | 3 | 149 | 22 |
| 1 | 40967 | 789 | 0x403A | 2 | 149 | 22 |

## Escritas de `0xC203`

| Ocorrências | Índices | Blocos | PC | Valor | FFFE | FFFF |
|---:|---|---|---|---:|---:|---:|
| 1 | 1 | 1 | 0x00AD | 0 | 1 | 130 |
| 1 | 255 | 44 | 0x4939 | 0 | 1 | 130 |
| 1 | 6961 | 265 | 0x4496 | 0 | 1 | 130 |
| 1 | 7023 | 285 | 0x40FA | 1 | 149 | 12 |
| 1 | 23461 | 527 | 0x432F | 0 | 149 | 12 |
| 1 | 23467 | 531 | 0x412D | 2 | 149 | 19 |
| 1 | 40940 | 789 | 0x4352 | 0 | 149 | 22 |
| 1 | 40968 | 789 | 0x403F | 1 | 149 | 22 |

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
1: run=1 pc=0x00AD 0xC203=0 banks=(1,130)
2: run=1 pc=0x00AD 0xC20B=0 banks=(1,130)
```

### Registro 17: run=41 pc=0x04E4 0xC008=1 banks=(1,130) (3 ocorrências com a mesma assinatura)

```text
15: run=41 pc=0x00D7 0xC020=0 banks=(1,130)
16: run=41 pc=0x8B8F 0xDE10=0 banks=(1,130)
17: run=41 pc=0x04E4 0xC008=1 banks=(1,130)
18: run=42 pc=0x04E4 0xC008=128 banks=(1,130)
19: run=42 pc=0x04E4 0xC008=3 banks=(1,130)
```

### Registro 18: run=42 pc=0x04E4 0xC008=128 banks=(1,130)

```text
16: run=41 pc=0x8B8F 0xDE10=0 banks=(1,130)
17: run=41 pc=0x04E4 0xC008=1 banks=(1,130)
18: run=42 pc=0x04E4 0xC008=128 banks=(1,130)
19: run=42 pc=0x04E4 0xC008=3 banks=(1,130)
20: run=42 pc=0x04E4 0xC008=3 banks=(1,130)
```

### Registro 19: run=42 pc=0x04E4 0xC008=3 banks=(1,130) (6191 ocorrências com a mesma assinatura)

```text
17: run=41 pc=0x04E4 0xC008=1 banks=(1,130)
18: run=42 pc=0x04E4 0xC008=128 banks=(1,130)
19: run=42 pc=0x04E4 0xC008=3 banks=(1,130)
20: run=42 pc=0x04E4 0xC008=3 banks=(1,130)
21: run=42 pc=0x04E4 0xC008=3 banks=(1,130)
```

### Registro 270: run=52 pc=0x04E4 0xC008=3 banks=(1,140) (19 ocorrências com a mesma assinatura)

```text
268: run=46 pc=0x8B8B 0xDD97=0 banks=(1,130)
269: run=46 pc=0x04E4 0xC008=1 banks=(1,130)
270: run=52 pc=0x04E4 0xC008=3 banks=(1,140)
271: run=52 pc=0x04E4 0xC008=3 banks=(1,140)
272: run=52 pc=0x04E4 0xC008=3 banks=(1,140)
```

### Registro 6939: run=265 pc=0x01A1 0xC008=0 banks=(1,130)

```text
6937: run=265 pc=0x810E 0xDD07=112 banks=(1,130)
6938: run=265 pc=0x8CE2 0xDDF7=168 banks=(1,130)
6939: run=265 pc=0x01A1 0xC008=0 banks=(1,130)
6940: run=265 pc=0x04E4 0xC008=3 banks=(1,130)
6941: run=265 pc=0x04E4 0xC008=3 banks=(1,130)
```

### Registro 7021: run=278 pc=0x04E4 0xC008=1 banks=(149,130)

```text
7019: run=278 pc=0x04E4 0xC008=3 banks=(1,130)
7020: run=278 pc=0x8B93 0xDD32=0 banks=(149,130)
7021: run=278 pc=0x04E4 0xC008=1 banks=(149,130)
7022: run=285 pc=0x40F5 0xC008=2 banks=(149,12)
7023: run=285 pc=0x40FA 0xC203=1 banks=(149,12)
```

### Registro 7022: run=285 pc=0x40F5 0xC008=2 banks=(149,12)

```text
7020: run=278 pc=0x8B93 0xDD32=0 banks=(149,130)
7021: run=278 pc=0x04E4 0xC008=1 banks=(149,130)
7022: run=285 pc=0x40F5 0xC008=2 banks=(149,12)
7023: run=285 pc=0x40FA 0xC203=1 banks=(149,12)
7024: run=285 pc=0x4073 0xC008=2 banks=(149,12)
```

### Registro 23465: run=527 pc=0x01A1 0xC008=0 banks=(149,130) (2 ocorrências com a mesma assinatura)

```text
23463: run=527 pc=0x8B71 0xDD05=0 banks=(149,130)
23464: run=527 pc=0x8090 0xDE17=0 banks=(149,130)
23465: run=527 pc=0x01A1 0xC008=0 banks=(149,130)
23466: run=531 pc=0x412A 0xC008=2 banks=(149,19)
23467: run=531 pc=0x412D 0xC203=2 banks=(149,19)
```

### Registro 23466: run=531 pc=0x412A 0xC008=2 banks=(149,19)

```text
23464: run=527 pc=0x8090 0xDE17=0 banks=(149,130)
23465: run=527 pc=0x01A1 0xC008=0 banks=(149,130)
23466: run=531 pc=0x412A 0xC008=2 banks=(149,19)
23467: run=531 pc=0x412D 0xC203=2 banks=(149,19)
23468: run=531 pc=0x4073 0xC008=2 banks=(149,22)
```

### Registro 40947: run=789 pc=0x04E4 0xC008=3 banks=(149,22) (19 ocorrências com a mesma assinatura)

```text
40945: run=789 pc=0x8C9F 0xDDB7=192 banks=(149,130)
40946: run=789 pc=0x01A1 0xC008=0 banks=(149,130)
40947: run=789 pc=0x04E4 0xC008=3 banks=(149,22)
40948: run=789 pc=0x04E4 0xC008=3 banks=(149,22)
40949: run=789 pc=0x04E4 0xC008=3 banks=(149,22)
```

### Registro 40967: run=789 pc=0x403A 0xC008=2 banks=(149,22)

```text
40965: run=789 pc=0x04E4 0xC008=3 banks=(149,22)
40966: run=789 pc=0x4159 0xC200=0 banks=(149,22)
40967: run=789 pc=0x403A 0xC008=2 banks=(149,22)
40968: run=789 pc=0x403F 0xC203=1 banks=(149,22)
40969: run=789 pc=0x406F 0xC203=1 banks=(149,22)
```

### Registro 1: run=1 pc=0x00AD 0xC203=0 banks=(1,130)

```text
0: run=1 pc=0x00AD 0xC008=0 banks=(1,130)
1: run=1 pc=0x00AD 0xC203=0 banks=(1,130)
2: run=1 pc=0x00AD 0xC20B=0 banks=(1,130)
3: run=1 pc=0x00AD 0xC22B=0 banks=(1,130)
```

### Registro 255: run=44 pc=0x4939 0xC203=0 banks=(1,130)

```text
253: run=44 pc=0x04E4 0xC008=3 banks=(1,130)
254: run=44 pc=0x492C 0xC021=5 banks=(1,130)
255: run=44 pc=0x4939 0xC203=0 banks=(1,130)
256: run=44 pc=0x4939 0xC21F=0 banks=(1,130)
257: run=44 pc=0x4939 0xC23F=0 banks=(1,130)
```

### Registro 6961: run=265 pc=0x4496 0xC203=0 banks=(1,130)

```text
6959: run=265 pc=0x04E4 0xC008=3 banks=(1,130)
6960: run=265 pc=0x00E5 0xFFFE=1 banks=(1,130)
6961: run=265 pc=0x4496 0xC203=0 banks=(1,130)
6962: run=265 pc=0x4496 0xC21A=0 banks=(1,130)
6963: run=265 pc=0x4496 0xC23A=0 banks=(1,130)
```

### Registro 7023: run=285 pc=0x40FA 0xC203=1 banks=(149,12)

```text
7021: run=278 pc=0x04E4 0xC008=1 banks=(149,130)
7022: run=285 pc=0x40F5 0xC008=2 banks=(149,12)
7023: run=285 pc=0x40FA 0xC203=1 banks=(149,12)
7024: run=285 pc=0x4073 0xC008=2 banks=(149,12)
7025: run=285 pc=0x4073 0xC008=2 banks=(149,12)
```

### Registro 23461: run=527 pc=0x432F 0xC203=0 banks=(149,12)

```text
23459: run=526 pc=0x406C ?=? banks=(149,12)
23460: run=526 pc=0x0038 ?=? banks=(149,12)
23461: run=527 pc=0x432F 0xC203=0 banks=(149,12)
23462: run=527 pc=0x0577 0x00DC=255 banks=(149,12)
23463: run=527 pc=0x8B71 0xDD05=0 banks=(149,130)
```

### Registro 23467: run=531 pc=0x412D 0xC203=2 banks=(149,19)

```text
23465: run=527 pc=0x01A1 0xC008=0 banks=(149,130)
23466: run=531 pc=0x412A 0xC008=2 banks=(149,19)
23467: run=531 pc=0x412D 0xC203=2 banks=(149,19)
23468: run=531 pc=0x4073 0xC008=2 banks=(149,22)
23469: run=531 pc=0x4073 0xC008=2 banks=(149,22)
```

### Registro 40940: run=789 pc=0x4352 0xC203=0 banks=(149,22)

```text
40938: run=788 pc=0x4073 ?=? banks=(149,22)
40939: run=788 pc=0x0038 ?=? banks=(149,22)
40940: run=789 pc=0x4352 0xC203=0 banks=(149,22)
40941: run=789 pc=0x0577 0x00DC=255 banks=(149,22)
40942: run=789 pc=0x8B81 0xDD0C=0 banks=(149,130)
```

### Registro 40968: run=789 pc=0x403F 0xC203=1 banks=(149,22)

```text
40966: run=789 pc=0x4159 0xC200=0 banks=(149,22)
40967: run=789 pc=0x403A 0xC008=2 banks=(149,22)
40968: run=789 pc=0x403F 0xC203=1 banks=(149,22)
40969: run=789 pc=0x406F 0xC203=1 banks=(149,22)
40970: run=789 pc=0x406F 0xC203=1 banks=(149,22)
```

## Interpretação operacional

Use este relatório para correlacionar os escritores dinâmicos com as rotinas paginadas e os bancos ativos. Um flag constante ou uma escrita repetida não deve ser tratado como conclusão de carregamento sem confirmar a rotina consumidora e a progressão normal do jogo.
