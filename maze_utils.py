from turtle import position
from mazelib import Maze
from mazelib.generate.Prims import Prims
from PIL import Image

import pins_utils

def gen_maze_sprite(width : int, height: int, seed:int) -> Image.Image:
    """Generates a new maze sprite

    Args:
        width (int): height of maze, in number of hallways
        height (int): width of maze, in number of hallways
        seed (int): seed to generate the maze

    Returns:
        Image: maze image using the PIL.Image library
    """
    pixel_width : int = width*2+1
    pixel_height : int = height*2+1
    
    m = Maze(seed)
    m.generator = Prims(width, height)
    m.generate()
    
    maze_grid_image : list[tuple[int,...]] = []
    for row in m.grid:
        for element in row:
            #white pixel, transparent if element is 0
            maze_grid_image.append((255,255,255,int(element)*255))

    img = Image.new('RGBA', (pixel_width, pixel_height))
    img.putdata(maze_grid_image)
    img.save('maze.png')
    return img

def gen_maze_sprite_pins(width : int, height: int, seed:int, pins : list[pins_utils.pin]) -> Image.Image:
    """Generates a new maze sprite

    Args:
        width (int): height of maze, in number of hallways
        height (int): width of maze, in number of hallways
        seed (int): seed to generate the maze

    Returns:
        Image: maze image using the PIL.Image library
    """
    pixel_width : int = width*2+1
    pixel_height : int = height*2+1
    
    m = Maze(seed)
    m.generator = Prims(width, height)
    m.generate()
    
    maze_grid_image : list[tuple[int,...]] = []
    skip = False
    i : int = 0
    for row in m.grid:
        i = i+1
        j : int = 0
        for element in row:
            j = j+1
            for pin in pins:
                if ((j-2)/2,(i-2)/2) == pin.position:
                    skip = True
                    maze_grid_image.append((24, 240, 0,255))
                    break
            if skip == True:
                skip = False
                continue
            #white pixel, black if element is 0
            maze_grid_image.append((int(element)*255,int(element)*255,int(element)*255,255))

    img = Image.new('RGBA', (pixel_width, pixel_height))
    img.putdata(maze_grid_image)
    img = img.resize((pixel_width*30,pixel_height*30), Image.Resampling.NEAREST)
    img.save('maze_pin.png')
    return img

def gen_empty_maze_sprite(width : int, height: int) -> Image.Image:
    pixel_width : int = width*2+1
    pixel_height : int = height*2+1
    
    maze_grid_image : list[tuple[int,...]] = []
    for i in range(pixel_width):
        for j in range(pixel_height):
            #the border is white
            if i==0 or i==pixel_width-1 or j == 0 or j == pixel_height-1:
                maze_grid_image.append((255,255,255,255))
            elif i%2==0 and j%2==0:
                maze_grid_image.append((255,255,255,255))
            else:
                maze_grid_image.append((0,0,0,255))
    
    img = Image.new('RGBA', (pixel_width, pixel_height))
    img.putdata(maze_grid_image)
    img.save('maze_empty.png')
    return img