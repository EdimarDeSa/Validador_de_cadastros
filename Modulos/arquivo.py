from Modulos import DictReader, DictWriter, join, askopenfilename, dirname, basename, register_dialect, list_dialects
from Modulos import EXTENSOES, QUOTE_NONE, STRING_COLUNA_CPF, CODECS, showwarning


class AbreArquivo:
    def __init__(self):
        self.__DIRETORIO_BASE = None
        self.ARQUIVO_ATUAL = None
        self.EXTENSAO_DEFAULT = '.csv'
        self.DIALETO_USADO = None
        self.TOTAL_DE_LINHAS = 0

    def dicionariza_csv(self) -> DictReader:
        diretorio_documento = self.__buscar_arquivo()
        objeto_csv = self.__abre_csv(diretorio_documento)
        self.TOTAL_DE_LINHAS = sum(1 for _ in objeto_csv)
        objeto_csv.seek(0)
        arquivo_dicionarizado = self.__verifica_dialeto(objeto_csv)
        return arquivo_dicionarizado

    def inicia_arquivo_filtrado(self, dicionario_csv):
        caminho = join(self.__DIRETORIO_BASE, 'filtrado.csv')
        file = open(file=caminho, mode='w', encoding='UTF-8')
        arquivo_filtrado = DictWriter(file, fieldnames=dicionario_csv.fieldnames, dialect=self.DIALETO_USADO)
        arquivo_filtrado.writeheader()
        return arquivo_filtrado

    def __buscar_arquivo(self) -> str:
        diretorio_documento = askopenfilename(defaultextension=self.EXTENSAO_DEFAULT, filetypes=EXTENSOES,
                                              initialdir=dirname(__file__), title='Selecione o arquivo')
        self.__DIRETORIO_BASE = dirname(diretorio_documento)
        self.ARQUIVO_ATUAL = basename(diretorio_documento)
        return diretorio_documento

    def __verifica_dialeto(self, file) -> DictReader:
        register_dialect('ponto_virgula', delimiter=';', quoting=QUOTE_NONE)
        for dialect in list_dialects():
            dicionario_arquivo = DictReader(file, dialect=dialect)
            if STRING_COLUNA_CPF in dicionario_arquivo.fieldnames:
                self.DIALETO_USADO = dialect
                return dicionario_arquivo
            else:
                file.seek(0)

    @staticmethod
    def __abre_csv(diretorio_documento):
        for codec in CODECS:
            try:
                objeto_csv = open(diretorio_documento, encoding=codec)
                if STRING_COLUNA_CPF in objeto_csv.readline():
                    objeto_csv.seek(0)
                    return objeto_csv
                objeto_csv.seek(0)

            except (UnicodeDecodeError, UnicodeError):
                pass
                    
        showwarning('Nenhum codec encontrado',
                    F'Não foi possível achar o campo "{STRING_COLUNA_CPF}" com nenhum codec disponível')
        
        return None
