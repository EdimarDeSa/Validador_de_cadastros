from win32print import ClosePrinter, EnumJobs, EnumPrinters, OpenPrinter
from win32printing import Printer


class Impressao:
    @staticmethod
    def listar_impressoras() -> list[str]:
        return [impressora[2] for impressora in EnumPrinters(2)]

    @staticmethod
    def imprimir(cpf, nome, impressora) -> None:
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

    @staticmethod
    def printer_job_checker(printer_list: list) -> list[dict]:
        jobs_list = list()
        jobs = None
        for printer_name in printer_list:
            phandle = OpenPrinter(printer_name)
            try:
                jobs = EnumJobs(phandle, 0, -1)
            finally:
                jobs_list.extend(list(jobs))
                ClosePrinter(phandle)
        return jobs_list
