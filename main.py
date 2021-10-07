import api

from model import Package, Vector3

from solver.order_align import OrderAlign as Solver

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


def parse_vehicle(game_info: dict) -> Vector3:
    return Vector3(
		x = game_info['vehicle']['length'],
		y = game_info['vehicle']['width'],
		z = game_info['vehicle']['height']
	)


def parse_packages(game_info: dict) -> list[Package]:
	packages = []
	for p in game_info['dimensions']:
		packages.append(Package(
			id = p['id'],
			dim = Vector3(p['length'], p['width'], p['height']),
			weightClass = p['weightClass'],
			orderClass = p['orderClass']
		))
	return packages


def log_solution(response: dict, submit_game_response: dict) -> None:
	map_name = response['mapName']
	score = submit_game_response['score']
	valid = submit_game_response['valid']
	link = submit_game_response['link'].split(' ')[-1]

	scoreData = valid
	if valid:
		gameStats = api.fetch_game(api_key, submit_game_response['gameId'])['gameStats']
		scoreData = '{:.2f}, {} / {} x, {} / {} order, {} weight ({} crushed)'.format(
			gameStats['packingEfficiency'],
			gameStats['packedLength'],
			gameStats['maxLengthScore'],
			gameStats['orderScore'],
			gameStats['maxOrderScore'],
			gameStats['weightScore'],
			gameStats['crushedPackages']
		)
	text = '{}, {}, {}, {}'.format(map_name, score, scoreData, link)
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
		main('training1')
	else:
		main(argv[1])
