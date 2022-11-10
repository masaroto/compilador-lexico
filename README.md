# Analisador Sintático

Autores:

Felipe Diniz Tomás								RA: 110752  
Gabriel Ossamu Maeda							RA: 108332  
Gustavo Rodrigues Wanke						    RA: 91671  
Pedro Henrique Landins							RA: 103572  

## Introdução

O analisador sintático funciona recebendo tokens criados pelo analisador léxico, processando-os de acordo com as regras gramaticais definidas na linguagem. Assim, o analisador pode ou não uma reconhecer uma entrada, que caso válida, será gerado uma <a href="https://en.wikipedia.org/wiki/Abstract_syntax_tree">Árvore Sintática</a> (Abstract Syntax Tree) contendo os tokens analisados.

### Regras da gramática

Foi considerado as seguintes regras da gramática de acordo com a especificação do trabalho, escrito na forma <a href="https://en.wikipedia.org/wiki/Extended_Backus%E2%80%93Naur_form">EBFN</a> :

    EX ::= EXS ( RE EXS)?
    RE ::= '=' | '<>' | '<' | '<=' | '>=' | '>'
    EXS ::= ('+' | '-')? T ( ( '+' | '-') T )*
    T ::= F ( ( '*' | '/' ) F )*
    F ::= V | N | '(' EX ')'
    V ::= ID
    ID ::= L ( ( L | D ) )*
    N ::= D D*
    D ::= '[0-9]+'
    L ::= '[A-Za-z][A-Za-z0-9_+]*'

## Funcionamento

A implementação do analisador sintático foi feita em python. Primeiramente o programa irá ler um arquivo contendo o código fonte da linguagem. O analisador léxico irá processar o conteúdo escrito no arquivo e irá criar um vetor com todos os tokens encontrados, sendo exibido na tela na respectiva ordem. Após isso o fluxo de tokens será analisado pelo analisador sintático (```class Parser```), verificando se a entrada esta de acordo com a gramática, assim será gerado árvore sintática e exibido na tela.

### Input

A entrada deve ser um arquivo de extensão ilp (<Nome_Arquivo>.ilp) e obrigatoriamente deve estar na raiz da pasta exemplos. Um exemplo de arquivo de entrada seria:

    46464 * dasdasd45 / 44564

### Output
 
A saída irá imprimir o código fonte, o fluxo de tokens e o resultado da análise sintática.
Nesse caso, a análise sintática será:

    ================== Análise Sintática ===================

    Entrada valida

    === Abstract Syntax Tree ===

    Expressao : Filhos ['Expressao_Simples']
    Expressao_Simples : Filhos ['termo']
    termo : Filhos ['Fator']
    Fator : Filhos ['Numero']
    Numero : Filhos ['46464']
    termo : Filhos ['Fator', '*']
    termo : Filhos ['Fator', '*', 'Fator']
    Fator : Filhos ['variavel']
    variavel : Filhos ['identificador']
    identificador : Filhos ['dasdasd45']
    termo : Filhos ['Fator', '*', 'Fator', '/']
    termo : Filhos ['Fator', '*', 'Fator', '/', 'Fator']
    Fator : Filhos ['Numero']
    Numero : Filhos ['44564']    

A impressão da árvore funciona imprimindo sempre mais a esquerda até encontrar um terminal, assim alguns não terminais
aparecem duplicados, de forma mais clara, esta árvore está assim:

```
Expressao
└── Expressao Simples
    └── Termo
        ├── Fator
        │   └── Numero
        │       └── 44564
        ├── /
        ├── Fator
        │   └── Variavel
        │       └── Identificador
        │           └── dasdasd45 
        ├── *
        └── Fator
            └── Numero
                └── 46464
```
