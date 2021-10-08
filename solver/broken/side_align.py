from model import PlacedPackage, Package, Vector3, Volume

from solver.solver import Solver


num_candidates = 20

class SideAlign(Solver):
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

            candidates = []                       
            for j in range(6):
                for p in self.where(package):
                    candidates.append((package, p))
                if j == 3:
                    package = package.rotate(package.dim.flip())
                package = package.rotate(package.dim.permutate())
            if len(candidates) == 0:
                exit('did not finish')

            def asdf(c):
                package, pos = c
                return 10*(pos.x + package.dim.x) + min(pos.y, self.vehicle.y - (pos.y + (package.dim.y / 2)))
            candidates = sorted(candidates, key=asdf)
            package, pos = candidates[0]
            self.place(package, pos)
            
            print('{}\t{}\t{}\t@ {}'.format(i, len(self.volumes), package, pos))
            self.volumes = [v for v in self.volumes if not self.small(v)] # filter out too small volumes
            self.set_min(i)
        return self.placed_packages
    
    def where(self, package: Package) -> list[Vector3]:
        positions = []
        for vol in self.volumes:
            if vol.dim_inside(package.dim):
                pos = vol.support.pos
                dim = vol.support.dim
                candidates = [pos]
                candidates.append(Vector3( # scoot left
                    max(vol.pos.x, pos.x - package.dim.x + 1),
                    max(vol.pos.y, pos.y - package.dim.y + 1),
                    pos.z
                ))
                candidates.append(Vector3(
                    min(vol.pos.x + vol.dim.x - package.dim.x, pos.x + dim.x - 1),
                    min(vol.pos.y + vol.dim.y - package.dim.y, pos.y + dim.y - 1),
                    pos.z
                ))
                for p in candidates:
                    if vol.vol_inside(Volume(p, package.dim, None)):
                        positions.append(p)
            if len(positions) > num_candidates:
                break
        return positions
        
    def initialize(self):
        self.set_min()
        # self.rejigger_dimensions()
    
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
