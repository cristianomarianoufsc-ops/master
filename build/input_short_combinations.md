# Combinações curtas na janela causal

Foram testadas as combinações internas `0x03`, `0x0C`, `0x10`, `0x20`, `0x30` e `0x3F` na janela de leitura do bloco 265, com durações de 1, 5 e 15 blocos, usando a conversão ativa-baixa do Dega.

Todos os casos terminaram em `0x4073` com `FFFF=0x82` (valor decimal 130), sem alcançar `0x4A8D`. As durações de 5 e 15 blocos produziram leituras posteriores no bloco 527 somente para `0x03` e `0x0C`; `0x10`, `0x20`, `0x30` e `0x3F` tiveram apenas a leitura inicial ou não alteraram o caminho final.

Conclusão: combinações curtas de botões na janela correta alteram a leitura e a cadência de IRQ, mas não provocam a transição para o diálogo. A causa continua sendo o estado da cena/dispatcher, não a ausência de entrada.
