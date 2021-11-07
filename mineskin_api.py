import os
import time

import cv2
import requests as rq

import playerdb as pdb
# Import to manipulate skins from users
import skin_generator_cv_tool as sgcv

# Get environemnt variables
API_KEY = os.environ.get('MINESKIN_API_KEY')
API_SECRET = os.environ.get('MINESKIN_API_SECRET')
# Some Constants
API_URL = "https://api.mineskin.org/"
GENERATE_UPLOAD = API_URL + 'generate/upload/?key={}'.format(API_KEY)
GENERATE_USER = API_URL + 'generate/user/?key={}'.format(API_KEY)

# Headers for the requests
headers = {'Authorization': 'Bearer {}'.format(API_SECRET)}


def generate_skin(uuid):
    """
    Generates a skin from a uuid
    """
    print(uuid)
    # Create the payload
    payload = {"uuid": uuid}
    # Send the request
    r = rq.post(GENERATE_USER, data=payload, headers=headers)
    # Return the response
    return r.json()


def upload_skin(username):
    """
    Uploads a skin to mineskin.org
    """
    user = pdb.get_player_info(username)
    if user['code'] != 'player.found':
        return

    # Now use the uuid
    uuid = user['data']['player']['id']
    # Generate skin
    skin = generate_skin(uuid)

    skin_url = skin['data']['texture']['url']
    # Download the skins
    img_data = rq.get(skin_url).content
    file_name = 'skins/{}.png'.format(uuid)
    with open(file_name, 'wb') as handler:
        handler.write(img_data)

    # Create the skins
    actual_skin = cv2.imread(file_name, cv2.IMREAD_UNCHANGED)
    guard_skin = sgcv.get_guard_for_skin(actual_skin)
    participant_skin = sgcv.get_participant_for_skin(actual_skin)

    guard_file_name = 'output/{}_guard.png'.format(uuid)
    participant_file_name = 'output/{}_participant.png'.format(uuid)

    sgcv.save_skin(guard_file_name, guard_skin)
    sgcv.save_skin(participant_file_name, participant_skin)

    # Create the payload
    payload = {}

    # Send the request
    time.sleep(5)
    r = rq.post(GENERATE_UPLOAD,
                data=payload,
                files={"file": open(guard_file_name, 'rb')},
                headers=headers)
    time.sleep(5)
    r2 = rq.post(GENERATE_UPLOAD,
                 data=payload,
                 files={"file": open(participant_file_name, 'rb')},
                 headers=headers)
    # Return the response
    return {"guard": r.json(), "not_guard": r2.json()}


# print(upload_skin("jcedeno"))
