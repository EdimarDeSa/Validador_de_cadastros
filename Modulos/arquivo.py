from os.path import dirname, join
from pathlib import Path
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import showwarning

import pandas as pd
from pandas.errors import ParserError

from .constants import EXTENSOES, CPF, CODECS, SEPARADORES, EXTENSAO_DEFAULT


__all__ = ['Arquivos']

DIRETORIO_BASE = Path(__file__).resolve().parent.parent


class Arquivos:
    @staticmethod
    def abre_documento(titulo='') -> Path:
        diretorio_documento = askopenfilename(defaultextension=EXTENSAO_DEFAULT, filetypes=EXTENSOES,
                                              # initialdir=DIRETORIO_BASE,
                                              title='Selecione o arquivo' if not titulo else titulo)
        return Path(diretorio_documento).resolve() if '.' in diretorio_documento else None

    @staticmethod
    def salva_arquivo_filtrado(arquivo: pd.DataFrame, caminho: str = None, tipo: str = None):
        if caminho is None:
            caminho = asksaveasfilename(confirmoverwrite=True, defaultextension='xlsx')
        nome_documento = tipo + '.xlsx'
        caminho_para_salvar = join(dirname(caminho), nome_documento)
        arquivo.to_excel(caminho_para_salvar)
        return caminho_para_salvar

    @staticmethod
    def abre_dataframe(diretorio_documento: Path) -> pd.DataFrame:
        def try_open_csv(encoding, sep):
            try:
                tipo_documento = diretorio_documento.suffix
                df = None
                if tipo_documento == '.csv':
                    df = pd.read_csv(diretorio_documento, encoding=encoding, dtype='string', sep=sep)
                if tipo_documento == '.xlsx':
                    df = pd.read_excel(diretorio_documento, dtype='string')
                if tipo_documento == '.txt':
                    df = pd.read_table(diretorio_documento, encoding=encoding, dtype='string', sep=sep)

                if CPF in df.columns:
                    return df

            except UnicodeDecodeError:
                pass

            except UnicodeError:
                pass

            except ParserError:
                pass

        for codec in CODECS:
            for sep in SEPARADORES:
                df = try_open_csv(codec, sep)
                if df is not None:
                    return df
        showwarning('Nenhum codec encontrado', F'Não foi possível achar o campo "{CPF}" com nenhum codec disponível')
        return pd.DataFrame()

    def get_save_path(self, titulo=None, nome_base_arquivo=None) -> [Path, None]:
        titulo = titulo if titulo else 'Salvar como'
        nome_base_arquivo = nome_base_arquivo if nome_base_arquivo else 'Arquivo.xlsx'
        busca = asksaveasfilename(
            confirmoverwrite=True, defaultextension='.xlsx', filetypes=(('Arquivos do Excel', '*.xlsx'),),
            initialdir=DIRETORIO_BASE, initialfile=nome_base_arquivo, title=titulo
        )
        return Path(busca).resolve() if busca != '' else None
