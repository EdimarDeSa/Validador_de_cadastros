from os.path import dirname, join, exists
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showwarning
import re
from typing import Literal

import pandas as pd
from PIL import Image

from Modulos import EXTENSOES, CPF, CODECS, SEPARADORES, EXTENSAO_DEFAULT


class AbreArquivo:
    __DIRETORIO_BASE = f'../{dirname(__file__)}'
    DIALETO_USADO = None
    caminho_imagem = 'icons/procurar.png'

    def abre_documento(self) -> str:
        diretorio_documento = askopenfilename(defaultextension=EXTENSAO_DEFAULT, filetypes=EXTENSOES,
                                              initialdir=self.__DIRETORIO_BASE, title='Selecione o arquivo')
        return diretorio_documento

    @staticmethod
    def salva_arquivo_filtrado(arquivo: pd.DataFrame, caminho: str, tipo: Literal["relatorio", "vencedores"]):
        relatorios = {
            'relatorio': 'relatorio_campanha.xlsx',
            'vencedores': 'vencedores_campanha.xlsx'
        }
        caminho_para_salvar = join(dirname(caminho), relatorios[tipo])
        arquivo.to_excel(caminho_para_salvar)
        return caminho_para_salvar

    @staticmethod
    def abre_dataframe(diretorio_documento: str) -> pd.DataFrame:
        def try_open_csv(encoding, sep):
            try:
                tipo_documento = re.findall(r'\.(\w+)', diretorio_documento)[0].lower()
                df = None

                if tipo_documento == 'csv':
                    df = pd.read_csv(diretorio_documento, encoding=encoding, dtype='string', sep=sep)
                if tipo_documento == 'xlsx':
                    df = pd.read_excel(diretorio_documento, dtype='string')
                if tipo_documento == 'txt':
                    df = pd.read_table(diretorio_documento, encoding=encoding, dtype='string', sep=sep)

                if CPF in df.columns:
                    return df

            except UnicodeDecodeError or UnicodeError or pd.errors.ParserError as err:
                pass

        for codec in CODECS:
            for sep in SEPARADORES:
                df = try_open_csv(codec, sep)
                if df is not None:
                    return df
        showwarning('Nenhum codec encontrado', F'Não foi possível achar o campo "{CPF}" com nenhum codec disponível')
        return pd.DataFrame()

    def abre_imagem(self):
        if not exists('icons/procurar_28x28.png'):
            lupa = Image.open(self.caminho_imagem)
            lupa_32 = lupa.resize((28, 28))
            lupa_32.save('icons/procurar_28x28.png')
        return 'icons/procurar_28x28.png'
