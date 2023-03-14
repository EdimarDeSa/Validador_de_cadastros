from Modulos import Tk, Frame, Label, Button, StringVar, Combobox, Progressbar, Thread, parse, validate, sleep
from Modulos import STRING_COLUNA_CPF, NOME_PARTICIPANTE
from Modulos.arquivo import AbreArquivo
from Modulos.imprimir import Impressao
from Modulos.configs import Configuracoes
from Modulos.log_panel import LogPanel


class Main(Tk):
    total_de_cadastros: int = 0
    participantes_validos: int = 0
    cpfs_invalidos: int = 0
    cadastros_repetidos: int = 0
    cadastro_atual: int = 0
    impressora_da_vez: bool = True
    arquivo_filtrado = None
    dicionario_csv = None

    def __init__(self):
        Tk.__init__(self)

        self.stringvar_cpfs_invalidos = StringVar(value='-')
        self.stringvar_cadastros_repetidos = StringVar(value='-')
        self.stringvar_participantes_validos = StringVar(value='-')
        self.stringvar_progresso = StringVar(value='- de -')

        self.configuracoes = Configuracoes(root=self)
        self.arquivos = AbreArquivo()
        self.impressao = Impressao()

        self.iniciar_root()
        self.inicia_frame()
        self.inicia_widgets()
        self.binds()

        self.mainloop()

    def iniciar_root(self):
        self.configure(**self.configuracoes.root_parametros)
        self.title('Validador de cadastros')
        self.resizable(False, False)
        self.geometry(f'{self.configuracoes.largura_da_tela}x{self.configuracoes.altura_da_tela}'
                      f'+{self.configuracoes.posicao_x}+{self.configuracoes.posicao_y}')

        self.configuracoes.frame_parametros['master'] = self

    def inicia_frame(self):
        frame = Frame(**self.configuracoes.frame_parametros, name='frame')
        frame.pack(padx=10, pady=10, ipady=285)

        self.configuracoes.label_parametros['master'] = frame
        self.configuracoes.buttons_parametros['master'] = frame
        self.configuracoes.combobox_parametros['master'] = frame
        self.configuracoes.barra_de_progresso_parametros['master'] = frame

    def inicia_widgets(self):
        Label(
            text='Selecione a impressora 1:', **self.configuracoes.label_parametros
        ).grid(column=0, row=0, padx=5, pady=5, sticky='w')

        Combobox(
            values=self.impressao.listar_impressoras(), name='impressora1', **self.configuracoes.combobox_parametros
        ).grid(column=1, row=0, padx=5, pady=5, sticky='nsew')
        self.children['frame'].children['impressora1'].current(3)

        Label(
            text='Selecione a impressora 2:', **self.configuracoes.label_parametros
        ).grid(column=0, row=1, padx=5, pady=5, sticky='w')

        Combobox(
            values=self.impressao.listar_impressoras(), name='impressora2', **self.configuracoes.combobox_parametros
        ).grid(column=1, row=1, padx=5, pady=5, sticky='nsew')
        self.children['frame'].children['impressora2'].current(2)

        Progressbar(
            **self.configuracoes.barra_de_progresso_parametros
        ).grid(column=0, columnspan=2, row=2, sticky='nsew', padx=5, pady=5)

        Label(
            text=f'Analisando: ', **self.configuracoes.label_parametros
        ).grid(column=0, row=3, padx=5, pady=5, sticky='w')

        Label(
            textvariable=self.stringvar_progresso, **self.configuracoes.label_parametros
        ).grid(column=1, row=3, padx=5, pady=5, sticky='ew')

        Label(
            text='Participantes válidos:', **self.configuracoes.label_parametros
        ).grid(column=0, row=4, padx=5, pady=5, sticky='w')

        Label(
            textvariable=self.stringvar_participantes_validos, **self.configuracoes.label_parametros
        ).grid(column=1, row=4, padx=5, pady=5, sticky='ew')

        Label(
            text='Cadastros repetidos:', **self.configuracoes.label_parametros
        ).grid(column=0, row=5, padx=5, pady=5, sticky='w')

        Label(
            textvariable=self.stringvar_cadastros_repetidos, **self.configuracoes.label_parametros
        ).grid(column=1, row=5, padx=5, pady=5, sticky='ew')

        Label(
            text='CPFs inválidos:', **self.configuracoes.label_parametros
        ).grid(column=0, row=6, padx=5, pady=5, sticky='w')

        Label(
            textvariable=self.stringvar_cpfs_invalidos, **self.configuracoes.label_parametros
        ).grid(column=1, row=6, padx=5, pady=5, sticky='ew')

        Button(
            command=self.inicia_verificacao, text='Iniciar análise', name='bt_inicia_analise',
            **self.configuracoes.buttons_parametros
        )

        Button(
            command=self.abre_arquivo, text='Abrir arquivo.csv', name='bt_abrir_arquivo',
            **self.configuracoes.buttons_parametros
        ).grid(column=0, row=9, padx=5, pady=5, sticky='nsew')

    def binds(self):
        def event_key(key):
            return key.keysym

        def ctrl_events(event):
            events = dict(
                a=self.abre_arquivo,
            )
            return events[event_key(event)]()
        self.bind('<Control-Key>', lambda event: ctrl_events(event))

    def inicia_verificacao(self):
        Thread(target=self.verifica, daemon=True).start()
        self.children['frame'].children['bt_inicia_analise'].grid_forget()

    def abre_arquivo(self):
        self.dicionario_csv = self.arquivos.dicionariza_csv()
        self.arquivo_filtrado = self.arquivos.inicia_arquivo_filtrado(self.dicionario_csv)
        self.registra_total_cadastros()
        self.title(f'Verificador - {self.arquivos.ARQUIVO_ATUAL}')

        self.children['frame'].children['bt_inicia_analise'].grid_forget()
        self.children['frame'].children['bt_inicia_analise'].grid(column=1, row=9, padx=5, pady=5, sticky='nsew')

    def verifica(self):
        ja_registrados = set()

        Thread(target=self.inicia_relatorio).start()

        for cadastro in self.dicionario_csv:
            self.atualiza_progresso()

            cpf_com_mascara = self.mascara_cpf(str(cadastro[STRING_COLUNA_CPF]))
            
            if cpf_com_mascara in ja_registrados:
                self.atualiza_cadastros_repetidos()
                continue
            
            if not self.cpf_valido(cpf_com_mascara):
                continue
            
            nome_participante = ' '.join([nome.capitalize() for nome in cadastro[NOME_PARTICIPANTE].split()])
            self.impressao.imprimir(cpf_com_mascara, nome_participante, self.verifica_vez_da_impressora())
            self.arquivo_filtrado.writerow(cadastro)
            ja_registrados.add(cpf_com_mascara)

            self.atualiza_participantes_validos()

    def registra_total_cadastros(self):
        self.total_de_cadastros = self.arquivos.TOTAL_DE_LINHAS - 1
        self.stringvar_progresso.set(
            f'{self.__formata_quantidade(0)} de {self.__formata_quantidade(self.total_de_cadastros)}'
            f' - {self.__formata_porcentagem(0)}')

    def atualiza_progresso(self):
        self.cadastro_atual += 1
        porcentagem = self.__calcula_porcentagem(self.cadastro_atual)
        self.stringvar_progresso.set(
            f'{self.__formata_quantidade(self.cadastro_atual)} de {self.__formata_quantidade(self.total_de_cadastros)}'
            f' - {self.__formata_porcentagem(porcentagem)}')

    def atualiza_participantes_validos(self):
        self.participantes_validos += 1
        porcentagem = self.__calcula_porcentagem(self.participantes_validos)
        self.stringvar_participantes_validos.set(
            f'{self.__formata_quantidade(self.participantes_validos)} - {self.__formata_porcentagem(porcentagem)}')

    def atualiza_cadastros_repetidos(self):
        self.cadastros_repetidos = self.cadastro_atual - self.participantes_validos - self.cpfs_invalidos
        porcentagem = self.__calcula_porcentagem(self.cadastros_repetidos)
        self.stringvar_cadastros_repetidos.set(
            f'{self.__formata_quantidade(self.cadastros_repetidos)} - {self.__formata_porcentagem(porcentagem)}')

    def atualiza_cpfs_invalidos(self):
        self.cpfs_invalidos += 1
        porcentagem = self.__calcula_porcentagem(self.cpfs_invalidos)
        self.stringvar_cpfs_invalidos.set(
            f'{self.__formata_quantidade(self.cpfs_invalidos)} - {self.__formata_porcentagem(porcentagem)}')

    @staticmethod
    def __formata_quantidade(valor: int) -> str:
        return f'{valor:03}'

    @staticmethod
    def __formata_porcentagem(porcentagem: float) -> str:
        return f'{porcentagem:03.2f}%'

    def __calcula_porcentagem(self, valor: int, precisao: int = 2):
        porcentagem = round(valor / self.total_de_cadastros * 100, precisao)
        return porcentagem

    @staticmethod
    def mascara_cpf(cpf_bruto):
        return parse(doclist=cpf_bruto, doctype='cpf', mask=True)

    def cpf_valido(self, cpf_com_mascara):
        validado = validate(doclist=cpf_com_mascara, doctype='cpf', lazy=False)
        if not validado:
            self.atualiza_cpfs_invalidos()
        return validado

    def verifica_vez_da_impressora(self):
        def inverte_impressora_da_vez():
            self.impressora_da_vez = not self.impressora_da_vez

        if not self.impressora2 or self.impressora_da_vez:
            inverte_impressora_da_vez()
            return self.impressora1
        else:
            inverte_impressora_da_vez()
            return self.impressora2

    def inicia_relatorio(self):
        log_panel = LogPanel(master=self, kw=self.configuracoes.label_parametros)
        jobs = [1]
        if self.impressora2:
            impressoras = [self.impressora1, self.impressora2]
        else:
            impressoras = [self.impressora1]
        while jobs:
            sleep(2)

            for indice, impressora in enumerate(impressoras):
                log_panel.log_clear(indice)
                jobs.clear()
                jobs = self.impressao.printer_job_checker(impressora)
                time_string = self.__calcula_tempo(len(jobs))
                log_panel.log_impressora(f'{impressora} - Tempo estimado: {time_string} minutos', indice)
                for job in jobs:
                    if job == 'Impressoes finalizadas':
                        log_panel.log_impressora(f'{job}...', indice)
                    else:
                        log_panel.log_impressora(f'Imprimindo: {job}', indice)

    @staticmethod
    def __calcula_tempo(quantidade: int):
        total_seconds = (quantidade - 1) * 2
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes}:{seconds:02}"

    @property
    def impressora1(self):
        return self.children['frame'].children['impressora1'].get()

    @property
    def impressora2(self):
        return self.children['frame'].children['impressora2'].get()


if __name__ == '__main__':
    Main()
