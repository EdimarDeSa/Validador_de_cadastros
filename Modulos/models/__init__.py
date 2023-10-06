from typing import Literal

import validate_docbr as vdb
import pandas as pd
import openpyxl as excel

from ..arquivo import AbreArquivo
from ..funcoes_sanitizacao import sanitiza_cpf, sanitiza_nome
# from ..busca_cep import Cep
from ..imprimir import Impressao
from Modulos.models.sorteio import Sorteio, Produto
from Modulos.constants import *


class Tabelas:
    def __init__(self, impressao: Impressao) -> None:
        self.__arquivo = AbreArquivo()
        self.__impressao = impressao
        self.__docbr = vdb.CPF()

        self.__tb_sorteios: pd.DataFrame = None
        self.__tb_vencedores: pd.DataFrame = None

        self.__caminho_tb_inscritos: pd.DataFrame = None
        self.__tb_inscritos = None
        self.__tb_inscricoes_validas = None

        self.__caminho_tb_colaboradores: pd.DataFrame = None
        self.__tb_colaboradores = None

        self.__total_cadastros_repetidos: pd.DataFrame = None
        self.__total_cpfs_invalidos = None
        self.__total_colaboradores_cadastrados = None

        self.__tb_jobs_em_andamento: pd.DataFrame = None

        self.busca = False

    def inicia_tb_jobs_em_andamento(self):
        self.__tb_jobs_em_andamento = pd.DataFrame(columns=COLUNAS_SERVICO_IMPRESSORAS)

    def update_tb_jobs_em_andamento(self, jobs_updated: list[dict]):
        del self.__tb_jobs_em_andamento
        update = pd.DataFrame(jobs_updated, columns=COLUNAS_SERVICO_IMPRESSORAS)
        self.__tb_jobs_em_andamento = update

        if not jobs_updated:
            return

        try:
            self.__tb_jobs_em_andamento.drop('Submitted', axis=1, inplace=True)
        except KeyError:
            pass

    def get_total_jobs_em_andamento(self, impressora) -> int:
        return (self.__tb_jobs_em_andamento['pPrinterName'] == impressora).sum()

    def get_log_jobs_em_andamento(self, impressora) -> str:
        df = self.__tb_jobs_em_andamento.query(f'pPrinterName=="{impressora}"')
        log = '\n'.join(df['pDocument'])
        return log

    def inicia_tb_inscritos(self, data: str, caminho=None):
        if caminho is None:
            caminho = self.__arquivo.abre_documento('Selecione o arquivo de inscritos')

        if not caminho:
            return
        df_sujo = self.__arquivo.abre_dataframe(caminho)
        df_com_data = df_sujo.assign(**{
            'Dia_do_evento': lambda df=df_sujo: df['Data'].apply(lambda x: str(x).split()[0] == data),
        })
        df_limpo = df_com_data.query('Dia_do_evento==True')

        self.__tb_inscritos = df_limpo
        self.__tb_inscricoes_validas = pd.DataFrame(columns=COLUNAS_DA_TABELA_DE_PARTICIPANTES)
        self.__caminho_tb_inscritos = caminho

    @property
    def get_total_inscritos(self):
        return self.__tb_inscritos.shape[0]

    @property
    def get_caminho_tb_inscritos(self):
        return self.__caminho_tb_inscritos

    def inicia_tb_colaboradores(self, caminho=None):
        if caminho is None:
            caminho = self.__arquivo.abre_documento('Selecione o arquivo de colaboradores')

        if not caminho:
            return

        df = self.__arquivo.abre_dataframe(caminho)
        self.__tb_colaboradores = df
        self.__caminho_tb_colaboradores = caminho

    @property
    def get_caminho_tb_colaboradores(self):
        return self.__caminho_tb_colaboradores

    def verifica_cadastros(self):
        self.__tb_inscritos[CPF] = self.__tb_inscritos[CPF].apply(sanitiza_cpf)
        self.__tb_inscritos[NOME] = self.__tb_inscritos[NOME].apply(sanitiza_nome)
        self.__tb_inscritos = self.__tb_inscritos.assign(**{
            DUPLICADA: self.__tb_inscritos.duplicated(subset=CPF, keep='last'),
            VALIDADE_CPF: lambda df: df.query(f'{DUPLICADA}==False')[CPF].apply(self.__docbr.validate),
            CPF: lambda df: df.query(f'{VALIDADE_CPF}==True')[CPF].apply(self.__docbr.mask),
            COLABORADOR: lambda df: df[CPF].isin(self.__tb_colaboradores[CPF]),
        })

        self.__total_cadastros_repetidos = (self.__tb_inscritos[DUPLICADA] == True).sum()
        self.__total_cpfs_invalidos = (self.__tb_inscritos[VALIDADE_CPF] == False).sum()
        self.__total_colaboradores_cadastrados = (self.__tb_inscritos[COLABORADOR] == True).sum()
        self.__tb_inscricoes_validas = self.__tb_inscritos.query(f'{VALIDADE_CPF}==True and {COLABORADOR}==False')

        # Thread(target=self.__busca_enderecos).start()

    # def __busca_enderecos(self):
    #     informacoes_cep = self.__tb_inscricoes_validas.CEP.apply(lambda cep: Cep(cep).series)
    #     self.__tb_inscricoes_validas = self.__tb_inscricoes_validas.merge(informacoes_cep, right_index=True,
    #                                                                       left_index=True)
    #     self.busca = True

    @property
    def get_total_cadastros_repetidos(self) -> int:
        return self.__total_cadastros_repetidos

    @property
    def get_total_cpfs_invalidos(self) -> int:
        return self.__total_cpfs_invalidos

    @property
    def get_total_colaboradores_cadastrados(self) -> int:
        return self.__total_colaboradores_cadastrados

    @property
    def get_total_inscricoes_validas(self) -> int:
        return self.__tb_inscricoes_validas.shape[0]

    @property
    def get_estado_dos_inscritos(self) -> int:
        return self.__tb_inscricoes_validas.value_counts(subset='uf')

    @property
    def get_cidades_dos_inscritos(self):
        return self.__tb_inscricoes_validas.value_counts(subset='localidade')

    @property
    def get_tb_inscricoes_validas(self):
        return self.__tb_inscricoes_validas

    @property
    def get_tb_vencedores(self):
        return self.__tb_vencedores

    def vencedor_exists(self, cpf: str):
        return any(self.__tb_inscricoes_validas[CPF] == cpf)

    def busca_vencedor(self, cpf: str):
        cpf = self.__docbr.mask(sanitiza_cpf(cpf))
        dados_vencedor: pd.DataFrame = self.__tb_inscricoes_validas.query(f'{CPF}=="{cpf}"')
        return dados_vencedor.values

    def salva_tabela(self, nome_da_tabela: Literal['tb_vencedores', 'tb_inscricoes_validas'], caminho: str):
        tabela: pd.DataFrame = getattr(self, f'get_{nome_da_tabela}')
        return self.__arquivo.salva_arquivo_filtrado(tabela, caminho, nome_da_tabela)

    def add_sorteio(self, lista_de_sorteios: list[Sorteio]):
        lista_premios = [
            [sorteio.nome_do_sorteio] + premio.valores
            for sorteio in lista_de_sorteios
            for premio in sorteio.premios
        ]
        self.__tb_sorteios = pd.DataFrame(lista_premios, columns=["sorteio"] + COLUNAS_DA_TABELA_DE_PREMIOS)

    def get_tb_sorteios_valores(self) -> [dict[list[Produto]], None]:
        sorteios = dict()
        for sorteio in self.__tb_sorteios.values:
            chave, *infos = sorteio
            sorteios.setdefault(chave, []).append(Produto(*infos))
        return sorteios

    def exportar_tb_vencedores(self, lista_de_sorteios: list[Sorteio]):
        dfs = []
        colunas = COLUNAS_DA_TABELA_DE_PARTICIPANTES + ['sorteio'] + COLUNAS_DA_TABELA_DE_PREMIOS
        wb = excel.Workbook()
        wb.remove(wb.active)

        for sorteio in lista_de_sorteios:
            ws = wb.create_sheet(sorteio.nome_do_sorteio)
            ws.cell(1, 1, sorteio.nome_do_sorteio)
            ws.cell(2, 1, sorteio.nome_vencedor)
            ws.cell(3, 1, 'CPF')
            ws.cell(3, 2, sorteio.cpf_vencedor)
            ws.cell(4, 1, 'RG')
            ws.cell(4, 2, sorteio.rg_vencedor)
            ws.cell(5, 1, 'Telefone')
            ws.cell(5, 2, sorteio.telefone_vencedor)
            ws.cell(6, 1, 'Email')
            ws.cell(6, 2, sorteio.email_vencedor)
            ws.cell(7, 1, 'Endereço de envio')
            ws.cell(7, 2, sorteio.endereco_vencedor)
            ws.cell(8, 1, 'CEP')
            ws.cell(8, 2, sorteio.cep_vencedor)

            ws.cell(2, 3, 'Quantidade')
            ws.cell(2, 4, 'Código do produto')
            ws.cell(2, 5, 'Descrição')
            ws.cell(2, 6, 'CC')
            ws.cell(2, 7, 'Data fechamento do cc')
            ws.cell(2, 8, 'Responsável pelo cc')
            data = sorteio.__dict__
            premios = data['premios']
            del data['premios']

            for linha, premio in enumerate(premios):
                ws.cell(linha + 3, 3, premio[0])
                ws.cell(linha + 3, 4, premio[1])
                ws.cell(linha + 3, 5, premio[2])
                ws.cell(linha + 3, 6, premio[3])
                ws.cell(linha + 3, 7, premio[4])
                ws.cell(linha + 3, 8, premio[5])
                atual = [dado for dado in data.values()] + [sorteio.nome_do_sorteio] + premio
                dfs.append(pd.DataFrame([atual], columns=colunas))

        wb.save('C:/Users/Edimar/Documents/GitHub/Validador_de_cadastros/data/data.xlsx')
        self.__tb_vencedores = pd.concat(dfs, ignore_index=True, verify_integrity=True)
        self.__arquivo.salva_arquivo_filtrado(self.__tb_vencedores, tipo='tabela_de_sorteados')

