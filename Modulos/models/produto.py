__all__ = ['Produto']


class Produto:
    def __init__(
        self,
        codigo='',
        nome='',
        quantidade='',
        cc='',
        data_fechamento_cc='',
        responsavel_cc='',
        *kw,
    ):
        if kw:
            codigo, nome, quantidade, cc, data_fechamento_cc, responsavel_cc = kw

        self.codigo = codigo
        self.nome = nome
        self.quantidade = quantidade
        self.cc = cc
        self.data_fechamento_cc = data_fechamento_cc
        self.responsavel_cc = responsavel_cc

    @property
    def valores(self):
        return list(self.__iter__())

    def __str__(self):
        return self.nome

    def __repr__(self):
        return f'<nome: {self.nome}>'

    def __iter__(self):
        return iter(
            [
                self.codigo,
                self.nome,
                self.quantidade,
                self.cc,
                self.data_fechamento_cc,
                self.responsavel_cc,
            ]
        )
