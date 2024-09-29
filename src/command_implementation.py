from StateManager import StateManager
import sys


def exit_command(state_manager: StateManager, arg1, arg2):
        state_manager.set('shouldExit', True)
        sys.exit()


def help_command(state_manager: StateManager, arg1, arg2):
    if(not arg1):
        print("Manual not written yet")
        return


    try:
        print(commands[arg1]['use']  + " : " + commands[arg1]['goal'])

    except KeyError:
        print("Command doesn't exist")
    
    if(not (arg1 in commands)):
        print("Command doesn't exist")
        return



def sdbg_command(state_manager: StateManager, arg1, arg2):
    state_manager.set('distance', float(10))
    state_manager.set('angular_velocity', float(10))
    state_manager.set('radial_velocity', float(10))

def list_command(state_manager: StateManager, arg1, arg2):

    if(not (arg1 == "variables")):
        for command in commands:
            print(command + " : " + commands[command]['goal'])

    else:
        variables = """distance : distance from black hole.
radial_velocity : initial radial velocity
angular_velocity : initial angular velocity
"""
        print(variables)


def run_command(state_manager: StateManager, arg1, arg2):
    state_manager.set('canRun',
                      state_manager.get('distance') and state_manager.get('angular_velocity') and state_manager.get('radial_velocity'))
    if(not state_manager.get('canRun')):
        print('Please, set distance, angular_velocity and radial_velocity before running the game.')



def set_command(state_manager: StateManager, arg1, arg2):
    if(not (arg1 and arg2)):
        print('Please, set variables the proper way')
        print(commands['set']['use'])
        return
    else:
        try:
            if(arg1 == 'distance'):
                state_manager.set('distance', float(arg2))
                            
            elif(arg1 == 'radial_velocity'):
                state_manager.set('radial_velocity', float(arg2))
                            
            elif(arg1 == 'angular_velocity'):
                state_manager.set('angular_velocity', float(arg2))
            else:
                print('Variable name not known. Type `list variables` to list all the variables.')
        except ValueError:
            print('Value not valid. Please, use a number.')
    
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
                'goal': 'run the game ; you need to  `set` variables before it runs'
        },

        'set': {
                'command': set_command,
                'use': '`set [distance|angular_velocity|radial_velocity]`',
                'goal': 'set a value to a given variable'
        },

        'sdbg': {
                'command': sdbg_command,
                'use': '`sdbg`',
                'goal': 'debugging purpose only'
        },
}






        
