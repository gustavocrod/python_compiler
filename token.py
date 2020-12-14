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
    NOVALINHA = 0
    NUMERO = 1
    NOME = 2
    STRING = 3
    # palavras-chave
    PONTOTURISTICO = 101
    VIAJAR = 102
    MOSTRAAI = 103
    LERDOTECLADO = 104
    ARBITRODEVIDEO = 105
    TESTAPOPAI = 106
    ENTAO = 107
    VALEUOTESTE = 108
    ENQUANTO = 109
    REPETE = 110
    CANSEIDEREPETIR = 111
    # operadores
    IGUAL = 201
    MAIS = 202
    MENOS = 203
    ASTERISCO = 204
    BARRA = 205
    IGUALIGUAL = 206
    DIFERENTE = 207
    MENOR = 208
    MENORIGUAL = 209
    MAIOR = 210
    MAIORIGUAL = 211
