from dataclasses import dataclass

from .vector import Vector3, Vector2

@dataclass(order=True, frozen=True)
class Area:
    pos: Vector3
    dim: Vector2

    
    def calc_area(self) -> int:
        return self.dim.x * self.dim.y
