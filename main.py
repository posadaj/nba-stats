import duckdb


"""
Cache the teams database because of its small size

Create a simple cache of the teams table with the mapping { team_id : [ team_name, team_conference] }
This cache allows us to display the results better, by resolving team_id to team_name, and allows us to
simplify our SQL queries and move some processing into code
"""
TEAM_CACHE = {}

def init_db_connection() -> None:
    duckdb.sql("CREATE TABLE games AS FROM 'db/games.json';")
    duckdb.sql("CREATE TABLE teams AS FROM 'db/teams.json';")
    print("Read games and teams tables into duckdb")


def cache_teams() -> None:
    """ Cache the teams so we can easily print the results throughout our program. """
    global TEAM_CACHE

    sql_statement = """SELECT team_id, team_name, conference from teams;"""
    response = duckdb.sql(sql_statement).fetchall()

    for record in response:
        TEAM_CACHE[record[0]] = (record[1], record[2])


def basic_extraction() -> None:
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


def win_loss_records() -> None:
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
        print(f"In {season}, the team {TEAM_CACHE[team_id][0]} had a record of {games_won}-{games_lost}")



def team_performance_by_season() -> None:
    """ Calculate the average points scored by each team per season over the last decade. """

    sql_statement = """
    SELECT season, team, AVG(score) as average_score FROM
        (
            SELECT season, home_team as team, home_score as score
            FROM games
            UNION ALL
            SELECT season, away_team as team, away_score as score
            FROM games
        ) as all_scores
    GROUP BY team, season;
    """

    response = duckdb.sql(sql_statement).fetchall()
    print("Printing the average points scored by each team for the last 10 seasons")
    for record in response:
        season, team_id, average_score = record
        print(f"In {season}, the team {TEAM_CACHE[team_id][0]} scored an average of {round(average_score, 2)} points per game")


def conference_analysis() -> None:
    """ Determine which conference has had the most wins in the last decade. """

    # Generate total wins over decade for each team and then add add conference analysis in code
    sql_statement = """
    SELECT COUNT(game_id),
        CASE
            WHEN @home_score > @away_score THEN home_team
            ELSE away_team
        END AS winning_team
    FROM games
    GROUP BY winning_team;
    """
    response = duckdb.sql(sql_statement).fetchall()

    # Add conference analysis in code with the help of our team cache
    conference_wins = {"East": 0, "West": 0}
    for record in response:
        team_win_total_decade, team_id = record
        team_conference = TEAM_CACHE[team_id][1]
        conference_wins[team_conference] = conference_wins[team_conference] + team_win_total_decade

    # Display the results
    if conference_wins["East"] > conference_wins["West"]:
        winner = "East"
        loser = "West"
    else:
        winner = "West"
        loser = "East"

    print(f"In the last decade, the {winner} conference had more wins with {conference_wins[winner]} total wins.")
    print(f"In the same time, the {loser} conference had less wins with {conference_wins[loser]} total wins.")


def detailed_game_analysis() -> None:
    """ Find the team with the highest margin of victory in the last decade. """

    sql_statement = """
    SELECT team, AVG(margin) as average_margin FROM (
        SELECT home_team as team, home_score-away_score AS margin
        FROM games
        UNION ALL
        SELECT away_team as team, away_score-home_score AS margin
        FROM games
    )
    GROUP BY team
    ORDER BY average_margin DESC
    LIMIT 1;
    """

    response = duckdb.sql(sql_statement).fetchall()
    team_id, margin = response[0]
    print(f"In the last decade, the team with the highest margin of victory is the {TEAM_CACHE[team_id][0]} with a per game margin of: {margin}")



def main():
    """
    Run through some basic tasks to interact with the NBA data
    """
    init_db_connection()

    cache_teams()

    # basic_extraction()

    # win_loss_records()

    # team_performance_by_season()

    # conference_analysis()

    detailed_game_analysis()


if __name__ == '__main__':
	main()