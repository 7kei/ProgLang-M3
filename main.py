import pygame
import pygame.freetype
import time
import sys
from pygame.sprite import Sprite
from pygame.rect import Rect
from enum import Enum
from Level import *


BLUE = (106, 159, 181)
WHITE = (255, 255, 255)
GREEN = (0, 102, 51)
RED = (204, 0, 0)

pygame.init()
pygame.font.init()
fount = "New folder/JainiPurva-Regular.ttf"
player_name =""

try:
    font = pygame.font.Font("C:/Users/ANYA/ProgLang/ProgLang-M3/New folder/JainiPurva-Regular.ttf", 32)
except pygame.error as e:
    print("Error loading font:", e)
    font = pygame.font.Font(None, 32) 

def create_surface_with_text(text, font_size, text_rgb, bg_rgb=None):
    """Returns surface with text written on it."""
    
    font = pygame.font.Font(fount, font_size)

    if bg_rgb is None:
        surface = font.render(text, True, text_rgb, None)
    else:
        surface = font.render(text, True, text_rgb, bg_rgb)

    return surface.convert_alpha() 


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


def confirm_quit(screen):

    background = pygame.image.load("New folder/exitquestion.png")

    BLACK = (0, 0, 0)
    BEIGE = (253,226,146)

    title_font = pygame.font.Font(fount, 30)
    title_text = title_font.render("ARE YOU SURE YOU WANT", True, BLACK)
    title2_text = title_font.render("TO QUIT THE GAME?", True, BLACK)
    title_rect = title_text.get_rect(center=(410, 270))
    title2_rect = title2_text.get_rect(center=(410, 300))
    
    no_btn = UIElement((475, 340), "NO", 30, None, BLACK, action=GameState.TITLE)
    yes_btn = UIElement((340, 340), "YES", 30, None, BLACK, action=GameState.QUIT)
    buttons =[no_btn, yes_btn]

    while True:

        mouse_up = False  # Reset mouse_up at the beginning of each frame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        
        screen.blit(background, (0, 0))

        screen.blit(title_text, title_rect)
        screen.blit(title2_text, title2_rect)

        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action:
                return ui_action
            button.draw(screen)

        pygame.display.flip()




def title_screen(screen):
    title1_font = pygame.font.SysFont("Inter", 34, bold=True)
    title1_text = title1_font.render("THE RISE OF THE", True, WHITE)
    title1_rect = title1_text.get_rect(center=(400, 200))

    title_font = pygame.font.Font(fount, 90)
    title_text = title_font.render("EIGENVAMPIRE", True, WHITE)
    title_rect = title_text.get_rect(center=(400, 240))

    background = pygame.image.load("New folder/mainbackground.png")
    animation = [pygame.image.load(f"New folder/main{i}.png") for i in range(1, 4)]

    start_btn = UIElement((400, 400), "START", 60, None, WHITE, action=GameState.NEWGAME)
    quit_btn = UIElement((400, 490), "QUIT GAME", 30, None, WHITE, action=GameState.QUIT)
    leaderboard_btn = UIElement((400, 450), "LEADERBOARD", 30, None, WHITE, action=GameState.LEADERBOARD)
    buttons = [start_btn, quit_btn, leaderboard_btn]

    frame = 0
    frame_delay = 10
    delay_counter = 0
    clock = pygame.time.Clock()

    while True:
        mouse_up = False  # Reset mouse_up at the beginning of each frame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if confirm_quit(screen):
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True

        delay_counter += 1
        if delay_counter >= frame_delay:
            frame = (frame + 1) % len(animation)
            delay_counter = 6

        screen.blit(background, (0, 0))
        screen.blit(animation[frame], (0, 0))
        screen.blit(title_text, title_rect)
        screen.blit(title1_text, title1_rect)

        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action:
                return ui_action
            button.draw(screen)

        pygame.display.flip()
        clock.tick(30)



def play_level(screen):
    return_btn = UIElement((680, 60), "Main Menu", 30, None, WHITE, action=GameState.TITLE)
    background = pygame.image.load("New folder/mainbackground.png")
    
    level = Level(screen)

    clock = pygame.time.Clock()
    while True:

        screen.blit(background, (0, 0))  

        event_list = pygame.event.get()
        if level.player.currentHealth <= 0:
            return GameState.GAMEOVER

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
        pygame.display.flip()
        clock.tick(60)


def loading_screen(screen):
    
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

    title1_font = pygame.font.Font(fount, 50) 
    title1_text = title1_font.render("Game Loading...", True, WHITE)
    title1_rect = title1_text.get_rect(center=(200,490))  

    loading_words = ["releasing the bats..."]
    
    clock = pygame.time.Clock()

    while True:
        mouse_up = False
        elapsed_time = time.time() - start_time

        delay_counter += 1
        if delay_counter >= frame_delay:
            frame = (frame + 1) % len(animation) 
            delay_counter = 6 
        if elapsed_time >= 5:
            return 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.QUIT
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True

        screen.blit(background, (0, 0))
        screen.blit(title1_text, title1_rect)
        screen.blit(animation[frame], (0,0))
        pygame.display.flip()
        clock.tick(30)  

