from abc import ABC, abstractmethod

from model import Package, PlacedPackage, Vector2, Vector3, Volume, Area


def max3(u: Vector3, v: Vector3) -> Vector3:
    return Vector3(
        max(u.x, v.x),
        max(u.y, v.y),
        max(u.z, v.z)
    )


class Solver(ABC):
    
    def __init__(self, vehicle: Vector3, packages: list[Package]):
        self.vehicle = vehicle
        self.packages = packages
        self.volumes = []
        self.volumes.append(Volume(
            pos = Vector3(0, 0, 0),
            dim = self.vehicle,
            support = Area(Vector3(0, 0, 0), Vector2(self.vehicle.x, self.vehicle.y))
        ))
        self.bounding_volume = Volume(
            pos = Vector3(0, 0, 0),
            dim = Vector3(0, 0, 0),
            support = None
        )
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
        # pvol = Volume(
        #     pos = pos,
        #     dim = package.dim,
        #     support = Area(
        #         pos = pos + Vector3(0, 0, package.dim.z),
        #         dim = Vector2(package.dim.x, package.dim.y)
        #     )
        # )
        package_volume = package.as_volume(pos)
        seen = set()
        volumes = []
        for v in self.volumes:
            newVolumes = v.remove(package_volume)
            for vol in newVolumes:
                key = vol.key()
                if key not in seen:
                    seen.add(key)
                    volumes.append(vol)
        self.volumes = volumes
        
        if not self.bounding_volume.vol_inside(package_volume):
            self.bounding_volume = self.bounding_volume.resize(max3(self.bounding_volume.dim, package_volume.get_far_corner()))
            print('resize ' + str(self.bounding_volume))