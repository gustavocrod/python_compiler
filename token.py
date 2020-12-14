import enum


class Token:
    def __init__(self, token_text, token_type):
        self.text = token_text  # texto atual do token. Usado para ids, strings e numeros
        self.kind = token_type  # o tipo do token que ele esta sendo classificado como

    @staticmethod
    def is_keyword(token_text):
        for kind in TokenType:
            # ve todos os valores de palavra-chave, que esta entre 1-- e 200
            if kind.name == token_text and 100 <= kind.value < 200:
                return kind
        return None


class TokenType(enum.Enum):
    EOF = -1
    NEWLINE = 0
    NUMBER = 1
    NAME = 2
    STRING = 3
    # palavras-chave
    LABEL = 101
    GOTO = 102
    PRINT = 103
    INPUT = 104
    LET = 105
    IF = 106
    THEN = 107
    ENDIF = 108
    WHILE = 109
    REPEAT = 110
    ENDWHILE = 111
    # operadores
    EQ = 201
    PLUS = 202
    MINUS = 203
    ASTERISTIK = 204
    SLASH = 205
    EQEQ = 206
    NOTEQ = 207
    LESST = 208
    LESSEQ = 209
    GREATERT = 210
    GREATEREQ = 211
