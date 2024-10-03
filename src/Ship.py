from IEntity import IEntity
from HeavyProjectile import HeavyProjectile
from LightProjectile import LightProjectile


class Ship(IEntity):
    def __init__(self, img_path, mass, rr, rtheta, rdot, thetadot):
        super().__init__(img_path, mass, rr, rtheta, rdot, thetadot)
        
        self.nb_heavy_missile_left = 5
        self.nb_light_missile_left = 3
       

    def is_colliding_with(self, entity):
        pcolliding = super().is_colliding_with(entity)

        if(pcolliding and isinstance(entity, LightProjectile)):
           entity.palive = False
           self.palive = False

        if(pcolliding and isinstance(entity, HeavyProjectile)):
           self.assign_result_collisions(entity)

        #if(pcolliding and entity.isPlayer):
            #self.assign_result_collisions(entity)
