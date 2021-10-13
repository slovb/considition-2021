import api
import log

from game import Game
from model.placed_package import PlacedPackage
from model.vector import Vector3
from solver.config import Config


with open('secret/apikey.txt', 'r') as f:
    api_key = f.read().rstrip('\n')


fetcher = lambda id: api.fetch_game(api_key, id)['gameStats']


def main(map: str) -> None:  
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
        ORDER_BASE=20.287098,
        ORDER_BASE_REDUCTION=1000,
        EXP_ORDER_N=2,
        MUL_ORDER_SKIP=1.6279713592284457,
        EXP_ORDER_SKIP=2,
        
        ENABLE_ORDER_BREAK=False,
        MUL_ORDER_BREAK=8.143448106597244e-12,
        
        ENABLE_BOUNDED_X=True,
        MUL_BOUNDED_X=178120.88369971208,
    )
    
    game = Game(api.new_game(api_key, map))
    placed_packages = game.solve(config)
    
    solution = [pp.as_solution() for pp in placed_packages]
    submit_game_response = api.submit_game(api_key, game.mapName(), solution)
    if submit_game_response is not None:
        log.log_solution(fetcher, game.mapName(), submit_game_response)
    else:
        exit('error')
        
    placed_packages = post_process(placed_packages, game.vehicle)
    solution = [pp.as_solution() for pp in placed_packages]
    submit_game_response = api.submit_game(api_key, game.mapName(), solution)
    if submit_game_response is not None:
        log.log_solution(fetcher, game.mapName(), submit_game_response)
    else:
        exit('error')


def post_process(placed_packages: list[PlacedPackage], vehicle: Vector3) -> list[PlacedPackage]:
    sort = lambda pps: sorted(pps, key=lambda pp: pp.pos.key())
    placed_packages: list[PlacedPackage] = sort(placed_packages)
    
    def validPackage(pp: PlacedPackage, pps: list[PlacedPackage]) -> bool:
        return pp.in_vehicle(vehicle) and not any(pp.check_collision_with(other) for other in pps)
    def move(pp: PlacedPackage, pps: list[PlacedPackage], move: Vector3) -> PlacedPackage:
        new = pp
        new = new.move_without_volume(move)
        while validPackage(new, pps):
            yield new
            new = new.move_without_volume(move)
    
    back = Vector3(-1, 0, 0)
    left = Vector3(0, -1, 0)
    down = Vector3(0, 0, -1)
    
    moved = True
    while moved:
        moved = False
        for i, placed_package in enumerate(placed_packages):
            other = [pp for pp in placed_packages if pp.package.id != placed_package.package.id]
            new = placed_package
            for new in move(new, other, back):
                moved = True
            for new in move(new, other, left):
                moved = True
            for new in move(new, other, down):
                moved = placed_package.package.is_heavy() # don't drop heavy packages on other stuff
            if moved:
                placed_packages[i] = new
                break
        placed_packages = sort(placed_packages)
    return placed_packages


if __name__ == "__main__":
    from sys import argv
    if len(argv) < 2:
        exit('missing arguments')
    for map in argv[1:]:
        main(map)
