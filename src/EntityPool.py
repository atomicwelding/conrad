from IEntity import IEntity

class EntityPool():


    def __init__(self):
        self.pool = {}


    def add(self, entity : IEntity):
        self.pool[entity.id] = entity

    def remove(self, entity : IEntity):
        self.pool.pop(entity.id)

    def  drawPool(self, screen):
        for id in self.pool:
            self.pool[id].draw()
