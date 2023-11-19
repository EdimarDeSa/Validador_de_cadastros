from csv import DictReader, DictWriter, Sniffer
from pathlib import Path
from typing import Any, Dict, List

from src.Contracts.serializer import Serializer

CODECS: list = [
    'utf_8_sig',
    'cp65001',
    'utf8',
    'UTF',
    'U8',
    'UTF-16LE',
    'UTF-16BE',
    'utf16',
    'U16',
    'UTF-32LE',
    'UTF-32BE',
    'utf32',
    'U32',
    'L10',
    'L1',
    'latin10',
    'latin1',
    'iso-8859-16',
    'iso-8859-1',
    'ascii',
    'cp437',
    'cp850',
    'big5',
    'unicode-1-1-utf-7',
]


class CsvSerializer(Serializer):
    def read(self, path: Path) -> List[Dict[str, Any]]:
        for CODEC in CODECS:
            try:
                with open(path, encoding=CODEC) as file:
                    dialect = Sniffer().sniff(
                        ''.join([file.readline() for _ in range(5)])
                    )
                    file.seek(0)

                    csv_file = DictReader(file, dialect=dialect)

                    if any(
                        [
                            field in ['CPF', 'Endereço completo']
                            for field in csv_file.fieldnames
                        ]
                    ):
                        return list(csv_file)
            except UnicodeDecodeError or UnicodeError:
                continue

    def save(self, path: Path, data: Any) -> None:
        pass
