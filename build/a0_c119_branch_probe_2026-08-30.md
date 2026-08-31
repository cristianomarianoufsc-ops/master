# Branch paginado após a limpeza A0 — 2026-08-30

## Captura

Foi executado um trace focalizado em `0x4558–0x4578`, com rastreamento automático de toda memória nessa faixa. A entrada foi `0xFF` até o bloco 260 e `0x10` por 30 blocos, sem desbloqueios sintéticos.

## Sequência observada

No bloco 277, o caminho paginado chega a `0x4569` com `A=0x82`, `F=0x10`, `DE=0x0003`, `HL=0x4547` e `FFFE=0x01`, `FFFF=0x82`. Depois do `CALL 0x8B62`, o retorno ocorre em `0x456C` com `A=0`, `F=0x20` e `C119=0x01`.

A sequência efetiva é:

```asm
456C  LD   A,(C119h) ; A = 01h
456F  CP   04h       ; comparação não igual; F = 93h no trace
4571  JR   Z,4592h   ; não tomado
4573  LD   A,05h
4575  LD   (C119h),A ; C119 = 05h
4578  LD   (C0A0h),A ; C0A0 = 05h
457B  LD   A,01h
457D  LD   (C11Dh),A ; C11D = 01h
4580  LD   HL,46C0h
4583  LD   DE,C0E0h
4586  LD   BC,0020h
4589  LDIR
```

Antes da chamada, `C119` foi escrito como `1` no bloco 277 por `0x4530`. O valor `1` não é residual acidental da pilha: é o valor explicitamente instalado pelo caminho anterior.

## Interpretação

O teste contra `4` não bloqueia o caminho nessa reprodução. Pelo contrário, a condição não igual seleciona a transição de estado para `5`, com atualização de `C0A0`, `C11D` e cópia de 32 bytes. Isso é uma mudança de estado concreta e potencialmente o primeiro passo de uma máquina de cenas, não uma desmontagem imediata da tarefa.

O trace anterior terminou em `0x4073` por limite de passos, portanto ainda não comprova que a cópia para `C0E0` leva ao diálogo. A hipótese de trabalho agora é que o gargalo está depois de `0x4589`, em quem consome `C0E0`, ou na diferença entre o estado `C119=5` e a condição especial `C119=4`.

O próximo passo deve seguir a execução depois de `0x4589`, registrar leituras de `C0A0`, `C11D`, `C0E0–C0FF` e localizar o próximo dispatcher ou renderizador. Nenhuma alteração de ROM deve ser feita ainda.
