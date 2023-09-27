from pathlib import Path
from threading import Thread
from tkinter.messagebox import showinfo
import re

from ttkbootstrap import *
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.tooltip import ToolTip
import validate_docbr as vdb

from ..log_panel import LogPanel
from ..configs import Configuracoes
from ..imprimir import Impressao
from .produto import Produto
from .sorteio import Sorteio

caminho_icons = Path(__file__).resolve().parent.parent.parent / "icons"
caminho_imagem_lupa = caminho_icons / "procurar_28x28.png"
caminho_imagem_editar = caminho_icons / "procurar_28x28.png"
caminho_imagem_deletar = caminho_icons / "procurar_28x28.png"


class Imagens:
    @property
    def img_deletar(self):
        image = PhotoImage(file=caminho_imagem_deletar)
        return image

    @property
    def img_editar(self):
        image = PhotoImage(file=caminho_imagem_editar)
        return image


class TreeViewLine(Imagens):
    def __init__(
        self, master: Window, linha, nome, informacoes, comando_deletar, comando_editar
    ):
        super(TreeViewLine, self).__init__()
        self.nome = nome
        self.informacoes = informacoes

        Frame(
            master,
        ).grid(column=0, row=0, sticky="w")

        Button(
            master,
            image=self.img_editar,
            width=28,
            command=lambda l=(linha - 1): comando_editar(l),
        ).grid(column=1, row=0)

        Button(
            master,
            image=self.img_deletar,
            width=28,
            command=lambda linha=(linha - 1): comando_deletar(linha),
        ).grid(column=2, row=0)


class TreeView(Tableview):
    def __init__(self, master: Window, titulo: str, configuracoes: Configuracoes):
        super(TreeView, self).__init__(master, **configuracoes.frame_parametros)

        self._configuracoes = configuracoes
        self.ultima_linha = 2
        self.var_zebrado = True

        self.cria_cabecalho(titulo)
        self._linhas = []

    def cria_cabecalho(self, titulo: str):
        Frame(self, text=titulo, **self._configuracoes.label_titulos).pack(fill="x")

        #############################

        Frame(
            self, text="  Nome", **self._configuracoes.label_parametros, width=40
        ).pack(side="left", anchor="n")

        Frame(
            self,
            text="Editar   Apagar",
            **self._configuracoes.label_parametros,
            width=40,
        ).pack(side="right", anchor="n")

        Frame(self, text="", **self._configuracoes.label_parametros).pack(fill="x")

    def add_linha(self, nome: str, informacoes: object):
        cor = self.seleciona_cor()

        linha = Frame(self, fg_color=cor)
        TreeViewLine(
            linha,
            self.ultima_linha,
            nome,
            informacoes,
            self.deletar_produto,
            self.editar_linha,
        )
        linha.pack(fill="x", ipadx=300)

        self._linhas.append(linha)

        self.ultima_linha += 1

    def seleciona_cor(self):
        self.__inverte_zebrar()
        return "green" if self.var_zebrado else "transparent"

    def editar_linha(self, linha):
        informacoes = self._linhas[linha]
        return informacoes

    def deletar_produto(self, linha):
        self.reseta_quadro()
        linhas_cp = self._linhas.copy()
        linhas_cp.pop(linha)
        self._linhas.clear()

        for linha in linhas_cp:
            self.add_linha(linha.nome, linha.informacoes)

    def reseta_quadro(self):
        if not self._linhas:
            return

        for linha in self._linhas:
            linha.destroy()

    def __inverte_zebrar(self):
        self.var_zebrado = not self.var_zebrado


class JanelaPadrao:
    def __init__(
        self,
        master: Frame,
        configuracoes: Configuracoes,
        tabelas,
        impressao: Impressao,
    ):
        self.master = master
        self.configuracoes = configuracoes
        self.tabelas = tabelas
        self.impressao = impressao
        self.lista_impressoras = self.impressao.listar_impressoras()

        self.img_lupa = PhotoImage(file=caminho_imagem_lupa)

    def valida_digito(self, event):
        print(event.__dict__)
        if event.char.isdigit():
            return event.char


