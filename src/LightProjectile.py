from Projectile import Projectile

class LightProjectile(Projectile):
    """
    Represents a light projectile with a higher speed compared to heavy projectiles.
    
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
        super().__init__(img_path='light-projectile.png',
                         mass=mass,
                         rr=rr,
                         rtheta=rtheta,
                         rdot=0,
                         thetadot=sign * 40 / rr)


    def is_colliding_with(self, entity):
        pcolliding = super().is_colliding_with(entity)


        if(pcolliding and isinstance(entity, LightProjectile)):
            self.palive = False
            entity.palive = False
