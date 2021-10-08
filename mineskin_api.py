import os

import requests as rq

import playerdb as pdb
# Import to manipulate skins from users
import skin_generator_cv_tool as sgcv

# Get environemnt variables
API_KEY = os.environ.get('MINESKIN_API_KEY')
API_SECRET = os.environ.get('MINESKIN_API_SECRET')
# Some Constants
API_URL = "https://api.mineskin.org/"
GENERATE_UPLOAD = API_URL+'generate/upload/?key={}'.format(API_KEY)

# Headers for the requests
headers = {
    'Authorization': 'Bearer {}'.format(API_SECRET)
}

# A function that uploads a skin to mineskin.org


def upload_skin(username, file):
    user = pdb.get_player_info(username)
    if user['code'] == 'player.found':
        print('uuid:', user['data']['player']['id'])
    # Create the payload
    payload = {}
    files = [('file', ('image_upload.png', file, 'image/png'))]

    # Send the request
    r = rq.post(GENERATE_UPLOAD, data=payload, files=files, headers=headers)
    # Return the response
    return r.json()


print(upload_skin("sds", "sdsds"))
