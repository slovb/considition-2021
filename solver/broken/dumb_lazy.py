from __future__ import annotations
from copy import copy

from model import PlacedPackage, Package, Vector3, Area, Volume

from solver.solver import Solver

''' Not sure what is wrong here, but I don't want to pursue this path right now '''

class Lazy(Volume):
    
    removal_queue: list[Volume] = []
    
    @staticmethod
    def from_volume(vol: Volume) -> Lazy:
        return Lazy(
            pos = vol.pos,
            dim = vol.dim,
            support = vol.support
        )
    
    
    def as_volume(self) -> Volume:
        return Volume(
            pos = self.pos,
            dim = self.dim,
            support = self.support
        )
    
    
    def remove(self, vol: Volume) -> list[Lazy]:
        self.removal_queue.append(vol)
        return [self]
    
    
    def has_queue(self) -> bool:
        return len(self.removal_queue) > 0
    
    
    def execute(self) -> list[Lazy]:
        volumes = [self.as_volume()]
        while len(self.removal_queue) > 0:
            to_remove = self.removal_queue.pop(0)
            vs = []
            for vol in volumes:
                vs = vs + vol.remove(to_remove)
            volumes = vs
        lazies = [Lazy.from_volume(vol) for vol in volumes]
        return lazies


class DumbLazy(Solver):
    placed_packages: list[PlacedPackage] = []

        
    def initialize(self):
        for i in range(len(self.volumes)):
            self.volumes[i] = Lazy.from_volume(self.volumes[i])
        self.set_min()
        self.rejigger_dimensions()
        self.packages = sorted(self.packages, key=lambda p: p.calc_area(), reverse=True)
        # self.packages = sorted(self.packages, key=lambda p: p.calc_area() * p.dim.z)
        self.packages = sorted(self.packages, key=lambda p: p.orderClass, reverse=True)
        # self.packages = sorted(self.packages, key=lambda p: p.weightClass * p.dim.z, reverse=True)
        # self.packages = sorted(self.packages, key=lambda p: p.weightClass, reverse=True)


    def solve(self) -> list[PlacedPackage]:        
        for i, package in enumerate(self.packages):
            self.volumes = self.sort_volumes(self.volumes, package)

            pos = self.where(package)
            
            # if not try rotations of the package
            for j in range(5):
                if pos is not None:
                    break
                if j == 2:
                    package.dim.flip()
                package.dim.permutate()
                pos = self.where(package)
            if pos is None:
                exit('did not finish')

            self.place(package, pos)
            
            print('{}\t{}\t{}\t@ {}'.format(i, len(self.volumes), package, pos))
            self.volumes = [v for v in self.volumes if not self.small(v)] # filter out too small volumes
            self.set_min(i)
        return self.placed_packages


    def sort_volumes(self, volumes: list, package: Package):
        if package.is_heavy():
            return sorted(volumes, key=lambda vol: (vol.pos.z, vol.pos.x))
        return sorted(volumes, key=lambda vol: vol.pos.x)

    
    def where(self, package: Package) -> Vector3:
        while len(self.volumes) > 0:
            vol = self.volumes.pop(0) # get the best
            if vol.has_queue():
                lazies = vol.execute()
                self.volumes = self.sort_volumes(lazies, package) + self.volumes
                continue
            self.volumes.append(vol) # add it back before we might quit out
            if vol.dim_inside(package.dim):
                pos = vol.support.pos
                if vol.vol_inside(Volume(pos, package.dim)):
                    return copy(pos)
        return None

    
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
