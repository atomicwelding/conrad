import code
import sys

list_command = """
exit : leave the game
help : print the help
list : list all commands
run : run the game
set : set variables
"""

list_variables = """
distance : distance from black hole.
radial_velocity : initial radial velocity
angular_velocity : initial angular velocity
""" 

help_command = "Help is not written for the moment. Come back later."

def command_handler(command, state_manager = None):
        parts = command.split()
        match parts[0]:

            case "exit":
                state_manager.set('shouldExit', True)
                sys.exit()

            case "help":
                print(help_command)


            case "sdev": # only for developers
                state_manager.set('distance', float(10))
                state_manager.set('angular_velocity', float(10))
                state_manager.set('radial_velocity', float(10))

            case "list":
                if(len(parts) > 1 and parts[1] == 'variables'):
                    print(list_variables)
                else: print(list_command)

            case "set":
                if(len(parts) < 3):
                    print('Please, set variables the proper way : `set var_name var_value`.')
                else:
                    try:
                        if(parts[1] == 'distance'):
                            state_manager.set('distance', float(parts[2]))
                        
                        elif(parts[1] == 'radial_velocity'):
                            state_manager.set('radial_velocity', float(parts[2]))
                        
                        elif(parts[1] == 'angular_velocity'):
                            state_manager.set('angular_velocity', float(parts[2]))

                        else:
                            print('Variable name not known. Type `list variables` to list all the variables.')
                    except ValueError:
                        print('Value not valid. Please, use a number.')

            case "run":
                state_manager.set('canRun', state_manager.get('distance')\
                                  and state_manager.get('angular_velocity') \
                                  and state_manager.get('radial_velocity'))

                if(not state_manager.get('canRun')):
                    print('Please, set distance, angular_velocity and radial_velocity before running the game.')

            case _:
                print("Please, use a defined command.")
                print("Type `list`to list all the commands.")
        return True

class CustomConsole(code.InteractiveConsole):
    def __init__(self, state_manager = None):
        super().__init__()
        self.state_manager = state_manager
    
    def runsource(self, source, filename="<input>", symbol="single"):
        if command_handler(source.strip(), state_manager = self.state_manager):
            return False  # Do not execute the command further
        return super().runsource(source, filename, symbol)
    
