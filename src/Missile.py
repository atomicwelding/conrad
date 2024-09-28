from IEntity import *

class Missile(IEntity):
    def __init__(self, mass = 1., rr = 0., rtheta = 0., rdot = 0., thetadot = 0.):
        super().__init__(mass,rr,rtheta,rdot,thetadot)

    def draw(self):
        raise NotImplementedError
