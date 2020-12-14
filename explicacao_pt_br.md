# 1. O lexer

# 2. O Parser

## 2.1 A gramatica da linguagem:

```
program ::= {statement}
statement ::= "PRINT" (expression | string) nl
    | "IF" comparison "THEN" nl {statement} "ENDIF" nl
    | "WHILE" comparison "REPEAT" nl {statement} "ENDWHILE" nl
    | "LABEL" name nl
    | "GOTO" name nl
    | "LET" name "=" expression nl
    | "INPUT" name nl
comparison ::= expression (("==" | "!=" | ">" | ">=" | "<" | "<=") expression)+
expression ::= term {( "-" | "+" ) term}
term ::= unary {( "/" | "*" ) unary}
unary ::= ["+" | "-"] primary
primary ::= number | name
nl ::= '\n'+ 
```

### 2.1.1 Program

`program ::= {statement}`
Um programa (program) é feito por uma ou mais declarações (statement)

Já um *statement* é uma outra regra de gramática:
### 2.1.2 Statement:
`statement ::= "PRINT" (expression | string) nl`

A regra de declaração aqui, é definida como uma palavra-chave PRINT, 
seguida por uma expressão ou uma `string`, finalizando com uma quebra de linha.

(Sendo string como um tipo de token definido pelo lexer)

Pode-se adicionar novas regras na declaração:

```
statement ::= "PRINT" (expression | string) nl
    | "LET" ident "=" expression nl
    | "IF" comparison "THEN" nl {statement} "ENDIF" nl
```

Agora, a regra do *statement* tem três opções: um PRINT, um LET ou um IF. Uma declaração de LET, 
significa a atribuição de um valor a uma variavel; A definição é a palavra-chave LET seguida por
um name e um "=" finalizando com uma *expression* e uma quebra de linha. `name` é um tipo de token
definido no lexer, que é o identificador da variávele; e expression é uma outra regra gramatical.
Uma declaração de IF é uma comparison seguida da palavra chave THEN, uma quebra de linha, 
um novo *statement* (**RECURSIVIDADE**), e uma outra palavra chave ENDIF, 
sinalizando o final do teste, e uma quebra de linha.

O restante das regras seguem o mesmo esquema. 

- {} significa zero ou mais
- [] significa zero ou um
- '+' significa um ou mais
- () é um agrupamento
- | ou lógico

### 2.1.3 expression
Expressões (*expression*) é alguma coisa que pode ser avaliada a um valor, como uma expressão
matemática (1 + 5 * 3) ou uma expressão booleana (x >= 10).

As expressões são essas:
```
comparison ::= expression (("==" | "!=" | ">" | ">=" | "<" | "<=") expression)+
expression ::= term {( "-" | "+" ) term}
term ::= unary {( "/" | "*" ) unary}
unary ::= ["+" | "-"] primary
primary ::= number | ident
```


Para atingir diferentes níveis de precedência, as regras gramaticais 
foram organizadas sequencialmente. Operadores com maior precedência 
precisam estar em níveis “inferiores” na gramática, consequentemente
mais baixos na árvore de análise. Os operadores mais próximos 
dos tokens na árvore (perto das folhas) terão uma precedência maior.

Fazendo isso, garante-se a ordem de operadores que se espera, por exemplo, 
em expressões matemáticas: 1 + 2 × 3 deve retornar 7, e não 9. 
Nas regras definidas, os operadores unários + e - (ex.: +5, -10)
estão mais baixos na árvore, então eles possuem maior precedência do que os operadores
× e /, que possui maior precedência que operadores binários + e -.

### 2.1.4 Comparison
Na regra de comparação, não queremos que operadores (ex.: !=) sejam permitidos 
em expressões matemáticas. Por isso, para controlar onde eles de fato são permitidos
(loops e testes condicionais), tem-se uma regra especial para eles que requer
pelo menos um operador de comparação. No lado esquerdo e direito do operador
ded comparação está uma *expression*. Agora, em qualquer lugar que permitimos
apenas expressões matemáticas, esperamos por uma *expression*, e em qualquer lugar
em que se permite uma expressão booleana, esperamos por uma *comparison*.

# 3. O Emitter
O *Emitter* (ou mesmo, gerador ou emissor) será o carinha que “produzirá” o código. 
Nesse caso, vamos gerar um código em C. Isso significa que aqui não faremos trabalho sujo
de passar por código intermediário (pois o próprio C já será uma espécie disso), e
não iremos ver um assembly, ou qualquer outra coisa complexa.

Em cada função do *parser*, será chamado o emitter para produzir o código C apropriado.
O *emitter* nesse caso, irá concatenar um monte de strings, conforme desce na 
árvore analítica. Para cada regra gramatical, deve-se descobrir o que seria o equivalente
em C.