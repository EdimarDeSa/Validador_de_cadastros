from pathlib import Path
from threading import Thread
import tkinter
from tkinter.messagebox import showinfo

from ttkbootstrap import *
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.tooltip import ToolTip
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.style import Bootstyle

from Modulos.log_panel import LogPanel
from Modulos.configuracoes import Configuracoes
from Modulos.imprimir import Impressao
from Modulos.models.produto import Produto
from Modulos.models.sorteio import Sorteio
from Modulos.constants import *
from Modulos.imagens import Imagens


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
        frm = ttk.Frame(self, bootstyle=style_color)
        frm.grid(row=self.cumulative_rows, column=0, sticky=EW)

        # header title
        header = Label(
            master=frm,
            text=title,
            bootstyle=(style_color, INVERSE)
        )
        if kwargs.get('textvariable'):
            header.configure(textvariable=kwargs.get('textvariable'))
        header.pack(side=LEFT, fill=BOTH, padx=10)

        # header toggle button
        def _func(c=child): return self._toggle_open_close(c)
        btn = ttk.Button(
            master=frm,
            image=self.images.img_seta_para_cima,
            bootstyle=style_color,
            command=_func
        )
        btn.pack(side=RIGHT)

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
            child.btn.configure(image=self.images.img_seta_para_cima)
        else:
            child.grid()
            child.btn.configure(image=self.images.img_seta_para_direita)


class JanelaPadrao:
    def __init__(self, master: Frame, configuracoes: Configuracoes, tabelas, impressao: Impressao):
        self.master = master
        self.configuracoes = configuracoes
        self.tabelas = tabelas
        self.impressao = impressao
        self.imagens = Imagens()


