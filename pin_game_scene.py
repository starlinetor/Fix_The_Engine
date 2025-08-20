import random
from re import I
import sys
import pygame
import pins_utils
import scene as sc
import scene_handler as sh
import pygame.freetype
import maze_utils
from PIL import Image

class PinGameScene(sc.Scene):
    def __init__(self, scene_handler: sh.SceneHandler, random_seed : bool, game_seed : int, maze_width : int, maze_height : int, scaling_factor : int, border : int, debug : bool) -> None:
        self.scene_handler : sh.SceneHandler = scene_handler
        #settings
        #use a random seed
        self.random_seed : bool = random_seed
        #if random_seed is false this is the seed that will be used
        self.game_seed : int = game_seed
        self.internal_random = random.Random()
        #maze data and settings
        self.maze_width : int = maze_width
        self.maze_height : int = maze_height
        #scale the maze to make it bigger
        self.scaling_factor : int = scaling_factor
        #border around the maze
        self.border : int = border
        #display extra information
        self.debug : bool = debug
    
    def start(self) -> None:
        #Colors
        self.WHITE = (255,255,255)
        self.BLACK = (0,0,0)
        self.YELLOW = (255, 200, 0)
        self.RED = (255,0,0)
        self.BLUE = (0,0,255)
        self.PURPLE = (195, 0, 255)
        self.CYAN = (0, 200, 255)

        #Random
        if self.random_seed:
            self.game_seed = self.internal_random.randint(0,2**32 - 1)
        self.internal_random.seed(self.game_seed)
        

        #maze and screen data
        self.maze_pixel_width : int = (self.maze_width*2+1)*self.scaling_factor 
        self.maze_pixel_height : int = (self.maze_height*2+1)*self.scaling_factor

        self.screen_width : int = (self.maze_pixel_width + (self.border * 2))*2
        self.screen_height : int = self.maze_pixel_height + (self.border * 2)

        #serial number of the engine
        self.serial_number : int = random.randint(1,1000)

        # pygame setup
        pygame.display.init()
        pygame.freetype.init()
        self.clock = pygame.time.Clock()
        self.running = True
        self.screen = pygame.display.set_mode((self.screen_width,self.screen_height))

        #pins
        self.pin_color = "None"
        self.pins, self.start_pin = pins_utils.generate_pins(self.maze_width,self.maze_height,self.scaling_factor,self.border, self.internal_random)
        self.pins = pins_utils.sort_pins(self.pins)
        if self.debug:
            for pin_ in self.pins:
                print(pin_.color)
                print(pin_.position)

        #Sprites
        #maze
        maze_image : Image.Image = maze_utils.gen_maze_sprite(self.maze_width,self.maze_height,self.game_seed)
        maze_image = maze_image.resize((self.maze_pixel_width,self.maze_pixel_height), Image.Resampling.NEAREST)
        self.maze = pygame.image.fromstring(maze_image.tobytes(), maze_image.size, maze_image.mode)
        self.maze_mask = pygame.mask.from_surface(self.maze)
        #generate maze with pins
        maze_utils.gen_maze_sprite_pins(self.maze_width,self.maze_height,self.game_seed, self.pins)

        #empty maze
        empty_maze_image = maze_utils.gen_empty_maze_sprite(self.maze_width, self.maze_height)
        empty_maze_image = empty_maze_image.resize((self.maze_pixel_width,self.maze_pixel_height), Image.Resampling.NEAREST)
        self.empty_maze = pygame.image.fromstring(empty_maze_image.tobytes(), empty_maze_image.size, empty_maze_image.mode)

        #pointer
        self.pointer  = pygame.Surface((1,1))
        self.pointer_mask = pygame.mask.from_surface(self.pointer)

        #Text
        font2screen : float = 0.07
        self.font_size = font2screen*self.screen_height
        self.font = pygame.freetype.Font("CascadiaMono.ttf", self.font_size)

        #pin logic
        self.pins_selected = []
        
        #start game state
        self.game_started = False
        
        #win and lose state
        self.game_ended = False
        self.won = False
    
    def update(self) -> None:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.scene_handler.quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.scene_handler.change_scene("pin_game")

        # fill the screen with a color to wipe away anything from last frame
        self.screen.fill("black")

        #mouse
        pos = pygame.mouse.get_pos()
        mouse_state = pygame.mouse.get_pressed()

        #makes you enter the maze before starting the game
        if not self.game_started:
            self.screen.blit(self.start_pin.surface, self.start_pin.screen_position)
            self.font.render_to(self.screen, (self.screen_height, self.font_size*1),"Go to the green square", self.WHITE)
            self.font.render_to(self.screen, (self.screen_height, self.font_size*3),"Then left click", self.WHITE)
            if self.pointer_mask.overlap(self.start_pin.mask, (self.start_pin.screen_position[0]-pos[0],self.start_pin.screen_position[1]-pos[1])) and mouse_state[0]:
                self.game_started = True
            pygame.display.flip()
            self.clock.tick(60)
            return
        
        #pin logic
        pin_color = "None"
        
        #render pins and selected pin logic
        for pin_ in self.pins:
            self.screen.blit(pin_.surface, pin_.screen_position)
            if self.pointer_mask.overlap(pin_.mask, (pin_.screen_position[0]-pos[0],pin_.screen_position[1]-pos[1])) and not self.game_ended:
                pin_color = pin_.color
                pins_utils.pin_selection_logic(mouse_state[0], pin_, self.pins_selected)
        
        #remove pins
        if not self.game_ended:
            pins_utils.pop_pin_logic(mouse_state[2], self.pins_selected)
        
        #game ending logic
        if self.maze_mask.overlap(self.pointer_mask, (pos[0]-self.border, pos[1]-self.border)):
                self.game_ended = True
                self.won = False
        
        if len(self.pins_selected) == 2:
            self.game_ended = True
            if pins_utils.check_win_state(self.pins, self.pins_selected, self.serial_number):
                self.won = True
            else :
                self.won = False
        
        #rendering
        
        self.screen.blit(self.maze, (self.border, self.border))
        self.screen.blit(self.empty_maze, (self.border,self.border))
        self.screen.blit(self.pointer, pos)
        if not self.game_ended:
            #only draw the cable if the game is working
            pins_utils.pin_draw_logic(self.pins_selected, pos, self.screen)
        
        #more text
        self.font.render_to(self.screen, (self.screen_height, self.font_size), f"Serial N : {self.serial_number}", self.WHITE)
        self.font.render_to(self.screen, (self.screen_height, self.font_size*3), f"Pin Color : {pin_color}", self.WHITE)
        if self.game_ended:
            self.font.render_to(self.screen, (self.screen_height, self.font_size*5),f"Game won : {self.won}", self.WHITE)
        
        #debug rendering
        if self.debug:
            #see the maze
            self.screen.blit(self.maze, (self.border, self.border))
            for pin_ in self.pins:
                self.screen.blit(pin_.surface, pin_.screen_position)
            
            #debug data
            self.font.render_to(self.screen, (self.screen_height, self.font_size*9),f"Seed : {self.game_seed}" , self.WHITE)
            #mouse position indicator
            self.font.render_to(self.screen, (self.screen_height, self.font_size*11), f"Mouse pos : {pos}", self.WHITE)
            #hit wall indicator
            if self.maze_mask.overlap(self.pointer_mask, (pos[0]-self.border, pos[1]-self.border)):
                self.font.render_to(self.screen, (self.screen_height, self.font_size*12), "Hit the wall : YES", self.WHITE)
            else :
                self.font.render_to(self.screen, (self.screen_height, self.font_size*12), "Hit the wall : NO", self.WHITE)
            #FPS indicator
            self.font.render_to(self.screen, (self.screen_height, self.font_size*13), f"FPS : {round(self.clock.get_fps(),2)}", self.WHITE)
            


        # flip() the display to put your work on screen
        pygame.display.flip()

        self.clock.tick(60)  # limits FPS to 60

    def on_exit(self) -> None:
        return super().on_exit()
    