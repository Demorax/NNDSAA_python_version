from dataclasses import dataclass


@dataclass
class Coord:
    def __init__(self):
        self.x: float
        self.y: float

    def __str__(self) -> str:
        return "f(${self.x},${self.y})"