# TODO

**Before next PR**
 - api endpoints
   - ~~league~~
   - ~~division~~
   - ~~season~~
   - player
   - team
   - player_team
   - free agent
 - convert all old routes (users/permissions) to using new helper functions 
 - change responses of POST/PUT (users/permissions) functions to new format (success code + link)


**For next deployment**
 - fix mail server (SPF records, certificate, hostnames - no idea tbh)


**Future**
 - api endpoints (list incomplete)
   - match + match_result
   - final + final_result
   - lobby stuff
   - match_data stuff
   - scheduling
   - awards
   - logging
 - get slapid and create/link player from steamID
 - integration with Slapshot Public API for lobby creation and retrieving match data
 - confirm user email

**Completed**
 - database models implemented
 - database built
 - user endpoints
 - permission endpoints
 - token authentication system
 - asgi support for hypercorn
 - user password reset
 - user password change
 - app token reset
 - remove all redundant code/templates
 - permission and discord endpoints
 - twitch account database support and endpoints
 - document error codes and formats