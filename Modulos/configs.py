from tkinter import Tk


class Configuracoes:
    __cor_da_borda = 'green'
    __cor_de_fundo = 'lightgreen'
    __estilo_de_fonte = 'Roboto'
    __tamanho_fonte_p = '10'
    __tamanho_fonte_m = '12'
    __tamanho_fonte_g = '15'
    __negrito = 'bold'
    __cor_da_fonte = 'black'

    def __init__(self, root: Tk):
        self.__root: Tk = root
        self.largura_da_tela: int = 800
        self.altura_da_tela: int = 380
        self.posicao_y: int = self.__calcula_posicao_y()
        self.posicao_x: int = self.__calcula_posicao_x()
        self.root_parametros: dict = self.__root_parametros
        self.frame_parametros: dict = self.__frame_parametros
        self.label_parametros: dict = self.__label_parametros
        self.buttons_parametros: dict = self.__buttons_parametros
        self.combobox_parametros: dict = self.__combobox_parametros
        self.barra_de_progresso_parametros: dict = self.__progress_bar_parametros
        self.entry_parametros: dict = self.__entry_parametros

    def __calcula_posicao_y(self) -> int:
        altura_livre_do_monitor = self.__root.winfo_screenheight() - self.altura_da_tela
        y_inicial = altura_livre_do_monitor // 10
        return int(y_inicial)

    def __calcula_posicao_x(self) -> int:
        largura_livre_do_monitor = self.__root.winfo_screenwidth() - self.largura_da_tela
        x_inicial = largura_livre_do_monitor // 2
        return int(x_inicial)

    @property
    def __root_parametros(self) -> dict:
        parametros = {
            'background': self.__cor_da_borda,
        }
        return parametros

    @property
    def __frame_parametros(self) -> dict:
        parametros = {
            'background': self.__cor_de_fundo,
        }
        return parametros

    @property
    def __label_parametros(self) -> dict:
        parametros = {
            'font': f'{self.__estilo_de_fonte} {self.__tamanho_fonte_p} {self.__negrito}',
            'foreground': self.__cor_da_fonte,
            'background': self.__cor_de_fundo,
        }
        return parametros

    @property
    def __combobox_parametros(self) -> dict:
        parametros = {
            'foreground': self.__cor_da_fonte,
            'background': self.__cor_de_fundo,
        }
        return parametros

    @property
    def __progress_bar_parametros(self) -> dict:
        parametros = {
            'orient': 'horizontal',
            'mode': 'determinate',
            'value': 0,
        }
        return parametros

    @property
    def __buttons_parametros(self) -> dict:
        parametros = {
            'font': f'{self.__estilo_de_fonte} {self.__tamanho_fonte_p}',
        }
        return parametros

    @property
    def __entry_parametros(self) -> dict:
        parametros = {
            'font': f'{self.__estilo_de_fonte} {self.__tamanho_fonte_p}',
            'fg': self.__cor_da_fonte
        }
        return parametros
