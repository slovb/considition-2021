from model import PlacedPackage, Package, Vector3, Volume

from .solver import Solver


preferred_num_candidates = 50

class WeightAlign(Solver):
    placed_packages: list[PlacedPackage] = []
    

    def initialize(self):
        self.set_min()
        ocLeft = [0]*5
        for p in self.packages:
            ocLeft[p.orderClass] += 1
        self.ocLeft = ocLeft

    
    def solve(self) -> list[PlacedPackage]:
        self.packages = sorted(self.packages, key=lambda p: p.calc_area(), reverse=True)
        # self.packages = sorted(self.packages, key=lambda p: p.calc_area() * p.dim.z)
        self.packages = sorted(self.packages, key=lambda p: p.orderClass, reverse=True)
        # self.packages = sorted(self.packages, key=lambda p: p.weightClass * p.dim.z, reverse=True)
        self.packages = sorted(self.packages, key=lambda p: p.weightClass, reverse=True)
        
        placed = set()
        
        while len(placed) < len(self.packages):
            packages = [package for package in self.packages if package.id not in placed]

            candidates: list[tuple[Package, Vector3, Volume]] = []
            for package in packages:
                if package.is_heavy():
                    self.volumes = sorted(self.volumes, key=lambda vol: (vol.pos.z, vol.pos.x))
                else:
                    self.volumes = sorted(self.volumes, key=lambda vol: vol.pos.x)
                for j in range(6):
                    for where in self.where(package):
                        candidates.append((package,) + where)
                    if j == 3:
                        package = package.rotate(package.dim.flip())
                    package = package.rotate(package.dim.permutate())
                if len(candidates) == 0:
                    exit('did not finish')
            candidates = sorted(candidates, key=lambda c: self.score(c[0], c[1], c[2]))
            package, pos, _ = candidates[0]
            self.place(package, pos)
            placed.add(package.id)
            self.ocLeft[package.orderClass] -= 1
            
            print('{}\t{}\t{}\t@ {}'.format(len(placed), len(self.volumes), package, pos))
            self.volumes = [v for v in self.volumes if not self.small(v)] # filter out too small volumes
        return self.placed_packages


    def score(self, package: Package, pos: Vector3, vol: Volume):
        #d = self.distances_from_optimal(package, pos)
        w = self.weight_score(package, pos, vol)
        s = self.side_align_score(package, pos)
        x = pos.x + package.dim.x / 2
        o = self.order_skip_score(package)
        b = -package.calc_volume()
        if not self.bounding_volume.vol_inside(package.as_volume_at(pos)):
            b += 10**7
        return w + s + x*x + b - o**2
    
    
    def side_align_score(self, package: Package, pos: Vector3) -> int:
        return min(
            pos.y,
            self.vehicle.y - pos.y - package.dim.y
        )
    
    
    def order_skip_score(self, package: Package) -> list:
        skips = self.ocLeft[:package.orderClass]
        score = 0
        for i, n in enumerate(skips):
            score += 10**(len(skips)-i) * n**2
        return score


    def weight_score(self, package, pos: Vector3, vol: Volume):
        if not package.is_heavy():
            return 1000
        score = 0
        for wc in vol.support.beneath:
            if wc == 0:
                score += 50
            elif wc == 1:
                score += 12
            else:
                score += 5
        return score


    def distances_from_optimal(self, package: Package, pos: Vector3) -> tuple:
        mid_x = pos.x + package.dim.x / 2
        mid_y = pos.y + package.dim.y / 2
        mid_z = pos.z + package.dim.z / 2
        optimal_x = (4 - package.orderClass) * self.vehicle.x / 4
        return [abs(mid_x - optimal_x),
                min(mid_y, self.vehicle.y - mid_y),
                abs(mid_z)]

    
    def where(self, package: Package) -> list[tuple[Vector3, Volume]]:
        positions: list[tuple[Vector3, Volume]] = []
        for vol in self.volumes:
            if vol.dim_inside(package.dim):
                pos = vol.support.area.pos
                dim = vol.support.area.dim
                candidates = [pos]
                candidates.append(Vector3( # scoot left
                    max(vol.pos.x, pos.x - package.dim.x + 1),
                    max(vol.pos.y, pos.y - package.dim.y + 1),
                    pos.z
                ))
                candidates.append(Vector3( # scoot right
                    max(vol.pos.x, pos.x - package.dim.x + 1),
                    min(vol.pos.y + vol.dim.y - package.dim.y, pos.y + dim.y - 1),
                    pos.z
                ))
                for p in candidates:
                    if vol.vol_inside(Volume(p, package.dim, None)):
                        positions.append((p, vol))
            if len(positions) > preferred_num_candidates:
                break
        return positions

        
    def set_min(self, id: int = 0):
        self.min_x = min([p.dim.x for p in self.packages[id:]])
        self.min_y = min([p.dim.y for p in self.packages[id:]])
        self.min_z = min([p.dim.z for p in self.packages[id:]])

    
    def small(self, vol: Volume) -> bool:
        return vol.dim.x < self.min_x or vol.dim.y < self.min_y or vol.dim.z < self.min_z
