# Reprodução local — 2026-08-30

## Escopo

A ROM fornecida pelo usuário foi instalada apenas em `input/KujakuOu_Japan.sms`, caminho ignorado pelo Git. O código-fonte do Dega 1.12 foi extraído somente para `/home/ubuntu/reference/dega-1.12/`; nenhum desses artefatos foi incluído no repositório.

## Validações executadas

Todos os scripts Python passaram por `python3 -m py_compile tools/*.py`. A captura foi executada com a semântica de I/O do Dega, agendamento de frame Dega, IRQ por scanline, pulso de controle na janela documentada (bloco 260 por 30 blocos), faixa de memória `DD00–DE37`, eventos forçados para `C008`, `C203`, `DD03` e `DD97`, e amostragem de trace a cada 32 eventos.

A execução terminou por limite de passos no PC `0x4070`, com `1100` blocos e `FFFF=0x82`; o breakpoint `0x4A8D` não foi alcançado. A auditoria retornou `status=risk`, com `BREAKPOINT_NOT_REACHED`, entrada variável e um loop dominante no PC `0x04E4`. Esse resultado não é snapshot válido e não deve ser usado para inferir `C280`.

## Observação do ciclo A0

O analisador de ciclo A0 foi aplicado à captura. Nesta configuração específica, foram registrados `11532` eventos selecionados; houve cinco escritas em `DD97`, com valores `0` e `4`, mas não foi registrada escrita no grupo `DDF7–DE16`. Isso não contradiz o relatório anterior `build/a0_task_lifecycle.md`: a configuração reproduzida aqui permaneceu em um caminho de boot diferente, terminando em `0x34D5` na captura direta e em `0x4070` no harness temporizado, e portanto não deve ser comparada como se fosse a mesma janela causal do experimento de 3500 blocos.

## Conclusão operacional

O ambiente está pronto para continuar a investigação sem publicar material proprietário. A próxima execução deve usar uma captura focalizada na janela já validada para o armamento A0, registrar `DD03`, `DD97`, `DDF7–DE16`, `DDB7` e o endereço de retorno antes de `0x8B81`, e só aceitar uma conclusão quando o auditor não identificar confusão entre loop, temporização e breakpoint.
