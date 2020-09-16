from args import *
from lexical_analyzer import lexical_analyzer


def main():
    """
    Funcao main, responsavel por conferir os parametros passados e de inicializar o servidor
    :return:
    """
    args = make_args()
    print(args)
    if args.i:
        archive = open(args.filename).read()
        lexical_analyzer(archive, args.d)
    else:
        lexical_analyzer("3 + 4\n kakkaka=10\n true || false\n #comentario", False)


if __name__ == "__main__":
    main()