from lexical_analysis import InvalidSyntaxError


class NumberNode:
    """
        Corresponde a um nodo da arvore da gramatica, que é um int ou float
    """
    def __init__(self, tok):
        self.token = tok

    def __repr__(self):
        return str(self.token)


class BinOpNode:
    """
    Nóso de operacoes binarias
    """
    def __init__(self, left_node, op_token, right_node):
        self.left_node = left_node
        self.op_token = op_token
        self.right_node = right_node

    def __repr__(self):
        return f"({self.left_node}, {self.op_token}, {self.right_node})"


class UnaryOpNode:
    """
        Nós de operações unárias
    """
    def __init__(self, op_token, node):
        self.op_token = op_token
        self.node = node

    def __repr__(self):
        return f"({self.op_token}, {self.node})"

class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None

    def register(self, result):
        if isinstance(result, ParseResult):
            if result.error:
                self.error = result.error
            return result.node

        return result

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        self.error = error
        return self


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_index = -1
        self.advance()

    def advance(self):
        """
            vai para o proximo token
        """
        self.token_index += 1
        # range dos tokens
        if self.token_index < len(self.tokens):
            # se ainda nao estourou a quantidade de token
            self.current_token = self.tokens[self.token_index] # pega o proximo
        return self.current_token

    def parse(self):
        result = self.expr()
        if not result.error and self.current_token.type != 'EOF':
            return result.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                "Eu ia compilar, mas esperava um '+', '-', '*' ou '/' "
            ))
        return result

    def expr(self):
        return self.bin_op(self.term, ['PLUS', 'MINUS'])

    def factor(self):
        result = ParseResult()
        token = self.current_token
        if str(token.type) in ('PLUS', 'MINUS'):
            result.register(self.advance())
            factor = result.register(self.factor())
            if result.error:
                return result
            return result.success(UnaryOpNode(token, factor))

        elif str(token.type) in ('INT', 'FLOAT'):
            result.register(self.advance())
            return result.success(NumberNode(token))

        elif str(token.type) == 'LPAREN':
            result.register(self.advance())
            expr = result.register(self.expr())
            if result.error:
                return result
            if str(self.current_token.type) == 'RPAREN':
                result.register(self.advance())
                return result.success(expr)
            else:
                return result.failure(InvalidSyntaxError(
                    self.current_token.pos_start, self.current_token.pos_end,
                    "Eu esperava por um ')' pra fechar aqui."
                ))

        # erro
        return result.failure(InvalidSyntaxError(
            token.pos_start,
            token.pos_end,
            "Hey, era pra ter mais um número por aqui. Não?"))

    def term(self):
        term = self.bin_op(self.factor, ['TIMES', 'DIV'])
        return term

    def bin_op(self, function, op_tokens):
        """
            function: funcao para criacao de um termo ou fator
            op_tokens: tupla contendo os tokens
        """
        result = ParseResult()
        left_factor = result.register(function())
        if result.error:
            return result

        while str(self.current_token.type) in op_tokens:
            op_token = self.current_token
            result.register(self.advance())
            right_factor = result.register(function())
            if result.error:
                return result

            left_factor = BinOpNode(left_factor, op_token, right_factor)

        return result.success(left_factor)