def leaderboard(screen):
    background = pygame.image.load("New folder/mainbackground.png")
    screen.blit(background, (0, 0)) 
    start_btn = UIElement((110, 70), "MAIN MENU", 30, None,WHITE, action=GameState.TITLE)
    quit_btn = UIElement((690, 70), "QUIT GAME", 30, None, WHITE, action=GameState.QUIT)
    buttons = [start_btn, quit_btn]

  
    title1_font = pygame.font.Font(fount,60)  # Larger font for title
    title1_text = title1_font.render("LEADERBOARD", True, WHITE)
    title1_rect = title1_text.get_rect(center=(400,150))  # Position at the top center

    while True:
        mouse_up = False  # Reset mouse_up at the beginning of each frame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if confirm_quit(screen):
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        screen.blit(background, (0, 0))

        screen.blit(title1_text, title1_rect)

        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action:
                return ui_action
            button.draw(screen)

        pygame.display.flip()



def story_screen(screen):

    background = pygame.image.load("New folder/mainbackground.png")
    screen.blit(background, (0, 0)) 
    

    game_state = GameState.STORY

    title1_font = pygame.font.Font(fount,60)  # Larger font for title
    title1_text = title1_font.render("", True, WHITE)
    title1_rect = title1_text.get_rect(center=(400,150))  # Position at the top center

    while True:
        mouse_up = False
        screen.blit(background, (0, 0))
        screen.blit(title1_text, title1_rect)
        pygame.display.flip()

def game_over(screen):
    background = pygame.image.load("New folder/gameover.png")
    title1_font = pygame.font.Font(fount, 90)  # Larger font for title
    title1_text = title1_font.render("GAME OVER!", True, WHITE)
    title1_rect = title1_text.get_rect(center=(400, 300))  # Position at the top center

    start_btn = UIElement((400, 400), "RETRY", 60, None, WHITE, action=GameState.NEWGAME)
    return_btn = UIElement((110, 70), "MAIN MENU", 30, None, WHITE, action=GameState.TITLE)
    quit_btn = UIElement((690, 70), "QUIT GAME", 30, None, WHITE, action=GameState.QUIT)
    leaderboard_btn = UIElement((400, 450), "LEADERBOARD", 30, None, WHITE, action=GameState.LEADERBOARD)
    buttons = [start_btn, quit_btn, leaderboard_btn,return_btn]


    while True:
        mouse_up = False  # Reset mouse_up at the beginning of each frame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if confirm_quit(screen):
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True

        screen.blit(background, (0, 0))
        screen.blit(title1_text, title1_rect)

        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action:
                return ui_action
            button.draw(screen)

        pygame.display.flip()



def finish_level():
    pass

def player_name_screen(screen):
    global player_name

    background = pygame.image.load("New folder/storytime.png")
    screen.blit(background, (0, 20))

    title_font = pygame.font.Font(fount, 50)
    title_text = title_font.render("Who's there?", True, WHITE)
    title_rect = title_text.get_rect(center=(400, 250))
    screen.blit(title_text, title_rect)


    input_font = pygame.font.Font(fount, 32)
    input_box = pygame.Rect(300, 300, 200, 40)
    color_inactive = pygame.Color(WHITE)
    color_active = pygame.Color(BLUE)
    color = color_inactive
    active = False
    text = ''

    clock = pygame.time.Clock()
    
    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        player_name = text
                        return GameState.TITLE
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.blit(background, (0, 0))
        screen.blit(title_text, title_rect)

        txt_surface = input_font.render(text, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)

        pygame.display.flip()
        clock.tick(30)


def main():
    screen = pygame.display.set_mode((800, 600))
    game_state = GameState.TITLE
    while True:
        if game_state == GameState.TITLE:
            game_state = title_screen(screen)
        elif game_state == GameState.NEWGAME:
            game_state = loading_screen(screen)
            game_state = player_name_screen(screen)  # Add player name screen before starting
            if game_state == GameState.TITLE:
                game_state = loading_screen(screen)
                if game_state != GameState.QUIT:  # Ensure the user hasn't quit from the loading screen
                    game_state = play_level(screen)
        elif game_state == GameState.FINISH:
            game_state = finish_level()
        elif game_state == GameState.QUIT: 
            pygame.quit()
            sys.exit()
        elif game_state == GameState.GAMEOVER:
            game_state = game_over(screen)
        elif game_state == GameState.LEADERBOARD:
            game_state = leaderboard(screen)

if __name__ == "__main__":
    main()
    
# def main():
#     screen = pygame.display.set_mode((800, 600))
#     game_state = GameState.TITLE
#     while True:
#         if game_state == GameState.TITLE:
#             game_state = title_screen(screen)
#         elif game_state == GameState.NEWGAME:
#             game_state = loading_screen(screen)
#             if game_state != GameState.QUIT:  # Ensure the user hasn't quit from the loading screen
#                 game_state = play_level(screen)
#         elif game_state == GameState.FINISH:
#             game_state = finish_level()
#         elif game_state == GameState.QUIT: 
#             pygame.quit()
#         elif game_state == GameState.GAMEOVER:
#             game_state = game_over(screen)
#             game_state = loading_screen(screen)
#         elif game_state == GameState.LEADERBOARD:
#             game_state = leaderboard(screen)
#             game_state = loading_screen(screen)

# if __name__ == "__main__":
#     main() 