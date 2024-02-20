import datetime
from enum import StrEnum
from pathlib import Path
from typing import Iterable, Optional

import tinydb
from tinydb import Query, where
import pandas as pd

from src.Contracts.serializer import Serializer
from src.Schemas.counters import Contadores
from src.Schemas.employee import Employee
from src.Schemas.event_parameters import EventParameters
from src.Schemas.participants import Participant, Prize, Sorteio
from src.Serializers.csvserializer import CsvSerializer
from src.Serializers.excelserializer import ExcelSerializer


class Tabelas(StrEnum):
    PRODUTOS = 'temp_produtos'
    PARTICIPANTES = 'temp_participantes'
    SORTEIOS = 'temp_sorteios'
    PERMANENTE = 'registro_permanente_participantes'
    EMPLOYEES = 'temp_funcionarios'


class Exten(StrEnum):
    CSV = '.csv'
    TXT = '.txt'
    XLSX = '.xlsx'


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
    def __init__(self, db_path: Path) -> None:
        self.__db = tinydb.TinyDB(db_path, indent=2)

        self.__reset_temp_infos()

    def connected(self) -> bool:
        return self.__db._opened

    def create(self, tabela: Tabelas, data: Participant | Sorteio | Employee) -> int:
        document = data.model_dump(mode='json', exclude_unset=True)
        return self.__db.table(tabela).insert(document)

    def create_multiple(
        self, tabela: Tabelas, datas: Iterable[Participant] | Iterable[Sorteio]
    ) -> Iterable[int]:
        documents = [info.model_dump(mode='json', exclude_unset=True) for info in datas]
        return self.__db.table(tabela).insert_multiple(documents)

    def update(self, tabela: Tabelas, new_data: dict, query_dict: dict[str, any]) -> None:
        self.__db.table(tabela).update(new_data, (Query().fragment(query_dict)))

    def search(self, tabela: str, query_dict: dict[str, any]):
        return self.__db.table(tabela).get(Query().fragment(query_dict))

    def delete(self, table: str, query_dict: dict[str, any]) -> tuple[int, ...]:
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

    def next_prize_draw(self) -> int:
        return len(self.__db.table(Tabelas.SORTEIOS).all()) + 1

    def create_prod_table(self, tabela: Tabelas, data: dict) -> tuple[int, ...]:
        return tuple(self.__db.table(tabela).insert_multiple(data))


