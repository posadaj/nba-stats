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

import json
import requests


BASE_URL = "https://api-nba-v1.p.rapidapi.com/"
API_KEY = "<KEY>"
HEADERS = {
  'x-rapidapi-key': API_KEY,
  'x-rapidapi-host': 'api-nba-v1.p.rapidapi.com'
}


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


def get_games_for_season(season: int) -> None:
    """ Get games for season and save locally. """
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

    with open(f'db/games-{season}.json', 'w') as file_id:
        file_id.write(json.dumps(games))


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


    get_games_for_season(2023)



if __name__ == '__main__':
	main()