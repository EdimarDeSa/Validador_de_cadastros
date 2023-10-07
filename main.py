import sys
import os

from ttkbootstrap import *

from Modulos.constants import *
from Modulos.configuracoes import Configuracoes
from Modulos.imprimir import Impressao
from Modulos.models import Tabelas
from Modulos.janelas.janelas import JanelaImpressao, JanelaSorteios, JanelaRegistroDeVencedor
from Modulos.imagens import Imagens


class Main(Window):
    def __init__(self):
        self.configuracoes = Configuracoes()
        Window.__init__(self, iconphoto='./icons/icons8-lottery-50.png')
        self.impressao = Impressao()
        self.tabelas = Tabelas(self.impressao)
        self._imagens = Imagens()

        self.configura_janela()
        self.inicia_variaveis_globais()
        self.inicia_ui()
        self.redimenciona_tela()

        self.mainloop()

    def configura_janela(self):
        self.resizable(False, False)
        self.title('Validador de cadastros')
        self.protocol("WM_DELETE_WINDOW", self.close_evet)
        self.style.theme_use(**self.configuracoes.root_parametros)

    def inicia_ui(self):
        self.notebook = Notebook(self)
        self.notebook.pack(fill=BOTH, expand=True)
        self.notebook.enable_traversal()

        tab_registro_de_campanha = Frame(self.notebook, name='tab_registro_de_campanha')
        self.notebook.add(tab_registro_de_campanha, text='Registro de sorteios')
        JanelaSorteios(tab_registro_de_campanha, self.configuracoes, self.tabelas,
                       list_sort=self._lista_de_sorteios, teste=True)

        tab_impressao = Frame(self.notebook, name='tab_impressao')
        self.notebook.add(tab_impressao, text='Validação e impressão')
        JanelaImpressao(tab_impressao, self.configuracoes, self.tabelas, self.impressao, teste=True)

        tab_registro_de_vencedor = Frame(self.notebook, name='tab_registro_de_vencedor')
        self.notebook.add(tab_registro_de_vencedor, text='Registro de vencedor')
        JanelaRegistroDeVencedor(tab_registro_de_vencedor, self.configuracoes, self.tabelas,
                                 list_sort=self._lista_de_sorteios, teste=True)

        # tab_relatorios = Frame(self.notebook, name='tab_relatorios')
        # self.notebook.add(tab_relatorios, text='Relatórios do sorteio')
        # JanelaRelatorios(tab_relatorios, self.configuracoes, self.tabelas, teste=True)

        # tab_wide_chat = Frame(self.notebook, name='tab_wide_chat')
        # self.notebook.add(tab_wide_chat, text='Wide Chat')
        # JanelaWideChat(tab_wide_chat, self.configuracoes, self.tabelas, teste=True)

    def inicia_variaveis_globais(self):
        self._lista_de_sorteios = []

    def redimenciona_tela(self):
        largura = 1200
        altura = 500
        self.geometry(f"{largura}x{altura}")
        self.place_window_center()

    @staticmethod
    def close_evet():
        sys.exit()


if __name__ == '__main__':
    Main()
