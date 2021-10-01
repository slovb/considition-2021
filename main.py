from refactored_solver import RefactoredSolver as Solver
import api
from model import Vehicle, Package

with open('secret/apikey.txt', 'r') as f:
    api_key = f.read().rstrip('\n')


def main(map_name: str) -> None:
	response = api.new_game(api_key, map_name)
	vehicle = parse_vehicle(response)
	packages = parse_packages(response)

	solver = Solver(vehicle=vehicle, packages=packages)
	placed_packages = solver.solve()
	solution = [pp.as_solution() for pp in placed_packages]
	
	submit_game_response = api.submit_game(api_key, map_name, solution)
	if submit_game_response is not None:
		log_solution(response, submit_game_response)


def parse_vehicle(game_info: dict) -> Vehicle:
	return Vehicle(**game_info['vehicle'])


def parse_packages(game_info: dict) -> list[Package]:
	return [Package(**package) for package in game_info["dimensions"]]


def log_solution(response: dict, submit_game_response: dict) -> None:
	map_name = response['mapName']
	score = submit_game_response['score']
	valid = submit_game_response['valid']
	link = submit_game_response['link'].split(' ')[-1]

	text = '{}, {}, {}, {}'.format(map_name, score, valid, link)
	print(text)

	if not valid:
		return
	filename = 'log/solution_{}.txt'.format(map_name)
	log(filename, text)


def log(filename: str, text: str) -> None:
	from datetime import datetime
	now = datetime.now().strftime("%Y%m%d, %H:%M:%S")
	with open(filename, 'a') as f:
		f.write('{}, {}\n'.format(now, text))


if __name__ == "__main__":
	from sys import argv
	if len(argv) < 2:
		print('missing parameter')
		exit()
	main(argv[1])
