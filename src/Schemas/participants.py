from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from ..cpf_cnpj import Documento
from ..data_hora_br import DatasBr
from ..telefone_celular import TelefoneECelular


class Participant(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    nome: str = Field(alias='Nome completo')
    cpf: str = Field(alias='CPF')
    rg: str = Field(alias='RG', default=None)
    data_nasc: str = Field(alias='Data de nascimento', default=None)
    telefone: str = Field(alias='Telefone')
    email: str = Field(alias='Email')
    cep: str = Field(alias='CEP', default=None)
    endereco: str = Field(alias='Endereço completo')
    data_de_cadastro: datetime = Field(alias='Data', frozen=True)
    validade_cpf: Optional[bool] = Field(default=None)
    numero: Optional[int] = Field(default=None)
    bairro: Optional[str] = Field(default=None)
    cidade: Optional[str] = Field(default=None)
    estado: Optional[str] = Field(default=None)

    @staticmethod
    def apenas_letras_e_espacos(d: str) -> bool:
        return d.isalpha() or d.isspace()

    @field_validator('nome')
    @classmethod
    def sanitiza_nome(cls, nome: str) -> str:
        ''.join(filter(cls.apenas_letras_e_espacos, nome))
        return nome.title()

    @field_validator('cpf')
    @classmethod
    def sanitiza_cpf(cls, value: str) -> str:
        doc = Documento(value, 'CPF')
        return doc.mascara_doc

    @field_validator('data_nasc')
    @classmethod
    def convert_data_nasc(cls, value: str) -> str:
        cleared = DatasBr(data=value, formato_data='%Y-%m-%d')
        return cleared.data

    @field_validator('telefone')
    @classmethod
    def convert_telefone(cls, value: str) -> str:
        return str(TelefoneECelular(value))

    @field_validator('cep')
    @classmethod
    def sanitiza_cep(cls, value: str) -> str:
        cleared = ''.join([digit for digit in value if digit.isdigit()])
        return cleared.zfill(8)

    @field_validator('data_de_cadastro', mode='before')
    @classmethod
    def convert_data_de_cadastro(cls, value: str) -> datetime:
        if 'T' in value:
            return datetime.fromisoformat(value)
        return datetime.strptime(value, '%d/%m/%Y %H:%M:%S')

    @model_validator(mode='after')
    def validate_cpf(self) -> 'Participant':
        doc = Documento(self.cpf, 'CPF')
        self.validade_cpf = doc.validade_doc
        return self


class Prize(BaseModel):
    descricao: str
    codigo: str
    quantidade: int
    centro_de_custos: str
    data_fechamento_cc: datetime
    responsavel_cc: str


class Sorteio(BaseModel):
    nome_do_sorteio: str
    dia_do_sorteio: datetime
    premios: List[Prize]
    data_do_registro: datetime
    vencedor: Optional[Participant] = None
    id_sorteio: Optional[int] = None
