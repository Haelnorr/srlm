### Current Version - 0.8.1
History:
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

Planned features:
- Manage finals fixtures
- Link user account to players
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

### Updating

The docker image is setup to avoid rebuilds on source code changes (except where changes to the docker environment have occurred).  
Unless explicitly specified, updating just requires pulling from the repo and restarting the docker image.

# Endpoints

For endpoint documentation access the /docs path in your browser