from __future__ import annotations
from dataclasses import dataclass

from .vector import clamp, Vector2, Vector3
from .area import Area

@dataclass(order=True, frozen=True)
class Support:
    area: Area
    weights: tuple
    
    
    def add_weights(self, weights: tuple) -> Support:
        return Support(
            area = self.area,
            weights = weights + self.weights
        )
    
    
    def calc_area(self) -> int:
        return self.area.calc_area()


    def crop(self, pos: Vector3, dim: Vector3) -> Support:
        a = self.area
        
        # if the area is wholy outside, set to None and stop
        if not (pos.x - a.dim.x <= a.pos.x <= pos.x + dim.x) or \
           not (pos.y - a.dim.y <= a.pos.y <= pos.y + dim.y) or \
           not (pos.z           <= a.pos.z <= pos.z + dim.z):
            return None
        
        adx = clamp(a.dim.x - (pos.x - a.pos.x), 0, a.dim.x) # left overshoot
        adx = min(adx, dim.x + pos.x - a.pos.x)              # right overshoot
        
        ady = clamp(a.dim.y - (pos.y - a.pos.y), 0, a.dim.y) # left overshoot
        ady = min(ady, dim.y + pos.y - a.pos.y)              # right overshoot
        
        return Support(
            area = Area(
                pos = a.pos.clamp(pos, pos + dim),
                dim = Vector2(adx, ady)
            ),
            weights = self.weights
        )
