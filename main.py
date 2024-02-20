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
import os.path
import sys
from pathlib import Path

from ttkbootstrap import Frame, Notebook, Window

from Modulos.configuracoes import *
from Modulos.constants import *
from Modulos.imagens import *
from Modulos.imprimir import *
from Modulos.janelas import *
from Modulos.models import *


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
        self.protocol('WM_DELETE_WINDOW', self.close_evet)
        self.style.theme_use(**self.configuracoes.root_parametros)

    def inicia_ui(self):
        self.notebook = Notebook(self)
        self.notebook.pack(fill=BOTH, expand=True)
        self.notebook.enable_traversal()

        tab_registro_de_campanha = Frame(self.notebook, name='tab_registro_de_campanha')
        self.notebook.add(
            tab_registro_de_campanha, text='Registro de sorteios', underline=0
        )
        JanelaSorteios(
            tab_registro_de_campanha,
            self.configuracoes,
            self.tabelas,
            list_sort=self._lista_de_sorteios,
            teste=False,
        )

        tab_impressao = Frame(self.notebook, name='tab_impressao')
        self.notebook.add(tab_impressao, text='Validação e Impressão', underline=12)
        JanelaImpressao(
            tab_impressao, self.configuracoes, self.tabelas, self.impressao, teste=False
        )

        tab_registro_de_vencedor = Frame(self.notebook, name='tab_registro_de_vencedor')
        self.notebook.add(
            tab_registro_de_vencedor, text='Registro de vencedor', underline=12
        )
        JanelaRegistroDeVencedor(
            tab_registro_de_vencedor,
            self.configuracoes,
            self.tabelas,
            list_sort=self._lista_de_sorteios,
            teste=False,
        )

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
        self.geometry(f'{largura}x{altura}')
        self.place_window_center()

    @staticmethod
    def close_evet():
        sys.exit()


import tomllib
from argparse import ArgumentParser

# from src.Views.view import View
from src.Models.model import Model

# from src.Controllers.controller import Controller


def main():
    view = View()
    model = Model()
    controller = Controller()

    controller.setup(view, model)

    controller.start()

    controller.loop()


def check_version() -> str:
    pyproject = 'pyproject.toml'

    if not os.path.exists(pyproject):
        pyproject = os.path.join('_internal', pyproject)

    with open(pyproject, 'rb') as file:
        toml = tomllib.load(file)
        configs = toml['tool']['poetry']
        version = configs.get('version')
        name = configs.get('name')
        return f'{name} - Versão: {version}'


if __name__ == '__main__':
    argparse = ArgumentParser(
        prog='Validador de inscrições',
    )
    argparse.add_argument('-v', '--version', action='version', version=check_version())
    args = argparse.parse_args()

    Main()
