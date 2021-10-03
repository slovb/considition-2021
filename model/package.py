from dataclasses import dataclass

from .vector import Vector

@dataclass
class Package:
    id: int
    dim: Vector
    weightClass: int
    orderClass: int
    
    def calc_area(self) -> int:
        return self.dim.y * self.dim.x
    
    
    def is_heavy(self) -> bool:
        return self.weightClass == 2       
