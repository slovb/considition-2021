from time import time
import api

import log
from solver.config_op import *
from game import Game
from solver.config import Config
from search import *
from searcher import Searcher

with open('secret/apikey.txt', 'r') as f:
    api_key = f.read().rstrip('\n')

fetcher = lambda id: api.fetch_game(api_key, id)['gameStats']

def main() -> None:
    maps = ['training1', 'training2']
    games = [Game(api.new_game(api_key, map)) for map in maps]
    
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
        PENALTY_HEAVY_ON_LIGHT=70
    )
    # ops = [set_op('PREFERRED_NUM_CANDIDATES', v) for v in range(1, 200)]
    
    # experiment with order scoring alternative
    
    # ops = [set_op('PENALTY_HEAVY_ON_LIGHT', v) for v in [10, 50, 90, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 10000]]
    # ops = [nop, set_op('ENABLE_WEIGHT', True)] + [set_op('PENALTY_HEAVY_ON_MEDIUM', v) for v in range(5, 20, 2)]
    # run_ops(games, config, ops)
    runner = lambda config: run_games(games, config)
    # search_1_attr(runner, config, 'EXP_X', 3, 1)
    searcher = Searcher(runner)
    
    # searcher.search(config, [
    #     ('PENALTY_HEAVY_ON_HEAVY', 5, 2),
    #     ('PENALTY_HEAVY_ON_MEDIUM', 12, 5),
    #     ('PENALTY_HEAVY_ON_LIGHT', 50, 20),
    # ])
    searcher.search(config, [
        ('MUL_ORDER_BREAK', 10000.0, 1000.0),
        ('ORDER_BASE', 10, 2),
        ('PENALTY_NOT_HEAVY', 1000, 100),
        ('PENALTY_BOUNDING_BREAK', 10**7, 10**6)
    ])


def run_ops(games: list[Game], config: Config, ops: list[ConfigOp]):
    history = []
    start = time()
    for i, op in enumerate(ops):
        config = op.action(config)
        print('-\t-\t-\t-\t-\t-\t-\t-')
        score = run_games(games, config)
        end = time()
        print('{}: {}\t{:.2f} seconds'.format(op.name, score, end - start))
        history.append((score, i, op.name))
        start = end
    print('=\t=\t=\t=\t=\t=\t=\t=')
    for h in sorted(history):
        print(h)


def run_games(games: list[Game], config: Config):
    score = 0
    for game in games:
        placed_packages = game.solve(config)
        solution = [pp.as_solution() for pp in placed_packages]
        submit_game_response = api.submit_game(api_key, game.name(), solution)
        if submit_game_response is not None:
            score += log.log_solution(fetcher, game.name(), submit_game_response)
    return score 


if __name__ == "__main__":
    main()
