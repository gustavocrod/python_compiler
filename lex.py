from token import *
import sys


class Lexer:
    def __init__(self, input_file, verbose):
        self.verbose = verbose
        self.source = input_file + '\n'  # entrada pro lex como uma string. \n no final pra simplificar o ultimmo token
        self.curr_char = ''  # char atual na string
        self.curr_pos = -1  # posicao atual na string
        self.next_char()

    def next_char(self):
        """
            Pega o proximo char
        """
        self.curr_pos += 1
        if self.curr_pos >= len(self.source):  # EOF
            self.curr_char = '\0'
        else:
            self.curr_char = self.source[self.curr_pos]  # proximo char

    def peek(self):
        """
            Retorna o char procurado em uma leitura antecipada (lookahead)
        """
        if self.curr_pos + 1 >= len(self.source):
            return '\0'
        return self.source[self.curr_pos + 1]

    @staticmethod
    def abort(message):
        """
            Token invalido, printa uma menssagem de erro e sai
        """
        sys.exit(f"Lexing error. {message}")

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
            token = Token(self.curr_char, TokenType.PLUS)

        elif self.curr_char == '-':
            token = Token(self.curr_char, TokenType.MINUS)

        elif self.curr_char == '*':
            token = Token(self.curr_char, TokenType.ASTERISTIK)

        # a funcao peek permite que olhemos pro proximo char sem descartar o curr
        elif self.curr_char == '=':
            if self.peek() == '=':  # um lookahead
                last_char = self.curr_char
                self.next_char()
                token = Token(last_char + self.curr_char, TokenType.EQEQ)
            else:
                token = Token(self.curr_char, TokenType.EQ)

        elif self.curr_char == '>':
            if self.peek() == '=':
                last_char = self.curr_char
                self.next_char()
                token = Token(last_char + self.curr_char, TokenType.GREATEREQ)  # maior igual
            else:
                token = Token(self.curr_char, TokenType.GREATERT)  # maior
        elif self.curr_char == '<':
            if self.peek() == '=':
                last_char = self.curr_char
                self.next_char()
                token = Token(last_char + self.curr_char, TokenType.LESSEQ)  # menor igual
            else:
                token = Token(self.curr_char, TokenType.LESST)  # menor

        elif self.curr_char == '!':
            if self.peek() == '=':
                last_char = self.curr_char
                self.next_char()
                token = Token(last_char + self.curr_char, TokenType.NOTEQ)  # diferente
            else:
                self.abort(f"Expected = after !, got !{self.peek()}")  # erro

        elif self.curr_char == '/':
            token = Token(self.curr_char, TokenType.SLASH)
        elif self.curr_char == '\n':
            token = Token(self.curr_char, TokenType.NEWLINE)
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
                    self.abort("Illegal character in string.")
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
                    self.abort("Illegal char in numeric")
                while self.peek().isdigit():
                    self.next_char()

            token_text = self.source[start_position: self.curr_pos + 1]  # pegando substring do numero
            token = Token(token_text, TokenType.NUMBER)

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
                token = Token(token_text, TokenType.NAME)

        else:
            # Unknown token!
            self.abort(f"Unknown token: {self.curr_char}")

        self.next_char()
        return token
