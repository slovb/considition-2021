from dataclasses import dataclass

@dataclass
class Pos:
    x: int = 0
    y: int = 0
    z: int = 0

    def __add__(self, other):
        return Pos(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z
        )

@dataclass
class Dimension:
    length: int = 0
    width: int = 0
    height: int = 0

@dataclass
class Package:
    id: int
    length: int
    width: int
    height: int
    weightClass: int
    orderClass: int

    def area(self) -> int:
        return self.width * self.length
    
    def is_heavy(self) -> bool:
        return self.weightClass == 2

@dataclass
class PlacedPackage:
    pos: Pos
    package: Package

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

@dataclass
class Vehicle:
    length: int
    width: int
    height: int

class RefactoredSolver:
    pos: Pos = Pos()
    heavyPackages: list[Package] = []
    otherPackages: list[Package] = []
    placedPackages: list[dict] = []
    lastKnownMax: Dimension = Dimension()

    def __init__(self, game_info: dict):
        self.vehicle = Vehicle(**game_info['vehicle'])
        self.packages = [Package(**package) for package in game_info["dimensions"]]
        self.heavyPackages = list(filter(lambda p: p.is_heavy(), self.packages))
        self.otherPackages = list(filter(lambda p: not p.is_heavy(), self.packages))

        self.lastKnownMax.height = max([p.height for p in self.heavyPackages])
        self.heavyPackages = sorted(
            self.heavyPackages, key=lambda i: (i.area()))
        self.otherPackages = sorted(
            self.otherPackages, key=lambda i: (i.area()))

    def Solve(self) -> list[dict]:
        while len(self.heavyPackages) + len(self.otherPackages) > 0:
            if self.pos.z <= self.lastKnownMax.height:
                package = self.heavyPackages.pop()
            elif len(self.otherPackages) > 0:
                package = self.otherPackages.pop()
            else:
                package = self.heavyPackages.pop()

            if self.DoesPackageFitZ(package):
                self.AddPackage(PlacedPackage(self.pos, package))
                self.pos.z += package.height

            elif self.DoesPackageFitY(package):
                self.pos.y += self.lastKnownMax.width
                self.pos.z = 0
                self.AddPackage(PlacedPackage(self.pos, package))
                self.pos.z = package.height
                self.lastKnownMax.width = 0

            elif self.DoesPackageFitX(package):
                self.pos.x += self.lastKnownMax.length
                self.pos.y = 0
                self.pos.z = 0
                self.AddPackage(PlacedPackage(self.pos, package))
                self.pos.z = package.height
                self.lastKnownMax.length = 0

            else:
                print("Something went terribly wrong!")
                break
            self.SetMaxX(package)
            self.SetMaxY(package)
        return self.placedPackages

    def DoesPackageFitX(self, package: Package) -> bool:
        return self.pos.x + self.lastKnownMax.length + package.length < self.vehicle.length

    def DoesPackageFitY(self, package: Package) -> bool:
        return self.pos.y + self.lastKnownMax.width + package.width < self.vehicle.width and self.pos.x + package.length < self.vehicle.length

    def DoesPackageFitZ(self, package: Package) -> bool:
        return self.pos.x + package.length < self.vehicle.length and self.pos.y + package.width < self.vehicle.width and self.pos.z + package.height < self.vehicle.height

    def SetMaxY(self, package: Package) -> None:
        if package.width > self.lastKnownMax.width:
            self.lastKnownMax.width = package.width

    def SetMaxX(self, package: Package) -> None:
        if package.length > self.lastKnownMax.length:
            self.lastKnownMax.length = package.length

    def AddPackage(self, placed_package: PlacedPackage) -> None:
        self.placedPackages.append(placed_package.as_solution())
