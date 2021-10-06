from __future__ import annotations
from dataclasses import dataclass

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
    support: Area

    __key: tuple = None


    def key(self) -> tuple:
        if self.__key is None:
            self.__key = (
                self.pos.key(),
                self.dim.key(),
                self.support.key()
            )
        return self.__key
        

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
    
    
    def get_midpoint(self) -> Vector3:
        return Vector3(
            self.pos.x + self.dim.x / 2,
            self.pos.y + self.dim.y / 2,
            self.pos.z + self.dim.z / 2
        )
    
    
    def get_far_corner(self) -> Vector3:
        return self.pos + self.dim
    
    
    def resize(self, dim: Vector3) -> Volume:
        return Volume(
            self.pos,
            dim,
            Volume.crop_support(self.pos, dim, self.support)
        )

 
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
            volumes.append(Volume(
                self.pos,
                d,
                Volume.crop_support(self.pos, d, self.support)
            ))
        
        # right moves past volume and shrinks until the right bound is hit
        r_pos = clamp3(self.pos + rel_pos_right, left_bound, right_bound)
        r_dim = clamp3(self.dim - (r_pos - self.pos), (0, 0, 0), self.dim)
        r_poses = oneOfLeftTwoOfRight(r_pos, self.pos)
        r_dims = oneOfLeftTwoOfRight(r_dim, self.dim)
        volumes.append(Volume(
            r_poses[0],
            r_dims[0],
            Volume.crop_support(r_poses[0], r_dims[0], self.support)
        ))
        volumes.append(Volume(
            r_poses[1],
            r_dims[1],
            Volume.crop_support(r_poses[1], r_dims[1], self.support)
        ))
        volumes.append(Volume(
            r_poses[2],
            r_dims[2],
            Volume.crop_support(r_poses[2], r_dims[2], vol.support)
        ))

        volumes = list(filter(lambda v: v.__is_valid(), volumes))
        return volumes

    
    def __is_valid(self) -> bool:
        return self.dim.x > 0 and \
               self.dim.y > 0 and \
               self.dim.z > 0 and \
               self.support is not None and \
               self.support.area() > 0

    
    @staticmethod
    def crop_support(pos: Vector3, dim: Vector3, a: Area) -> Area:
        if a is None:
            return None
        
        # if the area is wholy outside, set to None and stop
        if not (pos.x - a.dim.x <= a.pos.x <= pos.x + dim.x) or \
           not (pos.y - a.dim.y <= a.pos.y <= pos.y + dim.y) or \
           not (pos.z           <= a.pos.z <= pos.z + dim.z):
            return None
        
        adx = clamp(a.dim.x - (pos.x - a.pos.x), 0, a.dim.x) # left overshoot
        adx = min(adx, dim.x + pos.x - a.pos.x)              # right overshoot
        
        ady = clamp(a.dim.y - (pos.y - a.pos.y), 0, a.dim.y) # left overshoot
        ady = min(ady, dim.y + pos.y - a.pos.y)              # right overshoot
        
        return Area(
            pos = clamp3(a.pos, pos, pos + dim),
            dim = Vector2(adx, ady)
        )

    
    def __setitem__(self, key, _) -> None:
        raise AttributeError(key)
    
    def __delitem__(self, key) -> None:
        raise AttributeError(key)
