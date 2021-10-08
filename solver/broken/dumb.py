from copy import copy

from model import PlacedPackage, Package, Vector3, Area, Volume

from solver.solver import Solver

class Dumb(Solver):
    placed_packages: list[PlacedPackage] = []
    
    def solve(self) -> list[PlacedPackage]:
        self.packages = sorted(self.packages, key=lambda p: p.calc_area(), reverse=True)
        # self.packages = sorted(self.packages, key=lambda p: p.calc_area() * p.dim.z)
        self.packages = sorted(self.packages, key=lambda p: p.orderClass, reverse=True)
        # self.packages = sorted(self.packages, key=lambda p: p.weightClass * p.dim.z, reverse=True)
        # self.packages = sorted(self.packages, key=lambda p: p.weightClass, reverse=True)
        
        for i, package in enumerate(self.packages):
            if package.is_heavy():
                self.volumes = sorted(self.volumes, key=lambda vol: (vol.pos.z, vol.pos.x))
            else:
                self.volumes = sorted(self.volumes, key=lambda vol: vol.pos.x)

            pos = self.where(package)
            
            # if not try rotations of the package
            for j in range(5):
                if pos is not None:
                    break
                if j == 2:
                    package.dim = package.dim.flip()
                package.dim = package.dim.permutate()
                pos = self.where(package)
            if pos is None:
                exit('did not finish')

            self.place(package, pos)
            
            print('{}\t{}\t{}\t@ {}'.format(i, len(self.volumes), package, pos))
            self.volumes = [v for v in self.volumes if not self.small(v)] # filter out too small volumes
            self.set_min(i)
        return self.placed_packages
    
    def where(self, package: Package) -> Vector3:
        for vol in self.volumes:
            if vol.dim_inside(package.dim):
                pos = vol.support.pos
                if vol.vol_inside(Volume(pos, package.dim, None)):
                    return copy(pos)
        return None
        
    def initialize(self):
        self.set_min()
        self.rejigger_dimensions()
    
    def set_min(self, id: int = 0):
        self.min_x = min([p.dim.x for p in self.packages[id:]])
        self.min_y = min([p.dim.y for p in self.packages[id:]])
        self.min_z = min([p.dim.z for p in self.packages[id:]])
    
    def small(self, vol: Volume) -> bool:
        return vol.dim.x < self.min_x or vol.dim.y < self.min_y or vol.dim.z < self.min_z

    def rejigger_dimensions(self) -> None:
        for p in self.packages:
            values = sorted([p.dim.x, p.dim.y, p.dim.z])
            p.dim.x, p.dim.y, p.dim.z = values
