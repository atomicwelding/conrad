# features
from CustomConsole import CustomConsole
from StateManager import StateManager

# entities
from BlackHole import BlackHole
from Player import Player
from EntityPool import EntityPool
from Target import Target

from params import * 
import numpy as np
import pygame
import threading
import sys
import os

class Game:
    """
    Represents the main game class responsible for handling game setup, state management, 
    entity updates, and game logic.
    """

    def __init__(self):
        """
        Initializes the game, including state manager, pygame setup, and entity creation.
        """
        self.sm = StateManager(state={
            'canRun': False,
            'shouldExit': False,
            'playerTurn': True,
            'playerCanShootHeavy': True,
            'playerCanShootLight': True,
            'playerShot': False,
            'playerShotType': None,
            'playerShotAngle': None,
            'distance': None,
            'angular_velocity': None,
            'radial_velocity': None,
        })

        # Initialize pygame and scene
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption(GAME_TITLE)
        self.scene = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        # Initialize text messages
        self.text_your_turn = self.init_text('Your turn!')
        self.text_computing = self.init_text('Computing new positions ...')
        self.text_forwarding = self.init_text('Forwarding ...')
        self.text_you_won = self.init_text('You won')
        self.text_you_lose = self.init_text('You lose')
        self.current_text = self.text_your_turn

        # Initialize entity pool and add entities
        self.entity_pool = EntityPool()
        self.background = pygame.image.load(os.path.join(ASSETS_PATH, BACKGROUND_PATH)).convert()

        # Add game entities
        self.black_hole = BlackHole(mass=M, R_S=R_S)
        self.entity_pool.add(self.black_hole)

        self.player = Player(mass=m, rr=0, rdot=0, thetadot=0)
        self.entity_pool.add(self.player)

        self.target = Target(mass=m, rr=0, rdot=0, thetadot=0)
        self.entity_pool.add(self.target)

    def console_handler(self):
        """
        Handles the player's console input and manages game commands.
        """
        console = CustomConsole(state_manager=self.sm)
        welcome_msg = """
Welcome on board.
Type `help` to display a short manual.
Type `list [commands|variables]` to list all the commands/variables.
"""
        console.interact(welcome_msg)

    def should_game_exit(self):
        """
        Exits the game if the 'shouldExit' state is set.
        """
        if self.sm.get('shouldExit'):
            sys.exit()

    def check(self, key, callback):
        """
        Continuously checks for a condition to trigger the game loop.
        
        Parameters:
        -----------
        key : str
            The state variable to check.
        callback : function
            The function to call once the condition is met.
        """
        while True:
            self.should_game_exit()
            if self.sm.get(key):
                break
        callback()

    def init_text(self, txt: str, size=34) -> pygame.Surface:
        """
        Initializes a text surface for rendering.
        
        Parameters:
        -----------
        txt : str
            The text to render.
        size : int, optional
            The font size (default is 34 pixels).
        
        Returns:
        --------
        pygame.Surface
            The rendered text surface.
        """
        font = pygame.font.Font(os.path.join(ASSETS_PATH, 'golden-age.ttf'), size)
        return font.render(txt, False, (217, 0, 210))

    def update_entities(self):
        """
        Updates the positions and states of all entities in the game and checks for collisions.
        """
        # Handle player shooting
        projectile_player = self.player.handle_shoot_state(self.sm)
        if projectile_player:
            self.entity_pool.add(projectile_player)

        # Handle target shooting
        projectile_target = self.target.random_shoot()
        if projectile_target:
            self.entity_pool.add(projectile_target)

        # Update all entities and check collisions
        for entity in self.entity_pool.pool:
            current = self.entity_pool.pool[entity]
            if not current.palive:
                continue
            current.update(self.scene, radial_acc, dt)

            for other_entity in self.entity_pool.pool:
                other_current = self.entity_pool.pool[other_entity]
                if not other_current.palive or current.id == other_entity:
                    continue
                current.is_colliding_with(other_current)

    def init_entities(self):
        """
        Initializes the entities in the game, setting up initial states.
        """
        for entity in self.entity_pool.pool:
            self.entity_pool.pool[entity].init()

    def draw_scene(self):
        """
        Draws the current game scene, including all entities and text.
        """
        self.scene.blit(self.background, (0, 0))
        self.scene.blit(self.current_text, (0, 0))
        for entity in self.entity_pool.pool:
            if self.entity_pool.pool[entity].palive:
                self.entity_pool.pool[entity].draw(self.scene)
        pygame.display.flip()

    def gameloop(self):
        """
        The main game loop, alternating between player and AI turns.
        """
        distance = self.sm.get('distance')
        angular_velocity = self.sm.get('angular_velocity')
        radial_velocity = self.sm.get('radial_velocity')

        # Update player and target positions
        self.player.rr = distance
        self.player.rtheta = 0
        self.player.rdot = radial_velocity
        self.player.thetadot = angular_velocity / distance

        self.target.rr = distance
        self.target.rtheta = np.pi
        self.target.rdot = radial_velocity
        self.target.thetadot = angular_velocity / distance

        self.draw_scene()
        self.init_entities()

        # Set initial shooting ability
        self.sm.set('playerCanShootHeavy', self.player.nb_heavy_missile_left > 0)
        self.sm.set('playerCanShootLight', self.player.nb_light_missile_left > 0)

        while True:
            if not self.sm.get('playerTurn'):  # AI's turn
                self.current_text = self.text_computing if self.player.has_ammo() else self.text_forwarding
                self.target.canShoot = True
                for _ in range(nb_steps):
                    self.update_entities()
                    self.target.canShoot = False
                    self.draw_scene()
                if self.player.has_ammo():  # Forward to player if possible
                    self.sm.set('playerTurn', True)
            else:  # Player's turn
                self.current_text = self.text_your_turn

            # Check exit conditions
            if not self.player.palive:
                self.current_text = self.text_you_lose
                self.sm.set('shouldExit', True)
            elif not self.target.palive:
                self.current_text = self.text_you_won
                self.sm.set('shouldExit', True)

            self.draw_scene()
            self.should_game_exit()

            # Pygame event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

    def run(self):
        """
        Runs the game by starting the console and entering the main game loop.
        """
        console_thread = threading.Thread(target=self.console_handler)
        console_thread.start()

        # Start the game loop once conditions are met
        self.check('canRun', callback=self.gameloop)
