# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 11:07:34 2020

@author: abusara
"""

import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A class to manage bullets fired from the ship."""
    
    def __init__(self, ai_settings, screen, ship):
        """Create a bullet object at the ship's current position."""
        super().__init__()
        self.screen = screen
        
        #Create bullet at (0,0) and move it to correct position
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        
        #Store bullet's position as decimal value
        self.y = float(self.rect.y)
        
        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor
        
    def update(self):
        """Move bullets up the screen."""
        #Update the decimal position of the bullet.
        self.y -= self.speed_factor
        #Update the rect position
        self.rect.y = self.y
        
    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)
        