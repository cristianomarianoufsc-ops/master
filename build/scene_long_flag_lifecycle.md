# Ciclo de vida dos flags de carregamento de cena

Fonte: `/tmp/scene-long.json`

## Resumo

- Registros de trace: 123215
- Escritas de `C008`: 6249
- Escritas de `C203`: 16

## Escritas de `0xC008`

| Ocorrências | Índices | Blocos | PC | Valor | FFFE | FFFF |
|---:|---|---|---|---:|---:|---:|
| 1 | 0 | 1 | 0x00AD | 0 | 1 | 130 |
| 3 | 6–6939 | 41–267 | 0x04E4 | 1 | 1 | 130 |
| 1 | 7 | 42 | 0x04E4 | 128 | 1 | 130 |
| 6191 | 8–6983 | 42–278 | 0x04E4 | 3 | 1 | 130 |
| 19 | 246–264 | 52 | 0x04E4 | 3 | 1 | 140 |
| 1 | 6914 | 265 | 0x01A1 | 0 | 1 | 130 |
| 1 | 6984 | 278 | 0x04E4 | 1 | 149 | 130 |
| 1 | 6985 | 285 | 0x40F5 | 2 | 149 | 12 |
| 6 | 23426–112076 | 527–1837 | 0x01A1 | 0 | 149 | 130 |
| 1 | 23427 | 531 | 0x412A | 2 | 149 | 19 |
| 19 | 40904–40922 | 789 | 0x04E4 | 3 | 149 | 22 |
| 1 | 40924 | 789 | 0x403A | 2 | 149 | 22 |
| 2 | 58679–94278 | 1051–1575 | 0x4065 | 2 | 149 | 130 |
| 2 | 76478–112078 | 1313–1837 | 0x403A | 2 | 149 | 130 |

## Escritas de `0xC203`

| Ocorrências | Índices | Blocos | PC | Valor | FFFE | FFFF |
|---:|---|---|---|---:|---:|---:|
| 1 | 1 | 1 | 0x00AD | 0 | 1 | 130 |
| 1 | 242 | 44 | 0x4939 | 0 | 1 | 130 |
| 1 | 6936 | 265 | 0x4496 | 0 | 1 | 130 |
| 1 | 6986 | 285 | 0x40FA | 1 | 149 | 12 |
| 1 | 23424 | 527 | 0x432F | 0 | 149 | 12 |
| 1 | 23428 | 531 | 0x412D | 2 | 149 | 19 |
| 1 | 40901 | 789 | 0x4352 | 0 | 149 | 22 |
| 1 | 40925 | 789 | 0x403F | 1 | 149 | 22 |
| 1 | 58676 | 1051 | 0x432F | 0 | 149 | 22 |
| 2 | 58680–94279 | 1051–1575 | 0x406A | 2 | 149 | 130 |
| 2 | 76475–112074 | 1313–1837 | 0x4352 | 0 | 149 | 130 |
| 2 | 76479–112079 | 1313–1837 | 0x403F | 1 | 149 | 130 |
| 1 | 94275 | 1575 | 0x432F | 0 | 149 | 130 |

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

## Janelas locais das escritas

As janelas abaixo são contexto do trace, não prova de causalidade.

### Registro 0: run=1 pc=0x00AD 0xC008=0 banks=(1,130)

```text
0: run=1 pc=0x00AD 0xC008=0 banks=(1,130)
1: run=1 pc=0x00AD 0xC203=0 banks=(1,130)
2: run=1 pc=0x00AD 0xC20B=0 banks=(1,130)
3: run=1 pc=0x00AD 0xC22B=0 banks=(1,130)
```

### Registro 6: run=41 pc=0x04E4 0xC008=1 banks=(1,130) (3 ocorrências com a mesma assinatura)

```text
3: run=1 pc=0x00AD 0xC22B=0 banks=(1,130)
4: run=1 pc=0x00AD 0xC24B=0 banks=(1,130)
5: run=2 pc=0x0545 ?=0 banks=(1,130)
6: run=41 pc=0x04E4 0xC008=1 banks=(1,130)
7: run=42 pc=0x04E4 0xC008=128 banks=(1,130)
8: run=42 pc=0x04E4 0xC008=3 banks=(1,130)
9: run=42 pc=0x04E4 0xC008=3 banks=(1,130)
```

