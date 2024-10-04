from Projectile import Projectile



class LightProjectile(Projectile):

    def __init__(self, mass, rr, rtheta, sign = 1):
        super().__init__(img_path = 'light-projectile.png',
                         mass = mass,
                         rr = rr,
                         rtheta = rtheta,
                         rdot = 0,
                         thetadot = sign * 40 / rr)
