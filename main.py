from greedy_solver import GreedySolver
import api
import json

with open('secret/apikey.txt', 'r') as f:
    api_key = f.read().rstrip('\n')

map_name = "training1"


def main():
	print("Starting game...")
	response = api.new_game(api_key, map_name)
	greedy = GreedySolver(game_info=response)
	solution = greedy.Solve()
	submit_game_response = api.submit_game(api_key, map_name, solution)
	print(submit_game_response)

if __name__ == "__main__":
    main()