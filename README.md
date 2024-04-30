### Current Version - 0.8.14
History:
 - 0.8.14 - Added support for PostgreSQL (requires docker rebuild)
 - 0.8.13 - Expanded database and routes to handle teams, registrations and invites
 - 0.8.12 - Added leaderboard for season_division
 - 0.8.11 - Added some routes for easier permission management
 - 0.8.10 - Added better error messages for field validation
 - 0.8.9 - Modified user validate route to check permissions
 - 0.8.8 - Changes to get_match_stats
 - 0.8.7 - Changed MySQL Version to 8.0.36
 - 0.8.6 - Added endpoint for uploading match data from logs
 - 0.8.5 - Modified discord auth to work with frontend
 - 0.8.4 - Added list of players to season_division/teams lookup
 - 0.8.3 - Added better search functionality for Seasons and SeasonDivisions
 - 0.8.2 - Added support for Discord Auth (requires docker rebuild)
 - 0.8.1 - Updates to seasons endpoints

# Overview

This project is a database and API tool designed to help store data and manage the competitive leagues for the
Slapshot: Rebound Community.
The desired goal for the project is to have a complete tool for all the different leagues (OSL, SPL, EUSL) to have a
single, uniform database and API toolbox to track matches, teams, players and stats, as well as provide historical data
that has been ported over from the spreadsheet days.
As this is being built as a REST API, the idea is that it will be able to be used by multiple front-end websites or discord bots
so can be easily integrating into the existing community sites/projects.

Currently, the list of features is:
- Manage Leagues (i.e. regions)
- Manage Seasons and Divisions
- Manage Players and Teams
- Create matches between teams (linked to a season)
- Create lobbies for matches
- Automatic stat retrieval for lobbies
- Automatic stat validation
- User registration
- Match review system
- Link user account to players

Planned features:
- Manage finals fixtures
- Awards
- Match scheduling
- Web relay for discord notification/news bots

# Installation

### Initial Install

This project is dockerized. To get up and running, first clone the repo.  
Create a file inside the cloned repo at `.envfiles/.dev-env`.  
The following environment variables must be set:
<pre>
SECRET_KEY=somesecretkey-canbeanything
LOG_DIR=/var/log/srlm
MYSQL_USER=app
MYSQL_PASS=631a7yXL6&lt;km
MYSQL_HOST=db
MYSQL_PORT=3306
SLAP_API_KEY={api key provided by Oddshot}
SLAP_API_URL=https://staging.slapshot.gg/
REDIS_HOST=redis
REDIS_PORT=6379
</pre>

Run the command `docker compose up --build` to start the image. 

### Updating

The docker image is setup to avoid rebuilds on source code changes (except where changes to the docker environment have occurred).  
Unless explicitly specified, updating just requires pulling from the repo and restarting the docker image.  
Note: where an image rebuild is needed, you may have to run `docker compose down` and re-run `docker compose up`, otherwise the MySQL DB may persist and cause issues.

# Usage / Endpoints
API will go live on port 8000. (http://localhost:8000)  
For endpoint documentation access the [/docs](http://localhost:8000/docs) path in your browser 
