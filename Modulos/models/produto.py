class Produto():
    def __init__(self, codigo, nome, quantidade, cc, data_fechamento_cc, responsavel_cc):
        self.codigo = codigo
        self.nome = nome
        self.quantidade = quantidade
        self.cc = cc
        self.data_fechamento_cc = data_fechamento_cc
        self.responsavel_cc = responsavel_cc
    
    def __str__(self):
        return self.nome

