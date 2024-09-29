from CustomConsole import CustomConsole
from StateManager import StateManager

# entities
from BlackHole import BlackHole
from Player import Player
from EntityPool import EntityPool 

import pygame
import threading
import time
import sys
import os 


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
        screen = pygame.display.set_mode((512, 512))
        pygame.display.set_caption("Conrad")



        entity_pool = EntityPool()
        
        # instantiating entities
        bh = BlackHole()
        entity_pool.add(bh)
        
        player = Player(rr = self.sm.get('distance'),
                        rdot = self.sm.get('radial_velocity'),
                        thetadot = self.sm.get('angular_velocity') / self.sm.get('distance') )
        entity_pool.add(player)


        


        background = pygame.image.load(os.path.join('assets', 'green_bg.png')).convert()
        screen.blit(background, (0,0))
        pygame.display.flip()
        
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
