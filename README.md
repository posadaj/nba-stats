# Overview
An exploration of NBA stats


# Setup
### Fetch NBA Data
We get our data from [API-NBA](https://api-sports.io/documentation/nba/v2) and use `duckdb` to spin up a local database

First, grab an authentication key by following [these steps](https://api-sports.io/documentation/nba/v2#section/Authentication) and 
then run the setup script with your API Key to pull the relevant data:
```
python3 setup-db.py <API_KEY>
```
This script will pull NBA games and team data.


### Other Dependencies
To run the code, we just have a handful of dependencies that are assumed to be installed globally. We could also use a virtual environment like `pipenv` to manage these dependencies but these are widely used libraries so for simplicity, we asume they are available.


# Usage
Run the program by calling ... (TODO)

### Follow Ups
1. Data Cleanup 
 - NBA games per season is off. There should be 1230 games in a regular season, assuming 82 games per team and 30 teams. For some reason, these numbers are off.
 - NBA teams had a similar problem with a random team "Stephen A" but that was identified and removed in code.
2. Rate Limiting - Currently fails on fetching teams because of the 10 requests/minute limit.