### Registro 7: run=42 pc=0x04E4 0xC008=128 banks=(1,130)

```text
4: run=1 pc=0x00AD 0xC24B=0 banks=(1,130)
5: run=2 pc=0x0545 ?=0 banks=(1,130)
6: run=41 pc=0x04E4 0xC008=1 banks=(1,130)
7: run=42 pc=0x04E4 0xC008=128 banks=(1,130)
8: run=42 pc=0x04E4 0xC008=3 banks=(1,130)
9: run=42 pc=0x04E4 0xC008=3 banks=(1,130)
10: run=42 pc=0x04E4 0xC008=3 banks=(1,130)
```

### Registro 8: run=42 pc=0x04E4 0xC008=3 banks=(1,130) (6191 ocorrências com a mesma assinatura)

```text
5: run=2 pc=0x0545 ?=0 banks=(1,130)
6: run=41 pc=0x04E4 0xC008=1 banks=(1,130)
7: run=42 pc=0x04E4 0xC008=128 banks=(1,130)
8: run=42 pc=0x04E4 0xC008=3 banks=(1,130)
9: run=42 pc=0x04E4 0xC008=3 banks=(1,130)
10: run=42 pc=0x04E4 0xC008=3 banks=(1,130)
11: run=42 pc=0x04E4 0xC008=3 banks=(1,130)
```

### Registro 246: run=52 pc=0x04E4 0xC008=3 banks=(1,140) (19 ocorrências com a mesma assinatura)

```text
243: run=44 pc=0x4939 0xC219=0 banks=(1,130)
244: run=44 pc=0x4939 0xC239=0 banks=(1,130)
245: run=46 pc=0x04E4 0xC008=1 banks=(1,130)
246: run=52 pc=0x04E4 0xC008=3 banks=(1,140)
247: run=52 pc=0x04E4 0xC008=3 banks=(1,140)
248: run=52 pc=0x04E4 0xC008=3 banks=(1,140)
249: run=52 pc=0x04E4 0xC008=3 banks=(1,140)
```

### Registro 6914: run=265 pc=0x01A1 0xC008=0 banks=(1,130)

```text
6911: run=264 pc=0x3546 ?=? banks=(1,132)
6912: run=264 pc=0x0038 ?=? banks=(1,132)
6913: run=265 pc=0x055F 0x00DC=239 banks=(1,132)
6914: run=265 pc=0x01A1 0xC008=0 banks=(1,130)
6915: run=265 pc=0x04E4 0xC008=3 banks=(1,130)
6916: run=265 pc=0x04E4 0xC008=3 banks=(1,130)
6917: run=265 pc=0x04E4 0xC008=3 banks=(1,130)
```

### Registro 6984: run=278 pc=0x04E4 0xC008=1 banks=(149,130)

```text
6981: run=278 pc=0x04E4 0xC008=3 banks=(1,130)
6982: run=278 pc=0x04E4 0xC008=3 banks=(1,130)
6983: run=278 pc=0x04E4 0xC008=3 banks=(1,130)
6984: run=278 pc=0x04E4 0xC008=1 banks=(149,130)
6985: run=285 pc=0x40F5 0xC008=2 banks=(149,12)
6986: run=285 pc=0x40FA 0xC203=1 banks=(149,12)
6987: run=285 pc=0x4073 0xC008=2 banks=(149,12)
```

### Registro 6985: run=285 pc=0x40F5 0xC008=2 banks=(149,12)

```text
6982: run=278 pc=0x04E4 0xC008=3 banks=(1,130)
6983: run=278 pc=0x04E4 0xC008=3 banks=(1,130)
6984: run=278 pc=0x04E4 0xC008=1 banks=(149,130)
6985: run=285 pc=0x40F5 0xC008=2 banks=(149,12)
6986: run=285 pc=0x40FA 0xC203=1 banks=(149,12)
6987: run=285 pc=0x4073 0xC008=2 banks=(149,12)
6988: run=285 pc=0x4073 0xC008=2 banks=(149,12)
```

### Registro 23426: run=527 pc=0x01A1 0xC008=0 banks=(149,130) (6 ocorrências com a mesma assinatura)

