from dataclasses import dataclass

from .vector import Vector

@dataclass
class Area:
    pos: Vector
    dim_x: int
    dim_y: int

    
    def area(self) -> int:
        return self.dim_x * self.dim_y