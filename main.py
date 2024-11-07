import pygame
import pygame.freetype
import time
from pygame.sprite import Sprite
from pygame.rect import Rect
from enum import Enum
from Level import *

BLUE = (106, 159, 181)
WHITE = (255, 255, 255)
GREEN = (0, 102, 51)
RED = (204, 0, 0)

# Initialize pygame and font at the top to avoid errors
pygame.init()
pygame.font.init()
fount = "New folder/JainiPurva-Regular.ttf"

try:
    font = pygame.font.Font("C:/Users/ANYA/ProgLang/ProgLang-M3/New folder/JainiPurva-Regular.ttf", 32)
except pygame.error as e:
    print("Error loading font:", e)
    font = pygame.font.Font(None, 32)  # Default fallback

def create_surface_with_text(text, font_size, text_rgb, bg_rgb=None):
    """Returns surface with text written on it."""
    
    font = pygame.font.Font(fount, font_size)

    if bg_rgb is None:
        surface = font.render(text, True, text_rgb, None)
    else:
        surface = font.render(text, True, text_rgb, bg_rgb)

    return surface.convert_alpha()  # Ensure surface supports transparency


class UIElement(Sprite):
    def __init__(self, center_position, text, font_size, bg_rgb, text_rgb, action=None):
        self.mouse_over = False
        default_image = create_surface_with_text(text, font_size, text_rgb, bg_rgb)
        highlighted_image = create_surface_with_text(text, int(font_size * 1.2), text_rgb, bg_rgb)
        self.images = [default_image, highlighted_image]
        self.rects = [default_image.get_rect(center=center_position),
                      highlighted_image.get_rect(center=center_position)]
        self.action = action
        super().__init__()

    @property
    def image(self):
        return self.images[1] if self.mouse_over else self.images[0]

    @property
    def rect(self):
        return self.rects[1] if self.mouse_over else self.rects[0]

    def update(self, mouse_pos, mouse_up):
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
            if mouse_up:
                return self.action
        else:
            self.mouse_over = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)

def title_screen(screen):
     
    title1_font = pygame.font.SysFont("Inter", 34, bold=True)  # Larger font for title
    title1_text = title1_font.render("THE RISE OF THE", True, WHITE)
    title1_rect = title1_text.get_rect(center=(400,200))  # Position at the top center
    
    title_font = pygame.font.Font(fount, 90)  # Larger font for title
    title_text = title_font.render("EIGENVAMPIRE", True, WHITE)
    title_rect = title_text.get_rect(center=(400, 240))  # Position at the top center
    
    background = pygame.image.load("New folder/mainbackground.png")
    animation = [pygame.image.load(f"New folder/main{i}.png") for i in range(1, 4)]
    #New folder\main1.png

    start_btn = UIElement((400, 400), "START", 60, None,WHITE, action=GameState.NEWGAME)
    quit_btn = UIElement((400, 450), "QUIT GAME", 30, None, WHITE, action=GameState.QUIT)
    buttons = [start_btn, quit_btn]

    
    frame = 0 
    frame_delay = 10  
    delay_counter = 0 
    clock = pygame.time.Clock()

    while True:
        mouse_up = False


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.QUIT
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True

        # Update animation frame based on the delay counter
        delay_counter += 1
        if delay_counter >= frame_delay:
            frame = (frame + 1) % len(animation)  # Cycle to the next frame
            delay_counter = 6 # Reset the counter

        # Clear the screen with the background
        screen.blit(background, (0, 0))
        # Display animation frame
        screen.blit(animation[frame], (0,0))

        # Display title text
        screen.blit(title_text, title_rect)
        screen.blit(title1_text,title1_rect)

        # Draw buttons and handle button interactions
        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action:
                return ui_action
            button.draw(screen)

        pygame.display.flip()  # Update the display
        clock.tick(30)  # Control the screen refresh rate (frame rate)

