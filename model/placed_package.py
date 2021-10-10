from dataclasses import dataclass

from .vector import Vector3
from .package import Package
from .volume import Volume

@dataclass(frozen=True)
class PlacedPackage:
    pos: Vector3
    package: Package
    vol: Volume = None


    def key(self) -> tuple:
        return (self.pos.key(), self.package.key())


    def corners(self) -> list[Vector3]:
        positions = []
        for x in [0, self.package.dim.x]:
            for y in [0, self.package.dim.y]:
                for z in [0, self.package.dim.z]:
                    positions.append(self.pos + Vector3(x, y, z))
        return positions


    def as_solution(self) -> dict:
        data = {
            "id": self.package.id,
            "weightClass": self.package.weightClass, 
            "orderClass": self.package.orderClass
        }
        for i, p in enumerate(self.corners()):
            data['x{}'.format(i + 1)] = p.x
            data['y{}'.format(i + 1)] = p.y
            data['z{}'.format(i + 1)] = p.z
        return data
