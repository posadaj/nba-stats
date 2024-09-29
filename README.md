# Overview
An exploration of NBA stats


# Setup
We get our data from [API-NBA](https://api-sports.io/documentation/nba/v2) and use `duckdb` to spin up a local database



1. First, grab an authentication key by following these steps:

https://api-sports.io/documentation/nba/v2#section/Authentication


You can install `duckdb` using `brew install duckdb`


To run the code, we just have a handful of dependencies that are assumed to be installed globally. We could also use a virtual environment like `pipenv` to manage these dependencies but these are widely used libraries so for simplicity, we asume they are available.

You could also run these commands to install `requests`:
```
python -m pip install requests
```


### TODO
1. Data Cleanup - There should be 1230 games in a regular season, assuming 82 games per team and 30 teams. For some reason, these numbers are off.
2. 
