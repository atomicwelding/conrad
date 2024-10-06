from params import * 
from abc import ABC, abstractmethod
from uuid import uuid4
import numpy as np
import os
import pygame

class IEntity(ABC):
    """
    Abstract base class representing an entity in the game. 
    Each entity is defined by its position, velocity, and graphical representation.
    
    Attributes:
    -----------
    id : str
        Unique identifier for the entity.
    mass : float
        Mass of the entity.
    rr : float
        Radial distance from the origin.
    rtheta : float
        Angular position in polar coordinates.
    rdot : float
        Radial velocity.
    thetadot : float
        Angular velocity.
    palive : bool
        Whether the entity is alive.
    l0 : float
        Angular momentum constant for the entity's motion.
    img_path : str
        Path to the entity's image.
    surface : pygame.Surface
        Loaded image surface for the entity.
    """
    
    def __init__(self, img_path, mass, rr, rtheta, rdot, thetadot):
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
        sfw, sfh = self.surface.get_size()
        return (sfw + sfh) / 4

    def load(self) -> pygame.Surface:
        return pygame.image.load(os.path.join(ASSETS_PATH, self.img_path)).convert_alpha()

    def x(self):
        return self.rr * np.cos(self.rtheta)

    def y(self):
        return self.rr * np.sin(self.rtheta)

    def pyg_coords(self, scene):
        sfw, sfh = self.surface.get_size()
        scw, sch = scene.get_size()
        x = (self.x() - sfw // 2) + scw // 2
        y = (self.y() - sfh // 2) + sch // 2
        return (x, y)

    def update(self, scene, radial_acceleration, dt: float) -> None:
        self.thetadot = self.l0 / self.rr**2
        self.rtheta += self.l0 * dt / self.rr**2
        self.rdot += dt / 2 * radial_acceleration(self)
        self.rr += self.rdot * dt
        self.rdot += dt / 2 * radial_acceleration(self)

        # boundaries check
        scw, sch = scene.get_size()
        if (self.x() < -scw/2 or self.x() > scw/2
            or self.y() < - sch/2 or self.y() > sch/2):
            self.rr = scw / 2
            self.rtheta += np.pi
            self.rdot *= -1

    def draw(self, scene):
        scene.blit(self.surface, self.pyg_coords(scene))


    def is_colliding_with(self, entity) -> bool:
        rectA = self.surface.get_rect(center=(self.x(), self.y()))
        rectB = entity.surface.get_rect(center=(entity.x(), entity.y()))
        return rectA.colliderect(rectB)

    def assign_result_collisions(self, other):
        m1, m2 = self.mass, other.mass
        T1, T2 = self.angular_velocity(), other.angular_velocity()
        v1, v2 = self.radial_velocity(), other.radial_velocity()

        # Handle cases where either radial velocity is zero
        if v1 == 0 and v2 == 0:
            return  # No collision effect if both are stationary

        if v1 == 0:
            # Physically, object 1 gains velocity and direction based on the impact from object 2
            T1prime = T2  # After collision, object 1 will follow the trajectory of object 2
            v1prime = (2 * m2 / (m1 + m2)) * v2 * np.sin(T2)  # Gain velocity from object 2
        else:
            T1prime = np.atan(((m1 - m2) / (m1 + m2)) * np.tan(T1) + (2 * m2 / (m1 + m2)) * (v2 / v1) * np.sin(T2) / np.cos(T1))
            v1prime = np.sqrt((((m1 - m2) / (m1 + m2)) * v1 * np.sin(T1) + (2 * m2 / (m1 + m2)) * v2 * np.sin(T2)) ** 2 + (v1 * np.cos(T1)) ** 2)

        if v2 == 0:
            # Physically, object 2 gains velocity and direction based on the impact from object 1
            T2prime = T1  # After collision, object 2 will follow the trajectory of object 1
            v2prime = (2 * m1 / (m1 + m2)) * v1 * np.sin(T1)  # Gain velocity from object 1
        else:
            T2prime = np.atan(((m2 - m1) / (m1 + m2)) * np.tan(T2) + (2 * m1 / (m1 + m2)) * (v1 / v2) * np.sin(T1) / np.cos(T2))
            v2prime = np.sqrt((((m2 - m1) / (m1 + m2)) * v2 * np.sin(T2) + (2 * m1 / (m1 + m2)) * v1 * np.sin(T1)) ** 2 + (v2 * np.cos(T2)) ** 2)

        # Update the radial and angular velocities
        self.rdot, self.thetadot = v1prime, T1prime / self.rr
        other.rdot, other.thetadot = v2prime, T2prime / other.rr

        # Calculate the overlap and adjust positions if there's a collision
        distance = np.sqrt(self.rr**2 + other.rr**2 - 2 * self.rr * other.rr * np.cos(self.rtheta - other.rtheta))
        overlap_distance = self.radius() + other.radius() - distance

        if overlap_distance > 0:
            self.rr += overlap_distance / 2
            other.rr -= overlap_distance / 2