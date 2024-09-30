## Overview
An exploration of NBA stats

## Setup

### Install Dependencies
There are just a few dependencies in this project so instead of creating a virtual environment, let's quickly install
the dependencies globally. Note that we assume you have python3 and pip3 on your machine.
```
pip3 install requests
pip3 install duckdb
pip3 install dash
pip3 install pandas
```

### Fetch NBA Data
We get our data from [API-NBA](https://api-sports.io/documentation/nba/v2) and use `duckdb` to spin up a local database

First, grab an authentication key by following [these steps](https://api-sports.io/documentation/nba/v2#section/Authentication) and 
then run the setup script with your API Key to pull the relevant data:
```
python3 setup-db.py <API_KEY>
```
This script will pull NBA games and team data.

# Usage
Run the program by calling
```
python3 main.py
```
This will run the final task to display team performance over time and spin up a 
local server to display the results using plotly. Navigate to the URL (http://127.0.0.1:8050) after running
the above command to see the results visually.

### Follow Ups
1. Data Cleanup
 - NBA games per season is off. There should be 1230 games in a regular season, assuming 82 games per team and 30 teams. For some reason, these numbers are off.
 - NBA teams had a similar problem with a random team "Stephen A" but that was identified and removed in code.
2. Rate Limiting - Currently fails on fetching teams because of the 10 requests/minute limit.
3. Pretty print the team_id (add in team names and date instead of ID)
