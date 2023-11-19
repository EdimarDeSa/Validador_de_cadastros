from typing import Literal

from validate_docbr import CNPJ, CPF

__all__ = ['Documento']


class Documento:
    def __init__(self, doc_number: str, doc_type: [Literal['CPF'], Literal['CNPJ']]):
        self._doc_type = doc_type
        self._doc = self.sanitiza_doc(doc_number)
        self._validador_doc = self._get_validator()
        self._validade_do_doc = self._validador_doc.validate(self._doc)
        self._doc_com_mascara = self._validador_doc.mask(self._doc)

    def _get_validator(self):
        tipos_doc = {'CPF': CPF, 'CNPJ': CNPJ}
        return tipos_doc[self._doc_type]()

    def sanitiza_doc(self, doc_number):
        cleaned = ''.join(filter(str.isdigit, doc_number))
        to_fill = 11 if self._doc_type == 'CPF' else 14
        return cleaned.zfill(to_fill)

    @property
    def mascara_doc(self) -> str:
        return self._doc_com_mascara

    @property
    def numero_doc(self) -> str:
        return self._doc

    @property
    def validade_doc(self) -> bool:
        return self._validade_do_doc

    def __str__(self) -> str:
        return self._doc

    def __repr__(self) -> repr:
        return f'<Document number: {self._doc}>'


if __name__ == '__main__':
    print(repr(Documento('048.245.251-01', 'CPF')))
    # print(str(Documento('88.321.331/0001-01')))
