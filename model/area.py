from dataclasses import dataclass

from .vector import Vector3, Vector2

@dataclass
class Area:
    pos: Vector3
    dim: Vector2
    
    __key: tuple = None    
    

    def key(self) -> tuple:
        if self.__key is None:
            self.__key = (self.pos.key(), self.dim.key())
        return self.__key

    
    def area(self) -> int:
        return self.dim.x * self.dim.y
    
    
    def __setitem__(self, key, value) -> None:
        raise AttributeError(key)
    
    
    def __delitem__(self, key) -> None:
        raise AttributeError(key)
