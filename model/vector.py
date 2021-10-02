from dataclasses import dataclass

@dataclass
class Vector:
    x: int = 0
    y: int = 0
    z: int = 0

    def __add__(self, other):
        return Vector(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z
        )
    
    def __sub__(self, other):
        return Vector(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z
        )
        
    def abs(self):
        return Vector(
            abs(self.x),
            abs(self.y),
            abs(self.z)
        )
