from copy import copy

from model import PlacedPackage, Package, Vector, Area, Volume

from .solver import Solver

class Dumb(Solver):
    placed_packages: list[PlacedPackage] = []
    
    def solve(self) -> list[PlacedPackage]:
        self.packages = sorted(self.packages, key=lambda p: p.orderClass * p.calc_area(), reverse=True)
        self.packages = sorted(self.packages, key=lambda p: p.weightClass, reverse=True)
        
        for package in self.packages:
            pos = self.where(package)
            self.place(package, pos)
            
            print('{} placed {} at pos {}'.format(len(self.volumes), package, pos))
            self.volumes = [v for v in self.volumes if not self.small(v)] # filter out too small volumes
            self.volumes = sorted(self.volumes, key=lambda vol: vol.pos.x)
        return self.placed_packages
    
    def where(self, package: Package) -> Vector:
        for vol in self.volumes:
            if vol.dim_inside(package.dim):
                pos = vol.support.pos
                if vol.vol_inside(Volume(pos, package.dim)):
                    return copy(pos)
        print('Blep did not finish')
        exit()
        
    def initialize(self):
        self.min_x = min([p.dim.x for p in self.packages])
        self.min_y = min([p.dim.y for p in self.packages])
        self.min_z = min([p.dim.z for p in self.packages])
    
    def small(self, vol: Volume) -> bool:
        return vol.dim.x < self.min_x or vol.dim.y < self.min_y or vol.dim.z < self.min_z
