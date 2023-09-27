from ttkbootstrap import *
from ttkbootstrap.constants import *

from .models import Tabelas
from .imprimir import Impressao


class LogPanel(Toplevel):
    def __init__(self, impressoras: Impressao, tabelas: Tabelas, kw: dict, **kwargs):
        self.__incia_widgets(kw)
        self.servico_impressoras = impressoras
        self.monitorando = False
        self.__tabelas = tabelas

        self.protocol(self.wm_protocol()[0], self.__close_event)

    def __incia_widgets(self, kw: dict):
        kw['state'] = DISABLED
        kw['wrap'] = WORD
        super().__init__(title='Para printar')
        self.geometry(f'800x500+{self.winfo_rootx() + 600}+{self.winfo_rooty()}')

        self._tela1 = ScrolledText(self, **kw)
        self._tela1.place(relx=0, rely=0, relheight=1, relwidth=0.5)

        self._tela2 = ScrolledText(self, **kw)
        self._tela2.place(relx=0.5, rely=0, relheight=1, relwidth=0.5)

    def start_monitoramento(self):
        self.monitorando = True
        self.__tabelas.inicia_tb_jobs_em_andamento()
        self.after(1000, self.__monitoramento)

    def __monitoramento(self):
        jobs = self.servico_impressoras.printers_job_checker()
        self.__tabelas.update_tb_jobs_em_andamento(jobs)
        for indice, impressora in enumerate(self.servico_impressoras.get_lista_de_impresoras_em_uso()):
            total_na_fila = self.__tabelas.get_total_jobs_em_andamento(impressora)
            try:
                self.__log_clear(screen_number=indice + 1)
                if not jobs:
                    self.__impressoes_finalizadas(impressora, indice + 1)
                    self.monitorando = False
                    return
                self.__imprime_contador(indice + 1, impressora, total_na_fila)
                log = self.__tabelas.get_log_jobs_em_andamento(impressora)
                self.__log_impressora(log, indice + 1)
            except AttributeError:
                break

        self.after(500, self.__monitoramento)

    def __impressoes_finalizadas(self, impressora: str, indice: int):
        self.__log_impressora(f'{impressora} - Impressões finalizadas', indice)

    def __imprime_contador(self, indice: int, impressora: str, total_de_jobs: int):
        tempo_de_impressao = self.calcula_tempo_de_impressao_total(total_de_jobs)
        self.__log_impressora(f'{impressora} - Tempo estimado: {tempo_de_impressao} minutos', indice)

    def __log_impressora(self, info: str, screen_number: int):
        tela = self.__seleciona_tela(screen_number)
        tela.config(state=NORMAL)
        tela.insert(END, f'{info}\n')
        tela.config(state=DISABLED)

    def __log_clear(self, screen_number: int):
        tela = self.__seleciona_tela(screen_number)
        tela.config(state=NORMAL)
        tela.delete('1.0', END)
        tela.config(state=DISABLED)

    def __seleciona_tela(self, screen_number: int):
        return getattr(self, f'_tela{screen_number}')

    def __close_event(self):
        if self.monitorando:
            return
        else:
            self.destroy()

    @staticmethod
    def calcula_tempo_de_impressao_total(quantidade: int) -> str:
        total_seconds = (quantidade - 1) * 2
        minutes, seconds = divmod(total_seconds, 60)
        return f"{minutes:02}:{seconds:02}"
