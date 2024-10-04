from IEntity import *
from Player import Player
from Target import Target

class BlackHole(IEntity):
    """
    Represents a black hole entity in the game.
    
    Attributes:
    -----------
    R_S : float
        Schwarzschild radius of the black hole.
    """

    def __init__(self, mass=1., R_S=1.):
        super().__init__(img_path='black-hole.png',
                         mass=mass,
                         rr=0, rtheta=0,
                         rdot=0, thetadot=0)
        self.R_S = R_S

    def update(self, scene, radial_acceleration, dt):
        """
        Updates the black hole's state. Currently, no updates are needed as it is static.
        """
        pass

    def is_colliding_with(self, entity):
        """
        Checks if the black hole collides with another entity and handles the result.
        
        Parameters:
        -----------
        entity : IEntity
            The entity to check collision with.
        """
        pcolliding = super().is_colliding_with(entity)

        if pcolliding and isinstance(entity, IEntity):
            entity.palive = False
