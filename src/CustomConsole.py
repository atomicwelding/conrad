from StateManager import StateManager
from command_implementation import commands

import code
import sys


 

def command_handler(command, state_manager: StateManager):

        all_commands = [key for key in commands]

        try:
                parts = command.split()
                command_name = parts[0]
        except IndexError:
                return True

        if(not (command_name in all_commands)):
                print("Please, use a defined command.")
                print("Type `list` to list all the commands.")
                return True

        try:
                arg1 = parts[1]
        except IndexError:
                arg1 = None

        try:
                arg2 = parts[2]
        except IndexError:
                arg2 = None

        commands[command_name]['command'](state_manager, arg1, arg2)

        return True

                
class CustomConsole(code.InteractiveConsole):
    def __init__(self, state_manager):
        super().__init__()
        self.state_manager = state_manager
    
    def runsource(self, source, filename="<input>", symbol="single"):
        if command_handler(source.strip(), state_manager = self.state_manager):
            return False  # Do not execute the command further
        return super().runsource(source, filename, symbol)
    
