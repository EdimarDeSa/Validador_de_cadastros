from abc import ABC, abstractmethod
from pathlib import Path


class Serializer(ABC):
    @abstractmethod
    def read(self, path: Path, **kwargs) -> any:
        pass

    @abstractmethod
    def save(self, path: Path, data: any, **kwargs) -> None:
        pass
