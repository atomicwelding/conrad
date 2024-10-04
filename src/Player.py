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
            angle_input = state_manager.get('playerShotAngle')
            type_projectile = state_manager.get('playerShotType')

            state_manager.set('playerShot', False)
            state_manager.set('playerShotType', None)
            state_manager.set('playerShotAngle', None)
            
            return self.shoot(angle_input, type_projectile)
        return None
        
