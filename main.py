import pygame
import pygame.freetype
from pygame.sprite import Sprite
from pygame.rect import Rect
from enum import Enum
from Level import *

BLUE = (106, 159, 181)
WHITE = (255, 255, 255)

# Initialize pygame and font at the top to avoid errors
pygame.init()
pygame.font.init()
font = "C:/Users/ANYA/Downloads/New folder/JainiPurva-Regular.ttf"

try:
    font = pygame.font.Font("C:/Users/ANYA/Downloads/New folder/JainiPurva-Regular.ttf", 32)
except pygame.error as e:
    print("Error loading font:", e)
    font = pygame.font.Font(None, 32)  # Default fallback

def create_surface_with_text(text, font_size, text_rgb, bg_rgb=None):
    """Returns surface with text written on it."""
    
    # Create the font object
    font = pygame.font.Font(fount, font_size)

    # Render the text, the second argument is for anti-aliasing (True)
    if bg_rgb is None:
        # If no background color is provided, render text without background
        surface = font.render(text, True, text_rgb)
    else:
        # If background color is provided, render text with background
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
     
    title1_font = pygame.font.SysFont("Inter", 24, bold=True)  # Larger font for title
    title1_text = title1_font.render("THE RISE OF THE", True, WHITE)
    title1_rect = title1_text.get_rect(center=(400, 250))  # Position at the top center
    
    title_font = pygame.font.Font(fount, 70)  # Larger font for title
    title_text = title_font.render("EIGENVAMPIRE", True, WHITE)
    title_rect = title_text.get_rect(center=(400, 280))  # Position at the top center
    
    # Load background and animation frames
    background = pygame.image.load("C:/Users/ANYA/Downloads/New folder/mainbackground.png")
    animation = [pygame.image.load(f"C:/Users/ANYA/Downloads/New folder/main{i}.png") for i in range(1, 4)]

    # Create buttons
    start_btn = UIElement((400, 410), "START", 60, BLUE, WHITE, action=GameState.NEWGAME)
    quit_btn = UIElement((400, 470), "QUIT GAME", 30, BLUE, WHITE, action=GameState.QUIT)
    buttons = [start_btn, quit_btn]

    # Frame animation control
    frame = 0  # To track the current frame
    frame_delay = 10  # Frame delay (higher = slower animation)
    delay_counter = 0  # Counter for delaying frame changes
    clock = pygame.time.Clock()

    while True:
        mouse_up = False

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.QUIT
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True

        # Update animation frame based on the delay counter
        delay_counter += 1
        if delay_counter >= frame_delay:
            frame = (frame + 1) % len(animation)  # Cycle to the next frame
            delay_counter = 6  # Reset the counter

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
    return_btn = UIElement((140, 570), "Return to main menu", 20, BLUE, WHITE, action=GameState.TITLE)
    level = Level(screen)
    clock = pygame.time.Clock()
    while True:
        event_list = pygame.event.get()
        if level.player.currentHealth <= 0:
            return GameState.TITLE
        res = level.mainloop(event_list)
        if res == GameState.FINISH:
            return res
        mouse_up = False
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        ui_action = return_btn.update(pygame.mouse.get_pos(), mouse_up)
        if ui_action:
            return ui_action
        return_btn.draw(screen)
        clock.tick(60)
        pygame.display.flip()

def main():
    screen = pygame.display.set_mode((800, 600))
    game_state = GameState.TITLE
    while True:
        if game_state == GameState.TITLE:
            game_state = title_screen(screen)
        elif game_state == GameState.NEWGAME:
            game_state = play_level(screen)
        elif game_state == GameState.FINISH:
            game_state = finish_level(screen)
        elif game_state == GameState.QUIT:
            
            pygame.quit()
            return

if __name__ == "__main__":
    main()
