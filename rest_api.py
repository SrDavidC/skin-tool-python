from flask import Flask

import new_api as np

dict = {}

# Setup flask
app = Flask(__name__)


@app.route('/<id>')
def get_player_info(id):
    """
    Get player info from playerdb.py
    """
    return np.generate_player_skins(id)


# TODO: Add a route that can take a username and return skin property metadata using mineskin.org api
