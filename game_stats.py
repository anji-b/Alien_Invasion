# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 10:41:29 2020

@author: abusara
"""

class GameStats():
    """Tract statistics for alien invasion."""
    def __init__(self, ai_settings):
        """Initialize statistics."""
        self.ai_settings = ai_settings
        self.reset_stats()
        
        #Start Alien Invation in active state
        self.game_active = False
    
    def reset_stats(self):
        """Initialize stas that can change during the game."""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
