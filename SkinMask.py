# A class designed to hold a skin and it's masks including the slim variants.
class SkinMask:
    # Parameters normal
    skin = ""
    skin_mask = ""
    # Paramters slim
    skin_slim = ""
    skin_slim_mask = ""

    # Constructor
    def __init__(self, skin, skin_mask, skin_slim, skin_slim_mask):
        self.skin = skin
        self.skin_mask = skin_mask
        self.skin_slim = skin_slim
        self.skin_slim_mask = skin_slim_mask
