import requests
from datetime import datetime

BASE_URL = 'http://localhost:8080/'

MENU_OPTIONS = [
    'NEW GAME',
    'RANKING',
    'EXIT'
]

def get_list_of_the_best_players():
    return requests.get(url = BASE_URL + '/rank/sorted').json()

def save_game__to_database(login: str, points: int):
    payload = {'login': login,
        'date': datetime.now(),
        'points': points }

    return requests.post(url = BASE_URL + '/rank', data = payload)

def print_menu(current_position_index: int):
    options = MENU_OPTIONS[:]
    options[current_position_index] = MENU_OPTIONS[current_position_index] + ' <--'

    [print(x) for x in options]



if __name__ == "__main__":
    print_menu(0)