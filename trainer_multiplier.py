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
        MUL_WEIGHT=10.0,
        PENALTY_HEAVY_ON_HEAVY=3,
        PENALTY_HEAVY_ON_MEDIUM=17,
        PENALTY_HEAVY_ON_LIGHT=70,
        MUL_ORDER_BREAK=9000.0,
        ORDER_BASE=12,
        PENALTY_NOT_HEAVY=900,
        PENALTY_BOUNDING_BREAK=9000000,
    )
    
    searcher = Searcher(get_runner(['training1', 'training2']))
    searcher.search(config, [
        ('MUL_X', 1.0, 0.1),
        ('MUL_BOUNDING', 1.0, 0.1),
        ('MUL_WEIGHT', 10.0, 0.1),
        ('MUL_SIDE_ALIGN', 1.0, 0.1),
        ('MUL_ORDER_SKIP', 1.0, 0.1),
        ('MUL_ORDER_BREAK', 10.0**4, 0.1),
    ], options_builder=scaling_options)


if __name__ == "__main__":
    main()
