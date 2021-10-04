from dataclasses import dataclass

from .vector import Vector3, Vector2

@dataclass
class Area:
    pos: Vector3
    dim: Vector2

    def key(self) -> tuple:
        return (self.pos.key(), self.dim.key())

    
    def area(self) -> int:
        return self.dim.x * self.dim.y