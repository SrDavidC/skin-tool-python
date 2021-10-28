# Import request and flask for api related functions
import requests as rq
from flask import Flask

import mineskin_api as ms
import playerdb as pdb
# Import to manipulate skins from users
import skin_generator_cv_tool as sgcv

dict = {}

# Setup flask
app = Flask(__name__)


@app.route('/<id>')
def get_player_info(id):
    """
    Get player info from playerdb.py
    """

    if id in dict:
        return dict[id]
    else:
        res = ms.upload_skin(id)
        dict[id] = res
        return res


# TODO: Add a route that can take a username and return skin property metadata using mineskin.org api
