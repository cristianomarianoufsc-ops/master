# Matriz da janela causal de controle

A matriz foi executada com a semântica ativa-baixa compatível com o Dega, mantendo `0x00` até o bloco 239, aplicando cada máscara interna nos blocos 240–299 e mantendo `0x00` depois.

Todas as sete máscaras testadas (`0x01`, `0x02`, `0x04`, `0x08`, `0x10`, `0x20`, `0x00`) terminaram no loop `0x406C` com `FFFF=0x16`. As seis primeiras produziram leituras no bloco 265 correspondentes à conversão ativa-baixa (`0xFE`, `0xFD`, `0xFB`, `0xF7`, `0xEF`, `0xDF`); a máscara `0x00` produziu `0xFF`. Nos casos até `0x08`, houve nova leitura no bloco 527 com `0xC0`; para `0x10` e `0x20`, somente uma IRQ foi observada e não houve segunda leitura registrada.

Conclusão: a janela de entrada está sendo amostrada corretamente e altera o estado de controle/IRQ, mas nenhuma máscara testada provoca a transição ao breakpoint `0x4A8D`. A matriz não é evidência de diálogo nem de `C280` válido.
