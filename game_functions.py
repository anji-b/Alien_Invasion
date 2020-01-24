# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 19:04:11 2020

@author: abusara
"""

import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

def check_key_down_events(event, ai_settings, screen, ship, bullets):
    """Resopnd to key presses."""
    if event.key == pygame.K_RIGHT:
         ship.moving_right = True
    elif event.key == pygame.K_LEFT:
         ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def fire_bullet(ai_settings, screen, ship, bullets):
    """Fire a bullet if limit is not reachet"""
    #Create a new bullet and add it to the bullets group.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
        
def check_key_up_events(event, ship):
    """Respond to key releases."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings, screen, stats, play_button, ship, aliens,
                 bullets):
    """Respond to key presses and mouse movement."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, play_button, 
                              ship, aliens, bullets, mouse_x, mouse_y)
        elif event.type == pygame.KEYDOWN:
           check_key_down_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_key_up_events(event, ship)

def check_play_button(ai_settings, screen, stats, play_button, ship, aliens,
                      bullets, mouse_x, mouse_y):
    """Start new game when player clicks play button."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        #Reset the game settings
        ai_settings.initialize_dynamic_settings()
        
        #Hide the mouse cursor
        pygame.mouse.set_visible(False)
        
        #Reset the game statistics.
        stats.reset_stats()
        stats.game_active = True
        
        #Empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()
        
        #Create new fleet and center the ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
            

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    #Redraw the screen during each pass through the loop.
    screen.fill(ai_settings.bg_color)
    
    #Redraw all bullets behind ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    
    ship.blitme()
    aliens.draw(screen)
    
    #Draw the score information.
    sb.show_score()
    
    #Draw the play button if the game is inactive
    if not stats.game_active:
        play_button.draw_button()
    
    #Make the most recently drawn screen visible.
    pygame.display.flip()
    
def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Update position of the bullets and get rid of old bullets."""
    #update bullet's position
    bullets.update()
        
    #Get rid of bullets that have disappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <=0:
            bullets.remove(bullet)
    
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, 
                                  aliens, bullets)

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, 
                                  aliens, bullets):
    """Respond to bullet-alien collosions."""
    #Remove any aliens and bullets that have collided
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
    
    if len(aliens) == 0:
        #Destroy existing bullets, speed the game and create new fleet
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, ship, aliens)
    
def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien and place it in the row."""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def get_number_aliens_x(ai_settings, alien_width):
    """Determine the number of aliens fit in a row."""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen."""
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_fleet(ai_settings, screen, ship, aliens):
    """Create full fleet of aliens."""
    #create an alien and find number of aliens in a row.
    #Spacing between each alien is equal to the one align width
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    
    #Create fleet of aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)
            
def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
    """
    Check if fleet at an edge,
     and then update the positions of all aliens in the fleet.
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    
    #Look for alien-ship collisions
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
    
    #Look for aliens hitting the bottom of the screen
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)

def check_fleet_edges(ai_settings, aliens):
    """Respond appropriatly if any alien reached an edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet and change the fleet direction."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1
    
def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    """Respond to ship being hit by an alien."""
    if stats.ships_left > 0:
        #Decrement ships left
        stats.ships_left -= 1
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
    
    #Empty the list of aliens and bullets
    aliens.empty()
    bullets.empty()
    
    #Create a new fleet and center the ship
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()
    
    #Pause
    sleep(0.5)

def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    """Check if any aliens reached bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
            break
    
    
    