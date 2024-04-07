"""Function to interface with the SteamID endpoint """

from api.srlm.app.spapi import slap_api


def get_slap_id(steam_id):
    endpoint = f'api/public/players/steam/{steam_id}'
    response = slap_api.get(endpoint)
    return response
