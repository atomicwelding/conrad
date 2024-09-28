class StateManager():
    def __init__(self, state):
        self._state = state
        
    def set(self, key,val):
        self._state[key] = val
        return val

    def get(self, key):
        return self._state[key]
