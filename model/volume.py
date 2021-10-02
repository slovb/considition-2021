from __future__ import annotations
from dataclasses import dataclass, field

from .vector import Vector

@dataclass
class Volume:
    pos: Vector
    dim: Vector
    supported_positions: list[Vector] = field(default_factory=list)

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
 
    def remove(self, volume: Volume) -> list[Volume]:
        '''remove a volume, getting a list of all the maximal (pairwise intersecting) 
           volumes that can be created in the remaining space'''
        return [volume]
