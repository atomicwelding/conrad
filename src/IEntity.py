from params import * 

from abc import ABC, abstractmethod
from uuid import uuid4
import numpy as np
import os


import pygame





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

        self.l0 = self.rr ** 2 * self.thetadot
        
        self.img_path = img_path

        self.surface = self.load()


    def init(self):
        self.l0 = self.rr ** 2 * self.thetadot

    def radial_velocity(self):
        return self.rdot
        
    def angular_velocity(self):
        return self.rr * self.thetadot 

    def distance(self):
        return np.sqrt(self.rr**2 + self.rtheta**2)

    def velocity(self):
        return np.sqrt(self.radial_velocity()** 2 + self.angular_velocity()**2)

    def radius(self):
        # Define radius as a fraction of the surface's width, or use a custom value
        sfw, sfh = self.surface.get_size()
        return (sfw + sfh) / 4  # Example: half the average dimension of the surface


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

    def assign_result_collisions(self, other):
        m1 = self.mass
        m2 = other.mass

        T1 = self.angular_velocity()
        T2 = other.angular_velocity()

        v1 = self.radial_velocity()
        v2 = other.radial_velocity()

        # Compute post-collision angles and velocities
        T1prime = np.atan(((m1 - m2) / (m1 + m2)) * np.tan(T1) + (2 * m2 / (m1 + m2)) * (v2 / v1) * np.sin(T2) / np.cos(T1))
        v1prime = np.sqrt((((m1 - m2) / (m1 + m2)) * v1 * np.sin(T1) + (2 * m2 / (m1 + m2)) * v2 * np.sin(T2)) ** 2 + (v1 * np.cos(T1)) ** 2)
        
        T2prime = np.atan(((m2 - m1) / (m1 + m2)) * np.tan(T2) + (2 * m1 / (m1 + m2)) * (v1 / v2) * np.sin(T1) / np.cos(T2))
        v2prime = np.sqrt((((m2 - m1) / (m1 + m2)) * v2 * np.sin(T2) + (2 * m1 / (m1 + m2)) * v1 * np.sin(T1)) ** 2 + (v2 * np.cos(T2)) ** 2)

        self.rdot = v1prime
        self.thetadot = T1prime / self.rr

        other.rdot = v2prime
        other.thetadot = T2prime / other.rr
        
        # --- Position Correction to Avoid Overlap ---
        # Calculate the distance between the two ships using polar coordinates
        distance = np.sqrt(self.rr**2 + other.rr**2 - 2*self.rr*other.rr*np.cos(self.rtheta - other.rtheta))

        # Sum of radii to check for overlap
        overlap_distance = self.radius() + other.radius() - distance

        if overlap_distance > 0:  # If there's an overlap
            # Unit vector direction in polar coordinates
            direction_rtheta = (self.rtheta - other.rtheta) / distance
        
            # Push each ship apart by half the overlap distance
            self.rr += overlap_distance / 2
            other.rr -= overlap_distance / 2

        