class Model:
    def __init__(self) -> None:
        db_path = Path(__file__).resolve().parent.parent.parent / 'db.json'
        self.__db_con = DataBase(db_path=db_path)
        self.contadores = Contadores()
        self.event_params = EventParameters()

    @staticmethod
    def _create_list_of_participants(chunk: Iterable[dict]) -> list[Participant]:
        return [Participant(**data) for data in chunk]

    def create_participants(self, data: Iterable[dict]) -> tuple[int]:
        data = tuple(data)

        list_of_participants = self._create_list_of_participants(data)

        inserted = tuple(
            [
                self.__db_con.create(Tabelas.PARTICIPANTES, participant)
                for participant in list_of_participants
                if self._validate_participants(participant)
            ]
        )
        return inserted

    def create_employees(self, data: Iterable[dict]) -> tuple[int]:
        list_of_employees = [Employee(**info) for info in data]
        inserted = tuple(
            [
                self.__db_con.create(Tabelas.EMPLOYEES, employee)
                for employee in list_of_employees
            ]
        )
        return inserted

    def create_prize(
        self,
        descricao: str,
        codigo: str,
        quantidade: int,
        centro_de_custos: str,
        data_fechamento_cc: datetime,
        responsavel_cc: str,
    ) -> Prize:
        kwargs = dict(
            descricao=descricao,
            codigo=codigo,
            quantidade=quantidade,
            centro_de_custos=centro_de_custos,
            data_fechamento_cc=data_fechamento_cc,
            responsavel_cc=responsavel_cc,
        )
        return Prize(**kwargs)

    def create_prize_drawing(self, nome_do_sorteio: str, dia_do_sorteio: str, prizes: list[Prize]) -> int:
        sorteio = Sorteio(
            id_sorteio=self.__db_con.next_prize_draw(),
            nome_do_sorteio=nome_do_sorteio,
            dia_do_sorteio=datetime.datetime.strptime(dia_do_sorteio, '%d/%m/%Y').date(),
            premios=prizes,
            data_do_registro=datetime.datetime.now().date(),
        )

        id_ = self.__db_con.create(Tabelas.SORTEIOS, sorteio)

        return id_

    def read_participant_by_cpf(self, cpf: str) -> Optional[Participant]:
        data = self.__db_con.search(Tabelas.PARTICIPANTES, {str(CamposORM.CPF): cpf})
        if data:
            return Participant(**data)
        return None

    def read_prize_draw(self, id_sorteio: int) -> Sorteio:
        data = self.__db_con.search(
            Tabelas.SORTEIOS,
            {'id_sorteio': id_sorteio}
        )
        return Sorteio(**data)

    def delete_participant_by_cpf(self, cpf: str) -> Optional[tuple[int]]:
        id_ = self.__db_con.delete(Tabelas.PARTICIPANTES, {str(CamposORM.CPF): cpf})
        if id_:
            self.contadores.decrement_valido()
        return id_

    def read_file(self, file_path: Path, **kwargs) -> any:
        serializer = self._select_serializer(file_path.suffix)
        return serializer.read(file_path, **kwargs)

    @staticmethod
    def _select_serializer(extension: str) -> Serializer:
        match extension.lower():
            case Exten.CSV:
                return CsvSerializer()
            case Exten.TXT:
                return CsvSerializer()
            case Exten.XLSX:
                return ExcelSerializer()
            case _:
                raise ValueError('Invalid extension!')

    def update_event_date(self, date: str) -> None:
        self.event_params.update_event_date(date)

    def set_hora_inicio(self, value: str) -> None:
        self.event_params.set_hora_inicio(value)

    def set_hora_fim(self, value: str) -> None:
        self.event_params.set_hora_fim(value)

    def _validate_participants(self, participant: Participant) -> bool:
        if self.event_params.check_date:
            if participant.data_de_cadastro.date() != self.event_params.data_do_evento:
                return False

        if self.event_params.check_cpf:
            if not participant.validade_cpf:
                self.contadores.add_invalido()
                return False

        query_dict = {str(CamposORM.CPF): participant.cpf}

        if self.event_params.check_only_one:
            already_exists = self.__db_con.search(Tabelas.PARTICIPANTES, query_dict)
            if already_exists is not None:
                self.contadores.add_repetido()
                return False

        if self.event_params.check_employee:
            employee = self.__db_con.search(Tabelas.EMPLOYEES, query_dict)
            if employee is not None:
                self.contadores.add_colaboradores()
                return False

        if self.event_params.check_time:
            if (
                not self.event_params.hora_de_inicio
                < participant.data_de_cadastro.time()
                < self.event_params.hora_de_fim
            ):
                self.contadores.add_out_of_time()
                return False

        self.contadores.add_valido()
        return True

    # TODO: Criar os sorteios
    # TODO: Criar os produtos

    def close(self):
        self.__db_con.close()

    def insert_winner(self, id_sorteio: int, cpf: str):
        sorteio = self.read_prize_draw(id_sorteio)
        winner = self.read_participant_by_cpf(cpf)

        sorteio.vencedor = winner

        self.__db_con.update(
            Tabelas.SORTEIOS,
            sorteio.model_dump(mode='json', exclude_unset=True),
            {'id_sorteio': id_sorteio}
        )

    def read_product_table(self, path: str) -> None:
        if not path:
            return

        path = Path(path).resolve()
        prod_df: pd.DataFrame = self.read_file(path, sheet_name=0, header=6, usecols=[2, 3])

        e = self.__db_con.create_prod_table(
            Tabelas.PRODUTOS,
            prod_df.to_json()
        )

        print(e)
