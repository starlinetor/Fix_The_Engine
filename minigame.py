# Example file showing a basic pygame "game loop"
import pygame
import mazegenerator
from PIL import Image

# pygame setup
pygame.display.init()

maze_width : int = 14
maze_height : int = 14

scaling_factor : int = 25
border : int = 10
screen_width : int = (maze_width*2+1)*scaling_factor + (border * 2)
screen_height : int = (maze_height*2+1)*scaling_factor + (border * 2)

screen = pygame.display.set_mode((screen_width*2,screen_height))
clock = pygame.time.Clock()
running = True

#maze
maze_image : Image.Image = mazegenerator.gen_maze_sprite(maze_width,maze_height,123)
maze_image = maze_image.resize((screen_width-(border * 2),screen_height-(border * 2)), Image.Resampling.NEAREST)
maze = pygame.image.fromstring(maze_image.tobytes(), maze_image.size, maze_image.mode)
maze_mask = pygame.mask.from_surface(maze)

#empty maze
empty_maze_image = mazegenerator.gen_empty_maze_sprite(maze_width, maze_height)
empty_maze_image = empty_maze_image.resize((screen_width-(border * 2),screen_height-(border * 2)), Image.Resampling.NEAREST)
empty_maze = pygame.image.fromstring(empty_maze_image.tobytes(), empty_maze_image.size, empty_maze_image.mode)

#pointer
pointer  = pygame.Surface((1,1))
pointer_mask = pygame.mask.from_surface(pointer)

#indicator 
indicator = pygame.Surface((10,10))

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    #mouse
    pos = pygame.mouse.get_pos()

    # RENDER YOUR GAME HERE
    screen.blit(maze, (border, border))
    screen.blit(empty_maze, (border,border))
    screen.blit(pointer, pos)
    screen.blit(indicator,(0,0))
    
    if maze_mask.overlap(pointer_mask, (pos[0]-border, pos[1]-border)):
        indicator.fill((255,0,0))
    else :
        indicator.fill((255,255,255))

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()