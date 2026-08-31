# Mapa de glifos após a transformação 05B3E

A ferramenta existente `tools/transform_lad0c_05b3e.py`, revisada no projeto do Zed e já mantida no repositório principal, foi executada nas duas ROMs com banco físico 13, origem CPU `AD0C`, stride de `0x10` e 64 glifos.

A transformação produziu 8192 bytes em cada caso. Os hashes SHA-256 foram idênticos:

```text
ee4b13597f6f23eb3dfd3bb462c95d5ef1c79c170cbd55b2b3a564351b9a872a
```

Isso confirma que a fonte/grupo de glifos usado por essa etapa é compartilhado entre as versões japonesa e americana. Portanto, a regionalização está nos dados de códigos/streams e não nos glifos básicos dessa região. Alterar a fonte não é necessário para escrever PT-BR com os caracteres já disponíveis; o trabalho principal é mapear o código aceito por `C280` para cada glifo.

Foram gerados mapas visuais de 64 glifos em formato 8x16:

- `build/japan_glyph_map_05b3e.png`
- `build/usa_glyph_map_05b3e.png`

Os PNGs têm 256×128 pixels e devem ser tratados como referência visual do índice de glifo, não como prova de que todos os 64 códigos correspondem a letras. A igualdade byte a byte das duas saídas é a evidência mais forte desta etapa.

## Próximo passo técnico

Construir uma tabela `código do stream → índice de glifo → representação visual`, usando os valores não nulos de `C280` e os bytes aceitos pelo loop `0x96CA–0x9719`. Depois, cruzar essa tabela com os streams finais obtidos em runtime. Só após esse cruzamento será possível criar um alfabeto PT-BR seguro e o primeiro patch de teste.
