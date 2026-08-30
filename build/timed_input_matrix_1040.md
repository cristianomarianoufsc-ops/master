# Matriz de entrada temporizada após o ciclo de cena

A ferramenta `tools/run_input_matrix.py` foi executada com `press_start=1040`, `press_runs=30` e oito máscaras de controle, até 1800 blocos por caso.

As leituras de controle ocorreram somente nos blocos 265 e 527, ambas com valor `0xFF`; nenhum dos pulsos aplicados a partir do bloco 1040 foi amostrado. As máscaras `0xFE`, `0xFD`, `0xFB`, `0xF7`, `0xBF` e `0x7F` terminaram em `0x3536` com `FFFF=0x84`; `0xEF` e `0xDF` terminaram em `0x406F` com `FFFF=0x16`.

Conclusão: pulsos tardios não são uma forma válida de provocar a transição de cena no capturador atual, pois o jogo não consulta as portas nessa janela. A janela causal conhecida permanece no início, especialmente em torno do bloco 265. Todos os caminhos continuam sem alcançar `0x4A8D` e não constituem snapshot válido.
