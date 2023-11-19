from enum import StrEnum
from pathlib import Path
from typing import Any, Dict, Iterable, Optional, Tuple

import tinydb
from tinydb import Query, where

from src.Contracts.serializer import Serializer
from src.Schemas.counters import Contadores
from src.Schemas.employee import Employee
from src.Schemas.participants import Participant, Premio, Sorteio
from src.Serializers.csvserializer import CsvSerializer


class Tabelas(StrEnum):
    PARTICIPANTES = 'temp_participantes'
    SORTEIOS = 'temp_sorteios'
    PERMANENTE = 'registro_permanente_participantes'
    EMPLOYEES = 'funcionarios'


class Exten(StrEnum):
    CSV = '.csv'
    TXT = '.txt'


class CamposORM(StrEnum):
    CPF = 'cpf'
    NAME = 'nome'
    RG = 'rg'
    BIRTH_DATE = 'data_nasc'
    TEL = 'telefone'
    EMAIL = 'email'
    ZIP_CODE = 'cep'
    ADDRESS = 'endereco'
    ADRSS_NUM = 'numero'
    NEIGHBORHOOD = 'bairro'
    CITY = 'cidade'
    STATE = 'estado'
    REG_DATE = 'data_de_cadastro'
    VALIDADE_CPF = 'validade_cpf'


class DataBase:
    def __init__(self, db_path: str = './db.json') -> None:
        self.__db = tinydb.TinyDB(db_path)

        self.__reset_temp_infos()

    def connected(self) -> bool:
        return self.__db._opened

    def create(self, tabela: Tabelas, data: Participant | Sorteio | Employee) -> int:
        document = data.model_dump()
        return self.__db.table(tabela).insert(document)

    def create_multiple(
        self, tabela: Tabelas, datas: Iterable[Participant] | Iterable[Sorteio]
    ) -> Iterable[int]:
        documents = [info.model_dump() for info in datas]
        return self.__db.table(tabela).insert_multiple(documents)

    def search(self, tabela: str, query_dict: Dict[str, Any]):
        return self.__db.table(tabela).get(Query().fragment(query_dict))

    def delete(self, table: str, query_dict: Dict[str, Any]) -> Tuple[int]:
        items_to_delete = self.__db.table(table).search(Query().fragment(query_dict))
        ids_to_delete = [item.doc_id for item in items_to_delete]
        return tuple(self.__db.table(table).remove(doc_ids=ids_to_delete))

    def __reset_temp_infos(self) -> None:
        self.__db.drop_table(Tabelas.PARTICIPANTES)
        self.__db.drop_table(Tabelas.SORTEIOS)
        self.__db.drop_table(Tabelas.EMPLOYEES)
        self.__db.clear_cache()

    def close(self) -> None:
        datas = self.__db.table(Tabelas.PARTICIPANTES).all()
        for data in datas:
            query = where(CamposORM.CPF) == data[CamposORM.CPF]
            self.__db.table(Tabelas.PERMANENTE).upsert(data.copy(), query)

        self.__reset_temp_infos()


class Model:
    def __init__(self) -> None:
        self.__db_con = DataBase()
        self.contadores = Contadores()

    def create_participants(self, data: Iterable[dict]) -> Tuple[int]:
        list_of_participants = [Participant(**info) for info in data]
        inserted = tuple(
            [
                self.__db_con.create(Tabelas.PARTICIPANTES, participant)
                for participant in list_of_participants
                if self._validate_participants(participant)
            ]
        )
        return inserted

    def create_employees(self, data: Iterable[dict]) -> Tuple[int]:
        list_of_employees = [Employee(**info) for info in data]
        inserted = tuple(
            [
                self.__db_con.create(Tabelas.EMPLOYEES, employee)
                for employee in list_of_employees
            ]
        )
        return inserted

    def read_participant_by_cpf(self, cpf: str) -> Optional[Participant]:
        data = self.__db_con.search(Tabelas.PARTICIPANTES, {str(CamposORM.CPF): cpf})
        if data:
            return Participant(**data)
        return None

    def delete_participant_by_cpf(self, cpf: str) -> Optional[Tuple[int]]:
        id_ = self.__db_con.delete(Tabelas.PARTICIPANTES, {str(CamposORM.CPF): cpf})
        if id_:
            self.contadores.decrement_valido()
        return id_

    def read_file(self, file_path: Path) -> Any:
        serializer = self._select_serializer(file_path.suffix)
        return serializer.read(file_path)

    @staticmethod
    def _select_serializer(extension: str) -> Serializer:
        match extension.lower():
            case Exten.CSV:
                return CsvSerializer()
            case Exten.TXT:
                return CsvSerializer()
            case _:
                raise ValueError('Invalid extension!')

    def update_event_date(self, date: str) -> None:
        self.contadores.update_event_date(date)

    def _validate_participants(self, participant: Participant) -> bool:
        if self.contadores.data_do_evento is None:
            raise KeyError('É necessário registrar a data do evento')

        if not participant.validade_cpf:
            self.contadores.add_invalido()
            return False

        query_dict = {str(CamposORM.CPF): participant.cpf}

        already_exists = self.__db_con.search(Tabelas.PARTICIPANTES, query_dict)
        if already_exists is not None:
            self.contadores.add_repetido()
            return False

        colaborator = self.__db_con.search(Tabelas.EMPLOYEES, query_dict)
        if colaborator is not None:
            self.contadores.add_colaboradores()
            return False

        self.contadores.add_valido()
        return True

    def close(self):
        self.__db_con.close()
