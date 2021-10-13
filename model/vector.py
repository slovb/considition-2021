from __future__ import annotations
from dataclasses import dataclass


clamp = lambda n, lower, upper: max(min(upper, n), lower)


@dataclass(frozen=True)
class Vector2:
    x: int = 0
    y: int = 0


    def key(self) -> tuple:
        return (self.x, self.y)


    def clamp(self, lower: Vector2, upper: Vector2) -> Vector2:
        return Vector2(
            clamp(self.x, lower.x, upper.x),
            clamp(self.y, lower.y, upper.y)
        )
    
        
    def infinum(self, u: Vector2) -> Vector2:
        return Vector2(
            min(self.x, u.x),
            min(self.y, u.y)
        )


    def suprenum(self, u: Vector2) -> Vector2:
        return Vector2(
            max(self.x, u.x),
            max(self.y, u.y)
        )


@dataclass(frozen=True)
class Vector3:
    x: int = 0
    y: int = 0
    z: int = 0


    def key(self) -> tuple:
        return (self.x, self.y, self.z)


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

    
    def pairwise_less(self, rhs: Vector3) -> bool:
        return self.x < rhs.x and self.y < rhs.y and self.z < rhs.z


    def permutate(self) -> Vector3:
        return Vector3(self.y, self.z, self.x)
        
        
    def flip(self) -> Vector3:
        return Vector3(self.y, self.x, self.z)
    

    def abs(self) -> Vector3:
        if self.x < 0 or self.y < 0 or self.z < 0:
            return Vector3(
                abs(self.x),
                abs(self.y),
                abs(self.z)
            )
        return self

    
    def length(self) -> int:
        return abs(self.x) + abs(self.y) + abs(self.z)    


    def clamp(self, lower: Vector3, upper: Vector3) -> Vector3:
        return Vector3(
            clamp(self.x, lower.x, upper.x),
            clamp(self.y, lower.y, upper.y),
            clamp(self.z, lower.z, upper.z)
        )


    def infinum(self, u: Vector3) -> Vector3:
        return Vector3(
            min(self.x, u.x),
            min(self.y, u.y),
            min(self.z, u.z)
        )


    def suprenum(self, u: Vector3) -> Vector3:
        return Vector3(
            max(self.x, u.x),
            max(self.y, u.y),
            max(self.z, u.z)
        )
