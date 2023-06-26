from threading import Thread

from tkinter.messagebox import showinfo, showerror
import validate_docbr as vdb
import customtkinter as ctk
from tkinter import StringVar
from PIL import Image

from Modulos.imprimir import Impressao
from Modulos.configs import Configuracoes
from Modulos.log_panel import LogPanel
from Modulos.funcoes_main import calc_linha, calc_coluna
from Modulos.models import Tabelas


class Main(ctk.CTk):
    def __init__(self):
        ctk.CTk.__init__(self)
        self.configuracoes = Configuracoes(self)
        self.impressao = Impressao()
        self.tabelas = Tabelas()

        self.var_total_de_cadastros = StringVar(value=f'Total de cadastros: -')
        self.var_inscricoes_validas = StringVar(value=f'Participantes válidos: -')
        self.var_cadastros_repetidos = StringVar(value=f'Cadastros repetidos: -')
        self.var_cpfs_invalidos = StringVar(value=f'CPFs inválidos: -')
        self.var_colaboradores_cadastrados = StringVar(value=f'Colaboradores cadasrtados: -')
        self.var_caminho_inscritos = StringVar(value='Arquivo inscritos')
        self.var_caminho_colaboradores = StringVar(value='Arquivo colaboradores')
        self.var_cpf_sorteado = StringVar()
        self.var_vencedor_registrado = StringVar()

        self.iniciar_root()
        self.inicia_widgets()
        self.iniciar_binds()

        self.mainloop()

    def iniciar_root(self):
        self.configure(**self.configuracoes.root_parametros)
        self.title('Validador de cadastros')
        self.resizable(False, False)
        self.geometry(f'{self.configuracoes.largura_da_tela}x{self.configuracoes.altura_da_tela}'
                      f'+{self.configuracoes.posicao_x}+{self.configuracoes.posicao_y}')
        ctk.set_default_color_theme('green')
        ctk.set_appearance_mode('light')

    def inicia_widgets(self):
        self.notebook = ctk.CTkTabview(self)
        self.notebook.pack(fill="both", expand=True)
        tab_impressao = self.notebook.add('Impressao')

        # frame_sorteios = ctk.CTkFrame(master=self.notebook, **self.configuracoes.frame_parametros, name='frame_sorteios')
        # self.inicia_frame_sorteios_widgets(frame_sorteios)
        # self.notebook.add(frame_sorteios, state='hidden', text='Registro de sorteios')

        frame_impressao = ctk.CTkFrame(master=tab_impressao, **self.configuracoes.frame_parametros)
        frame_impressao.pack(fill='both', expand=True)
        frame_impressao.columnconfigure([0, 1, 2], minsize=250)
        frame_impressao.columnconfigure(3, minsize=50)
        self.inicia_frame_impressao_widgets(frame_impressao)

        # frame_graficos = Frame(master=self.notebook, **self.configuracoes.frame_parametros, name='frame_graficos')
        # self.notebook.add(frame_graficos, state='hidden', text='Graficos')
    
    # def inicia_frame_sorteios_widgets(self, master):
    #     Label(master=master, text='Sorteio:', **self.configuracoes.label_parametros, ).place(relx=calc_coluna(1), rely=calc_linha(1))
        
    def inicia_frame_impressao_widgets(self, master):
        lista_impressoras = self.impressao.listar_impressoras()
        ctk.CTkLabel(master, text='Selecione a impressora 1:', **self.configuracoes.label_parametros
                     ).grid(row=0, column=0, padx=5, pady=5)
        ctk.CTkComboBox(master, values=lista_impressoras, command=self.on_select).grid(row=0, column=1, padx=5, pady=5)

        ctk.CTkLabel(master, text='Selecione a impressora 2:', **self.configuracoes.label_parametros
                     ).grid(row=0, column=2, padx=5, pady=5)
        ctk.CTkComboBox(master, values=lista_impressoras, command=self.on_select).grid(row=0, column=3, padx=5, pady=5)

        ctk.CTkLabel(master, textvariable=self.var_total_de_cadastros, **self.configuracoes.label_parametros
                     ).grid(row=1, column=0, padx=5, pady=5)

        ctk.CTkLabel(master, textvariable=self.var_inscricoes_validas, **self.configuracoes.label_parametros
                     ).grid(row=1, column=1, padx=5, pady=5)

        ctk.CTkLabel(master, textvariable=self.var_cadastros_repetidos, **self.configuracoes.label_parametros
                     ).grid(row=1, column=2, padx=5, pady=5)

        ctk.CTkLabel(master, textvariable=self.var_cpfs_invalidos, **self.configuracoes.label_parametros
                     ).grid(row=1, column=3, padx=5, pady=5)

        ctk.CTkLabel(master, textvariable=self.var_colaboradores_cadastrados, **self.configuracoes.label_parametros
                     ).grid(row=2, column=0, padx=5, pady=5)

        ctk.CTkLabel(master, textvariable=self.var_caminho_inscritos, **self.configuracoes.label_parametros
                     ).grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky='w')

        ctk.CTkButton(master, image=self.img_lupa(), **self.configuracoes.buttons_parametros, text='', width=28,
                      command=self.abre_tb_inscritos).grid(row=3, column=3, padx=5, pady=5)

        ctk.CTkLabel(master, textvariable=self.var_caminho_colaboradores, **self.configuracoes.label_parametros
                     ).grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky='w')

        ctk.CTkButton(master, image=self.img_lupa(), **self.configuracoes.buttons_parametros, text='', width=28,
                      command=self.abre_tb_colaboradores).grid(row=4, column=3, padx=5, pady=5)

        self.bt_inicia_verificacao = ctk.CTkButton(master, command=self.verifica_cadastros, text='Verifica cadastros',
                                                   **self.configuracoes.buttons_parametros)

        self.bt_inicia_impressao = ctk.CTkButton(master, command=self.inicia_thread_impressao, text='Iniciar impressão',
                                                 **self.configuracoes.buttons_parametros)

        self.bt_cpf_sorteado = ctk.CTkButton(text='Registrar vencedor', **self.configuracoes.buttons_parametros,
                                             command=self.registra_vencedor, master=master)

        self.bt_salva_vencedores = ctk.CTkButton(text='Salva vencedores', **self.configuracoes.buttons_parametros,
                                                 command=self.salva_vencedores, master=master)

        # ctk.CTkLabel(master, textvariable=self.var_cpf_sorteado, **self.configuracoes.label_parametros
        #              ).grid(row=5, column=2, padx=5, pady=5)
        #
        # ctk.CTkLabel(master, textvariable=self.var_vencedor_registrado, **self.configuracoes.label_parametros
        #              ).place(relx=calc_coluna(1), rely=calc_linha(9))

        # placeholder = 'Digite o CPF: 00000000000 ou 000.000.000-00'
        # PlaceHolderEntry(master=master, placeholder=placeholder, name='entry_cpf_sorteado', width=len(placeholder),
        #                  **self.configuracoes.entry_parametros)
        #
    
    def abre_tb_inscritos(self):
        self.tabelas.inicia_tb_inscritos()

        caminho = self.tabelas.get_caminho_tb_inscritos
        if not caminho:
            return

        self.var_caminho_inscritos.set(self.ajusta_caminho(caminho))
        self.var_total_de_cadastros.set(f'Total de cadastros: {self.tabelas.get_total_inscritos}')

        self.bt_inicia_impressao.grid_forget()
        self.bt_inicia_verificacao.grid(row=6, column=0)

    def abre_tb_colaboradores(self):
        self.tabelas.inicia_tb_colaboradores()

        caminho = self.tabelas.get_caminho_tb_colaboradores
        if not caminho:
            return

        self.var_caminho_colaboradores.set(self.ajusta_caminho(caminho))

    def verifica_cadastros(self):
        self.tabelas.verifica_cadastros()
        
        self.var_cadastros_repetidos.set(f'Cadastros repetidos: {self.tabelas.get_total_cadastros_repetidos}')
        
        self.var_cpfs_invalidos.set(f'CPFs inválidos: {self.tabelas.get_total_cpfs_invalidos}')
        
        self.var_colaboradores_cadastrados.set(f'Colaboradores cadasrtados: '
                                               f'{self.tabelas.get_total_colaboradores_cadastrados}')
        
        self.var_inscricoes_validas.set(f'Participantes válidos: {self.tabelas.get_total_inscricoes_validas}')

        self.after(500, lambda: self.bt_inicia_impressao.grid(row=6, column=1))

    def inicia_thread_impressao(self):
        if not self.impressao.get_lista_de_impresoras_em_uso():
            return showinfo('Impressora', 'Selecione uma impressora.')

        Thread(target=self.inicia_impressao, daemon=True).start()
        self.bt_inicia_impressao.grid_forget()

    def inicia_impressao(self):
        log_panel = LogPanel(self.impressao, self.tabelas, self.configuracoes.label_parametros)
        log_panel.start_monitoramento()
        self.impressao.enviar_tabela_para_impressora(self.tabelas.get_tb_inscricoes_validas)
        # Thread(target=self.exporta_relatorio).start()

    def exporta_relatorio(self):
        while self.log_panel.monitorando:
            pass
        showinfo('Fim das impressões', 'Impressões finalizadas.')

        caminho = self.var_caminho_inscritos.get()
        relatorio = self.tabelas.salva_tabela('tb_inscricoes_validas', caminho)
        showinfo('Relatorio do sorteio', f'Foi gerado um relatório do sorteio em: {relatorio}')

        self.registra_vencedores()

    def registra_vencedores(self):
        info = 'Para registrar o vencedor insira o CPF e depois clique em registrar'
        self.var_cpf_sorteado.set(info)
        self.frame_children['entry_cpf_sorteado'].place(relx=calc_coluna(1), rely=calc_linha(8))
        self.frame_children['bt_cpf_sorteado'].place(relx=calc_coluna(3), rely=calc_linha(8))
        self.frame_children['bt_salva_vencedores'].place(relx=calc_coluna(4), rely=calc_linha(8))
        self.tabelas.inicia_tb_vencedores()

    def registra_vencedor(self):
        def pisca():
            self.var_vencedor_registrado.set(f'Participante registrado com sucesso!')
            self.after(2000, lambda: self.var_vencedor_registrado.set(' '))
            self.after(2001, self.update_idletasks)

        def registra(cpf):
            entry.delete(0, 'end')
            if not self.tabelas.vencedor_exists(cpf):
                return showerror('CPF inexistente',
                                 f'O CPF {cpf} não existe na lista de impressos. Verifique se foi digitado corretmente.')
            self.tabelas.register_winner(cpf)
            Thread(target=pisca).start()

        entry = self.frame_children['entry_cpf_sorteado']
        cpf_do_vencedor = vdb.CPF().mask(entry.get(), 'cpf', mask=True)
        registra(cpf_do_vencedor)

    def salva_vencedores(self):
        caminho = self.var_caminho_inscritos.get()
        relatorio = self.tabelas.salva_tabela('tb_vencedores', caminho)

        showinfo('Vencedores do sorteio', f'Foi gerado um relatório dos vencedores do sorteio em: {relatorio}')

    def on_select(self, nome_impressora):
        self.impressao.set_printer(nome_impressora)

    @staticmethod
    def img_lupa():
        imagem = Image.open('icons/procurar_28x28.png')
        return ctk.CTkImage(imagem)

    def iniciar_binds(self):
        pass
        # self.entry_cpf_sorteado.bind('<Return>', lambda e: self.registra_vencedor())
        #
        # self.impressora1.bind("<<ComboboxSelected>>", on_select)
        #
        # self.impressora2.bind("<<ComboboxSelected>>", on_select)

    def ajusta_caminho(self, caminho: str):
        return caminho


if __name__ == '__main__':
    Main()
