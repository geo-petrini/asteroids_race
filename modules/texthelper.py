import pygame
from modules.positionhelper import calc_textual_position
from modules.positionhelper import get_window_size

class TextRenderer:
    TOP='TOP'
    CENTER='CENTER'
    BOTTOM='BOTTOM'
    RANDOM='RANDOM'
    LEFT= 'LEFT'
    RIGHT= 'RIGHT'
    _lines = []
    position = (TOP, LEFT)
    margin = 0

    def __init__(self, font, color='WHITE'):
        self.font = font
        self.color = color

    @property
    def text(self):
        return '\n'.join(self.lines)
    
    @property
    def lines(self):
        return self._lines
    
    @lines.setter
    def lines(self, lines):
        if not isinstance(lines, list):
            lines = [lines]
        self._lines = lines
    
    def setPosition(self, x, y):
        self.position = (x, y)


    def __generate_text(self):
        text_elements = []
        for i, line in enumerate(self.lines):
            text_surface = self.font.render(line, True, self.color)
            text_rect = text_surface.get_rect()
            new_rect_x = 0  #TODO text align
            if i == 0:
                new_rect_y = 0 
            else:
                previous_text_rect =  text_elements[i-1][1]
                previous_text_rect_y = previous_text_rect.y
                previous_text_rect_height = previous_text_rect.height
                new_rect_y = previous_text_rect_y + previous_text_rect_height

            new_rect_x += self.margin
            new_rect_y += self.margin
            text_rect.move_ip( new_rect_x, new_rect_y) 

            element = (text_surface, text_rect)
            text_elements.append( element )   
        return text_elements
    
    def __generate_text_surface(self, text_elements):
        surface_width = 0
        surface_height = 0

        for element in text_elements:
            text_rect = element[1]
            if text_rect.width >surface_width: surface_width = text_rect.width

        surface_height = text_elements[-1][1].bottomleft[1]
        # print(f'surface w: {surface_width}, h: {surface_height}')

        surface = pygame.Surface((surface_width, surface_height), pygame.SRCALPHA)
        return surface

    def __blit_text(self, surface, text_elements):
        for element in text_elements:
            text_surface, text_rect = element
            surface.blit(text_surface, text_rect)
           
    def render(self, screen):
        text_elements = self.__generate_text()
        surface = self.__generate_text_surface(text_elements)
        self.__blit_text(surface, text_elements)
        position = calc_textual_position(surface , self.position )
        screen.blit( surface, position)
        


