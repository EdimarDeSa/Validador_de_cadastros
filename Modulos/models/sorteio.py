from ttkbootstrap import *

from Modulos.constants import *
from Modulos.models.produto import Produto


__all__ = ['Sorteio']


class Sorteio(Frame):
    def __init__(self, master: Frame, nome_do_sorteio):
        super(Sorteio, self).__init__(master)
        self.nome_vencedor = None
        self.rg_vencedor = None
        self.dia_do_evento_vencedor = None
        self.data_cadastro_vencedor = None
        self.cep_vencedor = None
        self.cpf_vencedor = None
        self.aceite_novidades_vencedor = None
        self.telefone_vencedor = None
        self.data_nascimento_vencedor = None
        self.email_vencedor = None
        self.endereco_vencedor = None
        self.duplicada_vencedor = None
        self.validade_cpf_vencedor = None
        self.colaborador_vencedor = None
        self.nome_do_sorteio = nome_do_sorteio
        self.premios: tuple[Produto] = ()

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
        self.premios = tuple(premios)
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
        for nome_coluna in COLUNAS_DA_TABELA_DE_PREMIOS:
            self.cria_label(linha, coluna, nome_coluna, font='roboto 10 bold')
            coluna += 1
            self.cria_separator(linha, coluna, VERTICAL, rowspan=(len(premios)+1) * 2, sticky=NS)
            coluna += 1

        linha += 1
        self.cria_separator(linha, 0, HORIZONTAL, columnspan=12, sticky=EW)

        for premio in self.premios:
            linha += 1
            coluna = 0
            for nome_coluna in COLUNAS_DA_TABELA_DE_PREMIOS:
                self.cria_label(linha, coluna, getattr(premio, nome_coluna), name=f'{nome_coluna}_premio_{linha}')
                coluna += 2
            linha += 1
            self.cria_separator(linha, 0, HORIZONTAL, columnspan=12, sticky=EW)

    def registra_vencedor(self, dados_sorteado: list):
        self.nome_vencedor = dados_sorteado[0]
        self.rg_vencedor = dados_sorteado[1]
        self.endereco_vencedor = dados_sorteado[2]
        self.email_vencedor = dados_sorteado[3]
        self.data_nascimento_vencedor = dados_sorteado[4]
        self.telefone_vencedor = dados_sorteado[5]
        self.aceite_novidades_vencedor = dados_sorteado[6]
        self.cpf_vencedor = dados_sorteado[7]
        self.cep_vencedor = dados_sorteado[8]
        self.data_cadastro_vencedor = dados_sorteado[9]
        self.dia_do_evento_vencedor = dados_sorteado[10]
        self.duplicada_vencedor = dados_sorteado[10]
        self.validade_cpf_vencedor = dados_sorteado[11]
        self.colaborador_vencedor = dados_sorteado[12]

    @property
    def __dict__(self):
        COLUNAS = COLUNAS_DA_TABELA_DE_PREMIOS + COLUNAS_DA_TABELA_DE_PARTICIPANTES
        dicionario = {
            'Nome completo': self.nome_vencedor,
            'RG': self.rg_vencedor,
            'Endereço completo': self.endereco_vencedor,
            'Email': self.email_vencedor,
            'Data de nascimento': self.data_nascimento_vencedor,
            'Telefone': self.telefone_vencedor,
            'aceite_novidades': self.aceite_novidades_vencedor,
            'CPF': self.cpf_vencedor,
            'CEP': self.cep_vencedor,
            'Data': self.data_cadastro_vencedor,
            'Dia_do_evento': self.dia_do_evento_vencedor,
            'Duplicada': self.duplicada_vencedor,
            'Validade_cpf': self.validade_cpf_vencedor,
            'Colaborador': self.colaborador_vencedor,
            'premios': [premio.valores for premio in self.premios]
        }
        return dicionario

    def __str__(self):
        return self.nome_do_sorteio

    def _limpa_tabela(self):
        for widget in self.winfo_children():
            widget.destroy()
