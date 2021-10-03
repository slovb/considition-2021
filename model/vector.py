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
        if key == 'x' or key == 0:
            return self.x
        elif key == 'y' or key == 1:
            return self.y
        elif key == 'z' or key == 2:
            return self.z
        else:
            raise KeyError(key)

    
    def __setitem__(self, key, value):
        if key == 'x' or key == 0:
            self.x = value
        elif key == 'y' or key == 1:
            self.y = value
        elif key == 'z' or key == 2:
            self.z = value
        else:
            raise KeyError(key)


    def permutate(self):
        self.x, self.y, self.z = self.y, self.z, self.x
        
        
    def flip(self):
        self.x, self.y, self.z = self.y, self.x, self.z
    

    def abs(self):
        return Vector(
            abs(self.x),
            abs(self.y),
            abs(self.z)
        )
