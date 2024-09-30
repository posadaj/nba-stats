import duckdb


# Cache a simple mapping of team_id to team_name to better display results
TEAM_CACHE = {}

def init_db_connection():
    duckdb.sql("CREATE TABLE games AS FROM 'db/games.json';")
    duckdb.sql("CREATE TABLE teams AS FROM 'db/teams.json';")
    print("Read games and teams tables into duckdb")


def cache_teams() -> None:
    """ Cache the teams so we can easily print the results throughout our program. """
    global TEAM_CACHE

    sql_statement = """SELECT team_id, team_name from teams;"""
    response = duckdb.sql(sql_statement).fetchall()

    for record in response:
        TEAM_CACHE[record[0]] = record[1]


def basic_extraction():
    """ Retrieve the top 10 highest-scoring games in the last decade. """

    sql_statement = """
    SELECT game_id, home_score + away_score as total_score
    FROM games
    WHERE season >= 2014 AND season <= 2024
    ORDER BY total_score DESC
    LIMIT 10
    """

    response = duckdb.sql(sql_statement).fetchall()
    print("Printing the top 10 highest-scoring games in the last decade")
    for index in range(len(response)):
        game_id, total_score = response[index]
        print(f"The #{index+1} highest-scoring game had a total score of {total_score} and game_id {game_id}")


def win_loss_records():
    """ Retrieve the win loss record for each team over the last decade. """

    sql_statement = """
    SELECT COUNT(game_id), season,
        CASE
            WHEN @home_score > @away_score THEN home_team
            ELSE away_team
        END AS winning_team,
    FROM games
    GROUP BY winning_team, season
    ORDER BY winning_team;
    """

    response = duckdb.sql(sql_statement).fetchall()
    print("Printing the win-loss record for teams in the last 10 years")
    for team_total_for_season in response:
        games_won, season, team_id = team_total_for_season
        games_lost = 82 - games_won
        print(f"In {season}, the team {TEAM_CACHE[team_id]} had a record of {games_won}-{games_lost}")


def main():
    """
    Run through some basic tasks to interact with the NBA data
    """
    init_db_connection()

    cache_teams()

    # basic_extraction()

    win_loss_records()


if __name__ == '__main__':
	main()