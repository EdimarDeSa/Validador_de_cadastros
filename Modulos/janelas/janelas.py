import tkinter
from pathlib import Path
from threading import Thread
from tkinter.messagebox import showinfo, askyesno, showerror

from ttkbootstrap import *
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.style import Bootstyle

from Modulos.configuracoes import Configuracoes
from Modulos.imagens import Imagens
from Modulos.imprimir import Impressao
from Modulos.models import Tabelas
from Modulos.log_panel import LogPanel
from Modulos.models.produto import Produto
from Modulos.models.sorteio import Sorteio
from Modulos.constants import *


class CollapsingFrame(ScrolledFrame):
    """A collapsible frame widget that opens and closes with a click."""

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.columnconfigure(0, weight=1)
        self.cumulative_rows = 0

        # widget images
        self.images = Imagens()

    def add(self, child, title="", bootstyle=PRIMARY, **kwargs):
        """Add a child to the collapsible frame

        Parameters:

            child (Frame):
                The child frame to add to the widget.

            title (str):
                The title appearing on the collapsible section header.

            bootstyle (str):
                The style to apply to the collapsible section header.

            **kwargs (Dict):
                Other optional keyword arguments.
        """
        if child.winfo_class() != 'TFrame':
            return

        style_color = Bootstyle.ttkstyle_widget_color(bootstyle)
        frm = Frame(self, bootstyle=style_color)
        frm.grid(row=self.cumulative_rows, column=0, sticky=EW)

        # header title
        header = Label(master=frm, text=title, bootstyle=(style_color, INVERSE))
        if kwargs.get('textvariable'):
            header.configure(textvariable=kwargs.get('textvariable'))
        header.pack(side=LEFT, fill=BOTH, padx=10)

        # header toggle button
        def _func(c=child):
            return self._toggle_open_close(c)

        btn = Button(master=frm, image=self.images.img_seta_para_cima, bootstyle=style_color, command=_func)
        btn.pack(padx=(0, 10), side=RIGHT)

        if kwargs.get('edita_sorteio'):
            edita_sorteio = kwargs.get('edita_sorteio')
            edit = Button(
                master=frm, image=self.images.img_editar, bootstyle=style_color,
                command=lambda c=child: edita_sorteio(c)
            )
            edit.pack(padx=(0, 10), side=RIGHT)

        # assign toggle button to child so that it can be toggled
        child.btn = btn
        child.grid(row=self.cumulative_rows + 1, column=0, sticky=NSEW)

        # increment the row assignment
        self.cumulative_rows += 2

    def _toggle_open_close(self, child):
        """Open or close the section and change the toggle button
        image accordingly.

        Parameters:

            child (Frame):
                The child element to add or remove from grid manager.
        """
        if child.winfo_viewable():
            child.grid_remove()
            child.btn.configure(image=self.images.img_seta_para_direita)
        else:
            child.grid()
            child.btn.configure(image=self.images.img_seta_para_cima)


class JanelaPadrao:
    def __init__(self, master: Frame, configuracoes: Configuracoes, tabelas: Tabelas, impressao: Impressao = None, **kwargs):
        self.master = master
        self.configuracoes = configuracoes
        self.tabelas = tabelas
        self.impressao = impressao
        self.imagens = Imagens()
        self.reg_verifica_digito_numerico = master.register(self.verifica_digito_numerico)

    @staticmethod
    def verifica_digito_numerico(entrada: str):
        return entrada.isnumeric() or entrada == ''


