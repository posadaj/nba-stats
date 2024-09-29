"""
Populate the 'games' table
Use the /games endpoint and some transformations

Games DB schema:
- game_id (in API)
- season (in API)
- date (in API, just take start_date)
- home_team (in API teams.home.id)
- away_team (in API teams.visitors.id)
- home_score (in API scores.home.points)
- away_score (in API scores.visitors.points)
"""
import sys
import os

import json
import requests
from typing import List


BASE_URL = "https://api-nba-v1.p.rapidapi.com/"
API_KEY = "<KEY>"
HEADERS = {
  'x-rapidapi-key': API_KEY,
  'x-rapidapi-host': 'api-nba-v1.p.rapidapi.com'
}

# 10 year window
START_SEASON = 2014
LAST_SEASON = 2023


def setup_client(api_key: str) -> None:
    """ Setup the API client. """

    global API_KEY
    API_KEY = api_key

    global HEADERS
    HEADERS = {
      'x-rapidapi-key': API_KEY,
      'x-rapidapi-host': 'api-nba-v1.p.rapidapi.com'
    }
    print("Just set the HEADERS")
    print(HEADERS)


def get_games_for_season(season: int) -> str:
    """
    Get games for season and save locally.

    Returns:
      The file_name used to store the games for a single season.
    """
    url = f"{BASE_URL}games?season={season}"

    print(f"Qualified URL: {url}")
    print(f"Headers: {HEADERS}")

    response = requests.request("GET", url, headers=HEADERS, data={})

    games = []
    for raw_game in response.json()['response']:
        game = {}
        game['game_id'] = raw_game['id']
        game['season'] = raw_game['season']
        game['date'] = raw_game['date']['start']
        game['home_team'] = raw_game['teams']['home']['id']
        game['away_team'] = raw_game['teams']['visitors']['id']
        game['home_score'] = raw_game['scores']['home']['points']
        game['away_score'] = raw_game['scores']['visitors']['points']
        game['league'] = raw_game['league']
        game['stage'] = raw_game['stage']
        games.append(game)

    file_name = f'db/games-{season}.json'
    with open(file_name, 'a') as file_id:
        file_id.write(json.dumps(games))

    return file_name


def combine_games_across_seasons(filenames: List[str]):
    """ Combine all JSON files for individual seasons into one file to represent games for desired window. """
    all_games = []
    for filename in filenames:
        with open(filename, 'r') as file_id:
            all_games.extend(json.loads(file_id.read()))

    with open('db/games.json', 'a') as file_id:
        file_id.write(json.dumps(all_games))


def setup_games_tables() -> None:
    """
    Setup the games table by pulling NBA data and persisting a single json file. Exists early if data already fetched.
    """
    # Check if data is already pulled

    file_path = os.getcwd() + '/db/games.json'
    if os.path.exists(file_path):
        print('Data already pulled for NBA games. Skipping setup.')
        return

    print("Pulling data for NBA games.")
    files_for_seasons = []
    for season in range(START_SEASON, LAST_SEASON+1):
        files_for_seasons.append(get_games_for_season(season))
    combine_games_across_seasons(files_for_seasons)


def main():
    """ Setup the database. """

    # TODO: Seed 'games' table for last 10 years
    # TODO: Filter out playoff games (call this out somewhere)

    # Populate the API_KEY
    if len(sys.argv) != 2:
        print("Error: To run the database setup, provide API key as an argument.")
        exit(1)

    global API_KEY
    API_KEY = sys.argv[1]

    setup_client(api_key=sys.argv[1])

    setup_games_tables()





if __name__ == '__main__':
	main()