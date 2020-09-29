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
        archive = open(args.i).read()
        lexical_analyzer(archive, args.d)
    else:
        lexical_analyzer('3 + 4\n kakkaka=10\n if(avestruz== "teste") {} \ntrue || false\n #comentario', True)



if __name__ == "__main__":
    main()
