from win32print import ClosePrinter, EnumJobs, EnumPrinters, OpenPrinter
from win32printing import Printer
import pandas as pd

from . import CPF, NOME


class Impressora:
    def set_printer(self, printer_name: str) -> None:
        self.__dict__[printer_name] = printer_name

    def get_lista_de_impresoras_em_uso(self) -> list[str]:
        printer_list = list(self.__dict__.values())
        printer_list = printer_list[2:]
        return printer_list
    
    def total_de_impressoras(self):
        return len(self.get_lista_de_impresoras_em_uso())


class Impressao(Impressora):
    def __init__(self):
        super(Impressora, self).__init__()
        self.__index_atual = 0
        self.__phandle_list: list[OpenPrinter] = []

    @staticmethod
    def listar_impressoras() -> list[str]:
        printer_list = [impressora[2] for impressora in EnumPrinters(2)]
        printer_list.append('')
        printer_list.sort()
        return printer_list

    @staticmethod
    def imprimir(cpf: str, nome: str, impressora: str):
        fonte_cpf = {
            "height": 10,
        }
        fonte_nome = {
            "height": 15,
        }

        with Printer(linegap=2, printer_name=impressora, doc_name=nome) as printer:
            printer.text(f"CPF: {cpf}", font_config=fonte_cpf)
            for _ in range(7):
                printer.text('', font_config=fonte_cpf)
            printer.text(f"Nome: {nome}", font_config=fonte_nome)

    def printers_job_checker(self) -> list[dict]:
        jobs_list = list()
        jobs = None

        if not self.__phandle_list:
            self.__inicia_phandle_list()

        for phandle in self.__phandle_list:
            jobs = EnumJobs(phandle, 0, -1)
            print(jobs)
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
        self.__index_atual = (self.__index_atual + 1) % self.total_de_impressoras()
        if printer:
            return printer

    def __imprime_inscrito(self, row):
        impressora = self.verifica_vez_da_impressora()
        nome_participante = row[NOME]
        cpf = row[CPF]
        self.imprimir(cpf, nome_participante, impressora)

    def enviar_tabela_para_impressora(self, tabela: pd.DataFrame):
        tabela.apply(self.__imprime_inscrito, axis=1)
