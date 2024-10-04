from Ship import Ship
from IEntity import IEntity
import numpy as np 

class Target(Ship):
    """
    Represents the target in the game, controlled by AI, with the ability to shoot projectiles at random intervals.
    
    Attributes:
    -----------
    canShoot : bool
        Determines whether the target is allowed to shoot in the current turn.
    """

    def __init__(self, mass, rr, rdot, thetadot):
        super().__init__(img_path='placeholder_target.png',
                         mass=mass, rr=rr, rtheta=np.pi, rdot=rdot, thetadot=thetadot)
        self.canShoot = False

    def random_shoot(self):
        """
        Determines if the target should shoot based on a random probability and whether it has ammo.
        
        Returns:
        --------
        projectile : HeavyProjectile or LightProjectile or None
            Returns the fired projectile if shooting, otherwise None.
        """
        should_shoot = np.random.choice([True, False], p=[1/1_000, 1 - 1/1_000])

        if not self.canShoot or (not self.has_ammo() and not should_shoot):
            return None 

        # Randomly choose an angle and projectile type
        angles = [0, 0.5, 1, 1.5]
        angle = np.random.choice(angles)

        types_missile = ['heavy', 'light']
        used_type = np.random.choice(types_missile)

        # Check if the target has enough ammo for the selected projectile
        if (used_type == 'heavy' and not (self.nb_heavy_missile_left > 0)) or \
           (used_type == 'light' and not (self.nb_light_missile_left > 0)):
            return None

        return self.shoot(angle, used_type)
