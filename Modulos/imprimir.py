from Modulos import ClosePrinter, EnumJobs, EnumPrinters, OpenPrinter, Printer


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
    def printer_job_checker(printer_name: str) -> list[str]:
        jobs = list()
        phandle = OpenPrinter(printer_name)
        try:
            print_jobs = EnumJobs(phandle, 0, -1)
            if print_jobs:
                jobs = [job['pDocument'] for job in print_jobs]
            else:
                jobs = ['Impressões finalizadas']
        finally:
            ClosePrinter(phandle)
        return jobs