def play_level(screen):
    return_btn = UIElement((680, 60), "Main Menu", 30, None, WHITE, action=GameState.TITLE)
    background = pygame.image.load("New folder/mainbackground.png")
    
    level = Level(screen)

    clock = pygame.time.Clock()
    while True:
        # Clear the screen and redraw the background first to prevent blinking
        screen.blit(background, (0, 0))  

        # Handle events
        event_list = pygame.event.get()
        if level.player.currentHealth <= 0:
            return GameState.GAMEOVER

        # Process level updates
        res = level.mainloop(event_list)
        if res == GameState.FINISH:
            return res  # Handle finish state (e.g., next level or victory)

        # Mouse interaction for buttons
        mouse_up = False
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        
        # Handle button update and check if clicked
        ui_action = return_btn.update(pygame.mouse.get_pos(), mouse_up)
        if ui_action:
            return ui_action  # Return the action (e.g., go to main menu)

        # Draw the button on top of the background (after everything else)
        return_btn.draw(screen)

        # Update the screen
        pygame.display.flip()

        # Control the frame rate
        clock.tick(60)


def loading_screen(screen):
    # Load and display the background image
    background = pygame.image.load("New folder/loadingbg.png") #
    animation = [pygame.image.load(f"New folder/load ({i}).png") for i in range(1, 4)]
    screen.blit(background, (0,0))
    start_time = time.time()
    clock = pygame.time.Clock()
        
    frame = 0 
    frame_delay = 10  
    delay_counter = 0 
    clock = pygame.time.Clock()

    pygame.display.update()

    title1_font = pygame.font.Font(fount, 50)  # Larger font for title
    title1_text = title1_font.render("Game Loading...", True, WHITE)
    title1_rect = title1_text.get_rect(center=(200,490))  # Position at the top center

    loading_words = ["releasing the bats..."]
    
    
    # Create the Quit button
    return_btn = UIElement((680, 60), "Main Menu", 30, None, WHITE, action=GameState.TITLE)
    buttons = [return_btn]

    # Set up a clock for managing the frame rate
    clock = pygame.time.Clock()

    while True:
        mouse_up = False
        elapsed_time = time.time() - start_time

        delay_counter += 1
        if delay_counter >= frame_delay:
            frame = (frame + 1) % len(animation)  # Cycle to the next frame
            delay_counter = 6 # Reset the counter

        # Exit loading screen after 3 seconds
        if elapsed_time >= 5:
            return  # Exit the function to continue to the game

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.QUIT
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True

        # Clear the screen and display the background image again
        screen.blit(background, (0, 0))
        screen.blit(title1_text, title1_rect)
        screen.blit(animation[frame], (0,0))

        # Draw and update buttons
        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action:
                return ui_action  # Return the action associated with the button (GameState.QUIT)
            button.draw(screen)

        # Update the display and control the frame rate
        pygame.display.flip()
        clock.tick(30)  # Set the frame rate to 30 FPS
        
def game_over(screen):
    background = pygame.image.load("New folder/gameover.png")
    title1_font = pygame.font.Font(fount, 50)  # Larger font for title
    title1_text = title1_font.render("GAME OVER!", True, WHITE)
    title1_rect = title1_text.get_rect(center=(400, 300))  # Position at the top center

    # Define buttons
    start_btn = UIElement((400, 400), "START", 60, None, WHITE, action=GameState.NEWGAME)
    quit_btn = UIElement((400, 450), "QUIT GAME", 30, None, WHITE, action=GameState.QUIT)
    buttons = [start_btn, quit_btn]

    while True:
        mouse_up = False

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.QUIT
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True

        # Clear the screen and display the background image again
        screen.blit(background, (0, 0))
        screen.blit(title1_text, title1_rect)

        # Update buttons and check if clicked
        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action:
                return ui_action  # Return action (NEWGAME or QUIT)
            button.draw(screen)

        # Update the screen
        pygame.display.flip()
        


def finish_level():
    pass
    
def main():
    screen = pygame.display.set_mode((800, 600))
    game_state = GameState.TITLE
    while True:
        if game_state == GameState.TITLE:
            game_state = title_screen(screen)
        elif game_state == GameState.NEWGAME:
            # Display the loading screen before starting the new game
            game_state = loading_screen(screen)
            if game_state != GameState.QUIT:  # Ensure the user hasn't quit from the loading screen
                game_state = play_level(screen)
        elif game_state == GameState.FINISH:
            game_state = finish_level()
        elif game_state == GameState.QUIT:
            pygame.quit()
            return
        
if __name__ == "__main__":
    main() 