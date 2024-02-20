from pathlib import Path

from pandas import read_excel, DataFrame

from src.Contracts.serializer import Serializer


class ExcelSerializer(Serializer):
    def read(self, path: Path, **kwargs) -> DataFrame:
        return read_excel(path, dtype='string', **kwargs)

    def save(self, path: Path, data: any, **kwargs) -> None:
        pass
