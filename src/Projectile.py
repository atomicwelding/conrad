from IEntity import *

class Projectile(IEntity):
    def __init__(self, img_path , mass, rr, rtheta, rdot, thetadot):
        super().__init__(img_path = img_path,
                         mass = mass, rr = rr, rtheta = rtheta, rdot = rdot, thetadot = thetadot)
