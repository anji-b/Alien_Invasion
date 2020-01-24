# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 17:05:24 2020

@author: abusara
"""

class Settings():
    """A class to store all settings for Alien Invasion."""
    def __init__(self):
        """Initialize the game's static settings"""
        #Screen settings
        self.screen_width = 800
        self.screen_height = 450
        self.bg_color = (230, 230, 230)
        
        #Bullet settings
        self.bullet_width = 7
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 30
        
        #Alien settings
        self.fleet_drop_speed = 60
        
        #Ship settings
        self.ship_limit = 1
        
        #How quickly game speeds up
        self.speedup_scale = 1.1
        
        #How quickly alien points increase.
        self.score_scale = 1.5
        
        self.initialize_dynamic_settings()
        
    def initialize_dynamic_settings(self):
        """Initialize the settings that change througout the game."""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        
        #Fleet directoin 1 represents right; -1 represents left
        self.fleet_direction = 1
        
        #scoring
        self.alien_points = 50
        
    def increase_speed(self):
        """Increase speed settings and alien points."""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)