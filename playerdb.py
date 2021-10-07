import requests as rq

def get_player_info(player_id):
    """
    Get player info from the API
    """
    url = 'https://playerdb.co/api/player/minecraft/{}'.format(player_id)
    response = rq.get(url)
    return response.json()