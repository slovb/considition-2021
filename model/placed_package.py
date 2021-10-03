from dataclasses import dataclass

from .vector import Vector
from .package import Package


@dataclass
class PlacedPackage:
    pos: Vector
    package: Package


    def corners(self) -> list[Vector]:
        positions = []
        for x in [0, self.package.dim.x]:
            for y in [0, self.package.dim.y]:
                for z in [0, self.package.dim.z]:
                    addition = Vector(x, y, z)
                    positions.append(self.pos + addition)
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
