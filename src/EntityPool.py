from IEntity import IEntity

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

    def drawPool(self, screen):
        """Draws all entities in the pool on the screen."""
        for entity in self.pool.values():
            entity.draw(screen)
