from time import time
import api

import log
from game import Game
from solver.config_op import *
from solver.config import Config

with open('secret/apikey.txt', 'r') as f:
    api_key = f.read().rstrip('\n')


fetcher = lambda id: api.fetch_game(api_key, id)['gameStats']


def get_runner(maps: list[str]) -> Callable[[Config], int]:
    games = [Game(api.new_game(api_key, map)) for map in maps]
    return lambda config: run_games(games, config)


def get_ops_runner(maps: list[str]) -> Callable[[Config, list[ConfigOp]], int]:
    games = [Game(api.new_game(api_key, map)) for map in maps]
    return lambda config, ops: run_games(games, config, ops)


def run_games(games: list[Game], config: Config) -> int:
    score = 0
    for game in games:
        placed_packages = game.solve(config)
        solution = [pp.as_solution() for pp in placed_packages]
        submit_game_response = api.submit_game(api_key, game.name(), solution)
        if submit_game_response is not None:
            score += log.log_solution(fetcher, game.name(), submit_game_response)
    return score


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
