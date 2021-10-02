import copy

from .pos import Pos
from .dimension import Dimension


class Volume:

    def __init__(self, pos: Pos, dim: Dimension):
        self.pos = copy.copy(pos)
        self.dim = copy.copy(dim)
