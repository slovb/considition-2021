from __future__ import annotations
from dataclasses import dataclass, field
from copy import copy

from .vector import Vector
from .area import Area

clamp = lambda n, lower, upper: max(min(upper, n), lower)

@dataclass
class Volume:
    pos: Vector
    dim: Vector
    support: Area = None

    def pos_inside(self, pos: Vector) -> bool:
        return (self.pos.x <= pos.x <= self.pos.x + self.dim.x) and \
               (self.pos.y <= pos.y <= self.pos.y + self.dim.y) and \
               (self.pos.z <= pos.z <= self.pos.z + self.dim.z) 

    def dim_inside(self, dim: Vector) -> bool:
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
        
    
    def corners(self) -> list[Vector]:
        positions = []
        for x in [0, self.dim.x]:
            for y in [0, self.dim.y]:
                for z in [0, self.dim.z]:
                    positions.append(self.pos + Vector(x, y, z))
        return positions
 
    def remove(self, vol: Volume) -> list[Volume]:
        '''remove a volume, getting a list of all the maximal (pairwise intersecting) 
           volumes that can be created in the remaining space'''
        if not self.vol_intersect(vol):
            return [self]
        volumes = []
        
        for c in ['x', 'y', 'z']:
            rel_pos_left = vol.pos[c] - self.pos[c]
            rel_pos_right = rel_pos_left + vol.dim[c]
            left_bound = self.pos[c]
            right_bound = self.pos[c] + self.dim[c]
            
            # left does not move, but shrinks until it hits the vol
            v = self.__duplicate()
            #v.dim[c] = max(0, min(v.dim[c], max(0, rel_pos_left))) # bound shrink 0 <= new d <= old d
            v.dim[c] = clamp(max(0, rel_pos_left), 0, v.dim[c]) # bound shrink 0 <= new d <= old d
            v.__fix_support()
            volumes.append(v)
            
            # right moves past volume and shrinks until the right bound is hit
            v = self.__duplicate()
            #newPos = max(right_bound, min(left_bound, v.pos[c] + rel_pos_right)) # bound move lb <= p <= rb
            newPos = clamp(v.pos[c] + rel_pos_right, left_bound, right_bound)
            #v.dim[c] = max(0, v.dim[c] - (newPos - v.pos[c])) # bound shrink 0 <= new d <= old d (implied if above correct)
            v.dim[c] = clamp(v.dim[c] - (newPos - v.pos[c]), 0, v.dim[c])
            v.pos[c] = newPos
            if c == 'z': # new support area ontop of removed volume
                v.support = Area(
                    pos = Vector(vol.pos.x, vol.pos.y, vol.pos.z + vol.dim.z),
                    dimX = vol.dim.x,
                    dimY = vol.dim.y
                )
            v.__fix_support()
            volumes.append(v)
        
        volumes = filter(lambda v: v.__is_valid(), volumes)
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
        if not (self.pos.x - a.dimX <= a.pos.x <= self.pos.x + self.dim.x) or \
           not (self.pos.y - a.dimY <= a.pos.y <= self.pos.y + self.dim.y) or \
           not (self.pos.z          <= a.pos.z <= self.pos.z + self.dim.z):
            self.support = None
            return
        # if the area starts outside, crop it
        if a.pos.x < self.pos.x:
            a.dimX = max(0, a.dimX - (self.pos.x - a.pos.x))
            a.pos.x = self.pos.x
        if a.pos.y < self.pos.y:
            a.dimY = max(0, a.dimY - (self.pos.y - a.pos.y))
            a.pos.y = self.pos.y
        # if the area goes outside, crop it
        a.dimX = min(a.dimX, self.dim.x)
        a.dimY = min(a.dimY, self.dim.y)
    
    def __duplicate(self) -> Volume:
        return Volume(
            pos = copy(self.pos),
            dim = copy(self.dim),
            support = copy(self.support)
        )
