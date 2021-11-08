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
                      skin_mask='nSkins/SquidGame_Mask_Classic.png',
                      skin_slim='nSkins/SquidGame_Guardia_Slim.png',
                      skin_slim_mask='nSkins/SquidGame_Mask_Slim.png')
PARTICIPANT_SKIN = SkinMask(skin='nSkins/SquidGame_Participant_Classic.png',
                            skin_mask='nSkins/SquidGame_Mask_Classic.png',
                            skin_slim='nSkins/SquidGame_Participant_Slim.png',
                            skin_slim_mask='nSkins/SquidGame_Mask_Slim.png')
CIVIL_SKIN = SkinMask(skin='nSkins/SquidGame_Civil_Classic.png',
                      skin_mask='nSkins/SquidGame_Mask_Classic.png',
                      skin_slim='nSkins/SquidGame_Civil_Slim.png',
                      skin_slim_mask='nSkins/SquidGame_Mask_Slim.png')


def get_player_data(player_id):
    """
    Get player data from Ashcon API.
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
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)

        # Get dimensions to determine if  format of skin (64x32) or (64x64)
        height, width, _ = image.shape

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

        else:
            print('New format')

        # Return duple of skin image and wether it is slim texture or not
        return image, slim


def magickFunction(fileName):
    """ Calls a bash script operation that uses magick to convert a given skin file from 64x32 to 64x64 """
    subprocess.call(['bash', 'script', fileName])


def deleteFile(fileName):
    subprocess.call(['rm', fileName])


get_player_data('ElRichMC')
