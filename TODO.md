# TODO

**Before next PR**
 - ~~user password reset~~
 - ~~user password change~~
 - ~~app token reset~~
 - ~~remove all redundant code/templates~~
 - ~~permission and discord endpoints~~
 - steam account link functionality + endpoints
 - twitch account link functionality + endpoints
 - ~~document error codes and formats~~


**For next deployment**
 - set env variable 'SRLM_APP_NAME' and DOMAIN
 - change supervisor file for hypercorn - app moved from api.lds:asgi to api:asgi
 - ~~setup mail server~~
 - configure mail server to work with the app


**Future**
 - api endpoints (list incomplete)
   - league
   - division
   - season
   - player
   - team
   - player_team
   - free agent
   - match + match_result
   - final + final_result
   - lobby stuff
   - match_data stuff
   - scheduling
   - awards
   - logging
 - get slapid and create/link player from steam account  
 - integration with Slapshot Public API for lobby creation and retrieving match data
 - document code
 - document endpoints
 - document features
 - confirm user email

**Completed**
 - database models implemented
 - database built
 - user endpoints
 - permission endpoints
 - token authentication system
 - asgi support for hypercorn