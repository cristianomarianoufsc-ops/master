# Cadeia de despacho das rotinas paginadas

A referência `call 04BBDh` no banco 21 não aponta para um decodificador de bytes. No banco 1, o endereço lógico `0x4BBD` contém `JP 3954h`; portanto, ele funciona como um trampoline para o banco fixo.

No banco fixo, `l3954h` executa:

```asm
ld a,(ix+018h)
rst 10h
jp (hl)
```

Assim, o comportamento real depende do estado do objeto em `(IX+0x18)`, que seleciona uma entrada por meio do dispatcher `RST 10h` e salta para o handler retornado em HL. A mesma arquitetura explica os calls paginados `5C16`, `5C02` e `5C21`: eles fazem parte do sistema de estados/objetos, e não são funções puras de conversão de ponteiros.

Consequência para a tradução: a extração de diálogos não pode ser concluída apenas seguindo constantes de ROM. É necessário reconstruir o estado que preenche IX e observar qual handler estabelece `C223/C238` antes de entrar no loop de glifos `0x96CA–0x9779`. A próxima ferramenta recomendada é um resolvedor de dispatch que combine `(IX+0x18)`, entradas do `RST 10h` e endereços de handlers.
