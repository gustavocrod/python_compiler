from token import *
import sys


class Lexer:
    def __init__(self, input_file, verbose):
        self.verbose = verbose
        self.source = input_file + '\n'  # entrada pro lex como uma string. \n no final pra simplificar o ultimmo token
        self.curr_char = ''  # char atual na string
        self.curr_pos = -1  # posicao atual na string
        self.next_char()
        self.curr_line = 1

    def next_char(self):
        """
            Pega o proximo char
        """
        self.curr_pos += 1
        if self.curr_pos >= len(self.source):  # EOF
            self.curr_char = '\0'
        else:
            self.curr_char = self.source[self.curr_pos]  # proximo char
            if self.curr_char == '\n':
                self.curr_line += 1

    def peek(self):
        """
            Retorna o char procurado em uma leitura antecipada (lookahead)
        """
        if self.curr_pos + 1 >= len(self.source):
            return '\0'
        return self.source[self.curr_pos + 1]

    def abort(self, message):
        """
            Token invalido, printa uma menssagem de erro e sai
        """
        sys.exit(f"[BUG] Erro léxico na linha {self.curr_line}! {message}")

    def skip_white_space(self):
        """
            Ignora espacos em branco, exceto quebra de linha,
            que sera utilizado para indicar o fim de uma deeclaracao

        """
        while self.curr_char == ' ' or self.curr_char == "\t" or self.curr_char == '\r':
            self.next_char()

    # Skip comments in the code.
    def skip_comments(self):
        """
            Ignora comentarios no codigo
        """
        if self.curr_char == '/':
            if self.peek() == '/':
                while self.curr_char != "\n":
                    self.next_char()
                self.curr_line += 1

    def get_token(self):
        """
            retorna o proximo token

            Testa se o primeiro caracter do token pra ver se pode decidir o que ele é
            Se é um operador binario, numero, identificado ou uma palavra chave, entao processa o resto
        """
        self.skip_white_space()
        self.skip_comments()

        token = None
        if self.curr_char == '+':
            token = Token(self.curr_char, TokenType.MAIS)

        elif self.curr_char == '-':
            token = Token(self.curr_char, TokenType.MENOS)

        elif self.curr_char == '*':
            token = Token(self.curr_char, TokenType.ASTERISCO)

        # a funcao peek permite que olhemos pro proximo char sem descartar o curr
        elif self.curr_char == '=':
            if self.peek() == '=':  # um lookahead
                last_char = self.curr_char
                self.next_char()
                token = Token(last_char + self.curr_char, TokenType.IGUALIGUAL)
            else:
                token = Token(self.curr_char, TokenType.IGUAL)

        elif self.curr_char == '>':
            if self.peek() == '=':
                last_char = self.curr_char
                self.next_char()
                token = Token(last_char + self.curr_char, TokenType.MAIORIGUAL)  # maior igual
            else:
                token = Token(self.curr_char, TokenType.MAIOR)  # maior
        elif self.curr_char == '<':
            if self.peek() == '=':
                last_char = self.curr_char
                self.next_char()
                token = Token(last_char + self.curr_char, TokenType.MENORIGUAL)  # menor igual
            else:
                token = Token(self.curr_char, TokenType.MENOR)  # menor

        elif self.curr_char == '!':
            if self.peek() == '=':
                last_char = self.curr_char
                self.next_char()
                token = Token(last_char + self.curr_char, TokenType.DIFERENTE)  # diferente
            else:
                self.abort(f"Esperado '=' depois !, recebido !{self.peek()}")  # erro

        elif self.curr_char == '/':
            token = Token(self.curr_char, TokenType.BARRA)
        elif self.curr_char == '\n':
            token = Token(self.curr_char, TokenType.NOVALINHA)
        elif self.curr_char == '\0':
            token = Token(self.curr_char, TokenType.EOF)

        #### STRINGS ####
        elif self.curr_char == '\"':
            # pega os caracteres entre aspas
            self.next_char()
            start_position = self.curr_pos

            while self.curr_char != '\"':
                # nao aceita char speciais, sem chars de escape, quebra de linha tab ou %
                if self.curr_char == '\r' or self.curr_char == '\n' or \
                        self.curr_char == '\t' or self.curr_char == '\\' or self.curr_char == '%':
                    self.abort(f"Char ilegal na string: {self.curr_char}")
                self.next_char()
            token_text = self.source[start_position: self.curr_pos]  # pega a substring marcado pelo doublequote.
            token = Token(token_text, TokenType.STRING)

        #### NUMEROS ###
        # .9 e 1. nao serao digitos, pois vamos ver uma sequencia de numeros de 0-9
        # a funcao peek vai nos habilitar de olhar os chars a frente, por isso nao da pra ser 1.

        elif self.curr_char.isdigit():
            start_position = self.curr_pos
            while self.peek().isdigit():
                self.next_char()
            if self.peek() == '.':  # ponto flutuante
                self.next_char()

                # precisa ter pelo menos um digito depois do ponto pra ser decimal
                if not self.peek().isdigit():
                    self.abort(f"Char ilegal no numero: {self.curr_char}")
                while self.peek().isdigit():
                    self.next_char()

            token_text = self.source[start_position: self.curr_pos + 1]  # pegando substring do numero
            token = Token(token_text, TokenType.NUMERO)

        #### PALAVRAS-CHAVE ####
        elif self.curr_char.isalpha():
            start_position = self.curr_pos
            while self.peek().isalnum():  # alfanumerico
                self.next_char()

            token_text = self.source[start_position: self.curr_pos + 1]  # substring
            keyword = Token.is_keyword(token_text)
            if keyword:  # palavra chave
                token = Token(token_text, keyword)
            else:  # entao é um id
                token = Token(token_text, TokenType.NOME)

        else:
            # Unknown token!
            self.abort(f"Não conheço esse token aqui: {self.curr_char}")

        self.next_char()
        return token
