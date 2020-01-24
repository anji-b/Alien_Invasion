# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 14:13:36 2020

@author: abusara
"""

import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single align in the fleet."""
    
    def __init__(self, ai_settings, screen):
        """Initialize the align and set it's starting position."""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        
        #Load the alien image and set it's rect attribute
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()
        
        #Start each align on the top left corner of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        #Store the align's exact position
        self.x = float(self.rect.x)
        
    def blitme(self):
        """Draw the align at it's current location."""
        self.screen.blit(self.image, self.rect)
        
    def update(self):
        """Move the alien right."""
        self.x += (self.ai_settings.alien_speed_factor * 
                   self.ai_settings.fleet_direction)
        self.rect.x = self.x
    
    def check_edges(self):
        """Return True if alien is at edge of the screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True