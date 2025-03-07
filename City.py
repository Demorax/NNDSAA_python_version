from dataclasses import dataclass
from typing import Optional

from Coord import Coord

@dataclass
class City:
    name: str
    coordinates: Optional[Coord] = None