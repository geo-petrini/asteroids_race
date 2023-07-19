import pygame
from modules.positionhelper import calc_textual_position
from modules.positionhelper import get_window_size

class GameObject(pygame.sprite.Sprite):

    def __init__(self, sprite, position=(0,0), scale=1, rotation=0):
        self._original_sprite = sprite
        self.scale = scale
        self.rotation = rotation

        self._scale()
        self._rotate()
        self.mask = pygame.mask.from_surface(self.sprite)
        self.setPosition(position)

    def _scale(self):
        if self.scale != 1:
            size = self._original_sprite.get_size()
            self.sprite = pygame.transform.scale(self._original_sprite, (int(size[0]*self.scale), int(size[1]*self.scale)))
        else:
            self.sprite = self._original_sprite

    def _rotate(self):
        if self.rotation != 0:
            size = self.sprite.get_size()
            rotated_sprite = pygame.transform.rotate(self.sprite, self.rotation)
            self.sprite = rotated_sprite
    
    @property
    def sprite(self):
        return self.image
    
    @sprite.setter
    def sprite(self, sprite):
        self.image = sprite
    
    @property
    def original_sprite(self):
        return self._original_sprite
    
    @property
    def x(self):
        return self.rect.x

    @x.setter
    def x(self, value):
        self.position = (value, self.position[1])
        self.setPosition(self.position)

    @property
    def y(self):
        return self.rect.y
    
    @y.setter
    def y(self, value):
        self.position = (self.position[0], value)
        self.setPosition(self.position)

    def setPosition(self, position):
        self.position = calc_textual_position(self.sprite, position)
        self.rect = self.sprite.get_rect()
        self.rect.move_ip(self.position)

    def render(self, screen):
        screen.blit(self.sprite, self.rect)
    