```text
23423: run=526 pc=0x0038 ?=? banks=(149,12)
23424: run=527 pc=0x432F 0xC203=0 banks=(149,12)
23425: run=527 pc=0x0577 0x00DC=255 banks=(149,12)
23426: run=527 pc=0x01A1 0xC008=0 banks=(149,130)
23427: run=531 pc=0x412A 0xC008=2 banks=(149,19)
23428: run=531 pc=0x412D 0xC203=2 banks=(149,19)
23429: run=531 pc=0x4146 0xC206=128 banks=(149,22)
```

### Registro 23427: run=531 pc=0x412A 0xC008=2 banks=(149,19)

```text
23424: run=527 pc=0x432F 0xC203=0 banks=(149,12)
23425: run=527 pc=0x0577 0x00DC=255 banks=(149,12)
23426: run=527 pc=0x01A1 0xC008=0 banks=(149,130)
23427: run=531 pc=0x412A 0xC008=2 banks=(149,19)
23428: run=531 pc=0x412D 0xC203=2 banks=(149,19)
23429: run=531 pc=0x4146 0xC206=128 banks=(149,22)
23430: run=531 pc=0x406F 0xC203=2 banks=(149,22)
```

### Registro 40904: run=789 pc=0x04E4 0xC008=3 banks=(149,22) (19 ocorrências com a mesma assinatura)

```text
40901: run=789 pc=0x4352 0xC203=0 banks=(149,22)
40902: run=789 pc=0x0577 0x00DC=255 banks=(149,22)
40903: run=789 pc=0x01A1 0xC008=0 banks=(149,130)
40904: run=789 pc=0x04E4 0xC008=3 banks=(149,22)
40905: run=789 pc=0x04E4 0xC008=3 banks=(149,22)
40906: run=789 pc=0x04E4 0xC008=3 banks=(149,22)
40907: run=789 pc=0x04E4 0xC008=3 banks=(149,22)
```

### Registro 40924: run=789 pc=0x403A 0xC008=2 banks=(149,22)

```text
40921: run=789 pc=0x04E4 0xC008=3 banks=(149,22)
40922: run=789 pc=0x04E4 0xC008=3 banks=(149,22)
40923: run=789 pc=0x4015 0xC200=16 banks=(149,22)
40924: run=789 pc=0x403A 0xC008=2 banks=(149,22)
40925: run=789 pc=0x403F 0xC203=1 banks=(149,22)
40926: run=789 pc=0x4073 0xC008=2 banks=(149,22)
40927: run=789 pc=0x4073 0xC008=2 banks=(149,22)
```

### Registro 58679: run=1051 pc=0x4065 0xC008=2 banks=(149,130) (2 ocorrências com a mesma assinatura)

```text
58676: run=1051 pc=0x432F 0xC203=0 banks=(149,22)
58677: run=1051 pc=0x0577 0x00DC=255 banks=(149,22)
58678: run=1051 pc=0x01A1 0xC008=0 banks=(149,130)
58679: run=1051 pc=0x4065 0xC008=2 banks=(149,130)
58680: run=1051 pc=0x406A 0xC203=2 banks=(149,130)
58681: run=1051 pc=0x4073 0xC008=2 banks=(149,130)
58682: run=1051 pc=0x4073 0xC008=2 banks=(149,130)
```

### Registro 76478: run=1313 pc=0x403A 0xC008=2 banks=(149,130) (2 ocorrências com a mesma assinatura)

```text
76475: run=1313 pc=0x4352 0xC203=0 banks=(149,130)
76476: run=1313 pc=0x0577 0x00DC=255 banks=(149,130)
76477: run=1313 pc=0x01A1 0xC008=0 banks=(149,130)
76478: run=1313 pc=0x403A 0xC008=2 banks=(149,130)
76479: run=1313 pc=0x403F 0xC203=1 banks=(149,130)
76480: run=1313 pc=0x406F 0xC203=1 banks=(149,130)
76481: run=1313 pc=0x406F 0xC203=1 banks=(149,130)
```

### Registro 1: run=1 pc=0x00AD 0xC203=0 banks=(1,130)

