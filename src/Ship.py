from IEntity import IEntity
from HeavyProjectile import HeavyProjectile
from LightProjectile import LightProjectile

from params import *

import numpy as np


class Ship(IEntity):
    def __init__(self, img_path, mass, rr, rtheta, rdot, thetadot):
        super().__init__(img_path, mass, rr, rtheta, rdot, thetadot)
        
        self.nb_heavy_missile_left = NB_HEAVY_MISSILE
        self.nb_light_missile_left = NB_LIGHT_MISSILE

    def has_ammo(self):
        return bool(self.nb_heavy_missile_left) or  bool(self.nb_light_missile_left)

    def shoot(self, angle, type_projectile):
        
        angle_input = angle * np.pi 

        # Calculate the projectile's initial position relative to the player's current position and angle_input
        xprojectile = self.x() + 40 * np.cos(angle_input)  # angle is now relative to traditional x,y axes
        yprojectile = self.y() + 40 * np.sin(angle_input)
        

        rr = np.sqrt(xprojectile**2 + yprojectile**2)
        rtheta = np.arctan2(yprojectile, xprojectile)

        

        # Determine the sign for the projectile's direction based on the angle
        angle_input_mod = angle_input % (2*np.pi)
        sign_speed_launching = -1 if (angle_input_mod > np.pi) else 1
        
        # Create the projectile and adjust ammo count
        if type_projectile == 'heavy':
            projectile = HeavyProjectile(beta * self.mass, rr, rtheta, sign = sign_speed_launching)
            self.nb_heavy_missile_left -= 1
        else:
            projectile = LightProjectile(gamma * self.mass, rr, rtheta, sign = sign_speed_launching)
            self.nb_light_missile_left -= 1

        return projectile
    
        
    def is_colliding_with(self, entity):
        pcolliding = super().is_colliding_with(entity)

        if(pcolliding and isinstance(entity, LightProjectile)):
           entity.palive = False
           self.palive = False

        if(pcolliding and isinstance(entity, HeavyProjectile)):
           self.assign_result_collisions(entity)

        if(pcolliding and isinstance(entity, Ship)):
            self.assign_result_collisions(entity)
