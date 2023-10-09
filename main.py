# Copyright (c) 2023 Edimar de Sá
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.


import sys
from pathlib import Path

from ttkbootstrap import Window, Frame, Notebook

from Modulos.constants import *
from Modulos.configuracoes import *
from Modulos.imprimir import *
from Modulos.models import *
from Modulos.janelas import *
from Modulos.imagens import *


class Main(Window):
    def __init__(self):
        self.configuracoes = Configuracoes()
        icon_path = str(Path(ICONE).resolve())
        Window.__init__(self, iconphoto=icon_path)
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
                       list_sort=self._lista_de_sorteios, teste=False)

        tab_impressao = Frame(self.notebook, name='tab_impressao')
        self.notebook.add(tab_impressao, text='Validação e impressão')
        JanelaImpressao(tab_impressao, self.configuracoes, self.tabelas, self.impressao, teste=False)

        tab_registro_de_vencedor = Frame(self.notebook, name='tab_registro_de_vencedor')
        self.notebook.add(tab_registro_de_vencedor, text='Registro de vencedor')
        JanelaRegistroDeVencedor(tab_registro_de_vencedor, self.configuracoes, self.tabelas,
                                 list_sort=self._lista_de_sorteios, teste=False)

        # tab_relatorios = Frame(self.notebook, name='tab_relatorios')
        # self.notebook.add(tab_relatorios, text='Relatórios do sorteio')
        # JanelaRelatorios(tab_relatorios, self.configuracoes, self.tabelas, teste=False)

        # tab_wide_chat = Frame(self.notebook, name='tab_wide_chat')
        # self.notebook.add(tab_wide_chat, text='Wide Chat')
        # JanelaWideChat(tab_wide_chat, self.configuracoes, self.tabelas, teste=False)

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
