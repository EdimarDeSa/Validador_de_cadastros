from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class Serializer(ABC):
    @abstractmethod
    def read(self, path: Path) -> Any:
        pass

    @abstractmethod
    def save(self, path: Path, data: Any) -> None:
        pass