# noinspection PyArgumentList
class JanelaSorteios(JanelaPadrao):
    def __init__(self, master: Frame, configuracoes, tabelas, impressao):
        super().__init__(master, configuracoes, tabelas, impressao)

        self.var_caminho_sorteio = StringVar(value="Clique para procurar")
        self.var_caminho_tabela_de_precos = StringVar(value="Clique para procurar")
        self.var_sorteio_atual = StringVar()
        self.var_formulario_de_produto_aberto = False

        frame_produtos = Frame(master)
        frame_produtos.place(relx=0.005, rely=0.01, relheight=0.49, relwidth=0.99)
        self.inicia_frame_produtos(frame_produtos)

        self.lista_de_sorteios = CollapsingFrame(master)
        self.lista_de_sorteios.place(relx=0.005, rely=0.51, relheight=0.49, relwidth=0.99)
        self.inicia_frame_registro_sorteio(self.lista_de_sorteios)

        # self.atualiza_sorteio_atual()
        # self.sorteio_atual: Sorteio = Sorteio(self.var_sorteio_atual.get())

    def inicia_frame_registro_sorteio(self, master):
        self.lista_de_sorteios.add(Frame(self.lista_de_sorteios), 'Sorteio 1')

    def inicia_frame_produtos(self, master: Frame):
        colunas = [
            dict(text="Código", width=80, stretch=False),
            dict(text="Nome", width=400, stretch=False),
            dict(text="Qtd", width=50, stretch=False),
            dict(text="CC", width=80, stretch=False),
            dict(text="Fechamento CC", width=120, stretch=False),
            dict(text="Responsável CC", width=250, stretch=False),
        ]

        data = [
            [
                "00000000000",
                "Produto 1",
                "1",
                "12345",
                "12/01/24",
                "Marta Rosa Nunes",
            ],
            (
                "00000000000",
                "Produto 2",
                "1",
                "12345",
                "12/01/24",
                "Marta Rosa Nunes",
            ),
            (
                "00000000000",
                "Produto 3",
                "1",
                "12345",
                "12/01/24",
                "Marta Rosa Nunes",
            ),
            (
                "00000000000",
                "Produto 4",
                "1",
                "12345",
                "12/01/24",
                "Marta Rosa Nunes",
            ),
            (
                "00000000000",
                "Produto 5",
                "1",
                "12345",
                "12/01/24",
                "Marta Rosa Nunes",
            ),
            (
                "00000000000",
                "Produto 6",
                "1",
                "12345",
                "12/01/24",
                "Marta Rosa Nunes",
            ),
        ]
        self.tabela_de_produtos = Tableview(
            master, coldata=colunas, rowdata=data, stripecolor=('#78c2ad', None), delimiter=";"
        )

        self.tabela_de_produtos.place(relx=0, rely=0, relwidth=0.79, relheight=1)

        Button(
            master, text="Adicionar produto", command=self.formulario_de_criacao_de_produto,
        ).place(relx=0.8, rely=0.3, relwidth=0.19)

        Button(
            master, text="Remover produto", command=self.remove_produto
        ).place(relx=0.8, rely=0.6, relwidth=0.19)

    def formulario_de_criacao_de_produto(self):
        if self.var_formulario_de_produto_aberto:
            return

        self.var_formulario_de_produto_aberto = True
        self.top = Toplevel(
            title="Cadastro de produto",
            size=(800, 260),
            resizable=(False, False),
        )

        reg_verifica_digito_numerico = self.top.register(self.verifica_digito_numerico)

        self.top.protocol("WM_DELETE_WINDOW", self.fechar_formulario_de_produto)
        self.top.bind('<FocusIn>', self.verifica_info)
        self.top.bind('<Key>', self.verifica_info)

        # ------- PRIMEIRA LINHA ------- #

        Label(self.top, text="Código", **self.configuracoes.label_parametros).place(
            x=10, y=10
        )
        self.codigo = Entry(
            self.top, validatecommand=(reg_verifica_digito_numerico, '%P'), validate='key',
            **self.configuracoes.entry_parametros
        )
        self.codigo.place(x=10, y=40, width=200)
        ToolTip(self.codigo, text='Para procurar o produto aperte o "ENTER"')

        Label(self.top, text="Produto", **self.configuracoes.label_parametros).place(
            x=220, y=10
        )
        self.nome_do_produto = Entry(self.top, **self.configuracoes.entry_parametros)
        self.nome_do_produto.place(x=220, y=40, width=410)

        Label(self.top, text="Quantidade", **self.configuracoes.label_parametros).place(x=640, y=10)
        self.quantidade = Entry(
            self.top, validatecommand=(reg_verifica_digito_numerico, '%P'), validate='key',
            **self.configuracoes.entry_parametros
        )
        self.quantidade.place(x=640, y=40, width=150)
        self.quantidade.insert(0, '1')

        # ------- SEGUNDA LINHA ------- #

        Label(self.top, text="Centro de Custos", **self.configuracoes.label_parametros).place(x=10, y=110)
        self.centro_de_custos = Entry(
            self.top, validatecommand=(reg_verifica_digito_numerico, '%P'), validate='key',
            **self.configuracoes.entry_parametros
        )
        self.centro_de_custos.place(x=10, y=140, width=200)
        self.centro_de_custos.insert(0, "23504")

        Label(self.top, text="Data de fechamento CC", **self.configuracoes.label_parametros).place(x=220, y=110)
        self.data_de_fechamento_cc = DateEntry(
            self.top
        )
        self.data_de_fechamento_cc.place(x=220, y=140)

        Label(self.top, text="Responsável pelo CC", **self.configuracoes.label_parametros).place(x=430, y=110)
        self.responsavel_pelo_cc = Entry(self.top, **self.configuracoes.entry_parametros)
        self.responsavel_pelo_cc.place(x=440, y=140, width=350)
        self.responsavel_pelo_cc.insert(0, "Marta Rosa Nunes")

        # ------- TERCEIRA LINHA ------- #

        Button(self.top, text="Adicionar", command=self.salva_produto).place(
            x=170, y=210, width=160
        )

        Button(self.top, text="Limpar", command=self.limpa_formulario_de_produto).place(
            x=500, y=210, width=160
        )

    def limpa_formulario_de_produto(self):
        self.codigo.delete(0, END)
        self.nome_do_produto.delete(0, END)
        self.quantidade.delete(0, END)
        self.centro_de_custos.delete(0, END)
        self.data_de_fechamento_cc.entry.delete(0, END)
        self.responsavel_pelo_cc.delete(0, END)
    
    def fechar_formulario_de_produto(self):
        self.var_formulario_de_produto_aberto = False
        self.top.destroy()

    @staticmethod
    def informa_falta_de_dado(campo: str):
        showinfo('Faltam informações', f'É necessário preencher o campo: {campo}')

    def salva_produto(self):
        codigo = self.codigo.get()
        nome_do_produto = self.nome_do_produto.get()
        quantidade = self.quantidade.get()
        cc = self.centro_de_custos.get()
        data_fechamento_cc = self.data_de_fechamento_cc.entry.get()
        responsavel_cc = self.responsavel_pelo_cc.get()

        if not codigo:
            self.informa_falta_de_dado('Código')
            self.codigo.focus_set()
            return

        if not nome_do_produto:
            self.informa_falta_de_dado('Nome do produto')
            self.nome_do_produto.focus_set()
            return

        if not quantidade:
            self.informa_falta_de_dado('Quantidade')
            self.quantidade.focus_set()
            return

        if not cc:
            self.informa_falta_de_dado('Centro de Custo')
            self.centro_de_custos.focus_set()
            return

        if not responsavel_cc:
            self.informa_falta_de_dado('Responsável pelo cc')
            self.responsavel_pelo_cc.focus_set()
            return

        self.tabela_de_produtos.insert_row(
            values=[
                codigo,
                nome_do_produto,
                quantidade,
                cc,
                data_fechamento_cc,
                responsavel_cc,
            ]
        )
        
        self.fechar_formulario_de_produto()
        self.tabela_de_produtos.load_table_data()

    def remove_produto(self):
        iids = self.tabela_de_produtos.view.selection()
        self.tabela_de_produtos.delete_rows(iids=iids)
    
    def salva_premio(self):
        codigo = self.codigo.get()
        nome = self.nome.get()
        quantidade = self.quantidade.get() if self.quantidade.get() else "1"
        cc = self.cc.get() if self.cc.get() else "23504"
        data_fechamento_cc = (
            self.data_fechamento_cc.get()
            if self.data_fechamento_cc.get()
            else "Não fecha"
        )
        responsavel_cc = (
            self.responsavel_cc.get()
            if self.responsavel_cc.get()
            else "Marta Rosa Nunes"
        )

        if not codigo or not nome:
            return showinfo(
                "Informação necessária",
                "É necessário que todas as informações do produto sejam preenchidas",
            )

        produto = Produto(
            codigo, nome, quantidade, cc, data_fechamento_cc, responsavel_cc
        )
        self.sorteio_atual.registra_premio(produto)

        self.frame_produtos.add_linha(nome, produto)

    def salva_sorteio(self):
        pass

    def editar_produto(self):
        pass

    def deletar_produto(self):
        pass

    def verifica_digito(self, event):
        codigo = self.codigo.get()
        if not str(event.char).isnumeric() and event.char not in (
            "",
            "\t",
            "\r",
            "\n",
            "\x08",
        ):
            self.codigo.after(10, lambda: self.codigo.delete(len(codigo) - 1))

        if len(codigo) > 8:
            self.procura_produto(codigo)

    def procura_produto(self, codigo):
        produto = codigo
        return produto

    def atualiza_sorteio_atual(self, atual=1):
        self.var_sorteio_atual.set(f"Editando o sorteio {atual}")

    def verifica_digito_numerico(self, entrada: str):
        return entrada.isnumeric()

    @staticmethod
    def verifica_info(event: tkinter.Event):
        widget: Entry = event.widget
        if isinstance(widget, Entry):
            info = widget.get()
            if not info:
                widget.config(bootstyle=DANGER)
            else:
                widget.config(bootstyle=DEFAULT)


