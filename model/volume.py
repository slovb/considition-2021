from __future__ import annotations
from dataclasses import dataclass
from copy import copy, deepcopy

from .vector import Vector2, Vector3
from .area import Area


clamp = lambda n, lower, upper: max(min(upper, n), lower)


def clamp2(v, lower, upper):
    return Vector2(
        clamp(v[0], lower[0], upper[0]),
        clamp(v[1], lower[1], upper[1])
    )


def clamp3(v, lower, upper):
    return Vector3(
        clamp(v[0], lower[0], upper[0]),
        clamp(v[1], lower[1], upper[1]),
        clamp(v[2], lower[2], upper[2])
    )


def oneOfLeftTwoOfRight(l: Vector3, r: Vector3):
    return [
        Vector3(l.x, r.y, r.z),
        Vector3(r.x, l.y, r.z),
        Vector3(r.x, r.y, l.z)
    ]


@dataclass
class Volume:
    pos: Vector3
    dim: Vector3
    support: Area = None

    def key(self) -> tuple:
        return (
            self.pos.key(),
            self.dim.key(),
            self.support.key()
        )
        

    def pos_inside(self, pos: Vector3) -> bool:
        return (self.pos.x <= pos.x <= self.pos.x + self.dim.x) and \
               (self.pos.y <= pos.y <= self.pos.y + self.dim.y) and \
               (self.pos.z <= pos.z <= self.pos.z + self.dim.z) 


    def dim_inside(self, dim: Vector3) -> bool:
        return dim.x <= self.dim.x and \
               dim.y <= self.dim.y and \
               dim.z <= self.dim.z   

    
    def vol_inside(self, vol: Volume) -> bool:
        for p in vol.corners():
            if not self.pos_inside(p):
                return False
        return True

    
    def vol_intersect(self, vol: Volume) -> bool:
        '''True if the volumes intersect at some point'''
        # calculate by checking if the midpoints are close enough to intersect
        # doing everything in 2x to avoid 0.5
        diff = (self.pos + self.pos + self.dim - vol.pos - vol.pos - vol.dim).abs()
        span = self.dim + vol.dim
        return diff.x < span.x and diff.y < span.y and diff.z < span.z
        
    
    def corners(self) -> list[Vector3]:
        positions = []
        for x in [0, self.dim.x]:
            for y in [0, self.dim.y]:
                for z in [0, self.dim.z]:
                    positions.append(self.pos + Vector3(x, y, z))
        return positions

 
    def remove(self, vol: Volume) -> list[Volume]:
        '''remove a volume, getting a list of all the maximal (pairwise intersecting) 
           volumes that can be created in the remaining space'''
        if not self.vol_intersect(vol):
            return [self]
        volumes = []
        
        rel_pos_left = vol.pos - self.pos
        rel_pos_right = rel_pos_left + vol.dim
        left_bound = self.pos
        right_bound = self.pos + self.dim
        
        # left does not move, but shrinks until it hits the vol
        l_dim = clamp3(rel_pos_left, (0, 0, 0), self.dim) # bound shrink 0 <= new d <= old d
        l_dims = oneOfLeftTwoOfRight(l_dim, self.dim)
        for d in l_dims:
            v = self.__duplicate()
            v.dim = d
            volumes.append(v)
        
        # right moves past volume and shrinks until the right bound is hit
        r_pos = clamp3(self.pos + rel_pos_right, left_bound, right_bound)
        r_dim = clamp3(self.dim - (r_pos - self.pos), (0, 0, 0), self.dim)
        r_poses = oneOfLeftTwoOfRight(r_pos, self.pos)
        r_dims = oneOfLeftTwoOfRight(r_dim, self.dim)
        for i in range(3):
            v = self.__duplicate()
            v.pos = r_poses[i]
            v.dim = r_dims[i]
            if i == 2: # z, new support area ontop of removed volume
                v.support = deepcopy(vol.support)
            volumes.append(v)

        for v in volumes:
            v.__fix_support()

        volumes = list(filter(lambda v: v.__is_valid(), volumes))
        return volumes

    
    def __is_valid(self) -> bool:
        return self.dim.x > 0 and \
               self.dim.y > 0 and \
               self.dim.z > 0 and \
               self.support is not None and \
               self.support.area() > 0

    
    def __fix_support(self) -> None:
        a = self.support
        # if the area is wholy outside, set to None and stop
        if not (self.pos.x - a.dim.x <= a.pos.x <= self.pos.x + self.dim.x) or \
           not (self.pos.y - a.dim.y <= a.pos.y <= self.pos.y + self.dim.y) or \
           not (self.pos.z           <= a.pos.z <= self.pos.z + self.dim.z):
            self.support = None
            return
        
        adx = clamp(a.dim.x - (self.pos.x - a.pos.x), 0, a.dim.x) # left overshoot
        adx = min(adx, self.dim.x + self.pos.x - a.pos.x)         # right overshoot
        
        ady = clamp(a.dim.y - (self.pos.y - a.pos.y), 0, a.dim.y) # left overshoot
        ady = min(ady, self.dim.y + self.pos.y - a.pos.y)         # right overshoot
        
        a.dim = Vector2(adx, ady)

        a.pos = clamp3(a.pos, self.pos, self.pos + self.dim)
    
    def __duplicate(self) -> Volume:
        return Volume(
            pos = copy(self.pos),
            dim = copy(self.dim),
            support = deepcopy(self.support)
        )
