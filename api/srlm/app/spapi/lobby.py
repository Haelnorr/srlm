"""Functions to interface with the Lobby endpoints of the Slapshot Public API"""
from api.srlm.app.api.utils.functions import clean_data
from api.srlm.app.spapi import slap_api


# match results GET /api/public/games/{id} id from /matches

# create lobby POST /api/public/lobbies
def create_lobby(json):

    valid_fields = ['region', 'name', 'password', 'creator_name', 'is_periods', 'current_period', 'initial_stats',
                    'arena', 'mercy_rule', 'match_length', 'game_mode', 'initial_score']
    required_fields = ['region', 'name', 'password', 'creator_name']

    for field in required_fields:
        missing_fields = []
        if field not in json:

            missing_fields.append(field)
        if len(missing_fields) > 0:
            return f'Failed to create lobby - missing fields: {missing_fields}'

    cleaned_data = clean_data(json, valid_fields)

    response = slap_api.post('api/public/lobbies', cleaned_data)
    response_json = response.json()
    if response_json['success']:
        return response_json['lobby_id']
    else:
        return response_json


# get lobby info GET /api/public/lobbies/{id}
def get_lobby(lobby_id):
    response = slap_api.get(f'api/public/lobbies/{lobby_id}')
    return response


# get matches from lobby GET /api/public/lobbies/{id}/matches
def get_lobby_matches(lobby_id):
    response = slap_api.get(f'api/public/lobbies/{lobby_id}/matches')
    return response


# delete lobby DELETE /api/public/lobbies/{id}
def delete_lobby(lobby_id):
    response = slap_api.delete(f'api/public/lobbies/{lobby_id}')
    return response.status_code
