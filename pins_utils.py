from math import ceil, fabs
import random
from time import sleep
import pygame


colors : tuple[str,...] = ("yellow", "red", "blue", "purple", "cyan")

max_pins : int = 6
min_pins : int = 3


color_values : dict[str , tuple[int,int,int]]= {
    "yellow" : (255, 200, 0),
    "red" : (255,0,0),
    "blue" : (0,0,255),
    "purple" : (195, 0, 255),
    "cyan" : (0, 200, 255),
    "green" : (0,255,0)
}

class pin : 
    def __init__(self, position : tuple[int,int], color : str, scaling : int, border:int, pin_id : int, maze_width : int, maze_height : int) -> None:
        self.position : tuple[int,int] = position
        self.screen_position : tuple[int,int]  = (border + (1 + position[0]*2)*scaling, border + (1 + position[1]*2)*scaling)
        self.color : str = color
        self.scaling : int = scaling
        self.maze_width = maze_width
        self.maze_height = maze_height
        self.color_value : tuple[int,int,int] = color_values[color]
        self.surface = pygame.Surface((scaling,scaling))
        self.mask = pygame.mask.from_surface(self.surface)
        self.surface.fill(self.color_value)
        self.pin_id : int = pin_id

def generate_position(maze_width : int, maze_height : int)-> list[tuple[int,int]]:
    pin_positions : list[tuple[int,int]] = []

    for i in range(maze_width):
        for j in range(maze_height):
            pin_positions.append((i,j))
    
    return pin_positions

def generate_pins(maze_height : int, maze_width : int, scaling :int, border : int, internal_random : random.Random) -> tuple[list[pin], pin]:
    """Generates the pins needed for the pin connection minigame

    Args:
        maze_height (int): 
        maze_width (int): 
        scaling (int): 
        border (int): 
        internal_random (random.Random): 

    Returns:
        tuple[list[pin], pin]: list of pin and starting pin
    """
    n_pin : int = internal_random.randint(min_pins, max_pins)
    maze_positions : list[tuple[int,int]] = generate_position(maze_width, maze_height)
    
    pins : list[pin] = []
    for i in range(n_pin):
        position : tuple[int,int] = internal_random.choice(maze_positions)
        maze_positions.remove(position)
        color = internal_random.choice(colors)
        pins.append(pin(position, color, scaling, border,i, maze_width, maze_height))
    
    position : tuple[int,int] = internal_random.choice(maze_positions)
    starting_pin = pin(position, "green", scaling, border, -1, maze_width, maze_height)
    return pins, starting_pin

def pin_selection_logic(left_click : bool, pin : pin, pins_selected : list[pin]) -> None:
    if not left_click :
        return
    if len(pins_selected) == 0:
        pins_selected.append(pin)
    elif pins_selected[0] != pin:
        pins_selected.append(pin)

def pop_pin_logic(right_click : bool, pins_selected : list[pin]):
    if right_click:
        if len(pins_selected) != 0:
            pins_selected.pop()

def pin_draw_logic(pins_selected : list[pin], mouse_pos : tuple[int,int], screen : pygame.surface.Surface) -> None:
    if len(pins_selected) == 0:
        return
    elif len(pins_selected) == 1: 
        start_pos : tuple[int,int] = (pins_selected[0].screen_position[0] + int(pins_selected[0].scaling/2), pins_selected[0].screen_position[1]+ int(pins_selected[0].scaling/2))
        pygame.draw.line(screen, pins_selected[0].color_value, start_pos, mouse_pos, ceil(pins_selected[0].scaling/2))
    else :
        start_pos : tuple[int,int] = (pins_selected[0].screen_position[0] + int(pins_selected[0].scaling/2), pins_selected[0].screen_position[1]+ int(pins_selected[0].scaling/2))
        end_pos  : tuple[int,int] = (pins_selected[1].screen_position[0] + int(pins_selected[1].scaling/2), pins_selected[1].screen_position[1]+ int(pins_selected[1].scaling/2))
        pygame.draw.line(screen, pins_selected[0].color_value, start_pos, end_pos, ceil(pins_selected[0].scaling/2))

def sort_pins(pins : list[pin]):
    
    linear_positions = []
    
    for pin_ in pins:
        linear_positions.append(pin_.position[0]+pin_.position[1]*pin_.maze_width)
    
    sorted_pins : list[pin] = [x for _, x in sorted(zip(linear_positions, pins))]
    return sorted_pins

