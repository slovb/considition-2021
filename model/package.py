from __future__ import annotations
from dataclasses import dataclass

from .area import Area
from .volume import Volume
from .vector import Vector2, Vector3

@dataclass
class Package:
    id: int
    dim: Vector3
    weightClass: int
    orderClass: int
    
    def calc_area(self) -> int:
        return self.dim.x * self.dim.y
    
    
    def calc_volume(self) -> int:
        return self.dim.x * self.dim.y * self.dim.z
    
    
    def as_volume(self, pos: Vector3) -> Volume:
        return Volume(
            pos = pos,
            dim = self.dim,
            support = Area(
                pos = pos + Vector3(0, 0, self.dim.z),
                dim = Vector2(self.dim.x, self.dim.y)
            )
        )
    
    
    def is_heavy(self) -> bool:
        return self.weightClass == 2


    def rotate(self, dim: Vector3) -> Package:
        return Package(
            id = self.id,
            dim = dim,
            weightClass = self.weightClass,
            orderClass = self.orderClass
        )
