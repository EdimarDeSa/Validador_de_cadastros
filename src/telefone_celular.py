import re

__all__ = ['TelefoneECelular']


class TelefoneECelular:
    def __init__(self, telefone):
        self._numero = self._sanitiza_telefone(telefone)
        if len(self._numero) <= 7:
            raise ValueError('Número inválido, deve ser um celular ou fixo com DDD')

    def _captura_numeros(self):
        return re.search(
            r'(\d{2,3}?)?(\d{2})([6-9])?(\d{4})(\d{4}$)', self._numero
        ).groups()

    def __str__(self):
        DDI, DDD, CEL, NUM1, NUM2 = self._captura_numeros()
        if not DDI:
            return (
                f'({DDD}) {NUM1}-{NUM2}' if not CEL else f'({DDD}) {CEL}{NUM1}-{NUM2}'
            )
        else:
            return (
                f'+{DDI} ({DDD}) {NUM1}-{NUM2}'
                if not CEL
                else f'+{DDI} ({DDD}) {CEL}{NUM1}-{NUM2}'
            )

    def _sanitiza_telefone(self, telefone) -> str:
        return ''.join(filter(str.isdigit, telefone))


if __name__ == '__main__':
    print(str(TelefoneECelular('+55 (65) 99912-3899')))
