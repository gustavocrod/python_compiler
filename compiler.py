from args import *
from lexical_analyzer import lexical_analyzer
from syntax_analyzer import syntax_analyzer

STRING_TEST = '3 + 4\n kakkaka=10\n if(avestruz== "teste") {} \ntrue || false\n #comentario'

def main():
    """
    Funcao main, responsavel por conferir os parametros passados e de inicializar o servidor
    :return:
    """
    args = make_args()
    print(args)
    if args.i:
        archive = open(args.i).read()
        lexical_analyzer(archive, args.d)
    else:
        lexical_analyzer(STRING_TEST, False)

    if args.i:
        with open(args.i, "r") as in_file:
            for line in in_file:
                row = line.strip()
                syntax_analyzer(row)

    else:
        line = STRING_TEST.split('\n')
        for row in line:
            syntax_analyzer(row)




if __name__ == "__main__":
    main()