```text
0: run=1 pc=0x00AD 0xC008=0 banks=(1,130)
1: run=1 pc=0x00AD 0xC203=0 banks=(1,130)
2: run=1 pc=0x00AD 0xC20B=0 banks=(1,130)
3: run=1 pc=0x00AD 0xC22B=0 banks=(1,130)
4: run=1 pc=0x00AD 0xC24B=0 banks=(1,130)
```

### Registro 242: run=44 pc=0x4939 0xC203=0 banks=(1,130)

```text
239: run=44 pc=0x04E4 0xC008=3 banks=(1,130)
240: run=44 pc=0x04E4 0xC008=3 banks=(1,130)
241: run=44 pc=0x04E4 0xC008=3 banks=(1,130)
242: run=44 pc=0x4939 0xC203=0 banks=(1,130)
243: run=44 pc=0x4939 0xC219=0 banks=(1,130)
244: run=44 pc=0x4939 0xC239=0 banks=(1,130)
245: run=46 pc=0x04E4 0xC008=1 banks=(1,130)
```

### Registro 6936: run=265 pc=0x4496 0xC203=0 banks=(1,130)

```text
6933: run=265 pc=0x04E4 0xC008=3 banks=(1,130)
6934: run=265 pc=0x04E4 0xC008=3 banks=(1,130)
6935: run=265 pc=0x00E5 0xFFFE=1 banks=(1,130)
6936: run=265 pc=0x4496 0xC203=0 banks=(1,130)
6937: run=265 pc=0x4496 0xC21A=0 banks=(1,130)
6938: run=265 pc=0x4496 0xC23A=0 banks=(1,130)
6939: run=267 pc=0x04E4 0xC008=1 banks=(1,130)
```

### Registro 6986: run=285 pc=0x40FA 0xC203=1 banks=(149,12)

```text
6983: run=278 pc=0x04E4 0xC008=3 banks=(1,130)
6984: run=278 pc=0x04E4 0xC008=1 banks=(149,130)
6985: run=285 pc=0x40F5 0xC008=2 banks=(149,12)
6986: run=285 pc=0x40FA 0xC203=1 banks=(149,12)
6987: run=285 pc=0x4073 0xC008=2 banks=(149,12)
6988: run=285 pc=0x4073 0xC008=2 banks=(149,12)
6989: run=285 pc=0x4073 0xC008=2 banks=(149,12)
```

### Registro 23424: run=527 pc=0x432F 0xC203=0 banks=(149,12)

```text
23421: run=526 pc=0x406C ?=162 banks=(149,12)
23422: run=526 pc=0x406C ?=? banks=(149,12)
23423: run=526 pc=0x0038 ?=? banks=(149,12)
23424: run=527 pc=0x432F 0xC203=0 banks=(149,12)
23425: run=527 pc=0x0577 0x00DC=255 banks=(149,12)
23426: run=527 pc=0x01A1 0xC008=0 banks=(149,130)
23427: run=531 pc=0x412A 0xC008=2 banks=(149,19)
```

### Registro 23428: run=531 pc=0x412D 0xC203=2 banks=(149,19)

```text
23425: run=527 pc=0x0577 0x00DC=255 banks=(149,12)
23426: run=527 pc=0x01A1 0xC008=0 banks=(149,130)
23427: run=531 pc=0x412A 0xC008=2 banks=(149,19)
23428: run=531 pc=0x412D 0xC203=2 banks=(149,19)
23429: run=531 pc=0x4146 0xC206=128 banks=(149,22)
23430: run=531 pc=0x406F 0xC203=2 banks=(149,22)
23431: run=531 pc=0x406F 0xC203=2 banks=(149,22)
```

### Registro 40901: run=789 pc=0x4352 0xC203=0 banks=(149,22)

```text
40898: run=788 pc=0x4073 ?=162 banks=(149,22)
40899: run=788 pc=0x4073 ?=? banks=(149,22)
40900: run=788 pc=0x0038 ?=? banks=(149,22)
40901: run=789 pc=0x4352 0xC203=0 banks=(149,22)
40902: run=789 pc=0x0577 0x00DC=255 banks=(149,22)
40903: run=789 pc=0x01A1 0xC008=0 banks=(149,130)
40904: run=789 pc=0x04E4 0xC008=3 banks=(149,22)
```

### Registro 40925: run=789 pc=0x403F 0xC203=1 banks=(149,22)

