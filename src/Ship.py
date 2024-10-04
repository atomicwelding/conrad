from IEntity import IEntity
from HeavyProjectile import HeavyProjectile
from LightProjectile import LightProjectile
from params import *
import numpy as np

class Ship(IEntity):
    """
    Represents a ship that can shoot projectiles and detect collisions.
    
    Attributes:
    -----------
    nb_heavy_missile_left : int
        Number of heavy missiles left for the ship.
    nb_light_missile_left : int
        Number of light missiles left for the ship.
    """

    def __init__(self, img_path, mass, rr, rtheta, rdot, thetadot):
        super().__init__(img_path, mass, rr, rtheta, rdot, thetadot)
        self.nb_heavy_missile_left = NB_HEAVY_MISSILE
        self.nb_light_missile_left = NB_LIGHT_MISSILE

    def has_ammo(self):
        """Checks if the ship has any ammo left."""
        return bool(self.nb_heavy_missile_left) or bool(self.nb_light_missile_left)

    def shoot(self, angle, type_projectile):
        """
        Shoots a projectile from the ship at the given angle.
        
        Parameters:
        -----------
        angle : float
            The angle (in multiples of pi) to shoot the projectile.
        type_projectile : str
            Type of projectile to shoot ('heavy' or 'light').
        
        Returns:
        --------
        projectile : HeavyProjectile or LightProjectile
            The created projectile object.
        """
        angle_input = angle * np.pi 

        # Calculate projectile's initial position
        xprojectile = self.x() + 40 * np.cos(angle_input)
        yprojectile = self.y() + 40 * np.sin(angle_input)

        rr = np.sqrt(xprojectile**2 + yprojectile**2)
        rtheta = np.arctan2(yprojectile, xprojectile)

        # Determine the projectile's speed direction based on angle
        angle_input_mod = angle_input % (2 * np.pi)
        sign_speed_launching = -1 if angle_input_mod > np.pi else 1

        # Create projectile based on type
        if type_projectile == 'heavy':
            projectile = HeavyProjectile(beta * self.mass, rr, rtheta, sign=sign_speed_launching)
            self.nb_heavy_missile_left -= 1
        else:
            projectile = LightProjectile(gamma * self.mass, rr, rtheta, sign=sign_speed_launching)
            self.nb_light_missile_left -= 1

        return projectile

    def is_colliding_with(self, entity):
        """
        Checks for collision with another entity and handles the result.
        
        Parameters:
        -----------
        entity : IEntity
            The entity to check collision with.
        """
        pcolliding = super().is_colliding_with(entity)

        if pcolliding and isinstance(entity, LightProjectile):
            entity.palive = False
            self.palive = False

        if pcolliding and isinstance(entity, HeavyProjectile):
            self.assign_result_collisions(entity)

        if pcolliding and isinstance(entity, Ship):
            self.assign_result_collisions(entity)
