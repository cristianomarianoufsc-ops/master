# Auditoria das ferramentas Python do projeto do Zed

## Resultado

O pacote contém vários scripts de extração e injeção. Nenhum foi copiado diretamente para o projeto principal porque os scripts de injeção assumem texto em Shift-JIS/ASCII e ponteiros lineares, enquanto a análise atual confirmou que o jogo usa códigos de glifo, bytecode e bancos paginados.

## Ferramentas aproveitáveis conceitualmente

`extract_japanese_text.py` contém validadores genéricos de sequências Shift-JIS e ASCII. Eles podem ser usados apenas como triagem de dados, não como decodificador definitivo: o formato de texto do jogo não está comprovado como Shift-JIS.

`extrair_textos_ponteiros.py` e `extrair_textos_limpos.py` implementam a ideia de agrupar ponteiros e remover duplicatas. A ideia foi substituída por `tools/extract_dialog_streams.py`, que respeita bancos SMS, termina em `FF` e classifica bytecode/estrutura antes de considerar texto.

`injetar_traducao_v2.py` contém uma rotina potencialmente útil para validação do checksum SMS, mas seu injetor é inseguro neste estágio: procura texto em toda a ROM, atualiza ponteiros em faixas amplas, usa Shift-JIS e pode alterar dados que apenas parecem ponteiros. A função de checksum será reimplementada isoladamente quando houver uma ROM traduzida validada.

`criar_template_traducao.py`, `filtrar_strings.py` e `traduzir_dialogos.py` podem ajudar na organização de glossário depois que o mapa de streams estiver confirmado. Os templates existentes, incluindo `traducao_manual.txt`, contêm tentativas preliminares como `004739: INICIAR`, mas não constituem um mapa validado de offsets e não devem ser aplicados automaticamente.

## Artefatos encontrados

O projeto do Zed possui listagens de strings, templates e tentativas de tradução, mas vários resultados exibem caracteres corrompidos quando tratados como Shift-JIS. Isso reforça a conclusão do projeto atual: primeiro mapear o código de glifo e os handlers `C223/C238`; somente depois preparar o injetor e a cópia traduzida.

## Decisão

Nenhuma ROM, emulador, objeto compilado ou script de injeção foi incorporado. As ferramentas novas do projeto principal continuam sendo mais adequadas porque registram bancos, terminadores, bytecode e evidência dinâmica. O pacote do Zed serviu para confirmar hipóteses e apontar material de glossário, mas não contém uma ferramenta pronta que possa gerar com segurança a ROM PT-BR.
