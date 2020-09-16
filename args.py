import argparse
language_name = 'teste'
command = '-i'


def make_args():
    """
    funcao que utiliza o argparse para receber arquivo de entrada
    :return: lista com os argumentos passados
    """
    parser = argparse.ArgumentParser(description="Compilador xqdl")

    parser.add_argument("--i", "-input", action="store", help="Arquivo de entrada para ser compilado")
    parser.add_argument("--d", "-debug", action="store_true", help="Comando para ligar os prints")

    args = parser.parse_args()

    return args


def print_help():
    print(f"[HELP] usage: ${language_name} {command}<inputfile>")
