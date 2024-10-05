from IEntity import IEntity
from params import * 
class EntityPool:
    """
    Manages a pool of entities, allowing adding, removing, and drawing entities on the screen.
    """

    def __init__(self):
        self.pool = {}

    def add(self, entity: IEntity):
        """Adds an entity to the pool."""
        self.pool[entity.id] = entity

    def remove(self, entity: IEntity):
        """Removes an entity from the pool."""
        self.pool.pop(entity.id)

    def init_entities(self):
        for entity in self.pool.values():
            entity.init()

    def draw_entities(self, scene):
        """Draws all entities in the pool on the screen."""
        for entity in self.pool.values():
            if entity.palive:
                entity.draw(scene)

    def update_entities(self, scene):
        """ Updates all entities in the pool on the screen."""

        for current in self.pool.values():
            
            if not current.palive:
                continue
            current.update(scene, radial_acc, dt)

            for other_entity in self.pool.values():
                if not other_entity.palive or current.id == other_entity.id:
                    continue
                current.is_colliding_with(other_entity)
