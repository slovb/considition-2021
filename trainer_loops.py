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
        
        PENALTY_HEAVY_ON_MEDIUM=17,
        PENALTY_HEAVY_ON_LIGHT=70,
        PENALTY_HEAVY_ON_HEAVY=0,
        
        # ORDER_BASE=12,
        # PENALTY_NOT_HEAVY=900,
        # PENALTY_BOUNDING_BREAK=9000000,
        # ORDER_BASE=57, PENALTY_NOT_HEAVY=269, PENALTY_BOUNDING_BREAK=1014454, 
        ORDER_BASE=42.75, PENALTY_NOT_HEAVY=269, PENALTY_BOUNDING_BREAK=507227, 
        
        MUL_X = 7.056158465317506, MUL_BOUNDING = 1.9355876185387513, MUL_WEIGHT = 62949116.06840276, MUL_SIDE_ALIGN = 5.498546002734376, MUL_ORDER_SKIP = 2.791446089212012, MUL_ORDER_BREAK = 24269.366582027556
    )
    
    
    for step, depth in [(0.5, 1), (0.5, 1), (0.5, 1), (0.2, 2), (0.2, 2), (0.1, 4)]:
        for attr in [
            'PENALTY_BOUNDING_BREAK',
            'ORDER_BASE',
            'PENALTY_NOT_HEAVY',
            # 'PENALTY_HEAVY_ON_LIGHT',
            # 'PENALTY_HEAVY_ON_MEDIUM',
            'MUL_X',
            'MUL_BOUNDING',
            'MUL_WEIGHT',
            'MUL_SIDE_ALIGN',
            'MUL_ORDER_SKIP',
            'MUL_ORDER_BREAK' ]:
            searcher = Searcher(get_runner(['training1', 'training2']))
            settings = [(name, getattr(config, name), step) for name in [attr]]
            cop = searcher.search(config, settings, depth=depth, options_builder=scaling_options)
            print('best c-op {}'.format(cop.name))
            config = cop.action(config)
        print(config)


if __name__ == "__main__":
    main()
