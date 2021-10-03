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

    
    def __getitem__(self, key):
        if key == 'x':
            return self.x
        elif key == 'y':
            return self.y
        elif key == 'z':
            return self.z
        else:
            raise KeyError(key)

    
    def __setitem__(self, key, value):
        if key == 'x':
            self.x = value
        elif key == 'y':
            self.y = value
        elif key == 'z':
            self.z = value
        else:
            raise KeyError(key)

    
    def abs(self):
        return Vector(
            abs(self.x),
            abs(self.y),
            abs(self.z)
        )
