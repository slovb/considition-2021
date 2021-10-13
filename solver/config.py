from __future__ import annotations
from dataclasses import dataclass, asdict


@dataclass(frozen=True)
class Config:
    
    RANDOMIZE: bool = False
    LOG_RESIZE: bool = True
    LOG_PLACED: bool = True
    
    ENABLE_LIMIT_NUM_CANDIDATES: bool = True
    PREFERRED_NUM_CANDIDATES: int = 50
    
    ENABLE_OPTIMAL_DISTANCE: bool = False
    MUL_OPTIMAL_X: float = 1.0
    MUL_OPTIMAL_Y: float = 1.0
    MUL_OPTIMAL_Z: float = 1.0
    
    ENABLE_HEAVY_PRIORITY: bool = True
    PENALTY_NOT_HEAVY: int = 1000
    
    ENABLE_WEIGHT: bool = True
    PENALTY_HEAVY_ON_LIGHT: int = 50
    PENALTY_HEAVY_ON_MEDIUM: int = 12
    PENALTY_HEAVY_ON_HEAVY: int = 5
    MUL_WEIGHT: float = 1.0
    
    ENABLE_SIDE_ALIGN: bool = True
    MUL_SIDE_ALIGN: float = 1.0
    
    ENABLE_X: bool = True
    MUL_X: float = 1.0
    EXP_X: int = 2
    
    ENABLE_BOUNDING: bool = True
    PENALTY_BOUNDING_BREAK: int = 10**7
    MUL_BOUNDING: float = 1.0
    EXP_BOUNDING: float = 1.0
    
    ENABLE_ORDER_SKIP: bool = True
    ORDER_BASE_REDUCTION: int = 1000
    ORDER_BASE: int = 10
    EXP_ORDER_N: int = 2
    MUL_ORDER_SKIP: float = 1.0
    EXP_ORDER_SKIP: int = 2
    
    ENABLE_ORDER_BREAK: bool = True
    MUL_ORDER_BREAK: float = 10000.0
    
    ENABLE_BOUNDED_X: bool = True
    MUL_BOUNDED_X: float = 10**6
    
    
    def set(self, attr: str, value) -> Config:
        d = asdict(self)
        d[attr] = value
        return Config(**d)