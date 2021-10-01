from dataclasses import dataclass

@dataclass
class Pos:
    x: int = 0
    y: int = 0
    z: int = 0

    def __add__(self, other):
        return Pos(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z
        )
