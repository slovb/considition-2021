import api

import log
from game import Game
from solver.config import Config

with open('secret/apikey.txt', 'r') as f:
    api_key = f.read().rstrip('\n')

fetcher = lambda id: api.fetch_game(api_key, id)['gameStats']


def main(maps: list[str]) -> None:
    config = Config(
        LOG_RESIZE=False,
        LOG_PLACED=False,
        ENABLE_LIMIT_NUM_CANDIDATES=False,
        PREFERRED_NUM_CANDIDATES=150,
        
        ENABLE_OPTIMAL_DISTANCE=False,
        MUL_OPTIMAL_X=1.0,
        MUL_OPTIMAL_Y=1.0,
        MUL_OPTIMAL_Z=1.0,
        
        ENABLE_HEAVY_PRIORITY=True,
        PENALTY_NOT_HEAVY=42.15992028364802,
        
        ENABLE_WEIGHT=True,
        PENALTY_HEAVY_ON_LIGHT=45.927,
        PENALTY_HEAVY_ON_MEDIUM=11.1537,
        PENALTY_HEAVY_ON_HEAVY=0,
        MUL_WEIGHT=27036.439482589834,
        
        ENABLE_SIDE_ALIGN=True,
        MUL_SIDE_ALIGN=1.1261022213600007,
        
        ENABLE_X=True,
        MUL_X=6.985596880664332,
        EXP_X=1.9800000000000002,
        
        ENABLE_BOUNDING=True,
        PENALTY_BOUNDING_BREAK=88329.8219153818,
        MUL_BOUNDING=1.9355876185387513,
        EXP_BOUNDING=1.0,
        
        ENABLE_ORDER_SKIP=True,
        ORDER_BASE_REDUCTION=1000,
        ORDER_BASE=20.287098,
        EXP_ORDER_N=2,
        MUL_ORDER_SKIP=1.6279713592284457,
        EXP_ORDER_SKIP=2.4200000000000004,
        
        ENABLE_ORDER_BREAK=True,
        MUL_ORDER_BREAK=8.143448106597244e3,
        
        ENABLE_BOUNDED_X=True,
        MUL_BOUNDED_X=178120.88369971208,
    )
    
    games = [Game(api.new_game(api_key, map)) for map in maps]
   
    for game in games:
        placed_packages = game.solve(config)
        solution = [pp.as_solution() for pp in placed_packages]
        submit_game_response = api.submit_game(api_key, game.mapName(), solution)
        if submit_game_response is not None:
            score = log.log_solution(fetcher, game.mapName(), submit_game_response)
            print()


if __name__ == "__main__":
	from sys import argv
	if len(argv) < 2:
		main(['training1'])
	else:
		main(argv[1:])
