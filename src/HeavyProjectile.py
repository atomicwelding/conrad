from Projectile import Projectile


class HeavyProjectile(Projectile):

    def __init__(self, mass, rr, rtheta):
        super().__init__(img_path = 'heavy-projectile.png',
                         mass = mass,
                         rr = rr,
                         rtheta = rtheta,
                         rdot = 0,
                         thetadot = +20. / rr)
