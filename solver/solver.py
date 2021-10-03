from abc import ABC, abstractmethod
from copy import copy

from model import Package, PlacedPackage, Vector, Volume, Area

class Solver(ABC):
    
    def __init__(self, vehicle: Vector, packages: list[Package]):
        self.vehicle = vehicle
        self.packages = packages
        self.volumes = []
        self.volumes.append(Volume(
            pos = Vector(0, 0, 0),
            dim = copy(self.vehicle),
            support = Area(Vector(0, 0, 0), self.vehicle.x, self.vehicle.y)
        ))
        self.initialize()


    def initialize(self) -> None:
        pass


    @abstractmethod
    def solve(self) -> list[PlacedPackage]:
        pass
    

    def place(self, package: Package, pos: Vector):
        self.placed_packages.append(PlacedPackage(
            pos = pos,
            package = package
        ))
        pvol = Volume(
            pos = pos,
            dim = copy(package.dim),
            support = Area(
                pos = pos + Vector(0, 0, package.dim.z),
                dim_x = package.dim.x,
                dim_y = package.dim.y
            )
        )
        volumes = []
        for v in self.volumes:
            volumes =  volumes + v.remove(pvol)
        self.volumes = volumes
    