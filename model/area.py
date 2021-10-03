from dataclasses import dataclass
from .vector import Vector

@dataclass
class Area:
    pos: Vector
    dimX: int
    dimY: int

    def area(self) -> int:
        return self.dimX * self.dimY