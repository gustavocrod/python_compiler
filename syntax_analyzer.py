import ply.yacc as yacc

# Get the token map from the lexer. This is required.
from lexical_analyzer import tokens


def p_expression_plus(p):
    'expression : expression PLUS term'
    p[0] = p[1] + p[3]


def p_expression_minus(p):
    'expression : expression MINUS term'
    p[0] = p[1] - p[3]


def p_expression_term(p):
    'expression : term'
    p[0] = p[1]


def p_term_times(p):
    'term : term TIMES factor'
    p[0] = p[1] * p[3]


def p_term_div(p):
    'term : term DIVIDE factor'
    p[0] = p[1] / p[3]


def p_term_factor(p):
    'term : factor'
    p[0] = p[1]


def p_factor_num(p):
    'factor : INT'
    p[0] = p[1]


def p_factor_expr(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]


def p_var(t):
    '''arbitro_de_video : VAR
                | VAR LCOLC expression RCOLC'''
    t[0] = t[1]


# Error rule for syntax errors
def p_error(p):
    print()
    print("Syntax error in input!")
    print(p)



def syntax_analyzer(s):
    # Build the parser
    parser = yacc.yacc()

    result = parser.parse(s)
    print(result)