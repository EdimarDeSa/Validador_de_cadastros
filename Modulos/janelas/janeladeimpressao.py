from pathlib import Path
from threading import Thread
from tkinter import Event

from ttkbootstrap import Button, Combobox, DateEntry, Entry, Frame, Label, StringVar
from ttkbootstrap.dialogs import Messagebox

from Modulos.constants import *
from Modulos.janelas.janelapadrao import *
from Modulos.janelas.paineldelogs import *

__all__ = ['JanelaImpressao']


class JanelaImpressao(JanelaPadrao):
    pula_linha = 0.15
    linha_1 = 0.02
    linha_2 = linha_1 + pula_linha
    linha_3 = linha_2 + pula_linha
    linha_4 = linha_3 + pula_linha
    linha_5 = linha_4 + pula_linha
    linha_6 = linha_5 + pula_linha

    def __init__(self, master: Frame, configuracoes, tabelas, impressao, **kwargs):
        super().__init__(master, configuracoes, tabelas, impressao)

        self.var_total_de_cadastros = StringVar(value='Total de cadastros: -')
        self.var_inscricoes_validas = StringVar(value='Participantes válidos: -')
        self.var_cadastros_repetidos = StringVar(value='Cadastros repetidos: -')
        self.var_cpfs_invalidos = StringVar(value='CPFs inválidos: -')
        self.var_colaboradores_cadastrados = StringVar(
            value='Colaboradores cadastrados: -'
        )
        self.var_caminho_inscritos = StringVar(value='Arquivo inscritos')
        self.var_caminho_colaboradores = StringVar(value='Arquivo colaboradores')
        self.var_cpf_sorteado = StringVar()

        self.inicia_ui_impressao(master)

        # Teste
        if kwargs.get('teste', False):
            date_entry: Entry = master.children.get('calendario').entry
            date_entry.delete(0, END)
            date_entry.insert(0, '28/09/2023')
            self.abre_tb_inscritos(
                Path('./data/9-28-2023-Evento_de_lancamentos-_Abril.csv').resolve()
            )
            self.abre_tb_colaboradores(Path('./data/Colaboradores.csv').resolve())
            self.escreve_resultado_de_verificacao()

    def inicia_ui_impressao(self, master: Frame):
        for i in range(4):
            master.columnconfigure(i, minsize=250)
        master.columnconfigure(3, minsize=50)

        # ------------ Linha 1 ------------ #
        self.inicia_widget_impressora(master, 0.01, self.linha_1, 1)
        self.inicia_widget_impressora(master, 0.31, self.linha_1, 2)

        Label(
            master, text='Data do evento:', **self.configuracoes.label_parametros
        ).place(relx=0.61, rely=self.linha_1)
        DateEntry(master, name='calendario').place(relx=0.73, rely=self.linha_1 - 0.01)

        # ------------ Linha 2 ------------ #
        self.inicia_widgets_de_variaveis(
            master, self.var_total_de_cadastros, 0.01, self.linha_2
        )
        self.inicia_widgets_de_variaveis(
            master, self.var_inscricoes_validas, 0.51, self.linha_2
        )

        # ------------ Linha 3 ------------ #
        self.inicia_widgets_de_variaveis(
            master, self.var_cadastros_repetidos, 0.01, self.linha_3
        )
        self.inicia_widgets_de_variaveis(
            master, self.var_cpfs_invalidos, 0.34, self.linha_3
        )
        self.inicia_widgets_de_variaveis(
            master, self.var_colaboradores_cadastrados, 0.67, self.linha_3
        )

        # ------------ Linha 4 ------------ #
        self.inicia_widget_localizazao_de_arquivo(
            master, self.var_caminho_inscritos, self.linha_4, self.abre_tb_inscritos
        )

        # ------------ Linha 5 ------------ #
        self.inicia_widget_localizazao_de_arquivo(
            master,
            self.var_caminho_colaboradores,
            self.linha_5,
            self.abre_tb_colaboradores,
        )

        # ------------ Linha 6 ------------ #
        Button(
            master,
            name='bt_inicia_verificacao',
            text='Verifica cadastros',
            command=self.escreve_resultado_de_verificacao,
        )
        Button(
            master,
            name='bt_inicia_impressao',
            text='Iniciar impressão',
            command=self.inicia_thread_impressao,
        )

    def inicia_widgets_de_variaveis(self, master, var_text, relx, rely):
        Label(
            master, textvariable=var_text, **self.configuracoes.label_parametros
        ).place(relx=relx, rely=rely)

    def inicia_widget_impressora(
        self, master: Frame, relx: float, rely: float, numero: int
    ):
        Label(
            master, text=f'Impressora {numero}:', **self.configuracoes.label_parametros
        ).place(relx=relx, rely=rely)

        impressora = Combobox(master, values=self.impressao.listar_impressoras())
        impressora.place(relx=relx + 0.1, rely=rely - 0.015)
        impressora.bind('<<ComboboxSelected>>', self.ao_selecionra_impressora)
        impressora.bind('<<Enter>>', self.ao_selecionra_impressora)

    def inicia_widget_localizazao_de_arquivo(self, master: Frame, var, linha, comando):
        Label(
            master, textvariable=var, **self.configuracoes.label_caminho_parametros
        ).place(relx=0.01, rely=linha)
        Button(
            master, image=self.imagens.img_lupa, command=comando, text='Procurar'
        ).place(relx=0.86, rely=linha)

    def ao_selecionra_impressora(self, event: Event):
        widget: Combobox = event.widget
        nome_da_impressora = widget.get()
        numero_impressora = widget.winfo_name()
        self.impressao.set_printer(numero_impressora, nome_da_impressora)

    def escreve_resultado_de_verificacao(self):
        self.tabelas.verifica_cadastros()

        self.var_cadastros_repetidos.set(
            f'Cadastros repetidos: {self.tabelas.get_total_cadastros_repetidos}'
        )

        self.var_cpfs_invalidos.set(
            f'CPFs inválidos: {self.tabelas.get_total_cpfs_invalidos}'
        )

        self.var_colaboradores_cadastrados.set(
            f'Colaboradores cadasrtados: {self.tabelas.get_total_colaboradores_cadastrados}'
        )

        self.var_inscricoes_validas.set(
            f'Participantes válidos: {self.tabelas.get_total_inscricoes_validas}'
        )

        self.master.after(
            500,
            lambda: self.master.children.get('bt_inicia_impressao').place(
                relx=0.26, rely=self.linha_6
            ),
        )

    def abre_tb_inscritos(self, caminho=None):

        self.tabelas.inicia_tb_inscritos(
            self.master.children.get('calendario').entry.get(), caminho
        )

        caminho: Path = self.tabelas.get_caminho_tb_inscritos
        if not caminho:
            return

        self.var_caminho_inscritos.set(self.ajusta_caminho(caminho))
        self.var_total_de_cadastros.set(
            f'Total de cadastros: {self.tabelas.get_total_inscritos}'
        )

        self.master.children.get('bt_inicia_impressao').place_forget()
        self.master.children.get('bt_inicia_verificacao').place(
            relx=0.01, rely=self.linha_6
        )

    def abre_tb_colaboradores(self, caminho=None):
        self.tabelas.inicia_tb_colaboradores(caminho)

        caminho = self.tabelas.get_caminho_tb_colaboradores
        if not caminho:
            return

        self.var_caminho_colaboradores.set(self.ajusta_caminho(caminho))

    def inicia_thread_impressao(self):
        if not self.impressao.get_lista_de_impresoras_em_uso():
            Messagebox.show_warning(
                title='Impressora', message='Selecione uma impressora.'
            )
            return

        Thread(target=self.inicia_impressao, daemon=True).start()
        self.master.children.get('bt_inicia_impressao').place_forget()
        self.master.children.get('bt_inicia_verificacao').place_forget()

    def inicia_impressao(self):
        log_panel = PainelDeLogs(
            self.impressao, self.tabelas, **self.configuracoes.label_parametros
        )
        log_panel.start_monitoramento()

        self.impressao.enviar_tabela_para_impressora(
            self.tabelas.get_tb_inscricoes_validas
        )

    @staticmethod
    def ajusta_caminho(caminho: Path) -> str:
        caminho_ajustado = str(caminho)
        if len(caminho_ajustado) > 100:
            caminho_ajustado = '...' + caminho_ajustado[-99:]

        return caminho_ajustado
