from .produto import Produto

class Sorteio():
    def __init__(self, nome=None):
        self.nome = nome
        self.produtos = ()
        self.vencedor = None
    
    def registra_premio(self, premio:Produto):
        lista = list(self.produtos)
        lista.append(premio)
        self.produtos = tuple(lista)
    
    def registra_vencedor(self, vencedor):
        self.vencedor = vencedor
    
    def __str__(self):
        return self.nome
    