# noinspection PyArgumentList
class JanelaSorteios(JanelaPadrao):
    def __init__(self, master: Frame, configuracoes, tabelas, **kwargs):
        super().__init__(master, configuracoes, tabelas)

        self.var_sorteio_atual: Sorteio = None
        self.tabela_de_produtos: Tableview = None
        self.var_caminho_sorteio = StringVar(value="Clique para procurar")
        self.var_caminho_tabela_de_precos = StringVar(value="Clique para procurar")
        self.var_formulario_de_produto_aberto = False
        self.var_sorteio_em_edicao = False
        self.var_lista_de_sorteios: list[Sorteio] = kwargs.get('list_sort')

        frame_produtos = Frame(master)
        frame_produtos.place(relx=0.005, rely=0.01, relheight=0.49, relwidth=0.99)
        self.inicia_ui_produtos(frame_produtos)

        self.frame_de_sorteios = Frame(master)
        self.frame_de_sorteios.place(relx=0.005, rely=0.51, relheight=0.49, relwidth=0.99)
        self.inicia_ui_sorteios(self.frame_de_sorteios)

        # Teste
        if kwargs.get('teste', False):
            for _ in range(8):
                for row in LINHAS_TESTE:
                    self.tabela_de_produtos.insert_row(values=list(row))
                self.tabela_de_produtos.load_table_data()
                self.salva_sorteio()

    def inicia_ui_produtos(self, master: Frame):
        self.tabela_de_produtos = Tableview(master, coldata=COLUNAS_DA_TELA_DE_SORTEIOS)
        self.tabela_de_produtos.place(relx=0, rely=0, relwidth=0.79, relheight=1)

        Button(
            master, text="Adicionar prêmio", command=self.abre_formulario_de_produto, style=DEFAULT
        ).place(relx=0.8, rely=0.1, relwidth=0.19)

        Button(
            master, text="Editar prêmio", command=self.editar_produto, style=INFO
        ).place(relx=0.8, rely=0.3, relwidth=0.19)

        Button(
            master, text="Salvar sorteio", command=self.salva_sorteio, style=SUCCESS
        ).place(relx=0.8, rely=0.55, relwidth=0.19)

        Button(
            master, text="Remover prêmio", command=self.remove_produto, style=DANGER
        ).place(relx=0.8, rely=0.8, relwidth=0.19)

    def inicia_ui_sorteios(self, master):
        self.tela_retratil_sorteios = CollapsingFrame(master)
        self.tela_retratil_sorteios.place(relx=0, rely=0, relwidth=0.79, relheight=1)

        self.var_sorteio_atual = Sorteio(self.tela_retratil_sorteios, self.checa_nome_do_sorteio)

        Button(
            master, text="Importar sorteios", state=DISABLED, style=PRIMARY
        ).place(relx=0.8, rely=0.3, relwidth=0.19)

        Button(
            master, text="Exportar sorteios", state=DISABLED, style=INFO
        ).place(relx=0.8, rely=0.5, relwidth=0.19)

    def abre_formulario_de_produto(
            self, codigo='', nome_do_produto='', quantidade='1', centro_de_custos='',
            data_de_fechamento_cc='', responsavel_pelo_cc='Marta Rosa Nunes', iid=None
    ):
        if self.var_formulario_de_produto_aberto:
            self.fechar_formulario_de_produto()
            self.abre_formulario_de_produto(
                codigo, nome_do_produto, quantidade, centro_de_custos, data_de_fechamento_cc, responsavel_pelo_cc
            )
            return

        self.var_formulario_de_produto_aberto = True
        self.top = Toplevel(
            title="Cadastro de produto", size=(800, 260), resizable=(False, False), transient=self.master
        )
        self.top.position_center()

        self.top.protocol("WM_DELETE_WINDOW", self.fechar_formulario_de_produto)

        # ------- PRIMEIRA LINHA ------- #

        Label(self.top, text="Código", **self.configuracoes.label_parametros).place(x=10, y=10)
        Entry(
            self.top, name='campo_codigo', validatecommand=(self.reg_verifica_digito_numerico, '%P'), validate='key',
            **self.configuracoes.entry_parametros
        ).place(x=10, y=40, width=200)
        self.top.children.get('campo_codigo').insert(0, codigo)
        self.top.children.get('campo_codigo').focus_set()
        self.top.children.get('campo_codigo').bind('<KeyRelease>', self.busca_produto)

        Label(self.top, text="Produto", **self.configuracoes.label_parametros).place(x=220, y=10)

        Entry(self.top, name='campo_nome_do_produto', **self.configuracoes.entry_parametros)
        self.top.children.get('campo_nome_do_produto').place(x=220, y=40, width=410)
        self.top.children.get('campo_nome_do_produto').insert(0, nome_do_produto)
        self.top.children.get('campo_nome_do_produto').bind('<Key>', self.verifica_info)

        Label(self.top, text="Quantidade", **self.configuracoes.label_parametros).place(x=640, y=10)
        Entry(self.top, name='campo_quantidade', validatecommand=(self.reg_verifica_digito_numerico, '%P'),
              validate='key',**self.configuracoes.entry_parametros)
        self.top.children.get('campo_quantidade').place(x=640, y=40, width=150)
        self.top.children.get('campo_quantidade').insert(0, quantidade)
        self.top.children.get('campo_quantidade').bind('<Key>', self.verifica_info)

        # ------- SEGUNDA LINHA ------- #

        Label(self.top, text="Centro de Custos", **self.configuracoes.label_parametros).place(x=10, y=110)
        Entry(self.top, name='campo_centro_de_custos', validatecommand=(self.reg_verifica_digito_numerico, '%P'),
              validate='key', **self.configuracoes.entry_parametros)
        self.top.children.get('campo_centro_de_custos').place(x=10, y=140, width=200)
        self.top.children.get('campo_centro_de_custos').insert(0, centro_de_custos)
        self.top.children.get('campo_centro_de_custos').bind('<Key>', self.verifica_info)

        Label(self.top, text="Data de fechamento CC", **self.configuracoes.label_parametros).place(x=220, y=110)
        data_inicial = datetime.strptime(data_de_fechamento_cc, '%d/%m/%Y') if data_de_fechamento_cc else None
        DateEntry(self.top, name='campo_data_de_fechamento_cc', startdate=data_inicial)
        self.top.children.get('campo_data_de_fechamento_cc').place(x=220, y=140)
        self.top.children.get('campo_data_de_fechamento_cc').bind('<Key>', self.verifica_info)

        Label(self.top, text="Responsável pelo CC", **self.configuracoes.label_parametros).place(x=430, y=110)
        Entry(self.top, name='campo_responsavel_pelo_cc', **self.configuracoes.entry_parametros)
        self.top.children.get('campo_responsavel_pelo_cc').place(x=440, y=140, width=350)
        self.top.children.get('campo_responsavel_pelo_cc').insert(0, responsavel_pelo_cc)
        self.top.children.get('campo_responsavel_pelo_cc').bind('<Key>', self.verifica_info)

        # ------- TERCEIRA LINHA ------- #
        Button(self.top, text="Adicionar", command=lambda _id=iid: self.salva_produto(_id)
               ).place(x=170, y=210, width=160)

        Button(self.top, text="Limpar", command=self.limpa_formulario_de_produto).place(x=500, y=210, width=160)

    def limpa_formulario_de_produto(self):
        self.top.children.get('campo_codigo').delete(0, END)
        self.top.children.get('campo_nome_do_produto').delete(0, END)
        self.top.children.get('campo_quantidade').delete(0, END)
        self.top.children.get('campo_centro_de_custos').delete(0, END)
        self.top.children.get('campo_data_de_fechamento_cc').entry.delete(0, END)
        self.top.children.get('campo_responsavel_pelo_cc').delete(0, END)

    def fechar_formulario_de_produto(self):
        self.var_formulario_de_produto_aberto = False
        self.top.destroy()

    def edita_sorteio(self, sorteio: Sorteio):
        iids = [iid.iid for iid in self.tabela_de_produtos.get_rows()]
        if iids:
            r = askyesno(
                'Prêmios em edição',
                'Existem prêmios em ediçõ ainda, tem certeza que continuar?\n'
                'Isso irá remover todos os prêmios atuais sem salva-los!'
            )
            if not r:
                return

        self.limpa_tabela_de_produtos()

        for obj_premio in sorteio.premios:
            premio = obj_premio.valores
            self.tabela_de_produtos.insert_row(values=premio)

        self.var_sorteio_atual = sorteio
        self.var_sorteio_em_edicao = True
        self.tabela_de_produtos.load_table_data()

    def salva_produto(self, iid=None, event: tkinter.Event = None):
        codigo = self.top.children.get('campo_codigo').get()
        if not codigo:
            self.informa_falta_de_dado('Código')
            self.top.children.get('campo_codigo').focus_set()
            return

        nome_do_produto = self.top.children.get('campo_nome_do_produto').get()
        if not nome_do_produto:
            self.informa_falta_de_dado('Nome do produto')
            self.top.children.get('campo_nome_do_produto').focus_set()
            return

        quantidade = self.top.children.get('campo_quantidade').get()
        if not quantidade:
            self.informa_falta_de_dado('Quantidade')
            self.top.children.get('campo_quantidade').focus_set()
            return

        cc = self.top.children.get('campo_centro_de_custos').get()
        if not cc:
            self.informa_falta_de_dado('Centro de Custo')
            self.top.children.get('campo_centro_de_custos').focus_set()
            return

        data_fechamento_cc = self.top.children.get('campo_data_de_fechamento_cc').entry.get()
        responsavel_cc = self.top.children.get('campo_responsavel_pelo_cc').get()
        if not responsavel_cc:
            self.informa_falta_de_dado('Responsável pelo cc')
            self.top.children.get('campo_responsavel_pelo_cc').focus_set()
            return

        valores = [codigo, nome_do_produto, quantidade, cc, data_fechamento_cc, responsavel_cc]
        if not iid:
            self.tabela_de_produtos.insert_row(values=valores)
        else:
            self.tabela_de_produtos.get_row(iid=iid).values = valores

        self.fechar_formulario_de_produto()
        self.tabela_de_produtos.load_table_data()

    def editar_produto(self):
        iids = self.get_iids_selecionados
        if not iids: return

        kwargs = dict(iid=iids[0])
        self.abre_formulario_de_produto(*self.tabela_de_produtos.get_row(**kwargs).values, **kwargs)

    def remove_produto(self):
        self.tabela_de_produtos.delete_rows(iids=self.get_iids_selecionados)

    def salva_sorteio(self):
        premios = [Produto(*linha.values) for linha in self.tabela_de_produtos.get_rows()]

        if not premios:
            self.informa_falta_de_dado('Prêmios')
            return

        self.var_sorteio_atual.atualiza_premios(premios)

        # Cria novo sorteio se não estiver em edição
        if not self.var_sorteio_em_edicao:
            self.tela_retratil_sorteios.add(
                self.var_sorteio_atual, self.checa_nome_do_sorteio, edita_sorteio=self.edita_sorteio
            )
            self.var_lista_de_sorteios.append(self.var_sorteio_atual)

        self.tabelas.add_sorteio(self.var_lista_de_sorteios)

        # Cria novo objeto de sorteio com nome sequencial à quantidade de sorteios
        self.var_sorteio_atual = Sorteio(self.tela_retratil_sorteios, self.checa_nome_do_sorteio)

        self.limpa_tabela_de_produtos()
        self.var_sorteio_em_edicao = False

    def limpa_tabela_de_produtos(self):
        iids = [iid.iid for iid in self.tabela_de_produtos.get_rows()]
        self.tabela_de_produtos.delete_rows(iids=iids)

    @property
    def get_iids_selecionados(self) -> list:
        return list(self.tabela_de_produtos.view.selection())

    @staticmethod
    def verifica_info(event: tkinter.Event):
        widget: Entry = event.widget
        if not widget.get():
            widget.config(bootstyle=DANGER)
        else:
            widget.config(bootstyle=DEFAULT)

    def busca_produto(self, event: tkinter.Event):
        codigo = event.widget.get()
        if len(codigo) < 7:
            return

        produto = self.tabelas.busca_produto(codigo)

        if produto is None:
            showerror('Planilha de produtos invalida', 'Planilha de produtos no formato inválido')

        self.top.children.get('campo_nome_do_produto').delete(0, END)
        self.top.children.get('campo_nome_do_produto').insert(0, '' if produto is 0 else produto.iloc[0])

    @property
    def checa_nome_do_sorteio(self):
        return f'Sorteio {len(self.var_lista_de_sorteios) + 1}'

    @staticmethod
    def informa_falta_de_dado(campo: str):
        showinfo('Faltam informações', f'É necessário preencher o campo: {campo}')


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

        self.var_total_de_cadastros = StringVar(value="Total de cadastros: -")
        self.var_inscricoes_validas = StringVar(value="Participantes válidos: -")
        self.var_cadastros_repetidos = StringVar(value="Cadastros repetidos: -")
        self.var_cpfs_invalidos = StringVar(value="CPFs inválidos: -")
        self.var_colaboradores_cadastrados = StringVar(value="Colaboradores cadastrados: -")
        self.var_caminho_inscritos = StringVar(value="Arquivo inscritos")
        self.var_caminho_colaboradores = StringVar(value="Arquivo colaboradores")
        self.var_cpf_sorteado = StringVar()

        self.inicia_ui_impressao(master)

        # Teste
        if kwargs.get('teste', False):
            date_entry: DateEntry = master.children.get('calendario')
            date_entry.entry.delete(0, END)
            date_entry.entry.insert(0, '28/09/2023')
            self.abre_tb_inscritos(Path('./data/9-28-2023-Evento_de_lancamentos-_Abril.csv').resolve())
            self.abre_tb_colaboradores(Path('./data/Colaboradores.csv').resolve())
            self.escreve_resultado_de_verificacao()

    def inicia_ui_impressao(self, master: Frame):
        for i in range(4):
            master.columnconfigure(i, minsize=250)
        master.columnconfigure(3, minsize=50)

        # ------------ Linha 1 ------------ #
        self.inicia_widget_impressora(master, 0.01, self.linha_1, 1)
        self.inicia_widget_impressora(master, 0.31, self.linha_1, 2)

        Label(master, text='Data do evento:', **self.configuracoes.label_parametros).place(relx=0.61, rely=self.linha_1)
        DateEntry(master, name='calendario').place(relx=0.73, rely=self.linha_1 - 0.01)

        # ------------ Linha 2 ------------ #
        self.inicia_widgets_de_variaveis(master, self.var_total_de_cadastros, 0.01, self.linha_2)
        self.inicia_widgets_de_variaveis(master, self.var_inscricoes_validas, 0.51, self.linha_2)

        # ------------ Linha 3 ------------ #
        self.inicia_widgets_de_variaveis(master, self.var_cadastros_repetidos, 0.01, self.linha_3)
        self.inicia_widgets_de_variaveis(master, self.var_cpfs_invalidos, 0.34, self.linha_3)
        self.inicia_widgets_de_variaveis(master, self.var_colaboradores_cadastrados, 0.67, self.linha_3)

        # ------------ Linha 4 ------------ #
        self.inicia_widget_localizazao_de_arquivo(master, self.var_caminho_inscritos, self.linha_4,
                                                  self.abre_tb_inscritos)

        # ------------ Linha 5 ------------ #
        self.inicia_widget_localizazao_de_arquivo(master, self.var_caminho_colaboradores, self.linha_5,
                                                  self.abre_tb_colaboradores)

        # ------------ Linha 6 ------------ #
        Button(master, name='bt_inicia_verificacao', text="Verifica cadastros",
               command=self.escreve_resultado_de_verificacao)
        Button(master, name='bt_inicia_impressao', text="Iniciar impressão",
               command=self.inicia_thread_impressao)

    def inicia_widgets_de_variaveis(self, master, var_text, relx, rely):
        Label(master, textvariable=var_text, **self.configuracoes.label_parametros).place(relx=relx, rely=rely)

    def inicia_widget_impressora(self, master: Frame, relx: float, rely: float, numero: int):
        Label(master, text=f'Impressora {numero}:', **self.configuracoes.label_parametros).place(relx=relx, rely=rely)

        impressora = Combobox(master, values=self.impressao.listar_impressoras())
        impressora.place(relx=relx + 0.1, rely=rely - 0.015)
        impressora.bind('<<ComboboxSelected>>', self.ao_selecionra_impressora)
        impressora.bind('<<Enter>>', self.ao_selecionra_impressora)

    def inicia_widget_localizazao_de_arquivo(self, master: Frame, var, linha, comando):
        Label(master, textvariable=var, **self.configuracoes.label_caminho_parametros).place(relx=0.01, rely=linha)
        Button(master, image=self.imagens.img_lupa, command=comando, text='Procurar').place(relx=0.86, rely=linha)

    def ao_selecionra_impressora(self, event: tkinter.Event):
        widget: Combobox = event.widget
        nome_da_impressora = widget.get()
        numero_impressora = widget.winfo_name()
        self.impressao.set_printer(numero_impressora, nome_da_impressora)

    def escreve_resultado_de_verificacao(self):
        self.tabelas.verifica_cadastros()

        self.var_cadastros_repetidos.set(f"Cadastros repetidos: {self.tabelas.get_total_cadastros_repetidos}")

        self.var_cpfs_invalidos.set(f"CPFs inválidos: {self.tabelas.get_total_cpfs_invalidos}")

        self.var_colaboradores_cadastrados.set(
            f"Colaboradores cadasrtados: {self.tabelas.get_total_colaboradores_cadastrados}")

        self.var_inscricoes_validas.set(f"Participantes válidos: {self.tabelas.get_total_inscricoes_validas}")

        self.master.after(500, lambda: self.master.children.get('bt_inicia_impressao').place(relx=0.26, rely=self.linha_6))

    def abre_tb_inscritos(self, caminho=None):

        self.tabelas.inicia_tb_inscritos(self.master.children.get('calendario').entry.get(), caminho)

        caminho: Path = self.tabelas.get_caminho_tb_inscritos
        if not caminho:
            return

        self.var_caminho_inscritos.set(self.ajusta_caminho(caminho))
        self.var_total_de_cadastros.set(f"Total de cadastros: {self.tabelas.get_total_inscritos}")

        self.master.children.get('bt_inicia_impressao').place_forget()
        self.master.children.get('bt_inicia_verificacao').place(relx=0.01, rely=self.linha_6)

    def abre_tb_colaboradores(self, caminho=None):
        self.tabelas.inicia_tb_colaboradores(caminho)

        caminho = self.tabelas.get_caminho_tb_colaboradores
        if not caminho:
            return

        self.var_caminho_colaboradores.set(self.ajusta_caminho(caminho))

    def inicia_thread_impressao(self):
        if not self.impressao.get_lista_de_impresoras_em_uso():
            return showinfo("Impressora", "Selecione uma impressora.")

        Thread(target=self.inicia_impressao, daemon=True).start()
        self.master.children.get('bt_inicia_impressao').place_forget()
        self.master.children.get('bt_inicia_verificacao').place_forget()

    def inicia_impressao(self):
        log_panel = LogPanel(self.impressao, self.tabelas, **self.configuracoes.label_parametros)
        log_panel.start_monitoramento()

        self.impressao.enviar_tabela_para_impressora(self.tabelas.get_tb_inscricoes_validas)

    @staticmethod
    def ajusta_caminho(caminho: Path) -> str:
        caminho_ajustado = str(caminho)
        if len(caminho_ajustado) > 100:
            caminho_ajustado = "..." + caminho_ajustado[-99:]

        return caminho_ajustado


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
            command=lambda s=self.lista_de_sorteios :self.tabelas.exportar_relatorio_vencedores(s)
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
                ).grid(row=i+1, column=0, pady=5, sticky=W)

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

    def busca_participante(self, e: tkinter.Event):
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
