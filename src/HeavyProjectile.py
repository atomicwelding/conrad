from Projectile import Projectile
import numpy as np 


class HeavyProjectile(Projectile):

    def __init__(self, mass, rr, rtheta, sign = 1):
        super().__init__(img_path = 'heavy-projectile.png',
                         mass = mass,
                         rr = rr,
                         rtheta = rtheta,
                         rdot = 0,
                         thetadot = sign *  12. / rr)
