# features
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


GAME_TITLE = 'conrad'


SCREEN_WIDTH = 512
SCREEN_HEIGHT = 512

ASSETS_PATH = 'assets'
BACKGROUND_PATH = 'green_bg.png'



class Game():
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
        welcome_msg = """Welcome on board.
        Type `help` to display a short manual.
        Type `list [commands|variables]` to list all the commands/variables.`
        """
        console.interact(welcome_msg)

    def should_game_exit(self):
        if(self.sm.get('shouldExit')):
            sys.exit()

    def check(key, callback):
        while True:
            should_game_exit() 
            if(self.sm.get(key)):
                break

        callback()
            

    def gameloop(self):
        # launch pygame
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)

        # instantiating entities in the pool 
        entity_pool = EntityPool()
        
        bh = BlackHole()
        entity_pool.add(bh)

        distance = self.sm.get('distance')
        radial_velocity = self.sm.get('radial_velocity')
        angular_velocity = self.sm.get('angular_velocity')
        
        player = Player(rr = distance,
                        rdot = radial_velocity,
                        thetadot = angular_velocity / radial_velocity)
        entity_pool.add(player)


        # setup the background image
        background = pygame.image.load(os.path.join(ASSETS_PATH,BACKGROUND_PATH)).convert()
        screen.blit(background, (0,0)) # add background to the scene


        # load entities imgs


        # update scene
        pygame.display.flip()
        
        # game loop
        while True:
            self.should_game_exit()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        
    def run(self):

        # player console
        console_thread = threading.Thread(target=self.console_handler)
        console_thread.start()

        # start the game 
        check('canRun', callback=self.gameloop)
