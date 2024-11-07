import pygame
import pygame.freetype
import random

from pygame.sprite import *
from pygame.rect import *
from enum import Enum
from Level import *
from GameState import *

# Title Screen Function
def title_screen(window):
    font = pygame.freetype.SysFont("Blackadder ITC", 50)
    title_font = pygame.freetype.SysFont("Blackadder ITC", 150)

    # Colors
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)

    # Title Text
    title_font.render_to(window, (300, 100), "Rise of the Eigenvampire", red)

    # Buttons and their positions
    start_button = pygame.Rect(650, 400, 200, 80)
    quit_button = pygame.Rect(650, 550, 200, 80)
    
    running = True
    while running:
        window.fill(black)
        title_font.render_to(window, (100, 100), "Rise of the Eigenvampire", red)
        
        # Draw buttons
        pygame.draw.rect(window, white, start_button)
        pygame.draw.rect(window, white, quit_button)
        
        # Render button text
        font.render_to(window, (start_button.x + 50, start_button.y + 20), "Start", black)
        font.render_to(window, (quit_button.x + 50, quit_button.y + 20), "Quit", black)

        pygame.display.flip()

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.QUIT
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    running = False
                    return GameState.NEWGAME
                elif quit_button.collidepoint(event.pos):
                    return GameState.QUIT

def play_level(window):
    level = Level(window)
    game_state = GameState.NEWGAME
    while game_state == GameState.NEWGAME:
        # event_list = pygame.event.get()
        # for event in event_list:
        #     if event.type == pygame.QUIT:
        #         return GameState.QUIT

        # Run the level main loop
        game_state = level.mainloop()
        
    return game_state

def main():
    pygame.init()

    window = pygame.display.set_mode((1500, 900))
    pygame.display.set_caption("Rise of the Eigenvampire")

    game_state = GameState.TITLE

    while True:
        if game_state == GameState.TITLE:
            game_state = title_screen(window)
        
        if game_state == GameState.NEWGAME:
            game_state = play_level(window)
        
        if game_state == GameState.FINISH:
            game_state = finish_level(window)  # Assuming a finish screen exists
        
        if game_state == GameState.QUIT:
            pygame.quit()
            return
    

if __name__ == "__main__":
    main()