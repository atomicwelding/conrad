from CustomConsole import CustomConsole
from StateManager import StateManager

import pygame
import threading
import time
import sys


class App():
    def __init__(self):
        self.sm = StateManager(state = {
            'canRun':False,
            'shouldExit':False,
            'distance':None,
            'angular_velocity':None,
            'radial_velocity':None
        })

    def console_handler(self):
        console = CustomConsole(state_manager=self.sm)
        console.interact("Welcome on board.\nType `help` to display a short manual.\nType `list` to list all the commands.")

    def check_shouldExit(self):
        if(self.sm.get('shouldExit')):
            sys.exit()

    def start_game(self):
        # wait for init
        while True:
            self.check_shouldExit()
            if(self.sm.get('canRun')):
                break

        self.game_loop()
        
    def game_loop(self):
        # launch pygame
        pygame.init()
        screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption("Hello World")

        # game loop
        while True:
            self.check_shouldExit()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        
    def run(self):

        # player console
        console_thread = threading.Thread(target=self.console_handler)
        console_thread.start()

        # scene handling
        self.start_game()
