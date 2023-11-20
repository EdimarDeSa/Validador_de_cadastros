from datetime import date, datetime, time
from typing import Optional

from pydantic import BaseModel


class EventParameters(BaseModel):
    check_date: bool = True
    check_time: bool = True
    check_cpf: bool = True
    check_only_one: bool = True
    check_employee: bool = True
    data_do_evento: Optional[date] = None
    hora_de_inicio: Optional[time] = None
    hora_de_fim: Optional[time] = None

    def update_event_date(self, value: str) -> None:
        self.data_do_evento = datetime.strptime(value, '%d/%m/%Y').date()

    def set_hora_inicio(self, value: str) -> None:
        self.hora_de_inicio = datetime.strptime(value, '%H:%M:%S').time()

    def set_hora_fim(self, value: str) -> None:
        self.hora_de_fim = datetime.strptime(value, '%H:%M:%S').time()
