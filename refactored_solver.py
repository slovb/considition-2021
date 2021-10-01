from model import *

class RefactoredSolver:
    pos: Pos = Pos()
    heavyPackages: list[Package] = []
    otherPackages: list[Package] = []
    placedPackages: list[Package] = []
    lastKnownMax: Dimension = Dimension()

    def __init__(self, vehicle: Vehicle, packages: list[Package]):
        self.vehicle = vehicle
        self.packages = packages
        self.heavyPackages = list(filter(lambda p: p.is_heavy(), self.packages))
        self.otherPackages = list(filter(lambda p: not p.is_heavy(), self.packages))

        self.lastKnownMax.height = max([p.height for p in self.heavyPackages])
        self.heavyPackages = sorted(
            self.heavyPackages, key=lambda i: (i.area()))
        self.otherPackages = sorted(
            self.otherPackages, key=lambda i: (i.area()))

    def solve(self) -> list[Package]:
        while len(self.heavyPackages) + len(self.otherPackages) > 0:
            if self.pos.z <= self.lastKnownMax.height:
                package = self.heavyPackages.pop()
            elif len(self.otherPackages) > 0:
                package = self.otherPackages.pop()
            else:
                package = self.heavyPackages.pop()

            if self.doesPackageFitZ(package):
                self.addPackage(PlacedPackage(self.pos, package))
                self.pos.z += package.height

            elif self.doesPackageFitY(package):
                self.pos.y += self.lastKnownMax.width
                self.pos.z = 0
                self.addPackage(PlacedPackage(self.pos, package))
                self.pos.z = package.height
                self.lastKnownMax.width = 0

            elif self.doesPackageFitX(package):
                self.pos.x += self.lastKnownMax.length
                self.pos.y = 0
                self.pos.z = 0
                self.addPackage(PlacedPackage(self.pos, package))
                self.pos.z = package.height
                self.lastKnownMax.length = 0

            else:
                print("Something went terribly wrong!")
                break
            self.setMaxX(package)
            self.setMaxY(package)
        return self.placedPackages

    def doesPackageFitX(self, package: Package) -> bool:
        return self.pos.x + self.lastKnownMax.length + package.length < self.vehicle.length

    def doesPackageFitY(self, package: Package) -> bool:
        return self.pos.y + self.lastKnownMax.width + package.width < self.vehicle.width and self.pos.x + package.length < self.vehicle.length

    def doesPackageFitZ(self, package: Package) -> bool:
        return self.pos.x + package.length < self.vehicle.length and self.pos.y + package.width < self.vehicle.width and self.pos.z + package.height < self.vehicle.height

    def setMaxY(self, package: Package) -> None:
        if package.width > self.lastKnownMax.width:
            self.lastKnownMax.width = package.width

    def setMaxX(self, package: Package) -> None:
        if package.length > self.lastKnownMax.length:
            self.lastKnownMax.length = package.length

    def addPackage(self, placed_package: PlacedPackage) -> None:
        self.placedPackages.append(placed_package)
