# TODO

**Before next PR**
 - ~~matches & lobbies~~
   - ~~create and view matches~~
   - ~~get match results~~
   - ~~update match & match results~~
   - ~~lobby creation and monitoring~~
   - ~~match_stats retrieval~~
   - ~~match data validation~~
   - ~~match review system~~
 - ~~integration with Slapshot Public API for lobby creation and retrieving match data~~
 - match_data stuff (including legacy)
 - import legacy match data
 - ~~api endpoints~~
   - ~~match review~~
   - ~~lobby creation and details~~
   - ~~reporting system~~
 - ~~get slapid and create/link player from steamID~~
 - ~~APIFairy~~

**Future**
 - api endpoints (list incomplete)
   - final + final_result
   - scheduling + view fixtures
   - awards
 - confirm user email
 - caching support
 - route cooldowns?
 - setup mysql in docker
 - web relay for discord bot notifications

**Completed**
 - database models implemented
 - database built
 - token authentication system
 - asgi support for hypercorn
 - user password reset
 - user password change
 - app token reset
 - remove all redundant code/templates
 - permission and discord endpoints
 - twitch account database support and endpoints
 - document error codes and formats
 - api endpoints
   - user
   - permission
   - league
   - division
   - season
   - season_division
   - player
   - team
   - player_team
   - free agent