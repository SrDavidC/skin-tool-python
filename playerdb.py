import requests as rq


def get_player_info(player_id):
    """
    Get player info from the API
    """
    url = 'https://playerdb.co/api/player/minecraft/{}'.format(player_id)
    response = rq.get(url)
    return response.json()


mineskin_url = "https://api.mineskin.org/generate/upload/?key=67338dcbf1c640fdd09bdd6e40167504345543eb8e85584c0801252f36cf1844"
# Make a function that
