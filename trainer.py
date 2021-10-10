from runner import get_runner
from solver.config import Config
from searcher import Searcher


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
    # ops = [set_op('PREFERRED_NUM_CANDIDATES', v) for v in range(1, 200)]
    
    # experiment with order scoring alternative
    
    # ops = [set_op('PENALTY_HEAVY_ON_LIGHT', v) for v in [10, 50, 90, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 10000]]
    # ops = [nop, set_op('ENABLE_WEIGHT', True)] + [set_op('PENALTY_HEAVY_ON_MEDIUM', v) for v in range(5, 20, 2)]
    # run_ops(games, config, ops)
    # search_1_attr(runner, config, 'EXP_X', 3, 1)
    
    searcher = Searcher(get_runner(['training1', 'training2']))

    searcher.search(config, [
        ('MUL_ORDER_BREAK', 9000.0, 900.0),
        ('ORDER_BASE', 12, 1),
        ('PENALTY_NOT_HEAVY', 900, 90),
        ('PENALTY_BOUNDING_BREAK', 9*10**6, 9*10**5)
    ])


if __name__ == "__main__":
    main()
