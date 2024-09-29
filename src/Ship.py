from IEntity import *

class Ship(IEntity):
    def __init__(self, mass = 1., rr = 0., rtheta = 0., rdot = 0., thetadot = 0.):
        super().__init__(img_path = None, mass, rr, rtheta, rdot, thetadot)
        
        self.nb_heavy_missile_left = 1
        self.nb_light_missile_left = 1

    def draw(self):
        pass

    def is_colliding(self):
        pass 
