from IEntity import *

class Ship(IEntity):
    def __init__(self, img_path, mass, rr, rtheta, rdot, thetadot):
        super().__init__(img_path, mass, rr, rtheta, rdot, thetadot)
        
        self.nb_heavy_missile_left = 1
        self.nb_light_missile_left = 1
