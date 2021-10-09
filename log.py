from typing import Callable


def log_solution(fetcher: Callable[[str], dict], map_name: str, submit_game_response: dict) -> int:
    score = submit_game_response['score']
    valid = submit_game_response['valid']
    link = submit_game_response['link'].split(' ')[-1]

    scoreData = valid
    if valid:
        gameStats = fetcher(submit_game_response['gameId'])
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
        return 0
    filename = 'log/solution_{}.txt'.format(map_name)
    log(filename, text)
    return score


def log(filename: str, text: str) -> None:
    from datetime import datetime
    now = datetime.now().strftime("%Y%m%d, %H:%M:%S")
    with open(filename, 'a') as f:
        f.write('{}, {}\n'.format(now, text))