# TODO

**Before next PR**
 - user password reset
 - user password change
 - app token reset
 - remove all redundant code/templates (only app/auth/routes.py remains)
 - permission and discord endpoints
 - steam account link functionality + endpoints
 - twitch account link functionality + endpoints


**For next deployment**
 - set env variable 'SRLM_APP_NAME'
 - change supervisor file for hypercorn - app moved from api.lds:asgi to api:asgi


**Future**
 - api endpoints for retrieving data
 - api endpoints for adding data
 - api endpoints for modifying data

 - integration with Slapshot Public API for lobby creation and retrieving match data
 - document code
 - document endpoints
 - document features