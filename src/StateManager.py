class StateManager:
    """
    Manages the game state, allowing for setting and retrieving state variables.
    
    Parameters:
    -----------
    state : dict
        A dictionary holding the current state of the game.
    """

    def __init__(self, state):
        self._state = state

    def set(self, key, val):
        """
        Sets a value for a given key in the state.
        
        Parameters:
        -----------
        key : str
            The state variable to set.
        val : any
            The value to assign to the state variable.
        
        Returns:
        --------
        val : any
            The value that was set.
        """
        self._state[key] = val
        return val

    def get(self, key):
        """
        Retrieves the value of a state variable.
        
        Parameters:
        -----------
        key : str
            The state variable to retrieve.
        
        Returns:
        --------
        any
            The value of the requested state variable.
        """
        return self._state[key]
