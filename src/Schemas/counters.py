from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Contadores(BaseModel):
    data_do_evento: Optional[datetime] = None
    hora_de_inicio: Optional[datetime] = None
    hora_de_fim: Optional[datetime] = None
    cadastros_repetidos: int = Field(default=0)
    cpfs_invalidos: int = Field(default=0)
    employees: int = Field(default=0)
    inscricoes_validas: int = Field(default=0)

    def add_repetido(self) -> None:
        self.cadastros_repetidos += 1

    def add_invalido(self) -> None:
        self.cpfs_invalidos += 1

    def add_colaboradores(self) -> None:
        self.employees += 1

    def add_valido(self) -> None:
        self.inscricoes_validas += 1

    def decrement_valido(self) -> None:
        self.inscricoes_validas -= 1

    def update_event_date(self, date: str) -> None:
        self.data_do_evento = datetime.strptime(date, '%d/%m/%Y')
