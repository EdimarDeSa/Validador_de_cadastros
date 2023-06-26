from tkinter import Toplevel, Text, Scrollbar, TclError
from threading import Thread

import time

from .models import Tabelas
from .imprimir import Impressao


class LogPanel(Toplevel):
    def __init__(self, impressoras: Impressao, tabelas: Tabelas, kw: dict):
        self.__incia_widgets(kw)
        self.servico_impressoras = impressoras
        self.monitorando = False
        
        self.__tabelas = tabelas
        
        self.protocol(self.wm_protocol()[0], self.__close_event)
    
    def __incia_widgets(self, kw) -> None:
        kw['state'] = 'disabled'
        kw['wrap'] = 'word'
        Toplevel.__init__(self)
        self.geometry(f'800x500+{self.winfo_rootx()+600}+{self.winfo_rooty()}')

        self._tela1 = Text(master=self, **kw)
        scrollbar1 = Scrollbar(master=self, command=self._tela1.yview)
        self._tela1.place(relx=0, rely=0, relheight=1, relwidth=0.485)
        self._tela1.configure(yscrollcommand=scrollbar1.set)
        scrollbar1.place(relx=0.485, rely=0, relheight=1, relwidth=0.015)

        self._tela2 = Text(master=self, **kw)
        scrollbar2 = Scrollbar(master=self, command=self._tela2.yview)
        self._tela2.place(relx=0.5, rely=0, relheight=1, relwidth=0.485)
        self._tela2.configure(yscrollcommand=scrollbar2.set)
        scrollbar2.place(relx=0.985, rely=0, relheight=1, relwidth=0.015)
        
    def start_monitoramento(self) -> None:
        self.monitorando = True
        Thread(target=self.__monitoramento).start()
    
    def __monitoramento(self) -> None:
        def delay(start) -> None:
            elapsed_time = time.time() - start
            time_to_wait = max(0, int(2 - elapsed_time))
            time.sleep(time_to_wait)

        jobs = [1]
        start_time = time.time()
        self.__tabelas.inicia_tb_jobs_em_andamento()

        while jobs:
            delay(start_time)

            jobs = self.servico_impressoras.printers_job_checker()
            self.__tabelas.update_tb_jobs_em_andamento(jobs)
            for impressora in self.servico_impressoras.get_lista_de_impresoras_em_uso():
                indice = self.servico_impressoras.get_lista_de_impresoras_em_uso().index(impressora)
                total_na_fila = self.__tabelas.get_total_jobs_em_andamento(impressora)
                try:
                    self.__log_clear(indice)
                    if not jobs:
                        self.__impressoes_finalizadas(impressora, indice)
                    self.__imprime_contador(indice, impressora, total_na_fila)
                    log = self.__tabelas.get_log_jobs_em_andamento(impressora)
                    self.__log_impressora(log, indice)
                except TclError:
                    del self.log_panel
                    break
                except AttributeError:
                    break
            start_time = time.time()
        self.monitorando = False

    def __impressoes_finalizadas(self, impressora, indice):
        self.__log_impressora(f'{impressora} - Impressões finalizadas', indice)

    def __imprime_contador(self, indice, impressora, total_de_jobs):
        tempo_de_impressao = self.calcula_tempo_de_impressao_total(total_de_jobs)
        self.__log_impressora(f'{impressora} - Tempo estimado: {tempo_de_impressao} minutos', indice)

    def __log_impressora(self, info, screen_number: int) -> None:
        telas = {
            0: self._tela1,
            1: self._tela2
        }
        tela = telas[screen_number]
        tela.config(state='normal')
        tela.insert('end', f'{info}\n')
        tela.config(state='disabled')
    
    def __log_clear(self, screen_number: int) -> None:
        if not screen_number:
            tela = self._tela1
        else:
            tela = self._tela2
        tela.config(state='normal')
        tela.delete('0.0', 'end')
        tela.config(state='disabled')

    def __close_event(self):
        if self.monitorando:
            return

    @staticmethod
    def calcula_tempo_de_impressao_total(quantidade: int) -> str:
        total_seconds = (quantidade - 1) * 2
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes}:{seconds:02}"