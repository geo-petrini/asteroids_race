import pygame
import random

def calc_x_textual_position(pos, screen_width, object_width):
    x = 0
    if pos == 'LEFT':
        x = 0
    if pos == 'CENTER':
        x = (screen_width - object_width) // 2
    if pos == 'RIGHT':
        x = screen_width - object_width
    if pos == 'RANDOM':
        x = random.randint(0, screen_width)    
    return x

def calc_y_textual_position(pos, screen_height, object_height):
    y = 0
    if pos == 'TOP':
        y = 0
    if pos == 'CENTER':
        y = (screen_height - object_height) // 2
    if pos == 'BOTTOM':
        y = screen_height - object_height
    if pos == 'RANDOM':
        y = random.randint(0, screen_height) 
    return y

def calc_textual_position(surface, position):
    screen_width, screen_height = get_window_size()
    position_x, position_y = position
    x = 0
    y = 0
    if isinstance(position_x, str):
        x = calc_x_textual_position(position_x, screen_width, surface.get_width())
    if isinstance(position_x, int):
        x = position_x     

    if isinstance(position_y, str):
        y = calc_y_textual_position(position_y, screen_height, surface.get_height())
    if isinstance(position_y, int):
        y = position_y

    return (x, y)

def get_window_size():
    return pygame.display.get_surface().get_size()