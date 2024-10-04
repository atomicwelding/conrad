from IEntity import *

class Projectile(IEntity):
    """
    Represents a generic projectile entity in the game.
    
    Parameters:
    -----------
    img_path : str
        The file path to the projectile's image.
    mass : float
        The mass of the projectile.
    rr : float
        Radial distance from the origin.
    rtheta : float
        Angular position in polar coordinates.
    rdot : float
        Radial velocity.
    thetadot : float
        Angular velocity.
    """

    def __init__(self, img_path, mass, rr, rtheta, rdot, thetadot):
        super().__init__(img_path=img_path, 
                         mass=mass, 
                         rr=rr, 
                         rtheta=rtheta, 
                         rdot=rdot, 
                         thetadot=thetadot)
