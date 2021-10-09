import api

import log
from game import Game
from solver.config import Config

with open('secret/apikey.txt', 'r') as f:
    api_key = f.read().rstrip('\n')

fetcher = lambda id: api.fetch_game(api_key, id)['gameStats']


def main(maps: list[str]) -> None:
    games = [Game(api.new_game(api_key, map)) for map in maps]
   
    for game in games:
        placed_packages = game.solve(None)
        solution = [pp.as_solution() for pp in placed_packages]
        submit_game_response = api.submit_game(api_key, game.name(), solution)
        if submit_game_response is not None:
            score = log.log_solution(fetcher, game.name(), submit_game_response)
            print()


if __name__ == "__main__":
	from sys import argv
	if len(argv) < 2:
		main(['training1'])
	else:
		main(argv[1:])
