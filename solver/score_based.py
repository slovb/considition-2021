from typing import Callable
from model import PlacedPackage, Package, Vector3, Volume

from .solver import Solver


def memoize(key, memory: dict, calc: Callable):
    if key not in memory:
        memory[key] = calc()
    return memory[key]


class ScoreBased(Solver):

    def initialize(self):
        self.set_min(self.packages)
        ocLeft = [0]*5
        for p in self.packages:
            ocLeft[p.orderClass] += 1
        self.ocLeft = ocLeft
        self.maxX = 0
        self.memory_order_skip = {}
        self.memory_not_heavy = {}
        self.memory_weight = {}
        self.memory_side_align = {}
        self.memory_volume = {}
        self.memory_x = {}

    
    def solve(self) -> list[PlacedPackage]:
        self.packages = sorted(self.packages, key=lambda p: p.orderClass, reverse=True)
        self.packages = sorted(self.packages, key=lambda p: p.weightClass, reverse=True)
        
        placed = set()
        
        while len(placed) < len(self.packages):
            packages = [package for package in self.packages if package.id not in placed]
            self.set_min(packages)

            heavyVolumes = sorted(self.volumes, key=lambda vol: (vol.pos.z, vol.pos.x))
            otherVolumes = sorted(self.volumes, key=lambda vol: vol.pos.x)
            # heavyVolumes = sorted(otherVolumes, key=lambda vol: vol.support.can_support_heavy(), reverse=True)
            candidates: list[tuple[Package, Vector3, Volume]] = []
            for package in packages:
                if package.is_heavy():
                    self.volumes = heavyVolumes
                else:
                    self.volumes = otherVolumes
                for j in range(6):
                    for where in self.where(package):
                        candidates.append((package,) + where)
                    if j == 2:
                        package = package.rotate(package.dim.flip())
                    package = package.rotate(package.dim.permutate())
                if len(candidates) == 0:
                    print('did not finish ({} remaining)'.format(len(packages)))
                    return self.placed_packages
            self.reset_score_memory()
            package, pos, vol = min(candidates, key=lambda c: self.score(c[0], c[1], c[2]))
            self.place(package, pos, vol)
            placed.add(package.id)
            self.ocLeft[package.orderClass] -= 1
            self.maxX = max(self.maxX, package.dim.x + pos.x)
            
            if self.config.LOG_PLACED:
                print('{}\t{}\t{}\t@ {}'.format(
                    len(placed),
                    len(self.volumes),
                    package,
                    pos))
            self.volumes = [v for v in self.volumes if not self.small(v)] # filter out too small volumes
        return self.placed_packages


    def reset_score_memory(self):
        self.memory_order_break = {}
        self.memory_bounding = {}
        self.memory_bounded_x = {}


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
        if self.config.ENABLE_VOLUME:
            score += self.score_volume(package)
        if self.config.ENABLE_ORDER_SKIP:
            score += self.penalty_order_skip(package)
        if self.config.ENABLE_ORDER_BREAK:
            score += self.order_break(package, pos, vol)
        if self.config.ENABLE_BOUNDED_X:
            score += self.score_bounded_x(package, pos)
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
        def calc():
            if not package.is_heavy():
                return self.config.PENALTY_NOT_HEAVY
            return 0
        return memoize(
            package.weightClass,
            self.memory_not_heavy,
            calc
        )


    def score_weight(self, package: Package, pos: Vector3, vol: Volume) -> float:
        def calc():
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
        return memoize(
            (package.weightClass) if package.weightClass < 2 else (package.weightClass, vol.support.weights_beneath()),
            self.memory_weight,
            calc
        )


    def score_side_align(self, package: Package, pos: Vector3) -> float:
        def calc():
            return self.config.MUL_SIDE_ALIGN * min(
                pos.y,
                self.vehicle.y - pos.y - package.dim.y
            )
        return memoize(
            (pos.y, package.dim.y),
            self.memory_side_align,
            calc
        )

    
    def score_x(self, package: Package, pos: Vector3) -> float:
        def calc():
            x = pos.x + package.dim.x / 2
            return (self.config.MUL_X * x)**self.config.EXP_X
        return memoize(
            (pos.x, package.dim.x),
            self.memory_x,
            calc
        )

    
    '''
    def penalty_order_skip(self, package: Package, pos: Vector3) -> float:
        skips = self.ocLeft[:package.orderClass]
        score = 0
        for i, n in enumerate(skips):
            score += self.config.ORDER_BASE**(len(skips)-i) * n**self.config.EXP_ORDER_N
        return -(self.config.MUL_ORDER_SKIP * score) ** self.config.EXP_ORDER_SKIP
    '''
    
    
    def penalty_order_skip(self, package: Package) -> float:
        def calc():
            skips = self.ocLeft[package.orderClass + 1:]
            score = 0
            # if sum(skips) > 0:
            #     score += self.config.ORDER_BASE_REDUCTION
            for i, n in enumerate(skips):
                score += self.config.ORDER_BASE**(len(skips)-i) * n**self.config.EXP_ORDER_N
            return (self.config.MUL_ORDER_SKIP * score) ** self.config.EXP_ORDER_SKIP
        return memoize(
            package.orderClass,
            self.memory_order_skip,
            calc
        )

    
    def order_break(self, package: Package, pos: Vector3, vol: Volume) -> float:
        def calc():
            def earlier_after(pp: PlacedPackage) -> bool:
                return package.orderClass < pp.package.orderClass and \
                    (pos.x < pp.pos.x or (pos.x == pp.pos.x and pos.z < pp.pos.z))
            score = 0
            score += len([pp for pp in self.placed_packages if earlier_after(pp)])
            # for p in vol.support.beneath:
            #     score += max(0, package.orderClass - p.orderClass)
            return self.config.MUL_ORDER_BREAK * score
        return memoize(
            (package.orderClass, pos.x, pos.z),
            self.memory_order_break,
            calc
        )


    def score_volume(self, package: Package):
        def calc():
            return -package.calc_volume() * self.config.MUL_VOLUME
        return memoize(
            package.id,
            self.memory_volume,
            calc
        )
    
    
    def score_bounding(self, package: Package, pos: Vector3) -> float:
        def calc():
            if self.bounding_volume.package_inside_at(package, pos):
                return 0
            return (self.config.MUL_BOUNDING * self.config.PENALTY_BOUNDING_BREAK) ** self.config.EXP_BOUNDING
        return memoize(
            (pos.key(), package.dim.key()),
            self.memory_bounding,
            calc
        )


    def score_bounded_x(self, package: Package, pos: Vector3) -> float:
        def calc():
            return self.config.MUL_BOUNDED_X * max(0, package.dim.x + pos.x - self.maxX)
        return memoize(
            (pos.x, package.dim.x), 
            self.memory_bounded_x,
            calc
        )


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
            if self.config.ENABLE_LIMIT_NUM_CANDIDATES and len(positions) > self.config.PREFERRED_NUM_CANDIDATES:
                break
        return positions

        
    def set_min(self, packages: list[Package]) -> None:
        self.min_x = min([p.dim.x for p in packages])
        self.min_y = min([p.dim.y for p in packages])
        self.min_z = min([p.dim.z for p in packages])

    
    def small(self, vol: Volume) -> bool:
        return vol.dim.x < self.min_x or vol.dim.y < self.min_y or vol.dim.z < self.min_z
