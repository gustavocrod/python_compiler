import argparse
language_name = 'complicador.py'
command = '-i <inputfile>'


def make_args():
    """
    funcao que utiliza o argparse para receber arquivo de entrada
    :return: lista com os argumentos passados
    """
    parser = argparse.ArgumentParser(description="Complicador")

    parser.add_argument("--i", "-input", action="store", help="Arquivo de entrada para compilação.")
    parser.add_argument("--v", "-verbose", action="store_true", help="Liga o verbose log.")
    parser.add_argument("--o", "-output", action="store", help="Nome do arquivo C de saída.", default='out.c')

    args = parser.parse_args()

    return args


def print_help():
    print(f"[HELP] Uso: $complicador.py {command}")


def print_welcome():
    print("------------------------------------------------------------------------- ")
    print("======================================================================")
    print(" _____ ________  ________ _    _____ _____  ___ ______ ___________ ")
    print("/  __ |  _  |  \/  | ___ | |  |_   _/  __ \/ _ \|  _  |  _  | ___ \\")
    print("| /  \| | | | .  . | |_/ | |    | | | /  \/ /_\ | | | | | | | |_/ /")
    print("| |   | | | | |\/| |  __/| |    | | | |   |  _  | | | | | | |    / ")
    print("| \__/\ \_/ | |  | | |   | |____| |_| \__/| | | | |/ /\ \_/ | |\ \ ")
    print(" \____/\___/\_|  |_\_|   \_____\___/ \____\_| |_|___/  \___/\_| \_|")
    print("=====================================================================")
    print("V. 0.1")
    print("------------------------------------------------------------------------- ")
