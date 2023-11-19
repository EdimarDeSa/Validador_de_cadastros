from pydantic import BaseModel, ConfigDict, Field


class Employee(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(alias='Cadastro', default=None)
    name: str = Field(alias='Nome', default=None)
    cpf: str = Field(alias='CPF')
