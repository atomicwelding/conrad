from Ship import *
from params import *

import numpy as np


class Player(Ship):
    
    def __init__(self, mass, rr, rdot, thetadot):
        super().__init__(img_path = 'placeholder_player.png',
                         mass = mass, rr = rr, rtheta = 0, rdot = rdot, thetadot = thetadot)

        self.isPlayer = True

    def handle_shoot_state(self, state_manager):
        state_manager.set('playerCanShootHeavy', self.nb_heavy_missile_left > 0)
        state_manager.set('playerCanShootLight', self.nb_light_missile_left > 0)
        
        if(state_manager.get('playerShot')):
            k = 1
            if(self.rtheta > -np.pi/2 and self.rtheta < np.pi / 2):
                k = -1
            angle_input = - state_manager.get('playerShotAngle') * np.pi
            sign = k * ( -1 if angle_input % (2*np.pi) <= np.pi else 1)


            # Calculate the projectile's initial position relative to the player's current position and angle_input
            xprojectile = self.x() + 40  * np.cos(self.rtheta + angle_input)
            yprojectile = self.y() + 40  * np.sin(self.rtheta + angle_input)

            # Convert the new projectile position back to polar coordinates for the game's system
            rr = np.sqrt(xprojectile**2 + yprojectile**2)
            rtheta = np.atan2(yprojectile, xprojectile)
            
            type_projectile = state_manager.get('playerShotType')
            
            if(type_projectile == 'heavy'):
                projectile = HeavyProjectile(beta*self.mass, rr, rtheta, sign = sign)
                self.nb_heavy_missile_left -= 1
            else:
                projectile = LightProjectile(gamma*self.mass, rr, rtheta, sign = sign)
                self.nb_light_missile_left -= 1

            state_manager.set('playerShot', False)
            state_manager.set('playerShotType', None)
            state_manager.set('playerShotAngle', None)

            return projectile
        return None
        
