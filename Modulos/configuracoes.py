from json import load
from pathlib import Path


__all__ = ['Configuracoes']
BASE = Path(__file__).resolve().parent.parent
ARQUIVO_DE_CONFIGURACOES = BASE / 'configuracoes/configuracoes.json'


class Configuracoes:
    def __init__(self):
        self._tamanho_da_fonte = 10
        self._estilo_da_fonte = 'Roboto'
        self._negrito = 'bold'
        self._themename = 'cyborg'

        self.abre_dados()

        self.root_parametros: dict = self.__parametros_root
        self.label_titulos: dict = self.__label_titulos
        self.label_parametros: dict = self.__label_parametros
        self.label_caminho_parametros: dict = self.__label_caminho_parametros
        self.entry_parametros: dict = self.__entry_parametros

    def abre_dados(self):
        with open(ARQUIVO_DE_CONFIGURACOES) as f:
            loaded_configs: dict = load(f)

        for key, value in loaded_configs.items():
            setattr(self, f"_{key}", value)

        del loaded_configs

    @property
    def _tamanho_da_fonte_m(self) -> int:
        return int(self._tamanho_da_fonte * 1.2)

    @property
    def _tamanho_da_fonte_g(self) -> int:
        return int(self._tamanho_da_fonte * 1.5)

    @property
    def __parametros_root(self) -> dict:
        parametros = {'themename': self._themename}
        return parametros

    @property
    def __label_titulos(self) -> dict:
        parametros = {'font': f'{self._estilo_da_fonte} {self._tamanho_da_fonte_g} bold', }
        return parametros

    @property
    def __label_parametros(self) -> dict:
        parametros = {'font': f'{self._estilo_da_fonte} {self._tamanho_da_fonte} bold', }
        return parametros

    @property
    def __label_caminho_parametros(self) -> dict:
        parametros = {'font': f'{self._estilo_da_fonte} {self._tamanho_da_fonte_m}', }
        return parametros

    @property
    def __entry_parametros(self) -> dict:
        parametros = {'font': f'{self._estilo_da_fonte} {self._tamanho_da_fonte}', }
        return parametros
