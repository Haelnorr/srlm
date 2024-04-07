"""Welcome to the Slapshot: Rebound League Manager API

## Overview

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

Planned features:
 - Match review system
 - Manage finals fixtures
 - Link user account to players
 - Awards
 - Match scheduling
 - Web relay for discord notification/news bots



"""


import api.srlm

from api.srlm import asgi, celery
