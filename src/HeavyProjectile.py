from Projectile import Projectile
from LightProjectile import LightProjectile

import numpy as np 


class HeavyProjectile(Projectile):

    def __init__(self, mass, rr, rtheta, sign = 1):
        super().__init__(img_path = 'heavy-projectile.png',
                         mass = mass,
                         rr = rr,
                         rtheta = rtheta,
                         rdot = 0,
                         thetadot = sign * 12 / rr)


        
    def is_colliding_with(self, entity):
        pcolliding = super().is_colliding_with(entity)

        if(pcolliding and isinstance(entity, HeavyProjectile)):
           self.assign_result_collisions(entity)

        if(pcolliding and isinstance(entity, LightProjectile)):
            self.assign_result_collisions(entity)
 
