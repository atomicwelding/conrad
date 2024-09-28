from abc import ABC, abstractmethod
from pygame import Vector2
from uuid import uuid4
import numpy as np


class IEntity(ABC):

    def __init__(self, mass,
                 rr, rtheta,
                 rdot, thetadot):
        self.id = uuid4().hex
        self.mass = mass
        self.rr = rr
        self.rtheta = rtheta
        self.rdot = rdot
        self.thetadot = thetadot


    def radial_velocity(self):
        return self.rdot
        
    def angular_velocity(self):
        return self.rr * self.thetadot 

    def distance(self):
        return np.sqrt(self.rr**2 + self.rtheta**2)

    def velocity(self):
        return np.sqrt(self.radial_velocity() ** 2 + self.angular_velocity()**2)

    def pos_as_vector(self):
        return Vector2().from_polar((self.rr, self.rtheta))

    def vel_as_vector(self):
        return Vector2().from_polar((self.angular_velocity(), self.radial_velocity()))
        
    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def is_colliding(self):
        pass
