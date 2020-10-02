from args import *
from lexical_analysis import Lexer

STRING_TEST = '3 + 4\n kakkaka=10\n if(avestruz== "teste") {} \ntrue || false\n #comentario'


def main():
    """
    Funcao main, responsavel por conferir os parametros passados e de inicializar o servidor
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
            lexer = Lexer(input_text)
            tokens, error = lexer.make_tokens()
            print(f"{tokens}")
            if error:
                print(f"Errors: {error}")


if __name__ == "__main__":
    main()
