from typing import Literal

import validate_docbr as vdb
import pandas as pd

from ..arquivo import AbreArquivo
from ..funcoes_main import limpeza_de_dados, capitaliza_nome
# from ..busca_cep import Cep
from ..imprimir import Impressao
from Modulos.constants import CPF, VALIDADE_CPF, NOME, DUPLICADA, COLABORADOR, COLUNAS_SERVICO_IMPRESSORAS


class Tabelas:

    def __init__(self) -> None:
        self.arquivo = AbreArquivo()
        self.impressao = Impressao()
        self.docbr = vdb.CPF()

        self.__caminho_tb_inscritos = None
        self.__tb_inscritos = None
        self.__tb_inscricoes_validas = None

        self.__caminho_tb_colaboradores = None
        self.__tb_colaboradores = None

        self.__tb_vencedores = None

        self.__total_cadastros_repetidos = None
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

    def inicia_tb_inscritos(self, data: str):
        caminho = self.arquivo.abre_documento()

        if not caminho:
            return

        df_sujo = self.arquivo.abre_dataframe(caminho)
        df_com_data = df_sujo.assign(**{
            'Dia_do_evento': lambda df=df_sujo: df['Data'].apply(lambda x: str(x).split()[0] == data),
        })
        df_limpo = df_com_data.query('Dia_do_evento==True')

        self.__tb_inscritos = df_limpo
        self.__tb_inscricoes_validas = pd.DataFrame(columns=df_limpo.columns)
        self.__caminho_tb_inscritos = caminho

    @property
    def get_total_inscritos(self):
        return self.__tb_inscritos.shape[0]

    @property
    def get_caminho_tb_inscritos(self):
        return self.__caminho_tb_inscritos

    def inicia_tb_colaboradores(self):
        caminho = self.arquivo.abre_documento()

        if not caminho:
            return

        df = self.arquivo.abre_dataframe(caminho)
        self.__tb_colaboradores = df
        self.__caminho_tb_colaboradores = caminho

    @property
    def get_caminho_tb_colaboradores(self):
        return self.__caminho_tb_colaboradores

    def verifica_cadastros(self):
        self.__tb_inscritos[CPF] = self.__tb_inscritos[CPF].apply(limpeza_de_dados)
        self.__tb_inscritos = self.__tb_inscritos.assign(**{
            NOME: lambda df: df[NOME].apply(capitaliza_nome),
            DUPLICADA: self.__tb_inscritos.duplicated(subset=CPF, keep='last'),
            VALIDADE_CPF: lambda df: df.query(f'{DUPLICADA}==False')[CPF].apply(self.docbr.validate),
            CPF: lambda df: df.query(f'{VALIDADE_CPF}==True')[CPF].apply(self.docbr.mask),
            COLABORADOR: lambda df: df[CPF].isin(self.__tb_colaboradores[CPF]),
        })

        self.__total_cadastros_repetidos = (self.__tb_inscritos[DUPLICADA] == True).sum()
        self.__total_cpfs_invalidos = (self.__tb_inscritos[VALIDADE_CPF] == False).sum()
        self.__total_colaboradores_cadastrados = (self.__tb_inscritos[COLABORADOR] == True).sum()
        self.__tb_inscricoes_validas = self.__tb_inscritos.query(f'{VALIDADE_CPF}==True and {COLABORADOR}==False')

        # Thread(target=self.__busca_enderecos).start()

    def __busca_enderecos(self):
        informacoes_cep = self.__tb_inscricoes_validas.CEP.apply(lambda cep: Cep(cep).series)
        self.__tb_inscricoes_validas = self.__tb_inscricoes_validas.merge(informacoes_cep, right_index=True,
                                                                          left_index=True)
        self.busca = True

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

    def inicia_tb_vencedores(self):
        self.__tb_vencedores = pd.DataFrame(columns=self.__tb_inscricoes_validas.columns)

    @property
    def get_tb_vencedores(self):
        return self.__tb_vencedores

    def vencedor_exists(self, cpf: str):
        return any(self.__tb_inscricoes_validas[CPF] == cpf)

    def register_winner(self, cpf: str):
        dados_vencedor: pd.DataFrame = self.__tb_inscricoes_validas.query(f'{CPF}=="{cpf}"')
        self.__tb_vencedores = pd.concat([self.__tb_vencedores, dados_vencedor], ignore_index=True)

    def salva_tabela(self, nome_da_tabela: Literal['tb_vencedores', 'tb_inscricoes_validas'], caminho: str):
        tabela: pd.DataFrame = getattr(self, f'get_{nome_da_tabela}')
        return self.arquivo.salva_arquivo_filtrado(tabela, caminho, nome_da_tabela)
