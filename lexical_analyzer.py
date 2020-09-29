import ply.lex as lex
DEBUG = True

reserved_worlds = {
    'bool': 'BOOL',
    'break': 'BREAK',
    'for': 'FOR',
    'while'	: 'WHILE',
    'false': 'FALSE',
    'true': 'TRUE',
    'if': 'IF',
    'else': 'ELSE',
    'int': 'INT',
    'short': 'SHORT',
    'long': 'LONG',
    'float': 'FLOAT',
    'string': 'STRING',
    'return': 'RETURN',
    'write': 'WRITE',
    'read': 'READ'
}

"""
All lexers must provide a list called tokens that defines all of the possible token names that can be produced 
by the lexer. This list is always required.
"""
tokens = ['NAME', 'NUMBER', 'NORMALSTRING', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'ASSIGN', 'RPAREN', 'LPAREN', 'RCOLC',
          'LCOLC', 'RBRACE', 'LBRACE', 'COMMA', 'SEMICOLON', 'OR', 'AND', 'EXCLAMATION',
          'INTERROGATION', 'COLON', 'EQUALS', 'DIFF', 'LESSTHAN', 'GREATERTHAN', 'LESSTHANOREQUAL',
          'GREATERTHANOREQUAL', 'SUMEQUALS',
          'MINUSEQUALS', 'TIMESEQUALS', 'DIVIDEEQUALS', 'MOD'] + list(reserved_worlds.values())


'''
# Regular expression rules for simple tokens
The regex rule for each string may be defined either as a string or as a function. In either case, 
the variable name should be prefixed by t_ to denote it is a rule for matching tokens.

( ) [ ] { } , ; + - * / == != > >= < <= || && ! = += -= *= /= %= ? :


If some kind of action needs to be performed, a token rule can be specified as a function.
Like t_NUMBER, t_NAME

'''
t_ignore = ' \n\t'

t_RPAREN = r'\)'
t_LPAREN = r'\('


t_RCOLC = r'\]'
t_LCOLC = r'\['
t_RBRACE = r'\}'
t_LBRACE = r'\{'

t_COMMA = r','
t_SEMICOLON = r';'
t_OR = r'\|\|'
t_AND = r'&&'
t_EXCLAMATION = r'!'
t_INTERROGATION = r'\?'
t_COLON = r':'


t_EQUALS = r'=='
t_DIFF = r'!='
t_LESSTHAN = r'<'
t_GREATERTHAN = r'>'
t_LESSTHANOREQUAL = r'<='
t_GREATERTHANOREQUAL = r'>='

t_SUMEQUALS = r'\+='
t_MINUSEQUALS = r'-='
t_TIMESEQUALS = r'\*='
t_DIVIDEEQUALS = r'/='
t_MOD = r'%='

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_ASSIGN = r'='



def t_NAME(t):
    """
    :param t:
    :return:
    """
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    if t.value in reserved_worlds:# Check for reserved words
        t.type = reserved_worlds[t.value]
    if DEBUG:
        print(t)
    return t


def t_NORMALSTRING(t):
    """

    :param t:
    :return:
    """
    r'\"([^\\\n]|(\\.))*?\"'
    if DEBUG:
        print(t)
    return t


def t_NUMBER(t):
    """
    Expressao regular com transformacao para inteiro
    :param t:
    :return:
    """
    r'\d+'
    if DEBUG:
        print(t)
    t.value = int(t.value)
    return t


def t_newline(t):
    """
        Definicao de regra para podermos contar a quantidade de linhas
    :param t:
    :return:
    """
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    """
        Regra de tratamento de erro
    :param t:
    :return:
    """
    if DEBUG:
        print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


def t_COMMENT_MONOLINE(t):
    r'//.*'
    pass
    # No return value. Token discarded


def t_ccode_comment(t):
    r'(/\*(.|\n)*?\*/)|(//.*)'
    pass


def lexical_analyzer(data, debug=False):
    """
        Like main function
    :param data: dados a serem tokenizados
    :param debug: flag para ligar prints
    :return:
    """
    global DEBUG
    DEBUG = debug
    lexer = lex.lex()
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)
