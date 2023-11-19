from ttkbootstrap import Toplevel
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledText

from Modulos.imprimir import *
from Modulos.models.tabelas import *

__all__ = ['PainelDeLogs']


class PainelDeLogs(Toplevel):
    def __init__(self, impressoras: Impressao, tabelas: Tabelas, **kwargs):
        super(PainelDeLogs, self).__init__(
            title='Monitoramento de impressões', resizable=[False, False], topmost=True
        )

        self._incia_widgets(**kwargs.copy())
        self.servico_impressoras = impressoras
        self.__tabelas = tabelas
        self.monitorando = False

        self.protocol(self.wm_protocol()[0], self._close_event)

    def _incia_widgets(self, **kwargs):
        kwargs['state'] = DISABLED
        kwargs['wrap'] = WORD
        kwargs['bootstyle'] = ROUND
        kwargs['autohide'] = True
        self.geometry(f'800x500+{self.winfo_rootx() + 600}+{self.winfo_rooty()}')
        self.position_center()

        self._tela1 = ScrolledText(self, **kwargs)
        self._tela1.place(relx=0, rely=0, relheight=1, relwidth=0.5)

        self._tela2 = ScrolledText(self, **kwargs)
        self._tela2.place(relx=0.5, rely=0, relheight=1, relwidth=0.5)

    def start_monitoramento(self):
        self.monitorando = True
        self.__tabelas.inicia_tb_jobs_em_andamento()
        self.after(2000, self._monitoramento)

    def _monitoramento(self):
        jobs = self.servico_impressoras.printers_job_checker()
        self.__tabelas.update_tb_jobs_em_andamento(jobs)
        for indice, impressora in enumerate(
            self.servico_impressoras.get_lista_de_impresoras_em_uso(), start=1
        ):
            total_na_fila = self.__tabelas.get_total_jobs_em_andamento(impressora)
            try:
                self._log_clear(indice)
                if not total_na_fila:
                    self._impressoes_finalizadas(impressora, indice)
                    break
                self._imprime_contador(indice, impressora, total_na_fila)
                log = self.__tabelas.get_log_jobs_em_andamento(impressora)
                self._log_impressora(log, indice)
            except AttributeError:
                break

        if not jobs:
            self.after(3000, self.destroy)
            self.monitorando = False
            return

        self.after(2000, self._monitoramento)

    def _impressoes_finalizadas(self, impressora: str, indice: int):
        self._log_impressora(f'{impressora} - Impressões finalizadas', indice)

    def _imprime_contador(self, indice: int, impressora: str, total_de_jobs: int):
        tempo_de_impressao = self.calcula_tempo_de_impressao_total(total_de_jobs)
        self._log_impressora(
            f'{impressora} - Estimado: {tempo_de_impressao} min', indice
        )

    def _log_impressora(self, info: str, screen_number: int):
        tela = self._seleciona_tela(screen_number).text
        tela.config(state=NORMAL)
        tela.insert(END, f'{info}\n')
        tela.config(state=DISABLED)

    def _log_clear(self, screen_number: int):
        tela = self._seleciona_tela(screen_number).text
        tela.config(state=NORMAL)
        tela.delete('1.0', END)
        tela.config(state=DISABLED)

    def _seleciona_tela(self, screen_number: int) -> ScrolledText:
        return getattr(self, f'_tela{screen_number}')

    def _close_event(self):
        if self.monitorando:
            return
        else:
            self.destroy()

    @staticmethod
    def calcula_tempo_de_impressao_total(quantidade: int) -> str:
        total_seconds = (quantidade - 1) * 2
        minutes, seconds = divmod(total_seconds, 60)
        return f'{minutes:02}:{seconds:02}'
