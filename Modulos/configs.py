from Modulos import Tk


class Configuracoes:
    __cor_da_borda = 'green'
    __cor_de_fundo = 'lightgreen'
    __fonte = 'Roboto 12 bold'

    def __init__(self, root: Tk):
        self.__root = root
        self.largura_da_tela = 500
        self.altura_da_tela = 305
        self.posicao_y = self.__calcula_posicao_y()
        self.posicao_x = self.__calcula_posicao_x()
        self.root_parametros: dict = self.__root_parametros
        self.frame_parametros: dict = self.__frame_parametros
        self.label_parametros: dict = self.__label_parametros
        self.buttons_parametros: dict = self.__buttons_parametros
        self.combobox_parametros: dict = self.__combobox_parametros
        self.barra_de_progresso_parametros: dict = self.__progress_bar_parametros

    def __calcula_posicao_y(self) -> int:
        altura_do_monitor = self.__root.winfo_screenheight()
        largura_livre_do_monitor = altura_do_monitor - self.altura_da_tela
        y_inicial = largura_livre_do_monitor // 2.5
        return int(y_inicial)

    def __calcula_posicao_x(self) -> int:
        largura_do_monitor = self.__root.winfo_screenwidth()
        largura_livre_do_monitor = largura_do_monitor - self.largura_da_tela - 800
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
            'font': self.__fonte,
            'foreground': 'black',
            'background': self.__cor_de_fundo,
        }
        return parametros

    @property
    def __combobox_parametros(self) -> dict:
        parametros = {
            'foreground': 'black',
            'background': self.__cor_de_fundo,
        }
        return parametros

    @property
    def __progress_bar_parametros(self) -> dict:
        parametros = {
            'orient': 'horizontal',
            'mode': 'determinate',
            'length': 470,
            'value': 0,
            'name': 'progresso',
        }
        return parametros

    @property
    def __buttons_parametros(self) -> dict:
        parametros = {
            'font': self.__fonte,
        }
        return parametros
