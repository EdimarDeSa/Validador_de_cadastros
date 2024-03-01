from tkinter import Event
from datetime import datetime

from ttkbootstrap import Frame, StringVar, Button, Toplevel, Label, Entry, DateEntry
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.tableview import Tableview

from Modulos.constants import *
from Modulos.janelas.janelapadrao import *
from Modulos.janelas import *
from Modulos.models import *


__all__ = ['JanelaSorteios']


# noinspection PyArgumentList
class JanelaSorteios(JanelaPadrao):
    def __init__(self, master: Frame, configuracoes, tabelas, **kwargs):
        super().__init__(master, configuracoes, tabelas)

        self.var_sorteio_atual: [Sorteio, None] = None
        self.tabela_de_produtos: [Tableview, None] = None
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
        self.tela_retratil_sorteios = CollapsingFrame(master, autohide=True, bootstyle=ROUND)
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
        self.top: Toplevel = Toplevel(
            title="Cadastro de produto", size=(800, 260), resizable=(False, False), transient=self.master
        )
        self.top.position_center()

        self.top.protocol("WM_DELETE_WINDOW", self.fechar_formulario_de_produto)

        # -------------- PRIMEIRA LINHA -------------- #

        Label(self.top, text="Código", **self.configuracoes.label_parametros).place(x=10, y=10)
        Entry(self.top, name='campo_codigo', validatecommand=(self.reg_verifica_digito_numerico, '%P'), validate='key',
              **self.configuracoes.entry_parametros).place(x=10, y=40, width=148)
        Button(self.top, image=self.imagens.img_lupa, command=self.busca_produto).place(x=162, y=37, width=48)
        self.top.children.get('campo_codigo').insert(0, codigo)
        self.top.children.get('campo_codigo').focus_set()
        self.top.children.get('campo_codigo').bind('<KeyRelease>', self.busca_produto)

        Label(self.top, text="Produto", **self.configuracoes.label_parametros).place(x=220, y=10)
        Entry(self.top, name='campo_nome_do_produto',
              **self.configuracoes.entry_parametros).place(x=220, y=40, width=410)
        self.top.children.get('campo_nome_do_produto').insert(0, nome_do_produto)
        self.top.children.get('campo_nome_do_produto').bind('<Key>', self.verifica_info)

        Label(self.top, text="Quantidade", **self.configuracoes.label_parametros).place(x=640, y=10)
        Entry(self.top, name='campo_quantidade', validatecommand=(self.reg_verifica_digito_numerico, '%P'),
              validate='key', **self.configuracoes.entry_parametros).place(x=640, y=40, width=150)
        self.top.children.get('campo_quantidade').insert(0, quantidade)
        self.top.children.get('campo_quantidade').bind('<Key>', self.verifica_info)

        # -------------- SEGUNDA LINHA -------------- #

        Label(self.top, text="Centro de Custos", **self.configuracoes.label_parametros).place(x=10, y=110)
        Entry(self.top, name='campo_centro_de_custos', validatecommand=(self.reg_verifica_digito_numerico, '%P'),
              validate='key', **self.configuracoes.entry_parametros).place(x=10, y=140, width=200)
        self.top.children.get('campo_centro_de_custos').insert(0, centro_de_custos)
        self.top.children.get('campo_centro_de_custos').bind('<Key>', self.verifica_info)

        data_inicial = datetime.strptime(data_de_fechamento_cc, '%d/%m/%Y') if data_de_fechamento_cc else None
        Label(self.top, text="Data de fechamento CC", **self.configuracoes.label_parametros).place(x=220, y=110)
        DateEntry(self.top, name='campo_data_de_fechamento_cc', startdate=data_inicial).place(x=220, y=140)
        self.top.children.get('campo_data_de_fechamento_cc').bind('<Key>', self.verifica_info)

        Label(self.top, text="Responsável pelo CC", **self.configuracoes.label_parametros).place(x=430, y=110)
        Entry(self.top, name='campo_responsavel_pelo_cc',
              **self.configuracoes.entry_parametros).place(x=440, y=140, width=350)
        self.top.children.get('campo_responsavel_pelo_cc').insert(0, responsavel_pelo_cc)
        self.top.children.get('campo_responsavel_pelo_cc').bind('<Key>', self.verifica_info)

        # -------------- TERCEIRA LINHA -------------- #
        Button(self.top, text="Adicionar", command=lambda _id=iid: self.salva_produto(_id)
               ).place(x=170, y=210, width=160)

        Button(self.top, text="Limpar", command=self.limpa_formulario_de_produto).place(x=500, y=210, width=160)

    def limpa_formulario_de_produto(self):
        campos = ['campo_codigo', 'campo_nome_do_produto', 'campo_quantidade']
        for campo in campos:
            self.top.children.get(campo).delete(0, END)
        self.top.children.get( 'campo_data_de_fechamento_cc').entry.delete(0, END)

    def fechar_formulario_de_produto(self):
        self.var_formulario_de_produto_aberto = False
        self.top.destroy()

    def edita_sorteio(self, sorteio: Sorteio):
        iids = [iid.iid for iid in self.tabela_de_produtos.get_rows()]
        if iids:
            r = Messagebox.yesno(
                title='Prêmios em edição',
                message='Existem prêmios em ediçõ ainda, tem certeza que continuar?\n'
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

    def salva_produto(self, iid=None, event: Event = None):
        codigo = self.top.children.get('campo_codigo').get()
        if not codigo:
            self.informa_falta_de_dado('Código', self.top.children.get('campo_codigo'))
            self.top.children.get('campo_codigo').focus_set()
            return

        nome_do_produto = self.top.children.get('campo_nome_do_produto').get()
        if not nome_do_produto:
            self.informa_falta_de_dado('Nome do produto', self.top.children.get('campo_nome_do_produto'))
            self.top.children.get('campo_nome_do_produto').focus_set()
            return

        quantidade = self.top.children.get('campo_quantidade').get()
        if not quantidade:
            self.informa_falta_de_dado('Quantidade', self.top.children.get('campo_quantidade'))
            self.top.children.get('campo_quantidade').focus_set()
            return

        cc = self.top.children.get('campo_centro_de_custos').get()
        if not cc:
            self.informa_falta_de_dado('Centro de Custo', self.top.children.get('campo_centro_de_custos'))
            self.top.children.get('campo_centro_de_custos').focus_set()
            return

        data_fechamento_cc = self.top.children.get('campo_data_de_fechamento_cc').entry.get()
        responsavel_cc = self.top.children.get('campo_responsavel_pelo_cc').get()
        if not responsavel_cc:
            self.informa_falta_de_dado('Responsável pelo cc', self.top.children.get('campo_responsavel_pelo_cc'))
            self.top.children.get('campo_responsavel_pelo_cc').focus_set()
            return

        continuar = Messagebox.yesnocancel(title='Continuar cadastros?', parent=self.master,
                                           message='Deseja salvar e continuar a cadastrar prêmios?')

        if continuar == 'Cancelar':
            return

        valores = [codigo, nome_do_produto, quantidade, cc, data_fechamento_cc, responsavel_cc]
        if not iid:
            self.tabela_de_produtos.insert_row(values=valores)
        else:
            self.tabela_de_produtos.get_row(iid=iid).values = valores

        self.tabela_de_produtos.load_table_data()

        if continuar == 'Sim':
            self.limpa_formulario_de_produto()

            self.top.children.get(codigo).focus_set()
            return

        self.fechar_formulario_de_produto()

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
    def verifica_info(event: Event):
        widget: Entry = event.widget
        if not widget.get():
            widget.config(bootstyle=DANGER)
        else:
            widget.config(bootstyle=DEFAULT)

    def busca_produto(self, event: Event = None):
        codigo = self.top.children.get('campo_codigo').get()
        if len(codigo) < 7:
            return

        produto = self.tabelas.busca_produto(codigo)

        if produto is None:
            Messagebox.show_error(title='Planilha de produtos invalida',
                                  message='Planilha de produtos no formato inválido')
            return

        self.top.children.get('campo_nome_do_produto').delete(0, END)
        self.top.children.get('campo_nome_do_produto').insert(0, '' if isinstance(produto, list) else produto.iloc[0])

    @property
    def checa_nome_do_sorteio(self) -> str:
        return f'Sorteio {len(self.var_lista_de_sorteios) + 1}'

    @staticmethod
    def informa_falta_de_dado(campo: str, parent=None):
        Messagebox.show_warning(title='Faltam informações', message=f'É necessário preencher o campo: {campo}',
                                parent=parent)
