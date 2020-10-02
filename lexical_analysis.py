from token import *
import re


class Error:
    def __init__(self, error_name, details):
        self.error_name = error_name
        self.details = details

    def __str__(self):
        return f"{self.error_name}: {self.details}"


class IllegalCharError(Error):
    def __init__(self, details):
        super().__init__('Illegal Character error', details)


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = -1   # posicao atual
        self.curr_char = None   # current char
        self.next()

    def next(self):
        """
            Funcao para avancar para o proximo caracter no texto
        """
        self.pos += 1
        self.curr_char = self.text[self.pos] if self.pos < len(self.text) else None

    def make_tokens(self):
        tokens = []
        while self.curr_char:
            if self.curr_char in ' \t':
                self.next()
            matched = False
            for key, value in TOKENS.items():

                if re.match(value, self.curr_char):
                    matched = True
                    if key == 't_NUMBER':
                        # print(f"[NUMBER DETECTED] RE: {value} | value: {self.curr_char}")
                        tokens.append(self.make_number())
                    else:
                        # print(f"[OTHER VALUE DETECTED] RE: {value} | value: {self.curr_char}")
                        tokens.append(Token(key.split('_')[1], self.curr_char))
                    self.next()
            if not matched:
                char = self.curr_char
                return [], IllegalCharError(f"'{char}'")
        return tokens, None

    def make_number(self):
        """
            Making number
        """
        num_str = ''
        dot_count = 0

        while self.curr_char and (re.match(r'\d+', self.curr_char) or self.curr_char == '.'):
            if self.curr_char == '.':
                if dot_count == 1:
                    break
                dot_count += 1
                num_str += '.'
            else:
                num_str += str(self.curr_char)
            self.next()

        if dot_count == 0:
            return Token('INT', int(num_str))
        else:
            return Token('FLOAT', float(num_str))
