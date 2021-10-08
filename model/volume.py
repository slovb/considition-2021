from __future__ import annotations
from dataclasses import dataclass

from .vector import clamp, Vector2, Vector3
from .support import Support

def oneOfLeftTwoOfRight(l: Vector3, r: Vector3):
    return [
        Vector3(l.x, r.y, r.z),
        Vector3(r.x, l.y, r.z),
        Vector3(r.x, r.y, l.z)
    ]


@dataclass(order=True, frozen=True)
class Volume:
    pos: Vector3
    dim: Vector3
    support: Support


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
            None if self.support is None else self.support.crop(self.pos, dim)
        )

 
    def remove(self, vol: Volume) -> list[Volume]:
        '''remove a volume, getting a list of all the maximal (pairwise intersecting) 
           volumes that can be created in the remaining space'''
        if not self.vol_intersect(vol):
            return [self]
        volumes: list[Volume] = []
        
        rel_pos_left = vol.pos - self.pos
        rel_pos_right = rel_pos_left + vol.dim
        left_bound = self.pos
        right_bound = self.pos + self.dim
        
        # left does not move, but shrinks until it hits the vol
        l_dim = rel_pos_left.clamp(Vector3(0, 0, 0), self.dim) # bound shrink 0 <= new d <= old d
        l_dims = oneOfLeftTwoOfRight(l_dim, self.dim)
        for d in l_dims:
            volumes.append(Volume(
                self.pos,
                d,
                self.support.crop(self.pos, d)
            ))
        
        # right moves past volume and shrinks until the right bound is hit
        r_pos = (self.pos + rel_pos_right).clamp(left_bound, right_bound)
        r_dim = (self.dim - (r_pos - self.pos)).clamp(Vector3(0, 0, 0), self.dim)
        r_poses = oneOfLeftTwoOfRight(r_pos, self.pos)
        r_dims = oneOfLeftTwoOfRight(r_dim, self.dim)
        volumes.append(Volume(
            r_poses[0],
            r_dims[0],
            self.support.crop(r_poses[0], r_dims[0])
        ))
        volumes.append(Volume(
            r_poses[1],
            r_dims[1],
            self.support.crop(r_poses[1], r_dims[1])
        ))
        volumes.append(Volume(
            r_poses[2],
            r_dims[2],
            vol.support.add_weights(self.support.weights).crop(r_poses[2], r_dims[2])
        ))

        volumes = [vol for vol in volumes if vol.__is_valid()]
        return volumes

    
    def __is_valid(self) -> bool:
        return self.dim.x > 0 and \
               self.dim.y > 0 and \
               self.dim.z > 0 and \
               self.support is not None and \
               self.support.calc_area() > 0