class JanelaSorteios(JanelaPadrao):
    def __init__(self, master: Window, configuracoes, tabelas, impressao):
        super().__init__(master, configuracoes, tabelas, impressao)

        self.var_caminho_sorteio = StringVar(value="Clique para procurar")
        self.var_caminho_tabela_de_precos = StringVar(value="Clique para procurar")
        self.var_sorteio_atual = StringVar()
        self.var_formulario_de_produto_aberto = False

        frame_produtos = Frame(master)
        frame_produtos.place(relx=0.005, rely=0.01, relheight=0.55, relwidth=0.99)
        self.inicia_frame_produtos(frame_produtos)
        # self.inicia_frame_registro_sorteio(frame_registro_sorteio)

        ################################

        # self.frame_produtos = CTkTreeView(
        #     master, titulo='Produtos registrados', configuracoes=self.configuracoes
        # )
        # self.frame_produtos.place(relwidth=0.245, relheight=0.485, relx=0.755, rely=0)

        # ################################

        # self.frame_sorteios = CTkTreeView(
        #     master, titulo='Sorteios registrados', configuracoes=self.configuracoes
        # )
        # self.frame_sorteios.place(relwidth=0.245, relheight=0.485, relx=0.755, rely=0.51)

        # ################################

        # self.atualiza_sorteio_atual()
        # self.sorteio_atual: Sorteio = Sorteio(self.var_sorteio_atual.get())

    def inicia_frame_produtos(self, master: Window):
        colunas = [
            dict(text="Código", width=80, stretch=False),
            dict(text="Nome", width=400, stretch=False),
            dict(text="Qtd", width=50, stretch=False),
            dict(text="CC", width=80, stretch=False),
            dict(text="Fechamento CC", width=120, stretch=False),
            dict(text="Responsável CC", width=250, stretch=False),
        ]

        linhas = [
            (
                "00000000000",
                "Produto 1",
                "1",
                "12345",
                "12/01/24",
                "Marta Rosa Nunes",
            ),
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
            master, coldata=colunas, rowdata=linhas, stripecolor=('#78c2ad', None), delimiter=","
        )

        self.tabela_de_produtos.place(relx=0, rely=0, relwidth=0.79, relheight=1)

        Button(
            master,
            text="Adicionar produto",
            command=self.formulario_de_criacao_de_produto,
        ).place(relx=0.8, rely=0.3, relwidth=0.19)

        Button(
            master,
            text="Remover produto",
            command=self.remove_produto
        ).place(relx=0.8, rely=0.6, relwidth=0.19)

        master.after(200, self.formulario_de_criacao_de_produto)

    def formulario_de_criacao_de_produto(self):
        if self.var_formulario_de_produto_aberto:
            print(self.master.winfo_toplevel())
            return

        self.var_formulario_de_produto_aberto = True
        self.top = Toplevel(
            title="Cadastro de produto",
            size=[800, 800],
            resizable=[False, False],
            topmost=True,
        )
        self.top.wm_protocol(
            "WM_DELETE_WINDOW",
            self.fechar_formulario_de_produto,
        )

        # ------- PRIMEIRA LINHA ------- #

        Label(self.top, text="Código", **self.configuracoes.label_parametros).place(
            x=10, rely=10
        )
        self.codigo = Entry(self.top, **self.configuracoes.entry_parametros)
        self.codigo.place(relx=10, rely=40, width=200)
        ToolTip(self.codigo, text='Para procurar o produto aperto o "ENTER"')

        Label(self.top, text="Produto", **self.configuracoes.label_parametros).place(
            x=220, rely=10
        )
        self.nome_do_produto = Entry(self.top, **self.configuracoes.entry_parametros)
        self.nome_do_produto.place(relx=220, rely=40, width=410)

        Label(self.top, text="Quantidade", **self.configuracoes.label_parametros).place(
            x=640, rely=10
        )
        self.quantidade = Entry(self.top, **self.configuracoes.entry_parametros)
        self.quantidade.place(relx=640, rely=40, width=150)

        # ------- SEGUNDA LINHA ------- #

        Label(
            self.top, text="Centro de Custos", **self.configuracoes.label_parametros
        ).place(relx=10, rely=110)
        self.centro_de_custos = Entry(self.top, **self.configuracoes.entry_parametros)
        self.centro_de_custos.place(relx=10, rely=140, width=200)
        self.centro_de_custos.insert(0, "23504")

        Label(
            self.top,
            text="Data de fechamento CC",
            **self.configuracoes.label_parametros,
        ).place(relx=220, rely=110)
        self.data_de_fechamento_cc = Entry(
            self.top, **self.configuracoes.entry_parametros
        )
        self.data_de_fechamento_cc.place(relx=220, rely=140, width=200)
        self.data_de_fechamento_cc.bind(
            "<KeyRelease>", self.mascara_data_de_fechamento_cc
        )

        Label(
            self.top, text="Responsável pelo CC", **self.configuracoes.label_parametros
        ).place(relx=430, rely=110)
        self.responsavel_pelo_cc = Entry(self.top, **self.configuracoes.entry_parametros)
        self.responsavel_pelo_cc.place(relx=430, rely=140, width=360)
        self.responsavel_pelo_cc.insert(0, "Marta Rosa Nunes")

        # ------- TERCEIRA LINHA ------- #

        Button(self.top, text="Adicionar", command=self.salva_produto).place(
            x=170, rely=210, width=160
        )

        Button(self.top, text="Limpar", command=self.limpa_formulario_de_produto).place(
            x=500, rely=210, width=160
        )

    def mascara_data_de_fechamento_cc(self, event):
        texto = self.data_de_fechamento_cc.get()

        if not texto:
            return

        self.data_de_fechamento_cc.delete(0, "end")
        texto_formatado = re.sub(r"\D", "", texto)
        caracteres = len(texto_formatado)

        if caracteres > 2:
            data = re.findall(r"(\d{1,2})", texto_formatado)
            dia, mes, ano = data[:3] + [None] * (3 - len(data))

            dia = str(min(int(dia), 31)).zfill(2)
            mes = min(int(mes), 12) if mes else None

            if caracteres > 3:
                mes = str(mes).zfill(2)

            if ano:
                texto_formatado = f"{dia}/{mes}/{ano}"
            else:
                texto_formatado = f"{dia}/{mes}"

        self.data_de_fechamento_cc.insert(0, texto_formatado)

    def limpa_formulario_de_produto(self):
        self.codigo.delete(0,'end')
        self.nome_do_produto.delete(0,'end')
        self.quantidade.delete(0,'end')
        self.centro_de_custos.delete(0,'end')
        self.data_de_fechamento_cc.delete(0,'end')
        self.responsavel_pelo_cc.delete(0,'end')
    
    def fechar_formulario_de_produto(self):
        self.var_formulario_de_produto_aberto = False
        self.top.destroy()

    def salva_produto(self):
        codigo = self.codigo.get()
        nome_do_produto = self.nome_do_produto.get()
        quantidade = self.quantidade.get()
        cc = self.centro_de_custos.get()
        data_fechamento_cc = self.data_de_fechamento_cc.get()
        responsavel_cc = self.responsavel_pelo_cc.get()

        self.tabela_de_produtos.insert_row(
            index='end',
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
        print(self.tabela_de_produtos.selection_get())
    
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

    def printa(self, event):
        print(event)

    def procura_produto(self, codigo):
        produto = codigo
        return produto

    def atualiza_sorteio_atual(self, atual=1):
        self.var_sorteio_atual.set(f"Editando o sorteio {atual}")


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

        self.var_impressora_1 = StringVar()
        self.var_impressora_2 = StringVar()

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
            command=self.verifica_cadastros,
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

        var_impressora = getattr(self, f'var_impressora_{numero}')

        impressora1 = Combobox(
            master, values=self.lista_impressoras, textvariable=var_impressora
        )
        impressora1.place(relx=coluna + 0.105, rely=linha - 0.01)
        impressora1.bind('<<ComboboxSelected>>', lambda event, var=var_impressora: self.on_select(var))

    def inicia_widget_localizazao_de_arquivo(self, master: Frame, var, linha, comando):
        Label(
            master,
            textvariable=var,
            **self.configuracoes.label_caminho_parametros,
        ).place(relx=0.01, rely=linha)

        Button(
            master,
            image=self.img_lupa,
            command=comando,
            text='Procurar',
            style='outline'
        ).place(relx=0.86, rely=linha)

    def inicia_frame_impressao_widgets(self, master: Window):
        # self.bt_cpf_sorteado = Button(
        #     master,
        #     text="Registrar vencedor",
        #     command=self.registra_vencedor,
        # )
        # 
        # self.bt_salva_vencedores = Button(
        #     master,
        #     text="Salva vencedores",
        #     command=self.salva_vencedores,
        # )
        # 
        # Frame(
        #     master,
        #     textvariable=self.var_cpf_sorteado,
        #     **self.configuracoes.label_parametros,
        # ).place(relx=0.01, rely=self.linha_6)
        #
        # self.lb_vencedor_registrado = Frame(
        #     master,
        #     text="Participante registrado com sucesso!",
        #     **self.configuracoes.label_parametros,
        # )
        #
        # placeholder = "Digite o CPF: 00000000000 ou 000.000.000-00"
        # self.entry_cpf_sorteado = Entry(
        #     master,
        #     # placeholder_text=placeholder,
        #     width=300,
        #     **self.configuracoes.entry_parametros,
        # )
        pass

    def on_select(self, var):
        self.impressao.set_printer(printer_name=var.get())

    def verifica_cadastros(self):
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

    def registra_vencedor(self):
        cpf = self.entry_cpf_sorteado.get()

        if not vdb.validate_cpf(cpf):
            return showerror("CPF inválido", "Digite um CPF válido.")

        if cpf in self.tabelas.get_cpfs_inscritos():
            return showerror(
                "CPF já inscrito", "Este CPF já foi registrado como participante."
            )

        self.tabelas.add_vencedor(cpf)
        self.var_cpf_sorteado.set("")

        self.lb_vencedor_registrado.place(relx=0.01, rely=self.linha_7)

    def salva_vencedores(self):
        self.tabelas.salva_vencedores()

        showinfo("Vencedores salvos", "A lista de vencedores foi salva com sucesso.")

    @staticmethod
    def ajusta_caminho(caminho: Path) -> str:
        caminho_ajustado = str(caminho)
        # if len(caminho_ajustado) > 100:
        #     caminho_ajustado = "..." + caminho_ajustado[-99:]

        return caminho_ajustado

    def iniciar_binds(self):
        self.entry_cpf_sorteado.bind("<Return>", lambda e: self.registra_vencedor())


class JanelaConfiguracoes(JanelaPadrao):
    def __init__(self, master: Window, configuracoes, tabelas, impressao):
        super().__init__(master, configuracoes, tabelas, impressao)


class JanelaRegistroDeVencedor(JanelaPadrao):
    pass
