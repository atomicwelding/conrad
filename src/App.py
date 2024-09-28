from CustomConsole import CustomConsole
from StateManager import StateManager
import threading
import time
import sys


class App():
    def __init__(self):
        self.sm = StateManager(state = {
            'canRun':False,
            'distance':None,
            'angular_velocity':None,
            'radial_velocity':None
        })

    def console_handler(self):
        console = CustomConsole(state_manager=self.sm)
        console.interact("Welcome on board.\nType `help` to display a short manual.\nType `list` to list all the commands.")


    def start_game(self):
        while True:
            time.sleep(1)
            if(self.sm.get('canRun')):
                break
        print("Game is running...")
        
    def run(self):
        
        # scene handling 
        # dumb_thread = threading.Thread(target=self.dumb_handler)
        #dumb_thread.start()
        game_thread = threading.Thread(target=self.start_game)
        game_thread.start()

        # player console
        self.console_handler()
            
