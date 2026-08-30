# Correlação do comando 0x0C com a tarefa DD57

A captura no estado bloqueado (`FFFF=0x0C`) mostrou 415 eventos DDxx dentro do dispatcher e execução das rotinas de processamento, incluindo `0x83E7`, `0x855E`, `0x8786`, `0x8CA6` e `0x8CE2`. Portanto, o banco não está simplesmente ausente ou inacessível.

A diferença decisiva em relação ao caminho que progride é o slot `DD57`: no caminho bloqueado ele permanece `0`, enquanto no caminho progressivo recebe `0x80`. A rotina `0x83E7` usa o comando em `DD03`; para comandos na faixa de `0x90–0xBF`, o dispatcher seleciona uma tabela e prepara `DE=DD57` antes de copiar os dados da tarefa. Mesmo com o dispatcher executado, o pedido associado ao estado `FFFF=0x0C` não resulta em uma tarefa ativa em `DD57`.

O estado reproduzível continua sendo `0x406F` lendo `C203=1`. O próximo passo é comparar o valor de `DD03` e o índice usado por `sub_857C` nos caminhos `FFFF=0x0C` e `FFFF=0x16`, para descobrir se a diferença está no comando, na tabela de ponteiros ou nos dados da tarefa.
