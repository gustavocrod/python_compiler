import argparse
language_name = 'teste'
command = '-i'


def make_args():
    """
    funcao que utiliza o argparse para receber arquivo de entrada
    :return: lista com os argumentos passados
    """
    parser = argparse.ArgumentParser(description="Compilador xqdl")

    parser.add_argument("--i", "-input", action="store", help="Input file to compile.")
    parser.add_argument("--d", "-debug", action="store_true", help="Turn on the DEBUG log.")
    parser.add_argument("--s", "-shell", action="store_true", help="Access the shell of xqdl language.")

    args = parser.parse_args()

    return args


def print_help():
    print(f"[HELP] usage: ${language_name} {command}<inputfile>")


def print_welcome():
    print("------------------------------------------------------------------------- ")
    print("XQDL Shell (by cr0d and AltOfControl)")
    print("Version 0.1")
    print("Type 'exit' to quit")
    print("------------------------------------------------------------------------- ")
