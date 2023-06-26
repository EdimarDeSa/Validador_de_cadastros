from threading import Thread
from time import time, sleep

from tkinter import Button, Frame, Label, StringVar, Tk, PhotoImage, TclError
from tkinter.ttk import Combobox
from tkinter.messagebox import showinfo, askyesno, showerror

from docbr import parse, validate
import pandas as pd

from Modulos import CPF, VALIDADE_CPF, NOME, DUPLICADA, COLABORADOR, COLUNAS_SERVICO_IMPRESSORAS
from Modulos.arquivo import AbreArquivo
from Modulos.imprimir import Impressao
from Modulos.configs import Configuracoes
from Modulos.log_panel import LogPanel
from Modulos.place_holder import PlaceHolderEntry
from Modulos.funcoes_main import limpeza_de_dados, capitaliza_nome, calcula_tempo_de_impressao_total, calc_linha, calc_coluna


class Main(Tk):
    impressora_da_vez: bool = True
    df_inscricoes: pd.DataFrame
    df_inscricoes_validas: pd.DataFrame
    df_colaboradores: pd.DataFrame
    df_vencedores: pd.DataFrame
    img_lupa: PhotoImage

    def __init__(self):
        Tk.__init__(self)
        self.configuracoes = Configuracoes(self)
        self.arquivos = AbreArquivo()
        self.impressao = Impressao()

        self.var_total_de_cadastros = StringVar(value=f'Total de cadastros: -')
        self.var_participantes_validos = StringVar(value=f'Participantes válidos: -')
        self.var_cadastros_repetidos = StringVar(value=f'Cadastros repetidos: -')
        self.var_cpfs_invalidos = StringVar(value=f'CPFs inválidos: -')
        self.var_colaboradores_cadastrados = StringVar(value=f'Colaboradores cadasrtados: -')
        self.var_caminho_inscritos = StringVar(value='CSV inscritos')
        self.var_caminho_colaboradores = StringVar(value='CSV colaboradores')
        self.var_cpf_sorteado = StringVar()
        self.var_vencedor_registrado = StringVar()
        self.img_lupa = PhotoImage(file=self.arquivos.abre_imagem())

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

        self.configuracoes.frame_parametros.update({'master': self})

    def inicia_widgets(self):
        frame = Frame(**self.configuracoes.frame_parametros, name='frame')
        frame.place(relheight=0.98, relwidth=0.98, relx=0.01, rely=0.01)

        self.inicia_labels(frame)
        self.inicia_entrys(frame)
        self.inicia_combobox(frame)
        self.inicia_buttons(frame)

    def inicia_labels(self, master):
        Label(text='Selecione a impressora 1:', **self.configuracoes.label_parametros, master=master
              ).place(relx=calc_coluna(1), rely=calc_linha(1))

        Label(
            text='Selecione a impressora 2:', **self.configuracoes.label_parametros, master=master
        ).place(relx=calc_coluna(3), rely=calc_linha(1))

        Label(textvariable=self.var_total_de_cadastros, **self.configuracoes.label_parametros, master=master
              ).place(relx=calc_coluna(1), rely=calc_linha(2))

        Label(textvariable=self.var_participantes_validos, **self.configuracoes.label_parametros, master=master
              ).place(relx=calc_coluna(2), rely=calc_linha(2))

        Label(textvariable=self.var_cadastros_repetidos, **self.configuracoes.label_parametros, master=master
              ).place(relx=calc_coluna(3), rely=calc_linha(2))

        Label(textvariable=self.var_cpfs_invalidos, **self.configuracoes.label_parametros, master=master
              ).place(relx=calc_coluna(4), rely=calc_linha(2))

        Label(textvariable=self.var_colaboradores_cadastrados, **self.configuracoes.label_parametros, master=master
              ).place(relx=calc_coluna(1), rely=calc_linha(3))

        Label(textvariable=self.var_caminho_inscritos, **self.configuracoes.label_parametros, master=master
              ).place(relx=calc_coluna(1), rely=calc_linha(4) + 0.01)

        Label(textvariable=self.var_caminho_colaboradores, **self.configuracoes.label_parametros, master=master
              ).place(relx=calc_coluna(1), rely=calc_linha(5) + 0.01)

        Label(textvariable=self.var_cpf_sorteado, master=master, **self.configuracoes.label_parametros
              ).place(relx=calc_coluna(1), rely=calc_linha(7))

        Label(textvariable=self.var_vencedor_registrado, master=master, **self.configuracoes.label_parametros,
              name='label_vencedor'
              ).place(relx=calc_coluna(1), rely=calc_linha(9))

    def inicia_entrys(self, master):
        placeholder = 'Digite o CPF: 00000000000 ou 000.000.000-00'
        PlaceHolderEntry(master=master, placeholder=placeholder, name='entry_cpf_sorteado', width=len(placeholder),
                         **self.configuracoes.entry_parametros)

    def inicia_combobox(self, master):
        lista_impressoras = self.impressao.listar_impressoras()

        Combobox(
            values=lista_impressoras, name='impressora1', **self.configuracoes.combobox_parametros, master=master
        ).place(relx=calc_coluna(2), rely=calc_linha(1), relwidth=0.23)

        Combobox(
            values=lista_impressoras, name='impressora2', **self.configuracoes.combobox_parametros, master=master
        ).place(relx=calc_coluna(4), rely=calc_linha(1), relwidth=0.23)

        try:
            master.children['impressora1'].current(lista_impressoras.index('Brother QL-800 1'))
            master.children['impressora2'].current(lista_impressoras.index('Brother QL-800 2'))

        except IndexError:
            pass

    def inicia_buttons(self, master):
        Button(image=self.img_lupa, **self.configuracoes.buttons_parametros,
               command=lambda: self.abre_arquivo('inscritos'), master=master
               ).place(relx=calc_coluna(4), rely=calc_linha(4))

        Button(image=self.img_lupa, **self.configuracoes.buttons_parametros,
               command=lambda: self.abre_arquivo('colaboradores'), master=master
               ).place(relx=calc_coluna(4), rely=calc_linha(5))

        Button(command=self.verifica_cadastros, text='Verifica cadastros', name='bt_inicia_verificacao',
               **self.configuracoes.buttons_parametros, master=master)

        Button(command=self.inicia_verificacao, text='Iniciar impressão', name='bt_inicia_impressao',
               **self.configuracoes.buttons_parametros, master=master)

        Button(text='Registrar vencedor', **self.configuracoes.buttons_parametros, name='bt_cpf_sorteado',
               command=self.registra_vencedor, master=master)

        Button(text='Salva vencedores', **self.configuracoes.buttons_parametros, name='bt_salva_vencedores',
               command=self.salva_vencedores, master=master)

    def abre_arquivo(self, arquivo):
        caminho = self.arquivos.abre_documento()
        if caminho == '':
            return

        df = self.arquivos.abre_dataframe(caminho)
        if arquivo == 'inscritos':
            self.df_inscricoes = df
            self.var_caminho_inscritos.set(caminho)
            self.df_inscricoes_validas = pd.DataFrame(columns=df.columns)
            self.registra_informacoes()

    def abre_tb_colaboradores(self):
        self.tabelas.inicia_tb_colaboradores()
        self.var_caminho_colaboradores.set()

    def inicia_verificacao(self):
        Thread(target=self.inicia_impressao, daemon=True).start()
        self.frame_children['bt_inicia_impressao'].place_forget()

    def registra_informacoes(self):
        self.var_total_de_cadastros.set(f'Total de cadastros: {self.df_inscricoes.shape[0]}')
        frame_children = self.frame_children
        frame_children['bt_inicia_impressao'].place_forget()
        frame_children['bt_inicia_verificacao'].place(relx=calc_coluna(2), rely=calc_linha(6))

    def verifica_cadastros(self):            
        self.df_inscricoes[CPF] = self.df_inscricoes[CPF].apply(lambda cpf: limpeza_de_dados(cpf))

        self.df_inscricoes = self.df_inscricoes.assign(**{
            NOME: lambda df: df[NOME].apply(lambda nome: capitaliza_nome(nome)),
            DUPLICADA: self.df_inscricoes.duplicated(subset=CPF, keep='last'),
            VALIDADE_CPF: lambda df: df.query(f'{DUPLICADA}==False')[CPF].apply(lambda cpf: validate(cpf, 'cpf')),
            CPF: lambda df: df.query(f'{VALIDADE_CPF}==True')[CPF].apply(lambda cpf: parse(cpf, 'cpf', mask=True)),
            COLABORADOR: lambda df: df[CPF].isin(self.df_colaboradores[CPF])
        })

        num_cadastros_repetidos = (self.df_inscricoes[DUPLICADA] == True).sum()
        self.var_cadastros_repetidos.set(f'Cadastros repetidos: {num_cadastros_repetidos}')

        num_cpfs_invalidos = (self.df_inscricoes[VALIDADE_CPF] == False).sum()
        self.var_cpfs_invalidos.set(f'CPFs inválidos: {num_cpfs_invalidos}')

        num_colaboradores_cadastrados = (self.df_inscricoes[COLABORADOR] == True).sum()
        self.var_colaboradores_cadastrados.set(f'Colaboradores cadasrtados: {num_colaboradores_cadastrados}')

        inscricoes_validas = self.df_inscricoes.query(f'{VALIDADE_CPF} == True and {COLABORADOR} == False')
        num_inscricoes_validas = inscricoes_validas.shape[0]
        self.var_participantes_validos.set(f'Participantes válidos: {num_inscricoes_validas}')

        self.df_inscricoes_validas = inscricoes_validas

        self.after(1000, lambda: self.frame_children['bt_inicia_impressao'].place(relx=calc_coluna(3), rely=calc_linha(6)))

    def inicia_impressao(self):
        def imprime_inscrito(row):
            nome_participante = row[NOME]
            cpf = row[CPF]
            impressora = self.verifica_vez_da_impressora()
            self.impressao.imprimir(cpf, nome_participante, impressora)

        Thread(target=self.inicia_relatorio).start()

        self.df_inscricoes_validas.apply(imprime_inscrito, axis=1)

    def verifica_vez_da_impressora(self):
        if not self.impressora2:
            return self.impressora1

        self.impressora_da_vez = not self.impressora_da_vez
        return self.impressora1 if self.impressora_da_vez else self.impressora2

    def inicia_relatorio(self):
        impressoras = [self.impressora1]
        if self.impressora2:
            impressoras.append(self.impressora2)

        jobs = [1]
        start_time = time()
        df_jobs_em_andamento = pd.DataFrame(columns=COLUNAS_SERVICO_IMPRESSORAS)

        while jobs:
            if not hasattr(self, 'log_panel'):
                self.log_panel = LogPanel(master=self, kw=self.configuracoes.label_parametros)

            elapsed_time = time() - start_time
            time_to_wait = max(0, int(2 - elapsed_time))
            sleep(time_to_wait)

            jobs = self.impressao.printer_job_checker(printer_list=impressoras)
            df_jobs_update = pd.DataFrame(jobs)

            if df_jobs_update.shape[0]:
                df_jobs_update.drop('Submitted', axis=1, inplace=True)
                df_jobs_em_andamento = df_jobs_em_andamento.merge(df_jobs_update, on=COLUNAS_SERVICO_IMPRESSORAS, how='outer')
                df_jobs_em_andamento['Na_fila'] = df_jobs_em_andamento['JobId'].isin(df_jobs_update['JobId'])
                for impressora in impressoras:
                    indice = impressoras.index(impressora)
                    log = df_jobs_em_andamento.query(f'pPrinterName=="{impressora}" and Na_fila==True')
                    total_na_fila = log.shape[0]
                    try:
                        self.log_panel.log_clear(indice)
                        if total_na_fila:

                            tempo_de_impressao = calcula_tempo_de_impressao_total(total_na_fila)

                            self.log_panel.log_impressora(f'{impressora} - Tempo estimado: {tempo_de_impressao} minutos', indice)
                            log['pDocument'].apply(lambda doc: self.log_panel.log_impressora(f'Imprimindo: {doc}', indice))
                        else:
                            self.log_panel.log_impressora(f'{impressora} - Impressões finalizadas', indice)
                    except TclError:
                        del self.log_panel
                        break
                    except AttributeError:
                        break

            start_time = time()

        self.log_panel.destroy()
        showinfo('Fim das impressões', 'Impressões finalizadas.')

        caminho = self.var_caminho_inscritos.get()
        relatorio = self.arquivos.salva_arquivo_filtrado(self.df_inscricoes, caminho, 'relatorio')
        showinfo('Relatorio da campanha', f'Foi gerado um relatório da campanha em: {relatorio}')

        self.registra_vencedores()

    def registra_vencedores(self):
        info = 'Para registrar o vencedor insira o CPF e depois clique em registrar'
        self.var_cpf_sorteado.set(info)
        self.frame_children['entry_cpf_sorteado'].place(relx=calc_coluna(1), rely=calc_linha(8))
        self.frame_children['bt_cpf_sorteado'].place(relx=calc_coluna(3), rely=calc_linha(8))
        self.frame_children['bt_salva_vencedores'].place(relx=calc_coluna(4), rely=calc_linha(8))
        self.df_vencedores = pd.DataFrame()

    def registra_vencedor(self):
        def pisca():
            self.after(500, lambda: self.var_vencedor_registrado.set(f'Participante registrado com sucesso!'))
            self.after(501, self.update_idletasks)
            self.after(1000, lambda: self.var_vencedor_registrado.set(' '))
            self.after(1001, self.update_idletasks)
            self.after(1500, lambda: self.var_vencedor_registrado.set(f'Participante registrado com sucesso!'))
            self.after(1501, self.update_idletasks)
            self.after(2000, lambda: self.var_vencedor_registrado.set(' '))
            self.after(2001, self.update_idletasks)
            self.after(2500, lambda: self.var_vencedor_registrado.set(f'Participante registrado com sucesso!'))
            self.after(2501, self.update_idletasks)
            self.after(6000, lambda: self.var_vencedor_registrado.set(' '))
            self.after(6001, self.update_idletasks)

        def registra(cpf):
            dados_vencedor = self.df_inscricoes.query(f'{CPF}=="{cpf}" and {DUPLICADA}==False')
            if not dados_vencedor.shape[0]:
                return showerror('CPF inexistente',
                                 f'O CPF {cpf} não existe na lista de impressos. Verifique se foi digitado corretmente.')
            self.df_vencedores = pd.concat([self.df_vencedores, dados_vencedor], ignore_index=True)
            entry.delete(0, 'end')
            Thread(target=pisca).start()

        entry = self.frame_children['entry_cpf_sorteado']
        cpf_do_vencedor = parse(entry.get(), 'cpf', mask=True)
        if CPF not in self.df_vencedores.columns or not any(self.df_vencedores[CPF] == cpf_do_vencedor):
            registra(cpf_do_vencedor)
        else:
            r = askyesno('Vencedor já registrado', 'Este vencedor já foi registrado, deseja registrá-lo novamente?')
            if r:
                registra(cpf_do_vencedor)
            else:
                return

    def salva_vencedores(self):
        caminho = self.var_caminho_inscritos.get()
        relatorio = self.arquivos.salva_arquivo_filtrado(self.df_vencedores, caminho, 'vencedores')

        showinfo('Vencedores da campanha', f'Foi gerado um relatório dos vencedores da campanha em: {relatorio}')

    def iniciar_binds(self):
        self.frame_children['entry_cpf_sorteado'].bind('<Return>', lambda e: self.registra_vencedor())

    @property
    def frame_children(self):
        return self.children['frame'].children

    @property
    def impressora1(self):
        return self.frame_children['impressora1'].get()

    @property
    def impressora2(self):
        return self.frame_children['impressora2'].get()


if __name__ == '__main__':
    Main()