class JanelaImpressao(JanelaPadrao):
    pula_linha = 0.15
    linha_1 = 0.02
    linha_2 = linha_1 + pula_linha
    linha_3 = linha_2 + pula_linha
    linha_4 = linha_3 + pula_linha
    linha_5 = linha_4 + pula_linha
    linha_6 = linha_5 + pula_linha

    def __init__(self, master: Frame, configuracoes, tabelas, impressao):
        self.root = master

        super().__init__(self.root, configuracoes, tabelas, impressao)

        self.var_total_de_cadastros = StringVar(value="Total de cadastros: -")
        self.var_inscricoes_validas = StringVar(value="Participantes válidos: -")
        self.var_cadastros_repetidos = StringVar(value="Cadastros repetidos: -")
        self.var_cpfs_invalidos = StringVar(value="CPFs inválidos: -")
        self.var_colaboradores_cadastrados = StringVar(value="Colaboradores cadastrados: -")
        self.var_caminho_inscritos = StringVar(value="Arquivo inscritos")
        self.var_caminho_colaboradores = StringVar(value="Arquivo colaboradores")
        self.var_cpf_sorteado = StringVar()

        self.inicia_form_impressao()

    def inicia_form_impressao(self):
        frame_impressao = Frame(self.root)
        frame_impressao.pack(fill=BOTH, expand=True)
        frame_impressao.columnconfigure(0, minsize=250)
        frame_impressao.columnconfigure(1, minsize=250)
        frame_impressao.columnconfigure(2, minsize=250)
        frame_impressao.columnconfigure(3, minsize=50)
        
        self.inicia_form_impressao_linha1(frame_impressao, self.linha_1)
        self.inicia_form_impressao_linha2(frame_impressao, self.linha_2)
        self.inicia_form_impressao_linha3(frame_impressao, self.linha_3)
        self.inicia_form_impressao_linha4(frame_impressao, self.linha_4)
        self.inicia_form_impressao_linha5(frame_impressao, self.linha_5)
        self.inicia_form_impressao_linha6(frame_impressao)

    def inicia_form_impressao_linha1(self, master: Frame, linha):
        self.inicia_widget_impressora(master, 0.01, linha, 1)
        self.inicia_widget_impressora(master, 0.31, linha, 2)

        Label(
            master, text='Data do evento:', **self.configuracoes.label_parametros,
        ).place(relx=0.61, rely=linha)

        self.data = DateEntry(master)
        self.data.place(relx=0.73, rely=linha - 0.01)

    def inicia_form_impressao_linha2(self, master: Frame, linha):
        Label(
            master,
            textvariable=self.var_total_de_cadastros,
            **self.configuracoes.label_parametros,
        ).place(relx=0.01, rely=linha)

        Label(
            master,
            textvariable=self.var_inscricoes_validas,
            **self.configuracoes.label_parametros,
        ).place(relx=0.51, rely=linha)

    def inicia_form_impressao_linha3(self, master: Frame, linha):
        Label(
            master,
            textvariable=self.var_cadastros_repetidos,
            **self.configuracoes.label_parametros,
        ).place(relx=0.01, rely=linha)

        Label(
            master,
            textvariable=self.var_cpfs_invalidos,
            **self.configuracoes.label_parametros,
        ).place(relx=0.34, rely=linha)

        Label(
            master,
            textvariable=self.var_colaboradores_cadastrados,
            **self.configuracoes.label_parametros,
        ).place(relx=0.67, rely=linha)

    def inicia_form_impressao_linha4(self, master: Frame, linha):
        self.inicia_widget_localizazao_de_arquivo(master, self.var_caminho_inscritos, linha, self.abre_tb_inscritos)
        
    def inicia_form_impressao_linha5(self, master: Frame, linha):
        self.inicia_widget_localizazao_de_arquivo(master, self.var_caminho_colaboradores, linha, self.abre_tb_colaboradores)

    def inicia_form_impressao_linha6(self, master: Frame):
        self.bt_inicia_verificacao = Button(
            master,
            command=self.escreve_resultado_de_verificacao,
            text="Verifica cadastros",
        )

        self.bt_inicia_impressao = Button(
            master,
            command=self.inicia_thread_impressao,
            text="Iniciar impressão",
        )

    def inicia_widget_impressora(self, master: Frame, coluna: float, linha: float, numero: int):
        Label(
            master, text=f'Impressora {numero}:', **self.configuracoes.label_parametros,
        ).place(relx=coluna, rely=linha)

        nome_widget = f'impressora{numero}'
        impressora = Combobox(master, name=nome_widget, values=self.impressao.listar_impressoras())
        impressora.place(relx=coluna + 0.1, rely=linha - 0.015)
        impressora.bind('<<ComboboxSelected>>', self.ao_selecionra_impressora)
        impressora.bind('<<Enter>>', self.ao_selecionra_impressora)

    def inicia_widget_localizazao_de_arquivo(self, master: Frame, var, linha, comando):
        Label(master, textvariable=var, **self.configuracoes.label_caminho_parametros).place(relx=0.01, rely=linha)

        Button(
            master, image=self.imagens.img_lupa, command=comando, text='Procurar', style=OUTLINE
        ).place(relx=0.86, rely=linha)

    def ao_selecionra_impressora(self, event: tkinter.Event):
        widget: Combobox = event.widget
        nome_da_impressora = widget.get()
        numero_impressora = widget.winfo_name()
        self.impressao.set_printer(numero_impressora, nome_da_impressora)

    def escreve_resultado_de_verificacao(self):
        self.tabelas.verifica_cadastros()

        self.var_cadastros_repetidos.set(
            f"Cadastros repetidos: {self.tabelas.get_total_cadastros_repetidos}"
        )

        self.var_cpfs_invalidos.set(
            f"CPFs inválidos: {self.tabelas.get_total_cpfs_invalidos}"
        )

        self.var_colaboradores_cadastrados.set(
            f"Colaboradores cadasrtados: {self.tabelas.get_total_colaboradores_cadastrados}"
        )

        self.var_inscricoes_validas.set(
            f"Participantes válidos: {self.tabelas.get_total_inscricoes_validas}"
        )

        self.master.after(
            500, lambda: self.bt_inicia_impressao.place(relx=0.26, rely=self.linha_6)
        )

    def abre_tb_inscritos(self):
        self.tabelas.inicia_tb_inscritos(data=self.data.entry.get())

        caminho: Path = self.tabelas.get_caminho_tb_inscritos
        if not caminho:
            return

        self.var_caminho_inscritos.set(self.ajusta_caminho(caminho))
        self.var_total_de_cadastros.set(
            f"Total de cadastros: {self.tabelas.get_total_inscritos}"
        )

        self.bt_inicia_impressao.place_forget()
        self.bt_inicia_verificacao.place(relx=0.01, rely=self.linha_6)

    def abre_tb_colaboradores(self):
        self.tabelas.inicia_tb_colaboradores()

        caminho = self.tabelas.get_caminho_tb_colaboradores
        if not caminho:
            return

        self.var_caminho_colaboradores.set(self.ajusta_caminho(caminho))

    def inicia_thread_impressao(self):
        if not self.impressao.get_lista_de_impresoras_em_uso():
            return showinfo("Impressora", "Selecione uma impressora.")

        Thread(target=self.inicia_impressao, daemon=True).start()
        self.bt_inicia_impressao.place_forget()
        self.bt_inicia_verificacao.place_forget()

    def inicia_impressao(self):
        if not self.impressao.get_lista_de_impresoras_em_uso():
            showinfo('Falha de impressora', 'Selecione ao menos uma impressora!')
            return 

        self.log_panel = LogPanel(
            self.impressao, self.tabelas, self.configuracoes.label_parametros
        )
        self.log_panel.start_monitoramento()

        self.impressao.enviar_tabela_para_impressora(self.tabelas.get_tb_inscricoes_validas)

        self.bt_inicia_verificacao.place(relx=0.01, rely=self.linha_6)
        self.bt_inicia_impressao.place_forget()

    def salva_vencedores(self):
        self.tabelas.salva_vencedores()

        showinfo("Vencedores salvos", "A lista de vencedores foi salva com sucesso.")

    @staticmethod
    def ajusta_caminho(caminho: Path) -> str:
        caminho_ajustado = str(caminho)
        # if len(caminho_ajustado) > 100:
        #     caminho_ajustado = "..." + caminho_ajustado[-99:]

        return caminho_ajustado
