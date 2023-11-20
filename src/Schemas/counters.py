from pydantic import BaseModel, Field


class Contadores(BaseModel):
    cadastros_repetidos: int = Field(default=0)
    cpfs_invalidos: int = Field(default=0)
    employees: int = Field(default=0)
    inscricoes_validas: int = Field(default=0)
    out_of_time: int = Field(default=0)

    def add_repetido(self) -> None:
        self.cadastros_repetidos += 1

    def add_invalido(self) -> None:
        self.cpfs_invalidos += 1

    def add_colaboradores(self) -> None:
        self.employees += 1

    def add_out_of_time(self) -> None:
        self.out_of_time += 1

    def add_valido(self) -> None:
        self.inscricoes_validas += 1

    def decrement_valido(self) -> None:
        self.inscricoes_validas -= 1
