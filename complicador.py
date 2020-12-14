from lex import *
from parse import *
from args import *
from emit import *
import sys


VERBOSE = False


def main():
    global DEBUG
    args = make_args()

    VERBOSE = args.v
    if args.i:
        print_welcome()
        with open(args.i, 'r') as inputFile:
            input_file = inputFile.read()
    else:
        print_help()
        sys.exit("")

    print()

    # Inicializa o lexer, o parser e o emitter.
    lexer = Lexer(input_file, VERBOSE)
    emitter = Emitter(args.o)
    parser = Parser(lexer, emitter, VERBOSE)

    parser.program()  # Roda o parser.
    emitter.write_file()  # escreve a saída no arquivo de saída
    print(f"Compilado em {args.o}.")
    print("===========================")


if __name__ == "__main__":
    main()