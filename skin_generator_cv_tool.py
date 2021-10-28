import cv2

# Import some constants
SKIN_PARTICIPANT = cv2.imread(
    'images/SquidGame_Participant_Classic.png', cv2.IMREAD_UNCHANGED)
SKIN_GUARD = cv2.imread(
    'images/SquidGame_Guardia_Classic.png', cv2.IMREAD_UNCHANGED)
SKIN_HOODIE = cv2.imread(
    'images/SquidGame_Guardia_Classic.png', cv2.IMREAD_UNCHANGED)
# Import the body mask with color scale 0 to turn into simple mask
SKIN_FEATURES_MASK = cv2.imread('masks/full_body_mask.png', 0)


def get_saved_skin(name):
    return cv2.imread(name, cv2.IMREAD_UNCHANGED)


def get_guard_for_skin(skin):
    # Get the relevant skin features
    features = get_skin_features(skin)
    # Add it to the guard skin
    return cv2.add(SKIN_GUARD, features)


def get_participant_for_skin(skin):
    # Get the relevant skin features
    features = get_skin_features(skin)
    # Add it to the participant skin
    return cv2.add(SKIN_PARTICIPANT, features)

def get_hoodie_for_skin(skin):
    # Get the relevant skin features
    features = get_skin_features(skin)
    # Add it to the participant skin
    return cv2.add(SKIN_PARTICIPANT, features)


def get_skin_features(skin):
    return cv2.bitwise_and(skin, skin, mask=SKIN_FEATURES_MASK)


def save_skin(name, skin):
    cv2.imwrite(name, skin)


def demo():
    """
    This function is used to test the skin generator. It opens a GUI with the skin item data that will get pasted in the other two skins.
    """
    # Load the skin
    skin = cv2.imread('images/b67edaf8bfe6df63.png', cv2.IMREAD_UNCHANGED)
    # Get the player's skin as a guard
    body_guard_skinned = get_guard_for_skin(skin)
    # Get the player's skin as a participant
    body_participant_skinned = get_participant_for_skin(skin)

    # Show the skins in the screen.
    cv2.imshow('Guard', body_guard_skinned)
    cv2.imshow('Participant', body_participant_skinned)

    # Output images
    cv2.imwrite('output/out_guard.png', body_guard_skinned)
    cv2.imwrite('output/out_participant.png', body_participant_skinned)
    # Exit
    cv2.waitKey(0)
    cv2.destroyAllWindows()
