import sys

from ttkbootstrap import *

from Modulos.constants import *
from Modulos.configuracoes import Configuracoes
from Modulos.imprimir import Impressao
from Modulos.models import Tabelas
from Modulos.janelas.janelas import JanelaImpressao
from Modulos.imagens import Imagens


class Main(Window):
    def __init__(self):
        self.configuracoes = Configuracoes()
        Window.__init__(self, iconphoto='.\icons\icons8-lottery-50.png', **self.configuracoes.root_parametros)
        self.impressao = Impressao()
        self.tabelas = Tabelas(self.impressao)
        self._imagens = Imagens()

        self.configura_janela()
        self.inicia_widgets()
        self.redimenciona_tela()

        self.mainloop()

    def configura_janela(self):
        self.resizable(False, False)
        self.title('Validador de cadastros')
        self.protocol("WM_DELETE_WINDOW", self.close_evet)

    def inicia_widgets(self):
        self.notebook = Notebook(self)
        self.notebook.pack(fill=BOTH, expand=True)

        # tab_registro_de_campanha = Frame(self)
        # self.notebook.add(tab_registro_de_campanha, text='Registro de sorteios')
        # JanelaSorteios(tab_registro_de_campanha, self.configuracoes.py, self.tabelas, self.impressao)

        tab_impressao = Frame(self)
        self.notebook.add(tab_impressao, text='Validação e impressão')
        JanelaImpressao(tab_impressao, self.configuracoes, self.tabelas, self.impressao)

        # tab_registro_de_vencedor = self.notebook.add('Registro de vencedor')
        # self.aba_registro_de_vencedor = AbaRegistroDevencedor(tab_registro_de_vencedor, self.configuracoes.py, self.tabelas, self.impressao)

        # frame_graficos = Frame(master=self.notebook, **self.configuracoes.py.frame_parametros, name='frame_graficos')
        # self.notebook.add(frame_graficos, state='hidden', text='Graficos')

    def redimenciona_tela(self):
        dimensoes = {
            'width': 1200,
            'height': 500,
            'pos_x': self.__calcula_posicao_x,
            'pos_y': self.__calcula_posicao_y,
        }

        # tela_selecionada = self.notebook.:

        width, height = dimensoes['width'], dimensoes['height']
        pos_x, pos_y = dimensoes['pos_x'](width), dimensoes['pos_y'](height)

        self.geometry(f"{width}x{height}+{pos_x}+{pos_y}")

    def __calcula_posicao_x(self, largura_da_janela) -> int:
        largura_livre_do_monitor = self.winfo_screenwidth() - largura_da_janela
        x_inicial = largura_livre_do_monitor // 2
        return x_inicial

    def __calcula_posicao_y(self, altura_da_janela) -> int:
        altura_livre_do_monitor = self.winfo_screenheight() - altura_da_janela
        y_inicial = altura_livre_do_monitor // 2
        return y_inicial

    @staticmethod
    def close_evet():
        sys.exit()


if __name__ == '__main__':
    Main()
