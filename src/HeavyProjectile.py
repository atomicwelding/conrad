from Projectile import Projectile
from LightProjectile import LightProjectile
import numpy as np 

class HeavyProjectile(Projectile):
    """
    Represents a heavy projectile with a specific speed and direction.
    
    Parameters:
    -----------
    mass : float
        The mass of the projectile.
    rr : float
        Radial distance from the origin.
    rtheta : float
        Angular position in polar coordinates.
    sign : int, optional
        Direction of the projectile's velocity (1 for positive, -1 for negative), default is 1.
    """

    def __init__(self, mass, rr, rtheta, sign=1):
        super().__init__(img_path='heavy-projectile.png',
                         mass=mass,
                         rr=rr,
                         rtheta=rtheta,
                         rdot=0,
                         thetadot=sign * 12 / rr)

    def is_colliding_with(self, entity):
        """
        Handles collisions with other projectiles, either heavy or light.
        
        Parameters:
        -----------
        entity : IEntity
            The entity to check collision with.
        """
        pcolliding = super().is_colliding_with(entity)

        if pcolliding and isinstance(entity, HeavyProjectile):
            self.assign_result_collisions(entity)

        if pcolliding and isinstance(entity, LightProjectile):
            self.assign_result_collisions(entity)
