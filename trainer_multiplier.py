from runner import get_runner
from solver.config import Config
from searcher import Searcher, scaling_options


def main() -> None:  
    config = Config(
        LOG_PLACED=False,
        LOG_RESIZE=False,
        PREFERRED_NUM_CANDIDATES=10000,
        
        ENABLE_BOUNDING=True,
        ENABLE_HEAVY_PRIORITY=True,
        ENABLE_OPTIMAL_DISTANCE=False,
        ENABLE_ORDER_BREAK=True,
        ENABLE_ORDER_SKIP=True,
        ENABLE_SIDE_ALIGN=True,
        ENABLE_WEIGHT=True,
        ENABLE_X=True,
        
        # PENALTY_HEAVY_ON_HEAVY=3,
        PENALTY_HEAVY_ON_HEAVY=0, # testing a bit of intuition
        PENALTY_HEAVY_ON_MEDIUM=17,
        PENALTY_HEAVY_ON_LIGHT=70,   
        
        ORDER_BASE=12,
        PENALTY_NOT_HEAVY=900,
        PENALTY_BOUNDING_BREAK=9000000,
        
        MUL_X = 1.33, 
        MUL_BOUNDING = 1.09,
        MUL_WEIGHT = 12.1,
        MUL_SIDE_ALIGN = 1.09,
        MUL_ORDER_SKIP = 0.81,
        MUL_ORDER_BREAK = 10890.0,
    )
    
    searcher = Searcher(get_runner(['training1', 'training2']))
    searcher.search(config, [
        ('MUL_X', config.MUL_X, 0.1),
        ('MUL_BOUNDING', config.MUL_BOUNDING, 0.1),
        ('MUL_WEIGHT', config.MUL_WEIGHT, 0.1),
        ('MUL_SIDE_ALIGN', config.MUL_SIDE_ALIGN, 0.1),
        ('MUL_ORDER_SKIP', config.MUL_ORDER_SKIP, 0.1),
        ('MUL_ORDER_BREAK', config.MUL_ORDER_BREAK, 0.1),
    ], options_builder=scaling_options)


if __name__ == "__main__":
    main()
