from runner import get_runner
from solver.config import Config
from searcher import Searcher, scaling_options


def main() -> None:  
    config = Config(
        LOG_PLACED=False,
        LOG_RESIZE=False,
        PREFERRED_NUM_CANDIDATES=200,
        
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
        
        # MUL_X = 1.33, MUL_BOUNDING = 1.09, MUL_WEIGHT = 10000.1, MUL_SIDE_ALIGN = 1.09, MUL_ORDER_SKIP = 0.81, MUL_ORDER_BREAK = 10890.0,
        # MUL_X = 2.3561761300000015, MUL_BOUNDING = 1.579910310000001, MUL_WEIGHT = 1067200.2435293144, MUL_SIDE_ALIGN = 0.6436341000000001, MUL_ORDER_SKIP = 0.7290000000000001, MUL_ORDER_BREAK = 1056517.6759172622,
        MUL_X = 3.1360704290300028, MUL_BOUNDING = 1.7205223275900012, MUL_WEIGHT = 3684264.6807295624, MUL_SIDE_ALIGN = 0.6436341000000001, MUL_ORDER_SKIP = 3.7219281189493496, MUL_ORDER_BREAK = 1035492.974166509
    )
    
    step = 0.5
    searcher = Searcher(get_runner(['training1', 'training2']))
    settings = [(name, config[name], step) for name in ['MUL_X', 'MUL_BOUNDING', 'MUL_WEIGHT', 'MUL_SIDE_ALIGN', 'MUL_ORDER_SKIP', 'MUL_ORDER_BREAK']]
    searcher.search(config, settings, options_builder=scaling_options)


if __name__ == "__main__":
    main()
