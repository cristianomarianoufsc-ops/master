# Kujaku Ō — PT-BR Direct Translation Research

Este repositório documenta a engenharia reversa e o desenvolvimento de um patch direto em português brasileiro para a versão japonesa de *Kujaku Ō* no Sega Master System/Mark III. O objetivo é modificar os dados e o código internos da ROM original, preservando comandos, ponteiros, paginação de bancos e o sistema gráfico do jogo.

## Estado atual

O projeto já identificou a fonte comprimida em `0x3181D` no banco `0x8C`, a rotina de descompressão que envia dados para a VRAM em `0x6380`, o sistema de dois slots (`FFFE` para `0x4000–0x7FFF` e `FFFF` para `0x8000–0xBFFF`), o dispatcher `RST 10h`, a rotina `05C16` de resolução de ponteiros, `05C02` de resolução de listas e o loop de texto em `0x96CA–0x9779`.

Também foram criadas ferramentas para analisar bancos, streams, estados, bytecode de cena, tabelas `AC0B/AC31`, referências paginadas e os handlers que alimentam `C223/C238`. Os relatórios em `build/` são evidências de trabalho e devem ser lidos antes de alterar a ROM.

> **Importante:** ainda não existe uma ROM traduzida final. Não aplicar alterações destrutivas antes de validar o mapa de caracteres, a tabela `C280`, o formato da fonte e os ponteiros de cada diálogo.

## Como continuar

O próximo agente deve começar por `build/static_script_findings.md`, `build/dialogue_resolution_graph.md`, `build/dialog_handler_candidates.md` e `build/resolved_paged_refs.md`. Em seguida, deve validar a regra exata de `C280` reproduzindo `04CFD/04D16` com os valores de runtime, identificar os streams consumidos por `C223/C238`, montar um mapa de códigos para a fonte japonesa e somente então preparar a fonte latina e o patch.

As ferramentas são scripts Python independentes. O arquivo original da ROM deve ser colocado localmente, fora do Git, com o nome documentado nos próprios scripts ou passado como argumento. Capturas devem ser submetidas ao auditor de falsos positivos antes de serem aceitas como evidência; em loops de espera, `--trace-every N` reduz a saturação sem remover eventos forçados de IRQ, VBlank e controle. Exemplos:

```bash
python3 tools/dump_bank_addresses.py /caminho/kujaku_ou_jp_original.sms 6e33 6f47 --banks 0-31
python3 tools/resolve_paged_refs.py build/bank21.asm --register ffff
python3 tools/run_sms_capture.py /caminho/kujaku_ou_jp_original.sms --out /tmp/capture.json --scanline-irq --dega-frame-schedule --trace-every 32
python3 tools/audit_false_positives.py /tmp/capture.json
python3 tools/extract_dialog_pointer_tables.py /caminho/kujaku_ou_jp_original.sms --bank 22 --table af55 --out build/dialog_pointer_af55.md
```

## Política de arquivos

Este repositório publica código, documentação, relatórios e pequenos artefatos de análise criados pelo projeto. A ROM comercial original, cópias completas da ROM, dumps completos de bancos e qualquer ROM modificada não devem ser publicados. Quando o patch estiver pronto, a distribuição recomendada será um arquivo IPS ou BPS que o usuário aplique à sua própria cópia legítima.

## Regra de sincronização

Cada avanço técnico significativo deve atualizar esta documentação ou um relatório específico, registrar o estado e criar um commit. Depois, o commit deve ser enviado ao repositório remoto. A mensagem do commit deve indicar a etapa, por exemplo `docs: document dual-slot mapper` ou `feat: add dialogue pointer extractor`.

## Estrutura

| Diretório | Conteúdo |
|---|---|
| `tools/` | Extratores, analisadores e emuladores auxiliares |
| `build/` | Relatórios, disassemblies, dumps pequenos e imagens de diagnóstico |
| `docs/` | Notas permanentes para continuidade e decisões técnicas |
| `patch/` | Futuramente, apenas IPS/BPS e metadados do patch |
| `input/` | Diretório local ignorado para a ROM original |

## Aviso legal

O repositório não fornece a ROM original nem uma cópia completa modificada. O usuário é responsável por possuir e utilizar uma cópia legal do jogo e por respeitar a legislação aplicável.
