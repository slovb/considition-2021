from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Vector2:
    x: int = 0
    y: int = 0
    
    
    def key(self) -> tuple:
        return (self.x, self.y)


    def __getitem__(self, key) -> int:
        if key == 'x' or key == 0:
            return self.x
        elif key == 'y' or key == 1:
            return self.y
        raise KeyError(key)


    def __setitem__(self, key, value) -> None:
        if key in ['x', 'y', 0, 1]:
            raise AttributeError(key)
        raise KeyError(key)
 
        
    def __delitem__(self, key) -> None:
        if key in ['x', 'y', 0, 1]:
            raise AttributeError(key)
        raise KeyError(key)


@dataclass
class Vector3:
    x: int = 0
    y: int = 0
    z: int = 0

    __key: tuple = None


    def key(self) -> tuple:
        if self.__key is None:
            self.__key = (self.x, self.y, self.z)
        return self.__key


    def __add__(self, other) -> Vector3:
        return Vector3(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z
        )

    
    def __sub__(self, other) -> Vector3:
        return Vector3(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z
        )

    
    def __getitem__(self, key) -> int:
        if key == 'x' or key == 0:
            return self.x
        elif key == 'y' or key == 1:
            return self.y
        elif key == 'z' or key == 2:
            return self.z
        else:
            raise KeyError(key)

    
    def __setitem__(self, key, value) -> None:
        if key in ['x', 'y', 'z', 0, 1, 2]:
            raise AttributeError(key)
        raise KeyError(key)
        
        
    def __delitem__(self, key) -> None:
        if key in ['x', 'y', 'z', 0, 1, 2]:
            raise AttributeError(key)
        raise KeyError(key)


    def permutate(self) -> Vector3:
        return Vector3(self.y, self.z, self.x)
        
        
    def flip(self) -> Vector3:
        return Vector3(self.y, self.x, self.z)
    

    def abs(self) -> Vector3:
        return Vector3(
            abs(self.x),
            abs(self.y),
            abs(self.z)
        )
        
    
    def length(self) -> int:
        v = self.abs()
        return v.x + v.y + v.z
