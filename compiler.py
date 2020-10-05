from args import *
from lexical_analysis import Lexer
from syntax_analysis import Parser

STRING_TEST = '3 + 4\n kakkaka=10\n if(avestruz== "teste") {} \ntrue || false\n #comentario'


def main():
    """
    Funcao main, responsavel por
        conferir os parametros passados,
        gerar tokens,
        conferir a gramatica,
    :return:
    """
    args = make_args()
    print(args)

    if args.s:
        print_welcome()

        while True:
            input_text = input(">>> ")
            if input_text == 'exit':
                exit()
            lexer = Lexer('<stdin>', input_text)

            # Gerar tokens
            tokens, error = lexer.make_tokens()
            print(f"Tokens: {tokens}")
            if error:
                print(f"Token error: {error}")

            # Gerar Abstract Syntax Tree (ast)
            parser = Parser(tokens)
            ast = parser.parse()
            if ast.error:
                print(ast.error)

            if ast.node:
                print(f"Arvore de sintaxe: {ast.node}")


if __name__ == "__main__":
    main()