```text
40922: run=789 pc=0x04E4 0xC008=3 banks=(149,22)
40923: run=789 pc=0x4015 0xC200=16 banks=(149,22)
40924: run=789 pc=0x403A 0xC008=2 banks=(149,22)
40925: run=789 pc=0x403F 0xC203=1 banks=(149,22)
40926: run=789 pc=0x4073 0xC008=2 banks=(149,22)
40927: run=789 pc=0x4073 0xC008=2 banks=(149,22)
40928: run=789 pc=0x4073 0xC008=2 banks=(149,22)
```

### Registro 58676: run=1051 pc=0x432F 0xC203=0 banks=(149,22)

```text
58673: run=1050 pc=0x406C ?=226 banks=(149,22)
58674: run=1050 pc=0x406C ?=? banks=(149,22)
58675: run=1050 pc=0x0038 ?=? banks=(149,22)
58676: run=1051 pc=0x432F 0xC203=0 banks=(149,22)
58677: run=1051 pc=0x0577 0x00DC=255 banks=(149,22)
58678: run=1051 pc=0x01A1 0xC008=0 banks=(149,130)
58679: run=1051 pc=0x4065 0xC008=2 banks=(149,130)
```

### Registro 58680: run=1051 pc=0x406A 0xC203=2 banks=(149,130) (2 ocorrências com a mesma assinatura)

```text
58677: run=1051 pc=0x0577 0x00DC=255 banks=(149,22)
58678: run=1051 pc=0x01A1 0xC008=0 banks=(149,130)
58679: run=1051 pc=0x4065 0xC008=2 banks=(149,130)
58680: run=1051 pc=0x406A 0xC203=2 banks=(149,130)
58681: run=1051 pc=0x4073 0xC008=2 banks=(149,130)
58682: run=1051 pc=0x4073 0xC008=2 banks=(149,130)
58683: run=1051 pc=0x4073 0xC008=2 banks=(149,130)
```

### Registro 76475: run=1313 pc=0x4352 0xC203=0 banks=(149,130) (2 ocorrências com a mesma assinatura)

```text
76472: run=1312 pc=0x406C ?=226 banks=(149,130)
76473: run=1312 pc=0x406C ?=? banks=(149,130)
76474: run=1312 pc=0x0038 ?=? banks=(149,130)
76475: run=1313 pc=0x4352 0xC203=0 banks=(149,130)
76476: run=1313 pc=0x0577 0x00DC=255 banks=(149,130)
76477: run=1313 pc=0x01A1 0xC008=0 banks=(149,130)
76478: run=1313 pc=0x403A 0xC008=2 banks=(149,130)
```

### Registro 76479: run=1313 pc=0x403F 0xC203=1 banks=(149,130) (2 ocorrências com a mesma assinatura)

```text
76476: run=1313 pc=0x0577 0x00DC=255 banks=(149,130)
76477: run=1313 pc=0x01A1 0xC008=0 banks=(149,130)
76478: run=1313 pc=0x403A 0xC008=2 banks=(149,130)
76479: run=1313 pc=0x403F 0xC203=1 banks=(149,130)
76480: run=1313 pc=0x406F 0xC203=1 banks=(149,130)
76481: run=1313 pc=0x406F 0xC203=1 banks=(149,130)
76482: run=1313 pc=0x406F 0xC203=1 banks=(149,130)
```

### Registro 94275: run=1575 pc=0x432F 0xC203=0 banks=(149,130)

```text
94272: run=1574 pc=0x406F ?=226 banks=(149,130)
94273: run=1574 pc=0x406F ?=? banks=(149,130)
94274: run=1574 pc=0x0038 ?=? banks=(149,130)
94275: run=1575 pc=0x432F 0xC203=0 banks=(149,130)
94276: run=1575 pc=0x0577 0x00DC=255 banks=(149,130)
94277: run=1575 pc=0x01A1 0xC008=0 banks=(149,130)
94278: run=1575 pc=0x4065 0xC008=2 banks=(149,130)
```

## Interpretação operacional

Use este relatório para correlacionar os escritores dinâmicos com as rotinas paginadas e os bancos ativos. Um flag constante ou uma escrita repetida não deve ser tratado como conclusão de carregamento sem confirmar a rotina consumidora e a progressão normal do jogo.
