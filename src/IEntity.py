from abc import ABC, abstractmethod
from uuid import uuid4
import numpy as np
import os


import pygame


ASSETS_PATH = "assets"


class IEntity(ABC):

    def __init__(self, img_path,
                 mass,
                 rr, rtheta,
                 rdot, thetadot):

        self.id = uuid4().hex
        self.mass = mass
        self.rr = rr
        self.rtheta = rtheta
        self.rdot = rdot
        self.thetadot = thetadot

        self.img_path = img_pathx


    def radial_velocity(self):
        return self.rdot
        
    def angular_velocity(self):
        return self.rr * self.thetadot 

    def distance(self):
        return np.sqrt(self.rr**2 + self.rtheta**2)

    def velocity(self):
        return np.sqrt(self.radial_velocity() ** 2 + self.angular_velocity()**2)


    def load(self) -> pygame.Surface :
        return pygame.image.load(os.path.join(ASSETS_PATH, self.img_path)).convert()
        
    @abstractmethod
    def draw(self, scene):
        pass

    @abstractmethod
    def is_colliding(self):
        pass
