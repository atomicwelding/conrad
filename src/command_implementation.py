from StateManager import StateManager
from params import *
import numpy as np
import sys

def exit_command(state_manager: StateManager, arg1, arg2):
    """Exits the game by setting the appropriate state and calling sys.exit()."""
    state_manager.set('shouldExit', True)
    sys.exit()

def help_command(state_manager: StateManager, arg1, arg2):
    """Displays help information for commands."""
    if not arg1:
        print("Manual not written yet")
        return

    try:
        print(commands[arg1]['use'] + " : " + commands[arg1]['goal'])
    except KeyError:
        print("Command doesn't exist")

def list_command(state_manager: StateManager, arg1, arg2):
    """Lists available commands or variables."""
    if arg1 != "variables":
        for command in commands:
            print(command + " : " + commands[command]['goal'])
    else:
        variables = """distance : distance from black hole.
radial_velocity : initial radial velocity
angular_velocity : initial angular velocity
"""
        print(variables)

def run_command(state_manager: StateManager, arg1, arg2):
    """Starts the game if required variables are set."""
    distance = state_manager.get('distance')
    angular_velocity = state_manager.get('angular_velocity')
    radial_velocity = state_manager.get('radial_velocity')

    if all([distance, angular_velocity, radial_velocity]):
        state_manager.set('canRun', True)
    else:
        print('Please, set distance, angular_velocity, and radial_velocity before running the game.')

def set_command(state_manager: StateManager, arg1, arg2):
    """Sets game variables such as distance, radial_velocity, or angular_velocity."""
    if not (arg1 and arg2):
        print('Please, set variables the proper way')
        print(commands['set']['use'])
        return
    try:
        if arg1 == 'distance':
            state_manager.set('distance', float(arg2) * R_S)
        elif arg1 == 'radial_velocity':
            state_manager.set('radial_velocity', float(arg2))
        elif arg1 == 'angular_velocity':
            state_manager.set('angular_velocity', float(arg2))
        else:
            print('Variable name not known. Type `list variables` to list all the variables.')
    except ValueError:
        print('Value not valid. Please, use a number.')

def sdbg_command(state_manager: StateManager, arg1, arg2):
    """Debugging command to set predefined values for game variables."""
    state_manager.set('distance', 2 * R_S)
    state_manager.set('angular_velocity', 30.0)
    state_manager.set('radial_velocity', 30.)

def shoot_command(state_manager: StateManager, arg1, arg2):
    """Handles shooting action, checking ammo availability and setting shot parameters."""
    if not state_manager.get('canRun'):
        print('Game is not running.')
        return
    if not state_manager.get('playerTurn'):
        print('Wait for your turn')
        return
    
    if arg1 not in ['heavy', 'light']:
        print("Not a valid projectile type")
        return
    if arg1 == 'heavy' and not state_manager.get('playerCanShootHeavy'):
        print("No heavy ammo left")
        return
    if arg1 == 'light' and not state_manager.get('playerCanShootLight'):
        print("No light ammo left")
        return

    state_manager.set('playerShotType', arg1)
    try:
        angle = float(arg2) * np.pi
        state_manager.set('playerShotAngle', angle)
    except (ValueError, TypeError):
        print('Please, provide a valid multiple of pi')
        return

    state_manager.set('playerShot', True)
    step_command(state_manager, arg1, arg2)

def step_command(state_manager: StateManager, arg1, arg2):
    """Proceeds to the next step by ending the player's turn."""
    state_manager.set('playerTurn', False)

def wait_command(state_manager: StateManager, arg1, arg2):
    """Waits for the next turn, allowing the player to skip their current turn."""
    if not state_manager.get('canRun'):
        print('Game is not running.')
        return
    if not state_manager.get('playerTurn'):
        print('Wait for your turn')
        return
    step_command(state_manager, arg1, arg2)

# Global command definitions
global commands
commands = {
    'exit': {
        'command': exit_command,
        'use': '`exit`',
        'goal': 'exit the game',
    },
    'help': {
        'command': help_command,
        'use': '`help [(command_name)]`',
        'goal': 'print a short manual if no command_name is providen ; helps with the command if provided',
    },
    'list': {
        'command': list_command,
        'use': '`list [variables|(commands)]`',
        'goal': 'list all variables or commands, depending on the argument you pass ; list all the commands by default',
    },
    'run': {
        'command': run_command,
        'use': '`run`',
        'goal': 'run the game ; you need to `set` variables before it runs'
    },
    'set': {
        'command': set_command,
        'use': '`set [distance (as multiple of variable)|angular_velocity|radial_velocity]`',
        'goal': 'set a value to a given variable'
    },
    'sdbg': {
        'command': sdbg_command,
        'use': '`sdbg`',
        'goal': 'debugging purpose only'
    },
    'shoot': {
        'command': shoot_command,
        'use': '`shoot [heavy|light] angle_multiple_of_pi`',
        'goal': 'shoot a projectile'
    },
    'wait': {
        'command': wait_command,
        'use': '`wait`',
        'goal': 'wait for a more favorable position'
    }
}
