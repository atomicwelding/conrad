from StateManager import StateManager
from command_implementation import commands
import code
import sys

def command_handler(command, state_manager: StateManager):
    """
    Handles the execution of a command based on the input string.
    
    Parameters:
    -----------
    command : str
        The input command from the user.
    state_manager : StateManager
        The game state manager used to execute commands.
    
    Returns:
    --------
    bool
        Always returns True to indicate command handling is completed.
    """
    all_commands = [key for key in commands]

    try:
        parts = command.split()
        command_name = parts[0]
    except IndexError:
        return True

    if command_name not in all_commands:
        print("Please, use a defined command.")
        print("Type `list` to list all the commands.")
        return True

    arg1 = parts[1] if len(parts) > 1 else None
    arg2 = parts[2] if len(parts) > 2 else None

    commands[command_name]['command'](state_manager, arg1, arg2)

    return True

class CustomConsole(code.InteractiveConsole):
    """
    A custom console for handling and executing game commands.
    
    Parameters:
    -----------
    state_manager : StateManager
        The game state manager that tracks and executes commands.
    """

    def __init__(self, state_manager):
        super().__init__()
        self.state_manager = state_manager
    
    def runsource(self, source, filename="<input>", symbol="single"):
        """
        Processes the input source and runs commands if they are valid.
        
        Parameters:
        -----------
        source : str
            The command input from the user.
        filename : str, optional
            The filename to associate with the command (default is '<input>').
        symbol : str, optional
            The mode of input (default is 'single').
        
        Returns:
        --------
        bool
            Returns False if the command is handled, otherwise proceeds with the standard interpreter.
        """
        if command_handler(source.strip(), state_manager=self.state_manager):
            return False  # Command was handled, no further execution needed
        return super().runsource(source, filename, symbol)
