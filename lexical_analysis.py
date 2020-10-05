from token import TOKENS, Token
from strings_with_arrows import string_with_arrows
import re


class Position:
    def __init__(self, idx, line, col, file_name, file_txt):
        self.idx = idx
        self.line = line
        self.col = col
        self.file_name = file_name
        self.file_text = file_txt

    def advance(self, curr_char=None):
        self.idx += 1
        self.col += 1

        # se quebrar a linha, reseta a coluna e incrementa linha
        if curr_char == "\n":
            self.col = 0
            self.line += 1

    def copy(self):
        """
            precisa pra salvar o inicio do erro
        """
        return Position(self.idx, self.line, self.col, self.file_name, self.file_text)


class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def __str__(self):
        string = f"{self.error_name}: {self.details}\n File {self.pos_start.file_name}, line {self.pos_start.line + 1}"
        string += f"\n\n {string_with_arrows(self.pos_start.file_text, self.pos_start, self.pos_end)}"
        return string


class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Não reconheço esse caractere aí não cara!', details)


class InvalidSyntaxError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Sintáxe inválida', details)


class Lexer:
    def __init__(self, file_name, text):
        self.file_name = file_name
        self.text = text
        self.pos = Position(-1, 0, -1, file_name, text)
        self.curr_char = None   # current char
        self.next()

    def next(self):
        """
            Funcao para avancar para o proximo caracter no texto
        """
        self.pos.advance(self.curr_char)
        self.curr_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    def make_tokens(self):
        tokens = []

        while self.curr_char:
            if self.curr_char in ' \t':
                self.next()
            matched = False
            for key, value in TOKENS.items():
                if re.match(value, str(self.curr_char)):
                    matched = True
                    if key == 't_NUMBER':
                        # print(f"[NUMBER DETECTED] RE: {value} | value: {self.curr_char}")
                        tokens.append(self.make_number())
                    else:
                        #print(f"[OTHER VALUE DETECTED] RE: {value}\nvalue: {self.curr_char}")
                        tokens.append(Token(key.split('_')[1], pos_start=self.pos))     # para remover o t_
                        self.next()
            if not matched:
                pos_start = self.pos.copy()
                char = self.curr_char
                self.next()
                return [], IllegalCharError(pos_start, self.pos, f"'{char}'")
        tokens.append(Token('EOF', pos_start=self.pos))
        return tokens, None

    def make_number(self):
        """
            Making number
        """
        num_str = ''
        dot_count = 0
        pos_start = self.pos.copy()

        while True:
            if self.curr_char and (re.match(r'\d+', str(self.curr_char)) or self.curr_char == '.'):
                #print(f"current char: {str(self.curr_char)}")
                if self.curr_char == '.':
                    if dot_count == 1:
                        break
                    dot_count += 1
                    num_str += '.'
                else:
                    num_str += str(self.curr_char)
                self.next()
                #print(f"next char: {str(self.curr_char)}")
            else:
                break

        if dot_count == 0:
            return Token('INT', int(num_str), pos_start, self.pos)
        else:
            return Token('FLOAT', float(num_str), pos_start, self.pos)
