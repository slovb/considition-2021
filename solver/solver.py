from abc import ABC, abstractmethod

from model import Package, HEAVY, PlacedPackage, Vector2, Vector3, Area, Support, Volume
from .config import Config

class Solver(ABC):
    
    def __init__(self, vehicle: Vector3, packages: list[Package], config: Config = None):
        self.vehicle = vehicle
        self.packages = packages
        self.config = config if config is not None else Config()
        self.volumes = []
        self.volumes.append(Volume(
            pos = Vector3(0, 0, 0),
            dim = self.vehicle,
            support = Support(
                area = Area(
                    pos = Vector3(0, 0, 0),
                    dim = Vector2(self.vehicle.x, self.vehicle.y)
                ),
                beneath = tuple()
            )
        ))
        self.bounding_volume = Volume(
            pos = Vector3(0, 0, 0),
            dim = Vector3(0, 0, 0),
            support = None
        )
        self.placed_packages: list[PlacedPackage] = []
        self.initialize()


    def initialize(self) -> None:
        pass


    @abstractmethod
    def solve(self) -> list[PlacedPackage]:
        pass
    

    def place(self, package: Package, pos: Vector3, vol: Volume = None):
        self.placed_packages.append(PlacedPackage(
            pos = pos,
            package = package,
            vol = vol
        ))

        package_volume = package.as_volume_at(pos)
        seen = set()
        volumes: list[Volume] = []
        for v in self.volumes:
            newVolumes = v.remove(package_volume)
            for vol in newVolumes:
                k = vol.key()
                if k not in seen:
                    seen.add(k)
                    volumes.append(vol)
                else:
                    pass
                    # TODO maybe merge supports into a list
        self.volumes = volumes
        
        if not self.bounding_volume.vol_inside(package_volume):
            self.bounding_volume = self.bounding_volume.resize(
                self.bounding_volume.dim.suprenum(package_volume.get_far_corner()))
            if self.config.LOG_RESIZE:
                print('resize ' + str(self.bounding_volume))