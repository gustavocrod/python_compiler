from lex import *


class Parser:
    """
        Classe responsavel por manter o controle do token atual
        e chegar se o código bate com a gramática
    """

    def __init__(self, lexer, emitter, verbose):
        self.verbose = verbose
        self.lexer = lexer
        self.emitter = emitter

        self.symbol_table = set()  # variavies declaradas ate entao
        self.labels_declared = set()  # labels (para goto) declaradas ate entao
        self.labels_gotoed = set()  # labels "gotoed" ate entao

        self.curr_token = None
        self.peek_token = None
        self.curr_line = 1

        # pular dois tokens, para inicializar o atual e o proximo (peek)
        self.next()
        self.next()

    def check_token(self, kind):
        """
            Testa se o tipo do token atual da match (na gramatica)
        """
        return self.curr_token.kind == kind

    def check_peek(self, kind):
        """
            Testa se o tipo do proximo token da match (na gramatica)

            - esses dois metodos de check, ajudam ao parser a saber qual regra gramatical aplicar.
        """
        return self.peek_token == kind

    def test_kind(self, kind):
        """
            Tenta dar match no token atual. Se não der match (com a gramatica), da erro.
            E daí avança para o próximo token.


            - Quando o parser ja sabe qual regra aplicar, utiliza-se desta funcao.
        """
        if not self.check_token(kind):
            self.abort(f"Esperado {kind.name}, e foi recebido um {self.curr_token.kind.name}: {self.curr_token.text}")
        self.next()

    def next(self):
        """
            Vai para o proximo token
        """
        self.curr_token = self.peek_token
        if self.verbose:
            if self.curr_token:
                if self.curr_token.text == "\n":
                    print(f"[LEXER] (\\n, {self.curr_token.kind})")
                else:
                    print(f"[LEXER] ({self.curr_token.text}, {self.curr_token.kind})")

        self.peek_token = self.lexer.get_token()
        # o proprio lexer vai tratar o final do arquivo EOF

    def abort(self, message):
        """
            Deu ruim, deu bug, deu cagada
        """
        sys.exit(f"[BUG] Deu ruim na linha {self.curr_line}: {message}")

    def print_type(self):
        """
            DEBUG print para tipo do token atual
        """
        if self.verbose:
            print(f"[PARSER] STATEMENT: {self.curr_token.text}, {self.curr_token.kind}")

    ###### REGRAS DE GRAMATICA
    def program(self):
        """
            program ::= {statement}
        """

        self.emitter.header_line("#include <stdio.h>")
        self.emitter.header_line("")
        self.emitter.header_line("int main(){")

        # arrumar algumas quebras de linha no inicio do input
        while self.check_token(TokenType.NOVALINHA):
            self.next()

        # Enquanto nao chegar ao fim
        while not self.check_token(TokenType.EOF):
            self.statement()

        # finaliza
        self.emitter.emit_line("return 0;")
        self.emitter.emit_line("}")

        # testar se cada label referenciado por um GOTO foi previamente declarado
        for label in self.labels_gotoed:
            if label not in self.labels_declared:
                self.abort(f"Erro ao tentar usar um GOTO para {label}: Não declarado!")

    def statement(self):
        """
            testa se o primeiro token para ver o tipo da declaração que é
        """

        # "PRINT" (expression | string)
        if self.check_token(TokenType.MOSTRAAI):
            self.print_type()
            self.next()

            if self.check_token(TokenType.STRING):  # string para printar
                self.print_type()
                self.emitter.emit_line(f"printf(\"{self.curr_token.text}\\n\");")
                self.next()

            else:  # uma expressao é esperada, e agora, printa o resultado como um float
                self.print_type()
                self.emitter.emit("printf(\"%" + ".2f\\n\", (float)(")
                self.expression()  # isso vai dentro do print
                self.emitter.emit_line("));")  # final do print

        # | "IF" comparison "THEN" nl {statement} "ENDIF"
        elif self.check_token(TokenType.TESTAPOPAI):
            self.print_type()
            self.next()
            self.emitter.emit("if(")
            self.comparison()

            self.test_kind(TokenType.ENTAO)
            self.print_type()
            self.nl()
            self.emitter.emit_line("){")  # inicio do body do if

            # teste de zero ou mais statements no teste do if
            while not self.check_token(TokenType.VALEUOTESTE):
                self.statement()  # chamada recursiva

            self.test_kind(TokenType.VALEUOTESTE)
            self.emitter.emit_line("}")  # final do if

        # | "WHILE" comparison "REPEAT" nl {statement} "ENDWHILE" nl
        elif self.check_token(TokenType.ENQUANTO):
            self.print_type()
            self.next()
            self.emitter.emit("while(")
            self.comparison()

            self.test_kind(TokenType.REPETE)
            self.nl()
            self.emitter.emit_line("){")  # inicio do body do loop

            # teste de zero ou mais statements no loop do WHILE
            while not self.check_token(TokenType.CANSEIDEREPETIR):
                self.statement()  # chamada recursiva

            self.test_kind(TokenType.CANSEIDEREPETIR)
            self.emitter.emit_line("}")  # final do while

        # | "LABEL" name nl
        elif self.check_token(TokenType.PONTOTURISTICO):
            self.print_type()
            self.next()

            # testar se o label ja nao existe
            if self.curr_token.text in self.labels_declared:
                self.abort(f"Label já existe: {self.curr_token.text}")
            self.labels_declared.add(self.curr_token.text)

            self.emitter.emit_line(f"{self.curr_token.text}:")  # declaracao de um label de goto
            self.test_kind(TokenType.NOME)

        # | "GOTO" name nl
        elif self.check_token(TokenType.VIAJAR):
            self.print_type()
            self.next()
            self.labels_gotoed.add(self.curr_token.text)
            self.emitter.emit_line(f"goto {self.curr_token.text};")  # ida ate o label
            self.test_kind(TokenType.NOME)

        # | "LET" name "=" expression nl
        elif self.check_token(TokenType.ARBITRODEVIDEO):
            self.print_type()
            self.next()

            # testar se o nome da variavel já existe na tabela de simbolos, se nao, tem que declarar
            if self.curr_token.text not in self.symbol_table:
                self.symbol_table.add(self.curr_token.text)
                # header e nao emit normal, por conta da convencao do C, de colocar as variaveis em cima.
                self.emitter.header_line(f"float {self.curr_token.text};")

            self.emitter.emit(f"{self.curr_token.text} = ")
            self.test_kind(TokenType.NOME)  # var
            self.test_kind(TokenType.IGUAL)  # atribuicao

            self.expression()  # expressao
            self.emitter.emit_line(";")

        # | "INPUT" name nl
        elif self.check_token(TokenType.LERDOTECLADO):
            self.print_type()
            self.next()

            # se a variavel ainda nao existe, declará-la
            if self.curr_token.text not in self.symbol_table:
                self.symbol_table.add(self.curr_token.text)
                self.emitter.header_line(f"float {self.curr_token.text};")  # declarando a variavel

            # se o valor for invalido, seta pra zero e limpa o input (isso em codigo C)
            # eh uma limitacao do scan aqui, teria que pensar melhor em como resolver
            # FIXME: Resolver o scan
            self.emitter.emit_line("if (scanf(\"%f\",  &" + self.curr_token.text + ") == 0) {")
            self.emitter.emit_line(f"{self.curr_token.text} = 0;")
            self.emitter.emit("scanf(\"%")
            self.emitter.emit_line("*s\");")
            self.emitter.emit_line("}")
            self.test_kind(TokenType.NOME)

        # declaracao invalida. Erro!
        else:
            self.abort(f"Declaração invalida {self.curr_token.text} ({self.curr_token.kind.name})")

        # nova linha
        self.nl()

    def is_comparison_op(self):
        """
            Retorna se o current token é um == ou > ou >= ou <= ou < ou !=
        """
        return self.check_token(TokenType.MAIOR) \
               or self.check_token(TokenType.MAIORIGUAL) \
               or self.check_token(TokenType.MENOR) \
               or self.check_token(TokenType.MENORIGUAL) \
               or self.check_token(TokenType.IGUALIGUAL) \
               or self.check_token(TokenType.DIFERENTE)

    def comparison(self):
        """
            comparison ::= expression (("==" | "!=" | ">" | ">=" | "<" | "<=") expression)+
        """

        self.expression()

        # precisa ter pelo menos um operador de comparacao e uma outra expr
        if self.is_comparison_op():
            if self.verbose:
                print(f"[PARSER] COMPARISON: {self.curr_token.text}")
            self.emitter.emit(self.curr_token.text)
            self.next()
            self.expression()
        else:
            self.abort(f"Esperado operador de comparacao na linha {self.curr_line} em: {self.curr_token.text}")

        # pode ter 0 ou mais operadores de comparacao e expressoes
        while self.is_comparison_op():
            self.emitter.emit(self.curr_token.text)
            self.next()
            self.expression()

    def expression(self):
        """
            expression ::= term {( "-" | "+") term}
        """
        if self.verbose:
            print(f"[PARSER] EXPRESSION: ", end=" ")
        self.term()

        # pode ter 0 ou mais +,- e expressoes
        while self.check_token(TokenType.MAIS) or self.check_token(TokenType.MENOS):
            self.emitter.emit(self.curr_token.text)
            self.next()
            self.term()

    def term(self):
        """
            term :== unary {( "/" | "*") unary}
        """

        self.unary()

        # pode ter 0 ou mais *,/ e expressoes
        while self.check_token(TokenType.ASTERISCO) or self.check_token(TokenType.BARRA):
            if self.verbose:
                print(f"TERM: {self.curr_token.text}")
            self.emitter.emit(self.curr_token.text)
            self.next()

            self.unary()

    def unary(self):
        """
            unary ::= ["+" | "-"] primary
        """

        # unario opcional, + ou -

        if self.check_token(TokenType.MAIS) or self.check_token(TokenType.MENOS):
            if self.verbose:
                print(f"UNARY: {self.curr_token.text}", end=" ")
            self.emitter.emit(self.curr_token.text)
            self.next()

        self.primary()

    def primary(self):
        """
            o primary é um numero ou um token id, que é o nome da variavel.

            primary ::= number | name
        """
        if self.verbose:
            print(f"PRIMARY: ({self.curr_token.text})")

        if self.check_token(TokenType.NUMERO):
            self.emitter.emit(self.curr_token.text)
            self.next()

        elif self.check_token(TokenType.NOME):
            # ter certeza que a variavel existe
            if self.curr_token.text not in self.symbol_table:
                self.abort(f"Referenciando uma variavel antes de declará-la: {self.curr_token.text}")

            self.emitter.emit(self.curr_token.text)
            self.next()
        else:
            # ERRO!
            self.abort(f"Eita! Um token inesperado: {self.curr_token.text}")

    def nl(self):
        """
            nl ::= '\n'+
        """
        #if self.verbose:
           # print("[PARSER] NEWLINE")
        self.test_kind(TokenType.NOVALINHA)
        self.curr_line += 1
        # Como é uma quebra de linha ou mais, fica em loop
        while self.check_token(TokenType.NOVALINHA):
            self.curr_line += 1
            self.next()
