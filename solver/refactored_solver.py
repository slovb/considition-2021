import copy

from model import *

class RefactoredSolver:
    pos: Vector = Vector()
    heavyPackages: list[Package] = []
    otherPackages: list[Package] = []
    placedPackages: list[PlacedPackage] = []
    lastKnownMax: Vector = Vector()

    def __init__(self, vehicle: Vector, packages: list[Package]):
        self.vehicle = vehicle
        self.packages = packages
        self.heavyPackages = list(filter(lambda p: p.is_heavy(), self.packages))
        self.otherPackages = list(filter(lambda p: not p.is_heavy(), self.packages))

        self.lastKnownMax.z = max([p.dim.z for p in self.heavyPackages])
        self.heavyPackages = sorted(
            self.heavyPackages, key=lambda i: (i.calc_area()))
        self.otherPackages = sorted(
            self.otherPackages, key=lambda i: (i.calc_area()))

    def solve(self) -> list[PlacedPackage]:
        while len(self.heavyPackages) + len(self.otherPackages) > 0:
            if self.pos.z <= self.lastKnownMax.z:
                package = self.heavyPackages.pop()
            elif len(self.otherPackages) > 0:
                package = self.otherPackages.pop()
            else:
                package = self.heavyPackages.pop()

            if self.doesPackageFitZ(package):
                self.addPackage(PlacedPackage(copy.copy(self.pos), package))
                self.pos.z += package.dim.z

            elif self.doesPackageFitY(package):
                self.pos.y += self.lastKnownMax.y
                self.pos.z = 0
                self.addPackage(PlacedPackage(copy.copy(self.pos), package))
                self.pos.z = package.dim.z
                self.lastKnownMax.y = 0

            elif self.doesPackageFitX(package):
                self.pos.x += self.lastKnownMax.x
                self.pos.y = 0
                self.pos.z = 0
                self.addPackage(PlacedPackage(copy.copy(self.pos), package))
                self.pos.z = package.dim.z
                self.lastKnownMax.x = 0

            else:
                print("Something went terribly wrong!")
                break
            self.setMaxX(package)
            self.setMaxY(package)
        return self.placedPackages

    def doesPackageFitX(self, package: Package) -> bool:
        return self.pos.x + self.lastKnownMax.x + package.dim.x < self.vehicle.x

    def doesPackageFitY(self, package: Package) -> bool:
        return self.pos.y + self.lastKnownMax.y + package.dim.y < self.vehicle.y and self.pos.x + package.dim.x < self.vehicle.x

    def doesPackageFitZ(self, package: Package) -> bool:
        return self.pos.x + package.dim.x < self.vehicle.x and self.pos.y + package.dim.y < self.vehicle.y and self.pos.z + package.dim.z < self.vehicle.z

    def setMaxY(self, package: Package) -> None:
        if package.dim.y > self.lastKnownMax.y:
            self.lastKnownMax.y = package.dim.y

    def setMaxX(self, package: Package) -> None:
        if package.dim.x > self.lastKnownMax.x:
            self.lastKnownMax.x = package.dim.x

    def addPackage(self, placed_package: PlacedPackage) -> None:
        self.placedPackages.append(placed_package)
