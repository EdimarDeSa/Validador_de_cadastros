from tkinter import Event

from ttkbootstrap import Label, Frame, Button, Separator, Entry
from ttkbootstrap.scrolled import ScrolledFrame

from Modulos.janelas.janelapadrao import *
from Modulos.models import *
from Modulos.constants import *


__all__ = ['JanelaRegistroDeVencedor']


class JanelaRegistroDeVencedor(JanelaPadrao):
    def __init__(self, master: Frame, configuracoes, tabelas, **kwargs):
        super().__init__(master, configuracoes, tabelas)

        self.lista_de_sorteios: list[Sorteio] = kwargs.get('list_sort')
        self.form_vencedor = Frame(master)
        self.form_vencedor.place(relx=0, rely=0, relwidth=0.48, relheight=1)
        self._configura_formulario_de_vencedor(self.form_vencedor)

        Separator(master, orient=VERTICAL).place(relx=0.49, rely=0, relwidth=0.02, relheight=1)

        self.form_sorteios = ScrolledFrame(master, autohide=True)
        self.form_sorteios.place(relx=0.52, rely=0, relwidth=0.48, relheight=1)

        master.bind('<Expose>', self._atualiza_sorteios)

        # Teste
        if kwargs.get('teste', False):
            pass

    def _configura_formulario_de_vencedor(self, master: Frame):
        Label(
            master, text='Busca de participante', anchor=CENTER, **self.configuracoes.label_titulos
        ).place(relx=0, rely=0.01, relwidth=1)

        conf_entrys = self.configuracoes.entry_parametros.copy()
        conf_entrys['state'] = READONLY

        Label(master, text='CPF:', **self.configuracoes.label_parametros).place(relx=0.01, rely=0.105)
        Entry(
            master, name='entry_cpf', **self.configuracoes.entry_parametros, validate='key',
            validatecommand=(self.reg_verifica_digito_numerico, '%P')
        ).place(relx=0.2, rely=0.1, relwidth=0.75)

        Label(
            master, name='frame_info', anchor=CENTER, **self.configuracoes.label_caminho_parametros
        ).place(relx=0.01, rely=0.205, relwidth=1)

        Label(master, text='Nome:', **self.configuracoes.label_parametros).place(relx=0.01, rely=0.305)
        Entry(master, name='entry_nome', **conf_entrys).place(relx=0.2, rely=0.3, relwidth=0.75)

        Label(master, text='CEP:', **self.configuracoes.label_parametros).place(relx=0.01, rely=0.405)
        Entry(master, name='entry_cep', **conf_entrys).place(relx=0.2, rely=0.4, relwidth=0.75)

        Label(master, text='Endereço:', **self.configuracoes.label_parametros).place(relx=0.01, rely=0.505)
        Entry(master, name='entry_endereco', **conf_entrys).place(relx=0.2, rely=0.5, relwidth=0.75)

        Label(master, text='Email:', **self.configuracoes.label_parametros).place(relx=0.01, rely=0.605)
        Entry(master, name='entry_email', **conf_entrys).place(relx=0.2, rely=0.6, relwidth=0.75)

        Label(master, text='Telefone:', **self.configuracoes.label_parametros).place(relx=0.01, rely=0.705)
        Entry(master, name='entry_telefone', **conf_entrys).place(relx=0.2, rely=0.7, relwidth=0.75)

        self.btn_salvar = Button(master, text='Salvar', bootstyle=SUCCESS)
        self.btn_salvar.place(relx=0.1, rely=0.85, relwidth=0.3)

        Button(
            master, text='Exportar relatório', bootstyle=(SUCCESS, OUTLINE),
            command=lambda s=self.lista_de_sorteios: self.tabelas.exportar_relatorio_vencedores(s)
        ).place(relx=0.6, rely=0.85, relwidth=0.3)

        master.children.get('entry_cpf').focus_set()
        master.children.get('entry_cpf').bind('<KeyRelease>', self.busca_participante)

    def _atualiza_sorteios(self, _):
        self.deleta_form_sorteios()
        if not self.lista_de_sorteios:
            return

        for sorteio in self.lista_de_sorteios:
            nome_sorteio = sorteio.nome_do_sorteio

            subframe = Frame(self.form_sorteios, name=f'frame_{nome_sorteio.lower()}')
            subframe.pack(fill=BOTH, expand=True, ipady=10)
            subframe.columnconfigure(0, weight=1)

            titulo = nome_sorteio if not sorteio.nome_vencedor else f'{nome_sorteio} - {sorteio.nome_vencedor}'
            Label(
                subframe, text=titulo, name=f'label_{nome_sorteio.lower()}', **self.configuracoes.label_titulos
            ).grid(row=0, columnspan=2)

            for i, premio in enumerate(sorteio.premios):
                Label(
                    subframe, text=premio.valores[1], justify=LEFT, **self.configuracoes.label_parametros
                ).grid(row=i + 1, column=0, pady=5, sticky=W)

            bt_row = (len(sorteio.premios) + 1) // 2
            Button(
                subframe, text=f'Abrir {nome_sorteio}', command=lambda s=nome_sorteio: self._selecionar_sorteado(s)
            ).grid(row=bt_row, column=1, padx=(0, 20))

            Separator(self.form_sorteios, orient=HORIZONTAL).pack(fill=X, expand=True, ipady=3, anchor=CENTER)

    def reseta_widgets(self):
        for child in self.form_sorteios.winfo_children():
            self._reset_widgets(child)

    def _reset_widgets(self, widget):
        widget.configure(bootstyle=DEFAULT)
        for child in widget.winfo_children():
            self._reset_widgets(child)

    @staticmethod
    def _set_selected_style(widget):
        widget.configure(bootstyle=INFO)

    def _selecionar_sorteado(self, nome_sorteio):
        self.reseta_widgets()

        sorteio_widgets = self.form_sorteios.children.get(f'frame_{nome_sorteio.lower()}')
        if sorteio_widgets:
            for child in sorteio_widgets.winfo_children():
                self._set_selected_style(child)

        self.btn_salvar.configure(command=lambda n=nome_sorteio: self._registra_vencedor(n))

    def deleta_form_sorteios(self):
        def deleta_tela(c):
            for sub_c in c.winfo_children():
                deleta_tela(sub_c)
            c.destroy()

        for child in self.form_sorteios.winfo_children():
            deleta_tela(child)

    def _registra_vencedor(self, nome_sorteio: str):
        frame_sorteio = self.form_sorteios.children.get(f'frame_{nome_sorteio.lower()}')
        nome_ganhador = self._sorteado[0]
        frame_sorteio.children.get(f'label_{nome_sorteio.lower()}').configure(text=f'{nome_sorteio} - {nome_ganhador}')
        for sorteio in self.lista_de_sorteios:
            if sorteio.nome_do_sorteio == nome_sorteio:
                sorteio.registra_vencedor(self._sorteado)

        self._limpa_formulario_de_vencedor()
        self.btn_salvar.configure(command='')
        self.reseta_widgets()

    def busca_participante(self, e: Event):
        cpf = e.widget.get()
        if len(cpf) < 11:
            return

        self.form_vencedor.children.get('frame_info').configure(text='Procurando...')
        participante = self.tabelas.busca_vencedor(cpf)
        if participante.any():
            self.form_vencedor.children.get('frame_info').configure(text='')
            dados = participante[0]
            self._altera_texto('entry_nome', dados[0])
            self._altera_texto('entry_cep', dados[8])
            self._altera_texto('entry_endereco', dados[2])
            self._altera_texto('entry_email', dados[3])
            self._altera_texto('entry_telefone', dados[5])
            self._sorteado = participante[0]

    def _altera_texto(self, w_name, data):
        self.form_vencedor.children.get(w_name).configure(state=NORMAL)
        self.form_vencedor.children.get(w_name).delete(0, END)
        self.form_vencedor.children.get(w_name).insert(0, data)
        self.form_vencedor.children.get(w_name).configure(state=READONLY)

    def _limpa_formulario_de_vencedor(self):
        self.form_vencedor.children.get('entry_cpf').delete(0, END)
        self._altera_texto('entry_nome', '')
        self._altera_texto('entry_cep', '')
        self._altera_texto('entry_endereco', '')
        self._altera_texto('entry_email', '')
        self._altera_texto('entry_telefone', '')
