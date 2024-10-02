from Ship import *





class Player(Ship):
    
    def __init__(self, mass, rr, rdot, thetadot):
        super().__init__(img_path = 'placeholder_player.png',
                         mass = mass, rr = rr, rtheta = 0, rdot = rdot, thetadot = thetadot)
