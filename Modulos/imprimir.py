import pandas as pd
from win32print import ClosePrinter, EnumJobs, EnumPrinters, OpenPrinter
from win32printing import Printer

from Modulos.constants import CPF, NOME


class Impressora:
    def __init__(self):
        self.__impressoras = {}

    def set_printer(self, numero_impressora: str, printer_name: str):
        if not printer_name:
            if numero_impressora in self.__impressoras.keys():
                self.__impressoras.pop(numero_impressora)
            return
        self.__impressoras.__setitem__(numero_impressora, printer_name)

    def get_lista_de_impresoras_em_uso(self) -> list[str]:
        return list(self.__impressoras.values())

    @property
    def total_de_impressoras(self):
        return len(self.__impressoras)


class Impressao(Impressora):
    def __init__(self):
        super(Impressao, self).__init__()
        self.__index_atual = 0
        self.__phandle_list: list[OpenPrinter] = []

    @staticmethod
    def listar_impressoras() -> list[str]:
        printer_list = [impressora[2] for impressora in EnumPrinters(2)]
        printer_list.append('')
        printer_list.sort()
        return printer_list

    @staticmethod
    def contagem_de_caracteres(nome: str):
        linha1 = ''
        linha2 = ''
        total_de_caracteres_linha1 = 0
        lista_nome: list = nome.split()

        for parte in lista_nome:
            total_de_caracteres_linha1 += (len(parte) + 1)
            if total_de_caracteres_linha1 < 30:
                linha1 = f'{linha1} {parte}'
            else:
                linha2 = f'{linha2} {parte}'

        linha1 = linha1.lstrip(' ')
        linha2 = linha2.lstrip(' ')
        return linha1, linha2

    def imprimir(self, cpf: str, nome: str, impressora: str):
        fonte_cpf = {
            "height": 6,
        }

        fonte_nome = {
            "height": 12,
        }

        linha1, linha2 = nome, ''

        if len(nome) > 28: linha1, linha2 = self.contagem_de_caracteres(nome)

        with Printer(linegap=2, printer_name=impressora, doc_name=nome) as printer:
            printer.text(f"CPF: {cpf}", align='right', font_config=fonte_cpf)
            printer.text(f'''\n\n\n{linha1}\n{linha2}''', font_config=fonte_nome)

    def printers_job_checker(self) -> list[dict]:
        jobs_list = list()
        jobs = None

        if not self.__phandle_list:
            self.__inicia_phandle_list()

        for phandle in self.__phandle_list:
            jobs = EnumJobs(phandle, 0, -1)
            jobs_list.extend(list(jobs))

        if not jobs_list:
            for phandle in self.__phandle_list:
                ClosePrinter(phandle)

        return jobs_list

    def __inicia_phandle_list(self) -> None:
        for printer_name in self.get_lista_de_impresoras_em_uso():
            phandle = OpenPrinter(printer_name)
            self.__phandle_list.append(phandle)

    def verifica_vez_da_impressora(self) -> str:
        printer_list: list = self.get_lista_de_impresoras_em_uso()
        printer = printer_list[self.__index_atual]
        self.__index_atual = (self.__index_atual + 1) % self.total_de_impressoras
        if printer:
            return printer

    def __imprime_inscrito(self, row):
        impressora = self.verifica_vez_da_impressora()
        nome_participante = row[NOME]
        cpf = row[CPF]
        self.imprimir(cpf, nome_participante, impressora)

    def enviar_tabela_para_impressora(self, tabela: pd.DataFrame):
        tabela.apply(self.__imprime_inscrito, axis=1)
