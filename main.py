from turtle import title
import ttkbootstrap as tkb

from Modulos.imprimir import Impressao
from Modulos.configs import Configuracoes
from Modulos.models import Tabelas
from Modulos.models.janelas import JanelaSorteios, JanelaImpressao

class Main(tkb.Window):
    def __init__(self):
        tkb.Window.__init__(self, themename='minty')
        self.configuracoes = Configuracoes()
        self.impressao = Impressao()
        self.tabelas = Tabelas()

        self.iniciar_root()
        self.inicia_widgets()
        self.redimenciona_tela()

        self.mainloop()
    
    def iniciar_root(self):
        self.resizable(False, True)
        self.title('Validador de inscrições')

    def inicia_widgets(self):
        self.notebook = tkb.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        # tab_registro_de_campanha = self.notebook.add('Registro de sorteios')
        # JanelaSorteios(tab_registro_de_campanha, self.configuracoes, self.tabelas, self.impressao)

        # tab_impressao = self.notebook.add('Validação e impressão')
        # JanelaImpressao(tab_impressao, self.configuracoes, self.tabelas, self.impressao)

        # tab_registro_de_vencedor = self.notebook.add('Registro de vencedor')
        # self.aba_registro_de_vencedor = AbaRegistroDevencedor(tab_registro_de_vencedor, self.configuracoes, self.tabelas, self.impressao)

        # frame_graficos = Frame(master=self.notebook, **self.configuracoes.frame_parametros, name='frame_graficos')
        # self.notebook.add(frame_graficos, state='hidden', text='Graficos')

    def redimenciona_tela(self):
        dimensoes = {
            'Registro de sorteios': {
                'width': 1200,
                'height': 500,
                'pos_x': self.__calcula_posicao_x,
                'pos_y': self.__calcula_posicao_y,
            },
            'Validação e impressão': {
                'width': 800,
                'height': 400,
                'pos_x': self.__calcula_posicao_x,
                'pos_y': self.__calcula_posicao_y,
            }
        }

        # tela_selecionada = self.notebook.:
        dimensoes_tela = dimensoes['Registro de sorteios']

        width, height = dimensoes_tela['width'], dimensoes_tela['height']
        pos_x, pos_y = dimensoes_tela['pos_x'], dimensoes_tela['pos_y']

        self.geometry(f"{width}x{height}+{pos_x}+{pos_y}")

    def __calcula_posicao_y(self) -> int:
        altura_livre_do_monitor = self.winfo_screenheight() - self.altura_da_tela
        y_inicial = altura_livre_do_monitor // 10
        return y_inicial

    def __calcula_posicao_x(self) -> int:
        largura_livre_do_monitor = self.winfo_screenwidth() - self.largura_da_tela
        x_inicial = largura_livre_do_monitor // 2
        return x_inicial


if __name__ == '__main__':
    Main()
