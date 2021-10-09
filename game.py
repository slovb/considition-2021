import api

from model import Package, Vector3, PlacedPackage

from solver.config import Config
from solver.score_based import ScoreBased as Solver


class Game:
    def __init__(self, info: dict):
        self.info = info
        self.vehicle = self.parse_vehicle()
        self.packages = self.parse_packages()


    def name(self):
        return self.info['mapName']

    
    def solve(self, config: Config) -> list[PlacedPackage]:
        return Solver(vehicle=self.vehicle, packages=self.packages, config=config).solve()
    
    
    def parse_vehicle(self) -> Vector3:
        return Vector3(
            x = self.info['vehicle']['length'],
            y = self.info['vehicle']['width'],
            z = self.info['vehicle']['height']
        )


    def parse_packages(self) -> list[Package]:
        packages = []
        for p in self.info['dimensions']:
            packages.append(Package(
                id = p['id'],
                dim = Vector3(p['length'], p['width'], p['height']),
                weightClass = p['weightClass'],
                orderClass = p['orderClass']
            ))
        return packages
