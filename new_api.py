import base64
import subprocess
import urllib.request as urllib

import cv2
import numpy as np
import requests as rq
import wget

from SkinMask import SkinMask

# Ashcon API url. Used for skins and stuff
ASHCON_APP = 'https://api.ashcon.app/mojang/v2/user/{}'

# Constant skin files.
TUXEDO_SKIN = SkinMask(skin='nSkins/SquidGame_Tuxedo_Classic.png',
                       skin_mask='nSkins/SquidGame_Mask_Tuxedo_Classic.png',
                       skin_slim='nSkins/SquidGame_Tuxedo_Slim.png',
                       skin_slim_mask='nSkins/SquidGame_Mask_Tuxedo_Slim.png')
GUARD_SKIN = SkinMask(skin='nSkins/SquidGame_Guardia_Classic.png',
                      skin_mask='nSkins/SquidGame_Mask_Guardia_Classic.png',
                      skin_slim='nSkins/SquidGame_Guardia_Slim.png',
                      skin_slim_mask='nSkins/SquidGame_Mask_Guardia_Slim.png')
PARTICIPANT_SKIN = SkinMask(
    skin='nSkins/SquidGame_Participant_Classic.png',
    skin_mask='nSkins/SquidGame_Mask_Participant_Classic.png',
    skin_slim='nSkins/SquidGame_Participant_Slim.png',
    skin_slim_mask='nSkins/SquidGame_Mask_Participant_Slim.png')
CIVIL_SKIN = SkinMask(skin='nSkins/SquidGame_Civil_Classic.png',
                      skin_mask='nSkins/SquidGame_Mask_Classic.png',
                      skin_slim='nSkins/SquidGame_Civil_Slim.png',
                      skin_slim_mask='nSkins/SquidGame_Mask_Slim.png')


def get_player_data(player_id):
    """
    Get player's skin data from Ashcon API. It also converts old skin formats to new ones automagickally.
    """
    # Format the url to query the skin
    url = ASHCON_APP.format(player_id)
    # Get the data
    response = rq.get(url)
    # Parse as json
    data = response.json()
    # If data not null keep going
    if data:
        # Get the properties object
        properties = data['textures']
        # If it's slim, do a different logic
        slim = properties['slim']

        # Get the skin url
        skin_url = properties['skin']['url']
        # Get the actual skin image from mojang
        resp = urllib.urlopen(skin_url)
        # Decode image into numpy array for opencv
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_UNCHANGED)

        # Get dimensions to determine if  format of skin (64x32) or (64x64)
        height, _, _ = image.shape

        # If height is 32, then old format
        if height == 32:
            #If height is 32, use magick to conver to correct modern format.
            target = 'temp/{}.png'.format(player_id)
            # Download the skin from the url and save in temp folder
            wget.download(skin_url, out=target)
            # Call magick function to convert to modern format
            magickFunction(target)
            # Delete the temp file
            deleteFile(target)
            # Store the file location to use for skin transformations
            converted = 'temp/{}_converted.png'.format(player_id)

            image = cv2.imread(converted, cv2.IMREAD_UNCHANGED)
        # Return duple of skin image and wether it is slim texture or not
        return image, slim


def apply_mask_to_skin(skin, mask):
    """ Apply a mask and perform a bitwise_and operation """
    return cv2.bitwise_and(skin, skin, mask=mask)


def generate_player_skins(player_id):
    """ Generate all skins for a player and returns them in a dict encoded in base64. """
    image, isSlim = get_player_data(player_id)
    # If it's slim, use the slim skin
    # Get the features to use with Civilian, Participant, and Guard skins
    guard_features = apply_mask_to_skin(
        image,
        cv2.imread(
            CIVIL_SKIN.skin_slim_mask if isSlim else CIVIL_SKIN.skin_mask, 0))
    participant_features = apply_mask_to_skin(
        image,
        cv2.imread(
            PARTICIPANT_SKIN.skin_slim_mask
            if isSlim else PARTICIPANT_SKIN.skin_mask, 0))
    civilian_features = apply_mask_to_skin(
        image,
        cv2.imread(
            CIVIL_SKIN.skin_slim_mask if isSlim else CIVIL_SKIN.skin_mask, 0))
    # Get mask and features for tuxedo skin
    tuxMask = cv2.imread(
        TUXEDO_SKIN.skin_slim_mask if isSlim else TUXEDO_SKIN.skin_mask, 0)
    tuxFeatures = apply_mask_to_skin(image, tuxMask)

    # Create all the skins.
    guard = cv2.add(
        guard_features,
        cv2.imread(GUARD_SKIN.skin_slim if isSlim else GUARD_SKIN.skin,
                   cv2.IMREAD_UNCHANGED))
    participant = cv2.add(
        participant_features,
        cv2.imread(
            PARTICIPANT_SKIN.skin_slim if isSlim else PARTICIPANT_SKIN.skin,
            cv2.IMREAD_UNCHANGED))
    civilian = cv2.add(
        civilian_features,
        cv2.imread(CIVIL_SKIN.skin_slim if isSlim else CIVIL_SKIN.skin,
                   cv2.IMREAD_UNCHANGED))

    tux = cv2.add(
        tuxFeatures,
        cv2.imread(TUXEDO_SKIN.skin_slim if isSlim else TUXEDO_SKIN.skin,
                   cv2.IMREAD_UNCHANGED))
    # Encode all skins to base64 and put in dict to return as json
    dict = {
        'slim': isSlim,
        'data': {
            'guard': encode_skin_base64(guard),
            'participant': encode_skin_base64(participant),
            'civilian': encode_skin_base64(civilian),
            'tux': encode_skin_base64(tux)
        }
    }

    return dict


def encode_skin_base64(skin):
    """ Encode a skin into base64 """
    return base64.b64encode(cv2.imencode('.png', skin)[1]).decode('utf-8')


def magickFunction(fileName):
    """ Calls a bash script operation that uses magick to convert a given skin file from 64x32 to 64x64 """
    subprocess.call(['bash', 'magickTransformer.sh', fileName])


def deleteFile(fileName):
    subprocess.call(['rm', fileName])
