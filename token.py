TOKENS = {
            't_RPAREN': r'\)',
            't_LPAREN': r'\(',
            't_RCOLC': r'\]',
            't_LCOLC': r'\[',
            't_RBRACE': r'\}',
            't_LBRACE': r'\{',
            't_COMMA': r',',
            't_SEMICOLON': r';',
            't_OR': r'\|\|',
            't_AND': r'&&',
            't_EXCLAMATION': r'!',
            't_INTERROGATION': r'\?',
            't_COLON': r':',
            't_EQUALS': r'==',
            't_DIFF': r'!=',
            't_LESSTHAN': r'<',
            't_GREATERTHAN': r'>',
            't_LESSTHANOREQUAL': r'<=',
            't_GREATERTHANOREQUAL': r'>=',
            't_SUMEQUALS': r'\+=',
            't_MINUSEQUALS': r'-=',
            't_TIMESEQUALS': r'\*=',
            't_DIVIDEEQUALS': r'/=',
            't_MOD': r'%=',
            't_PLUS': r'\+',
            't_MINUS': r'-',
            't_TIMES': r'\*',
            't_DIVIDE': r'/',
            't_ASSIGN': r'=',
            't_NUMBER': r'[0-9]*[.,]?[0-9]*\Z',
        }


class Token:
    """
    Classe para definição de token
    """
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        if self.value:
            return f"{self.type}: {self.value}"
        return f"{self.type}"
