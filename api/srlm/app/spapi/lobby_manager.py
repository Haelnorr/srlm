
def lobby_manager(match_id, lobby_settings):
    # get the details for creating a new lobby (match_id, password)
    # generate the password

    # create a new lobby with the slap API

    # create a lobby object in the database and store the lobby_id, match_id and password

    # start monitoring the lobby

    # check after 2 minutes + match_length
    # check every match_length for status
    # if (periods_enabled is "True" and current_period >= 4) or (periods_enabled is "False" and current_period is 2) and in_game=false
    # request match stats from api
    # if completed, destroy lobby, mark match as completed


    pass


def get_match_stats(lobby_id):
    # check match stats for correct number of valid periods
    # save each period into match_data, player_match_data and team_match_data
    # flag any potential issues or conflicts
    # if match data is valid and complete, send signal to lobby manager to destroy lobby
    pass