def n_colored_pins(pins : list[pin], color : str) -> int:
    n :  int = 0
    for pin_ in pins:
        if pin_.color == color:
            n = n+1
    return n

def check_win_state(pins : list[pin], selected_pins : list[pin], serial_number : int) -> bool:
    """
    Return true if a winning state is achieved, false otherwise\n
    pins must be already sorted

    Args:
        pins (list[pin]): list of all pins
        selected_pins (list[pin]): pair of selected pins
        serial_number (int): serial number of the engine

    Returns:
        bool: True if you won, false otherwise
    """
    
    unordered_pins : set[pin] = set(selected_pins)
    
    match len(pins):
        case 3:
            return check_win_state_3(pins, unordered_pins)
        case 4:
            return check_win_state_4(pins, unordered_pins, serial_number)
        case 5:
            return check_win_state_5(pins, unordered_pins, serial_number)
        case 6: 
            return check_win_state_6(pins, unordered_pins, serial_number)

def check_win_state_3(pins : list[pin], selected_pins : set[pin]) -> bool:
    #If there are no red pins connect second and third pin
    if n_colored_pins(pins, "red") == 0:
        return {pins[1],pins[2]} == selected_pins
    #Otherwise, if there is more than one blue pin, connect first blue pin and last blue pin
    elif n_colored_pins(pins, "blue") > 1:
        blue_pins : list[pin] = [pin_ for pin_ in pins if pin_.color == "blue"]
        return {blue_pins[0],blue_pins[-1]} == selected_pins
    #Otherwise, connect first and second pin
    else:
        return {pins[0], pins[1]} == selected_pins

def check_win_state_4(pins : list[pin], selected_pins : set[pin], serial_number:int) -> bool:
    #If there is more than one red wire and the last digit of the serial number is odd, connect first pin and last red pin. 
    n_red_pins = n_colored_pins(pins, "red")
    if n_red_pins > 1 and serial_number%2!=0:  
        red_pins : list[pin] = [pin_ for pin_ in pins if pin_.color=="red"]
        return {pins[0], red_pins[-1]} == selected_pins
    #Otherwise, if the last pin is yellow and there are no red pins, connect second pin and last pin
    elif pins[-1].color == "yellow" and n_red_pins == 0:
        return {pins[1],pins[-1]} == selected_pins
    #Otherwise, if there is exactly one blue pin, connect second pin and third pin
    elif n_colored_pins(pins, "blue") == 1:
        return {pins[1], pins[2]} == selected_pins
    #Otherwise, if there is more than one yellow pin, connect third pin and last pin
    elif n_colored_pins(pins, "yellow") > 1:
        return {pins[2], pins[-1]} == selected_pins
    #Otherwise, connect first pin and third pin
    else:
        return {pins[0],pins[2]} == selected_pins

def check_win_state_5(pins : list[pin], selected_pins : set[pin], serial_number:int) -> bool:
    # If the last pin is purple and the last digit of the serial number is odd, connect the third and fourth pin
    if pins[-1].color == "purple" and serial_number%2==1:
        return {pins[2], pins[3]} == selected_pins
    # Otherwise, if there is exactly one red pin and there is more than one yellow pin, connect first pin and second pin
    elif n_colored_pins(pins, "red") == 1 and n_colored_pins(pins, "yellow") > 1:
        return {pins[0], pins[1]} == selected_pins
    # Otherwise, if there are no purple pins, connect second pin and fifth pin
    elif n_colored_pins(pins, "purple") == 0:
        return {pins[1], pins[4]} == selected_pins
    # Otherwise, connect fourth pin and fifth pin
    else:
        return {pins[3], pins[4]} == selected_pins

def check_win_state_6(pins : list[pin], selected_pins : set[pin], serial_number:int) -> bool: 
    n_yellow_pin : int = n_colored_pins(pins, "yellow")
    #If there are no yellow pin and the last digit of the serial number is odd, connect third pin and sixth pin
    if n_yellow_pin == 0 and serial_number%2==1:
        return {pins[2], pins[5]} == selected_pins
    #Otherwise, if there is exactly one yellow pin and there is more than one cyan pin, connect fourth pin and sixth pin
    elif n_yellow_pin == 1 and n_colored_pins(pins, "cyan") > 1:
        return {pins[3], pins[5]} == selected_pins
    #Otherwise, if there are no red wires, connect first pin and second pin
    elif n_colored_pins(pins,"red") == 0:
        return {pins[0], pins[1]} == selected_pins
    #Otherwise, connect second pin and fifth pin
    else:
        return {pins[1], pins[4]} == selected_pins