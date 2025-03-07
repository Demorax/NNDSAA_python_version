from abc import ABC, abstractmethod
from dataclasses import dataclass

class HasDistance(ABC):
    @property
    @abstractmethod
    def distance(self) -> float:
        pass

@dataclass
class Road(HasDistance):
    from_location: str
    to_location: str
    _distance: float

    @property
    def distance(self) -> float:
        return self._distance

    def __str__(self) -> str:
        return str(self.distance)
