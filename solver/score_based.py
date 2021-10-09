from model import PlacedPackage, Package, Vector3, Volume

from .solver import Solver


class ScoreBased(Solver):

    def initialize(self):
        self.placed_packages: list[PlacedPackage] = []
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
            
            if self.config.LOG_PLACED:
                print('{}\t{}\t{}\t@ {}'.format(
                    len(placed),
                    len(self.volumes),
                    package,
                    pos))
            self.volumes = [v for v in self.volumes if not self.small(v)] # filter out too small volumes
        return self.placed_packages


    def score(self, package: Package, pos: Vector3, vol: Volume):
        score = 0
        if self.config.ENABLE_OPTIMAL_DISTANCE:
            score += self.score_optimal_distances(package, pos)
        if self.config.ENABLE_HEAVY_PRIORITY:
            score += self.penalty_not_heavy(package)
        if self.config.ENABLE_WEIGHT:
            score += self.score_weight(package, pos, vol)
        if self.config.ENABLE_SIDE_ALIGN:
            score += self.score_side_align(package, pos)
        if self.config.ENABLE_X:
            score += self.score_x(package, pos)
        if self.config.ENABLE_BOUNDING:
            score += self.score_bounding(package, pos)
        if self.config.ENABLE_ORDER_SKIP:
            score += self.penalty_order_skip(package, pos)
        if self.config.ENABLE_ORDER_BREAK:
            score += self.order_break(package, vol)
        return score    
  

    def score_optimal_distances(self, package: Package, pos: Vector3) -> tuple:
        mid_x = pos.x + package.dim.x / 2
        mid_y = pos.y + package.dim.y / 2
        mid_z = pos.z + package.dim.z / 2
        optimal_x = (4 - package.orderClass) * self.vehicle.x / 4
        score = self.config.MUL_OPTIMAL_X * abs(mid_x - optimal_x)
        score += self.config.MUL_OPTIMAL_Y * min(mid_y, self.vehicle.y - mid_y)
        score += self.config.MUL_OPTIMAL_Z * abs(mid_z)
        return score
  

    def penalty_not_heavy(self, package: Package) -> int:
        if not package.is_heavy():
            return self.config.PENALTY_NOT_HEAVY
        return 0


    def score_weight(self, package: Package, pos: Vector3, vol: Volume) -> float:
        if not package.is_heavy():
            return 0
        score = 0
        for p in vol.support.beneath:
            wc = p.weightClass
            if wc == 0:
                score += self.config.PENALTY_HEAVY_ON_LIGHT
            elif wc == 1:
                score += self.config.PENALTY_HEAVY_ON_MEDIUM
            else:
                score += self.config.PENALTY_HEAVY_ON_HEAVY
        return self.config.MUL_WEIGHT * score


    def score_side_align(self, package: Package, pos: Vector3) -> float:
        return self.config.MUL_SIDE_ALIGN * min(
            pos.y,
            self.vehicle.y - pos.y - package.dim.y
        )

    
    def score_x(self, package: Package, pos: Vector3) -> float:
        x = pos.x + package.dim.x / 2
        return (self.config.MUL_X * x)**self.config.EXP_X

    
    def penalty_order_skip(self, package: Package, pos: Vector3) -> float:
        skips = self.ocLeft[:package.orderClass]
        score = 0
        for i, n in enumerate(skips):
            score += self.config.ORDER_BASE**(len(skips)-i) * n**self.config.EXP_ORDER_N
        return -(self.config.MUL_ORDER_SKIP * score) ** self.config.EXP_ORDER_SKIP
    
    
    def order_break(self, package: Package, vol: Volume) -> float:
        # if E placed on A then big penalty
        score = 0
        for p in vol.support.beneath:
            score += max(0, package.orderClass - p.orderClass)
        return self.config.MUL_ORDER_BREAK * score

    
    def score_bounding(self, package: Package, pos: Vector3) -> float:
        b = -package.calc_volume()
        if not self.bounding_volume.vol_inside(package.as_volume_at(pos)):
            b += self.config.PENALTY_BOUNDING_BREAK
        return (self.config.MUL_BOUNDING * b) ** self.config.EXP_BOUNDING


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
            if len(positions) > self.config.PREFERRED_NUM_CANDIDATES:
                break
        return positions

        
    def set_min(self, id: int = 0):
        self.min_x = min([p.dim.x for p in self.packages[id:]])
        self.min_y = min([p.dim.y for p in self.packages[id:]])
        self.min_z = min([p.dim.z for p in self.packages[id:]])

    
    def small(self, vol: Volume) -> bool:
        return vol.dim.x < self.min_x or vol.dim.y < self.min_y or vol.dim.z < self.min_z
