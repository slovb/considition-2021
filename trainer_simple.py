from runner import get_runner, get_randomized_runner
from solver.config import Config
from simple_searcher import SimpleSearcher


def main() -> None:  
    config = Config(
        # LOG_RESIZE=False,
        # LOG_PLACED=False,
        # PREFERRED_NUM_CANDIDATES=200,
        # ENABLE_OPTIMAL_DISTANCE=False,
        # MUL_OPTIMAL_X=1.0,
        # MUL_OPTIMAL_Y=1.0,
        # MUL_OPTIMAL_Z=1.0,
        # ENABLE_HEAVY_PRIORITY=True,
        # PENALTY_NOT_HEAVY=242.1,
        # ENABLE_WEIGHT=True,
        # PENALTY_HEAVY_ON_LIGHT=70,
        # PENALTY_HEAVY_ON_MEDIUM=17,
        # PENALTY_HEAVY_ON_HEAVY=0,
        # MUL_WEIGHT=4325830.31721437,
        # ENABLE_SIDE_ALIGN=True,
        # MUL_SIDE_ALIGN=2.2522044427200014,
        # ENABLE_X=True,
        # MUL_X=7.056158465317506,
        # EXP_X=2,
        # ENABLE_BOUNDING=True,
        # PENALTY_BOUNDING_BREAK=138015.34674278405,
        # MUL_BOUNDING=1.9355876185387513,
        # EXP_BOUNDING=1.0,
        # ENABLE_ORDER_SKIP=True,
        # ORDER_BASE=39.623238281249996,
        # EXP_ORDER_N=2,
        # MUL_ORDER_SKIP=1.6279713592284457,
        # EXP_ORDER_SKIP=2,
        
        # ENABLE_ORDER_BREAK=False,
        # MUL_ORDER_BREAK=1667.7781722310992
        RANDOMIZE=True,
        LOG_RESIZE=False,
        LOG_PLACED=False,
        ENABLE_LIMIT_NUM_CANDIDATES=False,
        PREFERRED_NUM_CANDIDATES=200,
        ENABLE_OPTIMAL_DISTANCE=False,
        MUL_OPTIMAL_X=1.0,
        MUL_OPTIMAL_Y=1.0,
        MUL_OPTIMAL_Z=1.0,
        
        ENABLE_HEAVY_PRIORITY=True,
        PENALTY_NOT_HEAVY=242.1,
        ENABLE_WEIGHT=True,
        PENALTY_HEAVY_ON_LIGHT=70,
        PENALTY_HEAVY_ON_MEDIUM=17,
        PENALTY_HEAVY_ON_HEAVY=0,
        MUL_WEIGHT=27036.439482589834,
        ENABLE_SIDE_ALIGN=True,
        MUL_SIDE_ALIGN=1.1261022213600007,
        ENABLE_X=True,
        MUL_X=7.056158465317506,
        EXP_X=2,
        ENABLE_BOUNDING=True,
        PENALTY_BOUNDING_BREAK=138015.34674278405,
        MUL_BOUNDING=1.9355876185387513,
        EXP_BOUNDING=1.0,
        ENABLE_ORDER_SKIP=True,
        ORDER_BASE=39.623238281249996,
        EXP_ORDER_N=2,
        MUL_ORDER_SKIP=1.6279713592284457,
        EXP_ORDER_SKIP=2,
        
        ENABLE_ORDER_BREAK=False,
        MUL_ORDER_BREAK=8.143448106597244e-12,
        
        ENABLE_BOUNDED_X=True,
        MUL_BOUNDED_X=85899.34592000004,
    )
    
    maps = ['training1', 'training2']
    runner = get_randomized_runner(maps)
    score = runner(config)
    print('baseline: {}'.format(score))
    print('----------------------------------------------------------------')
    for step in [0.2] * 5:
        for attr in [
            'MUL_BOUNDED_X',
            'PENALTY_BOUNDING_BREAK',
            'ORDER_BASE',
            'PENALTY_NOT_HEAVY',
            'PENALTY_HEAVY_ON_LIGHT',
            'PENALTY_HEAVY_ON_MEDIUM',
            'EXP_X',
            'MUL_X',
            'MUL_BOUNDING',
            'MUL_WEIGHT',
            'MUL_SIDE_ALIGN',
            'EXP_ORDER_SKIP',
            'MUL_ORDER_SKIP',
            ]:
            searcher = SimpleSearcher(runner)
            settings = [(name, getattr(config, name), step) for name in [attr]]
            cop, s = searcher.search(config, settings)
            if s > score:
                score = s
                print('best ({}) from {}'.format(score, cop.name))
            else:
                print('no improvement from {} to {}'.format(getattr(config, attr), cop.name))
            config = cop.action(config) # just in case the attribute got decreased
        print(config)
        print('randomize')
        runner = get_randomized_runner(maps)


if __name__ == "__main__":
    main()
