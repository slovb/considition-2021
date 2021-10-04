from abc import ABC, abstractmethod
from copy import copy

from model import Package, PlacedPackage, Vector2, Vector3, Volume, Area

class Solver(ABC):
    
    def __init__(self, vehicle: Vector3, packages: list[Package]):
        self.vehicle = vehicle
        self.packages = packages
        self.volumes = []
        self.volumes.append(Volume(
            pos = Vector3(0, 0, 0),
            dim = copy(self.vehicle),
            support = Area(Vector3(0, 0, 0), Vector2(self.vehicle.x, self.vehicle.y))
        ))
        self.initialize()


    def initialize(self) -> None:
        pass


    @abstractmethod
    def solve(self) -> list[PlacedPackage]:
        pass
    

    def place(self, package: Package, pos: Vector3):
        self.placed_packages.append(PlacedPackage(
            pos = pos,
            package = package
        ))
        pvol = Volume(
            pos = pos,
            dim = copy(package.dim),
            support = Area(
                pos = pos + Vector3(0, 0, package.dim.z),
                dim = Vector2(package.dim.x, package.dim.y)
            )
        )
        seen = set()
        volumes = []
        for v in self.volumes:
            newVolumes = v.remove(pvol)
            for vol in newVolumes:
                key = vol.key()
                if key not in seen:
                    seen.add(key)
                    volumes.append(vol)
        self.volumes = volumes
    