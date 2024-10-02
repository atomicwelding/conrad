from abc import ABC, abstractmethod
from uuid import uuid4
import numpy as np
import os


import pygame


ASSETS_PATH = "assets"


class IEntity(ABC):

    def __init__(self,
                 img_path,
                 mass,
                 rr, rtheta,
                 rdot, thetadot):

        self.id = uuid4().hex
        self.mass = mass
        self.rr = rr
        self.rtheta = rtheta
        self.rdot = rdot
        self.thetadot = thetadot
        self.palive = True

        self.l0 = self.rr**2 * self.thetadot

        self.img_path = img_path

        self.surface = self.load()


    def radial_velocity(self):
        return self.rdot
        
    def angular_velocity(self):
        return self.rr * self.thetadot 

    def distance(self):
        return np.sqrt(self.rr**2 + self.rtheta**2)

    def velocity(self):
        return np.sqrt(self.radial_velocity()** 2 + self.angular_velocity()**2)


    def load(self) -> pygame.Surface :
        return pygame.image.load(os.path.join(ASSETS_PATH, self.img_path)).convert_alpha()

    def x(self):
        return self.rr * np.cos(self.rtheta)

    def y(self):
        return self.rr * np.sin(self.rtheta)
    
    def pyg_coords(self, scene):
        # translating in pygame's coordinate
        sfw, sfh = self.surface.get_size()
        scw, sch = scene.get_size()

        x = (self.x() - sfw//2) + scw//2
        y = (self.y() - sfh//2) + sch//2

        return (x,y)

    def update(self, scene, radial_acceleration, dt : float) -> None :
        self.thetadot = self.l0 / self.rr*2
        self.rtheta += self.l0*dt / self.rr**2
        self.rdot += dt / 2 * radial_acceleration(self)
        self.rr += self.rdot * dt
        self.rdot += dt / 2 * radial_acceleration(self)
        
        # boundaries --> special case of angles? how to treat them
        # at the top right corner x = 181 y = 313
        # it goes right to bottom left corner straight to top right again ... fucked up
        scw, sch = scene.get_size()
        if(self.x() <= -scw/2 or self.y() <= -sch/2):
            self.rtheta += np.pi
            self.rdot *= -1
        elif(self.x() >= scw/2 or self.y() >= sch/2):
            self.rtheta -= np.pi
            self.rdot *= -1
        
    
    def draw(self, scene):
        scene.blit(self.surface, self.pyg_coords(scene))

    def is_colliding_with(self, entity) -> bool:
        rectA = self.surface.get_rect(center=(self.x(), self.y()))
        rectB = entity.surface.get_rect(center=(entity.x(), entity.y()))
        return rectA.colliderect(rectB)
