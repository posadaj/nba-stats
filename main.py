import duckdb


def init_db_connection():
    duckdb.sql("CREATE TABLE games AS FROM 'db/games.json';")
    duckdb.sql("CREATE TABLE teams AS FROM 'db/teams.json';")
    print("Read games and teams tables into duckdb")



def basic_extraction():
    """ Retrieve the top 10 highest-scoring games in the last decade. """

    sql_statement = """
    SELECT game_id, home_score + away_score as total_score
    FROM games
    WHERE season >= 2014 AND season <= 2024
    ORDER BY total_score DESC
    LIMIT 10
    """

    # sql_statement = "SELECT id FROM games LIMIT 10"
    response = duckdb.sql(sql_statement).fetchall()
    print("Printing the top 10 highest-scoring games in the last decade")
    for index in range(len(response)):
        game_id, total_score = response[index]
        print(f"The #{index+1} highest-scoring game had a total score of {total_score} and game_id {game_id}")


def main():
    """
    Run through some basic tasks to interact with the NBA data
    """
    init_db_connection()

    basic_extraction()


if __name__ == '__main__':
	main()