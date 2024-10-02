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
R_S = 100

# scaling factors
alpha = 10e-18

# physical quantities
M = 1/(2*G) 
m = alpha * M
mu = M*G

radial_acc = lambda entity: ( - G*M/entity.rr**2 ) + (entity.rr - 3/2 * R_S) * (entity.l0**2)/(entity.rr**4)

# physical integration 
dt = 0.01
T = 2
nb_steps = int(T / dt)




class Game():
    def __init__(self):
        
        self.sm = StateManager(state = {
            'canRun':False,
            'shouldExit':False,
            'playerTurn':False,

            'playerShot': False,
            
            'distance':None,
            'angular_velocity':None,
            'radial_velocity':None,
        })


        # init pygame & scene
        pygame.init()
        pygame.font.init() 
        self.scene = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

        # init some helper msgs 
        self.text_your_turn = self.init_text('Your turn!')
        self.text_computing = self.init_text('Computing new positions ...')
        self.text_you_won = self.init_text('You won')
        self.text_you_lose = self.init_text('You lose')

        # init text that will be displayed
        self.current_text = self.text_your_turn

        # create the entity pool and add some entities
        self.entity_pool = EntityPool()

        # set the background image
        self.background = pygame.image.load(os.path.join(ASSETS_PATH, BACKGROUND_PATH)).convert()

        # create black hole, player and target and add them to pool
        self.black_hole = BlackHole(mass = M, R_S = R_S)
        self.entity_pool.add(self.black_hole)
        
        self.player = Player(mass = m,
                             rr = 0,
                             rdot = 0,
                             thetadot = 0)
        self.entity_pool.add(self.player)

        self.target = Target(mass = m,
                             rr = 0,
                             rdot = 0,
                             thetadot = 0)
        self.entity_pool.add(self.target)


    # handler for the console part
    def console_handler(self):
        console = CustomConsole(state_manager=self.sm)
        welcome_msg = """
Welcome on board.
Type `help` to display a short manual.
Type `list [commands|variables]` to list all the commands/variables.`
"""
        console.interact(welcome_msg)



    # utils 
    def should_game_exit(self):
        if(self.sm.get('shouldExit')):
            sys.exit()
       
    def check(self, key, callback):
        while True:
            self.should_game_exit() 
            if(self.sm.get(key)):
                break
        callback()

    def init_text(self, txt: str, size = 34) -> pygame.Surface:
        font = pygame.font.Font(os.path.join(ASSETS_PATH, 'golden-age.ttf'), size)
        return font.render(txt, False, (217,0,210))
    
        
    # dynamics & rendering
    def update_entities(self):
        # iterate over entities
        for entity in self.entity_pool.pool:
            current = self.entity_pool.pool[entity]
            if(not current.palive):
                continue
        
            current.update(self.scene, radial_acc, dt)
                
            # test for collisions
            for other_entity in self.entity_pool.pool:
                other_current = self.entity_pool.pool[other_entity]
                if(not other_current.palive or current.id == other_entity):
                    continue    
                current.is_colliding_with(other_current)

                
    def draw_scene(self):
        self.scene.blit(self.background, (0,0))
        self.scene.blit(self.current_text, (0,0))
        for entity in self.entity_pool.pool:
            if(self.entity_pool.pool[entity].palive): 
                self.entity_pool.pool[entity].draw(self.scene)
        pygame.display.flip()


   
    def gameloop(self):
        distance = self.sm.get('distance')
        angular_velocity = self.sm.get('angular_velocity')
        radial_velocity = self.sm.get('radial_velocity')

        self.player.rr = distance
        self.player.rtheta = 0
        self.player.rdot = radial_velocity
        self.player.thetadot = angular_velocity / distance


        self.target.rr = distance
        self.target.rtheta = np.pi
        self.target.rdot = radial_velocity
        self.target.thetadot = angular_velocity / distance

        self.draw_scene()

        while True:
            if(not self.sm.get('playerTurn')): # computer's turn
                self.current_text = self.text_computing
                for _ in range(nb_steps):
                    self.update_entities()
                    self.draw_scene()
                self.sm.set('playerTurn', True)

            else: # player's turn
                self.current_text = self.text_your_turn


            # exiting conditions
            if(not self.player.palive):
                self.current_text = self.text_you_lose
                self.sm.set('shouldExit', True)
            elif(not self.target.palive):
                self.current_text = self.text_you_won
                self.sm.set('shouldExit', True)


            self.draw_scene()
            self.should_game_exit()


            # event loop of pygame
            for event in pygame.event.get():
                if(event.type == pygame.QUIT):
                    pygame.quit()
                    sys.exit()

    # entry point
    def run(self):

        # player console
        console_thread = threading.Thread(target=self.console_handler)
        console_thread.start()

        # start the game
        self.check('canRun', callback=self.gameloop)
