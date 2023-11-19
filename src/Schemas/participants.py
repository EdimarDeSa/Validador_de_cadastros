from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from ..cpf_cnpj import Documento
from ..data_hora_br import DatasBr
from ..telefone_celular import TelefoneECelular


class Participant(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    validade_cpf: Optional[bool] = Field(default=None)
    nome: str = Field(alias='Nome completo')
    rg: str = Field(alias='RG')
    cpf: str = Field(alias='CPF')
    data_nasc: str = Field(alias='Data de nascimento')
    telefone: str = Field(alias='Telefone')
    email: str = Field(alias='Email')
    cep: str = Field(alias='CEP')
    endereco: str = Field(alias='Endereço completo')
    data_de_cadastro: str = Field(alias='Data', frozen=True)
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
    def sanitiza_cpf(cls, value):
        doc = Documento(value, 'CPF')
        cls.validade_cpf = doc.validade_doc
        return doc.mascara_doc

    @field_validator('data_nasc')
    @classmethod
    def convert_data_nasc(cls, value):
        cleared = DatasBr(data=value, formato_data='%Y-%m-%d')
        return cleared.data

    @field_validator('telefone')
    @classmethod
    def convert_telefone(cls, value):
        return str(TelefoneECelular(value))

    @field_validator('cep')
    @classmethod
    def sanitiza_cep(cls, value):
        cleared = ''.join([digit for digit in value if digit.isdigit()])
        return cleared.zfill(8)

    @field_validator('data_de_cadastro')
    @classmethod
    def convert_data_de_cadastro(cls, value):
        cleared = DatasBr(data_e_hora=value)
        return cleared.data_e_hora

    @model_validator(mode='after')
    def validate_cpf(self) -> 'Participant':
        doc = Documento(self.cpf, 'CPF')
        self.validade_cpf = doc.validade_doc
        return self


class Premio(BaseModel):
    descricao: str
    codigo: str
    quantidade: int
    centro_de_custosc: str
    data_fechamento_cc: datetime
    responsavel_cc: str


class Sorteio(BaseModel):
    id_sorteio: int
    nome_do_sorteio: str
    dia_do_sorteio: datetime
    premios: List[Premio]
    vencedor: Participant
    data_do_registro: datetime
