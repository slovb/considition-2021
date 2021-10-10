from time import time
import api

import log
from model.placed_package import PlacedPackage
from solver.config_op import *
from game import Game
from solver.config import Config

with open('secret/apikey.txt', 'r') as f:
    api_key = f.read().rstrip('\n')

fetcher = lambda id: api.fetch_game(api_key, id)['gameStats']

def main() -> None:
    maps = ['training1']
    games = [Game(api.new_game(api_key, map)) for map in maps]
    
    config = Config(
        LOG_PLACED=False,
        LOG_RESIZE=False,
        PREFERRED_NUM_CANDIDATES=100,
        # ENABLE_BOUNDING=False,
        # ENABLE_HEAVY_PRIORITY=False,
        # ENABLE_OPTIMAL_DISTANCE=False,
        # ENABLE_ORDER_BREAK=False,
        # ENABLE_ORDER_SKIP=False,
        # ENABLE_SIDE_ALIGN=False,
        # ENABLE_WEIGHT=False,
        # ENABLE_X=False
    )
    # ops = [set_op('PREFERRED_NUM_CANDIDATES', v) for v in range(1, 200)]
    
    # experiment with order scoring alternative
    
    # ops = [set_op('PENALTY_HEAVY_ON_LIGHT', v) for v in [10, 50, 90, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 10000]]
    ops = [nop]
    
    history = []
    
    start = time()
    for i, op in enumerate(ops):
        print('-\t-\t-\t-\t-\t-\t-\t-')
        score = 0
        config = op.action(config)
        for game in games:
            placed_packages = game.solve(config)
            solution = [pp.as_solution() for pp in placed_packages]
            submit_game_response = api.submit_game(api_key, game.name(), solution)
            if submit_game_response is not None:
                score += log.log_solution(fetcher, game.name(), submit_game_response)        
        end = time()
        print('{}: {}\t({}s)'.format(op.name, score, end - start))
        history.append((score, i, op.name))
        start = end
    
    print('=\t=\t=\t=\t=\t=\t=\t=')
    for h in sorted(history):
        print(h)


if __name__ == "__main__":
    main()
