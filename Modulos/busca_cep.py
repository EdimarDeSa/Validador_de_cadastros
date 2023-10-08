from requests import get


__all__ = ['BuscaEndereco']


class BuscaEndereco:
    def __init__(self, cep: str):
        self._cep = self._sanitiza_cep(cep)
        if not self._valida_cep():
            raise ValueError("CEP inválido.")
        self._dados = self._pesquisa_cep()

    @staticmethod
    def _sanitiza_cep(cep: str) -> str:
        return ''.join(filter(str.isdigit, cep))

    def _valida_cep(self) -> bool:
        return len(self._cep) == 8

    def _pesquisa_cep(self) -> dict:
        url = f"https://viacep.com.br/ws/{self._cep}/json/"
        return get(url).json()

    @property
    def cep(self) -> str:
        return self._dados['cep']

    @property
    def logradouro(self) -> str:
        return self._dados['logradouro']

    @property
    def complemento(self) -> str:
        return self._dados['complemento']

    @property
    def bairro(self) -> str:
        return self._dados['bairro']

    @property
    def localidade(self) -> str:
        return self._dados['localidade']

    @property
    def uf(self) -> str:
        return self._dados['uf']

    @property
    def __dict__(self) -> dict:
        return self._dados

    def __str__(self) -> str:
        return f'CEP: {self.cep} - Cidade: {self.localidade} - Estado: {self.uf}'

    def __repr__(self) -> repr:
        return repr(self._dados)


if __name__ == '__main__':
    busca = BuscaEndereco('88.132-600')
    print(busca.__dict__)
