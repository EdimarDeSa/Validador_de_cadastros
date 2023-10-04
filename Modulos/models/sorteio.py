from ttkbootstrap import *

from Modulos.constants import *
from Modulos.models.produto import Produto


class Sorteio(Frame):
    def __init__(self, master: Frame, nome_do_sorteio):
        super(Sorteio, self).__init__(master)
        self._nome = nome_do_sorteio
        self._premios = ()
        self._vencedor = None

    def configura_colunas(self, col_weights: dict):
        for col, weight in col_weights.items():
            self.grid_columnconfigure(col, weight=weight)

    def cria_separator(self, row, col, orient, rowspan=1, columnspan=1, sticky=None):
        separator = Separator(self, orient=orient)
        separator.grid(row=row, column=col, rowspan=rowspan, columnspan=columnspan, sticky=sticky)
        return separator

    def cria_label(self, linha: int, coluna: int, texto: str, name=None, font='roboto 8'):
        kwargs = {}
        if name: kwargs['name'] = name

        label = Label(self, text=texto.upper(), font=font, **kwargs)
        label.grid(row=linha, column=coluna)
        return label

    def atualiza_premios(self, premios):
        self._limpa_tabela()
        self._premios = premios
        tamnhos_das_colunas = {
            0: 100,
            2: 300,
            4: 50,
        }

        for i in range(1, (len(premios) + 1) * 2, 2):
            tamnhos_das_colunas[i] = 50

        self.configura_colunas(tamnhos_das_colunas)

        linha = 0
        coluna = 0
        for nome_coluna in NOMES_DAS_COLUNAS:
            self.cria_label(linha, coluna, nome_coluna, font='roboto 10 bold')
            coluna += 1
            self.cria_separator(linha, coluna, VERTICAL, rowspan=(len(premios)+1) * 2, sticky=NS)
            coluna += 1

        linha += 1
        self.cria_separator(linha, 0, HORIZONTAL, columnspan=12, sticky=EW)

        for premio in self._premios:
            linha += 1
            coluna = 0
            for nome_coluna in NOMES_DAS_COLUNAS:
                self.cria_label(linha, coluna, getattr(premio, nome_coluna), name=f'{nome_coluna}_premio_{linha}')
                coluna += 2
            linha += 1
            self.cria_separator(linha, 0, HORIZONTAL, columnspan=12, sticky=EW)

    def registra_vencedor(self, vencedor):
        self._vencedor = vencedor

    @property
    def premios(self):
        return self._premios

    @property
    def vencedor(self):
        return self._vencedor

    @property
    def nome_do_sorteio(self):
        return self._nome

    def __str__(self):
        return self._nome

    def _limpa_tabela(self):
        for widget in self.winfo_children():
            widget.destroy()
