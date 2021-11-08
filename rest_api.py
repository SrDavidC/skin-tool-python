from flask import Flask

import new_api as np

dict = {}

# Setup flask
app = Flask(__name__)


@app.route('/<id>')
def get_player_info(id):
    """
    Get all the data from our utility functions from new_api
    """
    return np.generate_player_skins(id)
