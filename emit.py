class Emitter:
    """
        Classe responsável por traduzir o código gerado
        e a salvar isso em arquivo de saida.

        Funciona simplesmente concatenando strings
    """
    def __init__(self, full_path):
        self.full_path = full_path
        self.header = ""
        self.code = ""

    def emit(self, code):
        """
            printa na mesma linha
        """
        self.code += code

    def emit_line(self, code):
        """
            printa e quebra linha
        """
        self.code += code + "\n"

    def header_line(self, code):
        self.header += code + "\n"

    def write_file(self):
        with open(self.full_path, 'w') as outputFile:
            outputFile.write(self.header + self.code)
