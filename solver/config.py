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
    
    ENABLE_VOLUME: bool = True
    MUL_VOLUME: float = 1.0
    
    ENABLE_ORDER_SKIP: bool = True
    # ORDER_BASE_REDUCTION: int = 1000
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
    
    
currentConfig = config = Config(
    RANDOMIZE=False, 
    LOG_RESIZE=False,
    LOG_PLACED=False,
    ENABLE_LIMIT_NUM_CANDIDATES=False,
    PREFERRED_NUM_CANDIDATES=150,
    
    ENABLE_OPTIMAL_DISTANCE=False,
    MUL_OPTIMAL_X=1.0,
    MUL_OPTIMAL_Y=1.0,
    MUL_OPTIMAL_Z=1.0,
    
    ENABLE_HEAVY_PRIORITY=True,
    PENALTY_NOT_HEAVY=42.15992028364802,
    
    ENABLE_WEIGHT=True,
    PENALTY_HEAVY_ON_LIGHT=45.927,
    PENALTY_HEAVY_ON_MEDIUM=11.1537,
    PENALTY_HEAVY_ON_HEAVY=0,
    
    MUL_WEIGHT=91247.98325374069,
    ENABLE_SIDE_ALIGN=True,
    MUL_SIDE_ALIGN=1.1261022213600007,
    
    ENABLE_X=True,
    MUL_X=6.985596880664332,
    EXP_X=1.9800000000000002,
    
    ENABLE_BOUNDING=True,
    PENALTY_BOUNDING_BREAK=88329.8219153818,
    MUL_BOUNDING=1.548470094831001,
    EXP_BOUNDING=1.0,
    
    ENABLE_VOLUME=True,
    MUL_VOLUME=1.9355876185387513,

    ENABLE_ORDER_SKIP=True,
    ORDER_BASE=20.287098,
    EXP_ORDER_N=1.0240000000000002,
    MUL_ORDER_SKIP=4.861096431114389,
    EXP_ORDER_SKIP=2.4200000000000004,

    ENABLE_ORDER_BREAK=True,
    MUL_ORDER_BREAK=36229.58986764314,

    ENABLE_BOUNDED_X=True,
    MUL_BOUNDED_X=178120.88369971208
)