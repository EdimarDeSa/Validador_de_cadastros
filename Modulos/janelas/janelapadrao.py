from ttkbootstrap import *

from Modulos.configuracoes import *
from Modulos.imagens import *
from Modulos.imprimir import *
from Modulos.models import *

__all__ = ['JanelaPadrao']


class JanelaPadrao:
    def __init__(
        self,
        master: Frame,
        configuracoes: Configuracoes,
        tabelas: Tabelas,
        impressao: Impressao = None,
        **kwargs
    ):
        self.master = master if master else kwargs.get('master', None)
        self.configuracoes = (
            configuracoes if configuracoes else kwargs.get('configuracoes', None)
        )
        self.tabelas = tabelas if tabelas else kwargs.get('tabelas', None)
        self.impressao = impressao if impressao else kwargs.get('impressao', None)
        self.imagens = Imagens()

        self.reg_verifica_digito_numerico = master.register(
            self.verifica_digito_numerico
        )

    @staticmethod
    def verifica_digito_numerico(entrada: str):
        return entrada.isnumeric() or entrada == ''
