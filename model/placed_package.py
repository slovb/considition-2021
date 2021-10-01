import copy
from .pos import Pos
from .package import Package

class PlacedPackage:

    def __init__(self, pos: Pos, package: Package):
        self.pos = copy.copy(pos)
        self.package = copy.copy(package)

    def corners(self) -> list[Pos]:
        positions = []
        for x in [0, self.package.length]:
            for y in [0, self.package.width]:
                for z in [0, self.package.height]:
                    addition = Pos(x, y, z)
                    positions.append(self.pos + addition)
        return positions

    def corner(self, i: int) -> Pos:
        return self.corners()[i]

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
