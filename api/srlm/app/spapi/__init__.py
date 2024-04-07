"""Package for interfacing with the Slapshot Public API"""

from api.srlm.app.spapi import config

slap_api = config.SlapAPI()

from api.srlm.app.spapi import slapid, lobby
