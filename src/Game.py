# features
from CustomConsole import CustomConsole
from StateManager import StateManager

# entities
from BlackHole import BlackHole
from Player import Player
from EntityPool import EntityPool
from Target import Target


import numpy as np
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

# physical constants
G = 6.67*10e-11
c = 1
R_S = 1

# scaling factors
alpha = 10e-18

# physical quantities
M = 1/(2*G)
m = alpha * M
mu = M*G

class Game():
    def __init__(self):
        self.sm = StateManager(state = {
            'canRun':False,
            'shouldExit':False,
            'playerTurn':True,

            
            'distance':None,
            'angular_velocity':None,
            'radial_velocity':None,
        })

    def console_handler(self):
        console = CustomConsole(state_manager=self.sm)
        welcome_msg = """
Welcome on board.
Type `help` to display a short manual.
Type `list [commands|variables]` to list all the commands/variables.`
"""
        console.interact(welcome_msg)

    def should_game_exit(self):
        if(self.sm.get('shouldExit')):
            sys.exit()

    def check(self, key, callback):
        while True:
            self.should_game_exit() 
            if(self.sm.get(key)):
                break

        callback()
            

    def gameloop(self):
        # launch pygame
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption(GAME_TITLE)

        # instantiating entities in the pool 
        entity_pool = EntityPool()

        bh = BlackHole(mass = M, R_S = R_S)
        entity_pool.add(bh)

        distance = self.sm.get('distance')
        radial_velocity = self.sm.get('radial_velocity')
        angular_velocity = self.sm.get('angular_velocity')
        
        player = Player(mass = m,
                        rr = distance,
                        rdot = radial_velocity,
                        thetadot = angular_velocity / radial_velocity)
        entity_pool.add(player)


        target = Target(mass = m,
                        rr = distance,
                        rdot = radial_velocity,
                        thetadot = angular_velocity / radial_velocity)
        entity_pool.add(target)


        # setup the background image
        background = pygame.image.load(os.path.join(ASSETS_PATH,BACKGROUND_PATH)).convert()
        screen.blit(background, (0,0)) # add background to the scene


        # load entities imgs
        sfbh = bh.load()
        sfplayer = player.load()
        sftarget = target.load()


        # draw
        for entity in entity_pool.pool:
            entity_pool.pool[entity].draw(screen) # ugly

            
        # update scene
        pygame.display.flip()
        
        # game loop
        while True:
            self.should_game_exit()

            if(not self.sm.get('playerTurn')):
                player.rtheta += np.pi/3
                self.sm.set('playerTurn', True)
                
                screen.blit(background, (0,0))
                for entity in entity_pool.pool:
                    entity_pool.pool[entity].draw(screen) # ugly
                pygame.display.flip()
            

            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        
    def run(self):

        # player console
        console_thread = threading.Thread(target=self.console_handler)
        console_thread.start()

        # start the game
        self.check('canRun', callback=self.gameloop)
