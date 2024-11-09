import pygame
import pygame.freetype
import time
import sys
from pygame.sprite import *
from pygame.rect import *
from Database import *
from pygame.sprite import Sprite
from enum import Enum
from Level import *
from GameState import *

BLUE = (106, 159, 181)
WHITE = (255, 255, 255)
GREEN = (0, 102, 51)
RED = (204, 0, 0)

pygame.init()
pygame.font.init()

# Load the custom font once and store it as a font object
try:
    fount = pygame.font.Font("New folder/JainiPurva-Regular.ttf", 32)
    player_name = ""
except pygame.error as e:
    print("Error loading font:", e)
    fount = pygame.font.Font(None, 32)  # Default fallback

def create_surface_with_text(text, font_size, text_rgb, bg_rgb=None):
    """Returns surface with text written on it."""
    # Use the preloaded font object, resize it if necessary
    font = pygame.font.Font("New folder/JainiPurva-Regular.ttf", font_size)  # Create a font object with given size
    if bg_rgb is None:
        surface = font.render(text, True, text_rgb, None)
    else:
        surface = font.render(text, True, text_rgb, bg_rgb)
    return surface.convert_alpha()  # Ensure surface supports transparency


class UIElement(Sprite):
    def __init__(self, center_position, text, font_size, bg_rgb, text_rgb, action=None, ):
        self.mouse_over = False
        default_image = create_surface_with_text(text, font_size, text_rgb, bg_rgb)
        highlighted_image = create_surface_with_text(text, int(font_size * 1.2), RED, bg_rgb)
        self.images = [default_image, highlighted_image]
        self.rects = [
            default_image.get_rect(center=center_position),
            highlighted_image.get_rect(center=center_position)
        ]
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


def create_surface_with_text(text, font_size, text_rgb, bg_rgb=None):
    font = pygame.font.Font("New folder/JainiPurva-Regular.ttf", font_size)

    if bg_rgb is None:
        surface = font.render(text, True, text_rgb, None)
    else:
        surface = font.render(text, True, text_rgb, bg_rgb)

    return surface.convert_alpha()

def confirm_quit(screen):

    background = pygame.image.load("New folder/exitquestion.png")

    BLACK = (0, 0, 0)


    title_font = pygame.font.Font("New folder/JainiPurva-Regular.ttf", 30)
    title_text = title_font.render("ARE YOU SURE YOU WANT", True, BLACK)
    title2_text = title_font.render("TO QUIT THE GAME?", True, BLACK)
    title_rect = title_text.get_rect(center=(410, 270))
    title2_rect = title2_text.get_rect(center=(410, 300))

    
    
    no_btn = UIElement((475, 340), "NO", 30, None, BLACK, action=GameState.TITLE)
    yes_btn = UIElement((340, 340), "YES", 30, None, BLACK, action=GameState.QUIT)
    buttons = [no_btn, yes_btn]

    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True

        screen.blit(background, (0, 0))

        screen.blit(title_text, title_rect)
        screen.blit(title2_text, title2_rect)
        
        if no_btn.update(pygame.mouse.get_pos(), mouse_up):
            return ui_action
            
        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action:
                return ui_action
            button.draw(screen)

        pygame.display.flip()

def title_screen(screen):

    pygame.mixer.init()
    pygame.mixer.music.load("DavidKBD - Spooky Pack - Spooky Playtime-03 - Haunted Mansion.ogg")  # Replace with your actual music file path
    pygame.mixer.music.set_volume(0.5)  # Optional: Set volume to 50%
    pygame.mixer.music.play(-1)

    title1_font = pygame.font.SysFont("Inter", 34, bold=True)
    title1_text = title1_font.render("THE RISE OF THE", True, WHITE)
    title1_rect = title1_text.get_rect(center=(400, 200))

    title_font = pygame.font.Font("New folder/JainiPurva-Regular.ttf", 90)
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
        mouse_up = False
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

        if quit_btn.update(pygame.mouse.get_pos(), mouse_up):
            if confirm_quit(screen):  # Ask for confirmation before quitting
                pygame.quit()
                sys.exit()

        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action:
                return ui_action
            button.draw(screen)

        pygame.display.flip()
        clock.tick(30)
        

def play_level(screen, database: Database):

    pygame.mixer.init()
    pygame.mixer.music.load("mainbg.mp3")  # Replace with your actual music file path
    pygame.mixer.music.set_volume(0.5)  # Optional: Set volume to 50%
    pygame.mixer.music.play(-1)

    return_btn = UIElement((680, 60), "Main Menu", 30, None, WHITE, action=GameState.TITLE)
    background = pygame.image.load("New folder/mainbackground.png")
    
    pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    level = Level(screen, database)
    clock = pygame.time.Clock()
    
    while True:

        screen.blit(background, (0, 0))  

        event_list = pygame.event.get()
        if level.player.current_health <= 0:
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
    pygame.mixer.init()
    pygame.mixer.music.load("Thunderstorm sound effect.mp3")  # Replace with your actual music file path
    pygame.mixer.music.set_volume(0.5)  # Optional: Set volume to 50%
    pygame.mixer.music.play(-1)
    animation = [pygame.image.load(f"New folder/load ({i}).png") for i in range(1, 4)]
    animationbg = [pygame.image.load(f"New folder/loadingbg/{i}.png") for i in range(16, 23)]
    
    start_time = time.time()
    clock = pygame.time.Clock()

    frame = 0
    frame_delay = 10
    delay_counter = 0
    clock = pygame.time.Clock()

    frame = 0
    frame_delay = 10
    delay_counter = 0

    title1_font = pygame.font.Font("New folder/JainiPurva-Regular.ttf", 50)
    title1_text = title1_font.render("Game Loading...", True, WHITE)
    title1_rect = title1_text.get_rect(center=(200, 490))

    clock = pygame.time.Clock()

    while True:
        elapsed_time = time.time() - start_time
        delay_counter += 1
        if delay_counter >= frame_delay:
            frame = (frame + 1) % len(animation)
            delay_counter = 1
        if elapsed_time >= 1:
            return
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.QUIT
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        
        screen.blit(animationbg[frame], (0, 0))
        screen.blit(animation[frame], (0, 0))
        screen.blit(title1_text, title1_rect)
        pygame.display.flip()
        clock.tick(30)



def leaderboard(screen, database: Database):
    background = pygame.image.load("New folder/mainbackground.png")
    screen.blit(background, (0, 0)) 
    start_btn = UIElement((110, 70), "MAIN MENU", 20, None, WHITE, action=GameState.TITLE)
    quit_btn = UIElement((690, 70), "QUIT GAME", 20, None, WHITE, action=GameState.QUIT)
    buttons = [start_btn, quit_btn]

    subtitle_font = pygame.font.Font("New folder/JainiPurva-Regular.ttf", 30)
    subtitle1_text = subtitle_font.render("PLAYER", True, WHITE)
    subtitle1_rect = subtitle1_text.get_rect(center=(110, 150))
    subtitle2_text = subtitle_font.render("HITS", True, WHITE)
    subtitle2_rect = subtitle2_text.get_rect(center=(400, 150))
    subtitle3_text = subtitle_font.render("SECONDS", True, WHITE)
    subtitle3_rect = subtitle3_text.get_rect(center=(690, 150))

    game_state = GameState.LEADERBOARD

    to_blit = []

    title1_font = pygame.font.Font("New folder/JainiPurva-Regular.ttf", 60)
    title1_text = title1_font.render("LEADERBOARD", True, WHITE)
    title1_rect = title1_text.get_rect(center=(400, 70))
    to_blit.append((title1_text, title1_rect))

    leaderboard = database.getLeaderboard()
    sortByKill = sorted(leaderboard, key=lambda tup: tup[1], reverse=True)

    # Define scrolling parameters
    scroll_offset = 0
    max_display_count = 10  # Number of rows to display at a time
    row_height = 50
    max_scroll_offset = max(0, (len(sortByKill) - max_display_count) * row_height)

    def render_rows(offset):
        rendered = []
        for idx, entry in enumerate(sortByKill):
            y_position = 200 + (idx * row_height) - offset
            if 200 <= y_position <= screen.get_height():
                name_font = pygame.font.Font("New folder/JainiPurva-Regular.ttf", 30)
                name_text = name_font.render(entry[0], True, WHITE)
                name_rect = name_text.get_rect(center=(110, y_position))
                rendered.append((name_text, name_rect))

                kill_font = pygame.font.Font("New folder/JainiPurva-Regular.ttf", 30)
                kill_text = kill_font.render(str(entry[1]), True, RED)
                kill_rect = kill_text.get_rect(center=(400, y_position))
                rendered.append((kill_text, kill_rect))

                time_font = pygame.font.Font("New folder/JainiPurva-Regular.ttf", 20)
                time_text = time_font.render(str(entry[2]), True, WHITE)
                time_rect = time_text.get_rect(center=(690, y_position))
                rendered.append((time_text, time_rect))
        return rendered

    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
            if event.type == pygame.MOUSEWHEEL:
                scroll_offset = min(max(scroll_offset - event.y * row_height, 0), max_scroll_offset)

        # Render background and subtitles
        screen.blit(background, (0, 0))
        screen.blit(title1_text, title1_rect)
        screen.blit(subtitle1_text, subtitle1_rect)
        screen.blit(subtitle2_text, subtitle2_rect)
        screen.blit(subtitle3_text, subtitle3_rect)

      
        rows_to_blit = render_rows(scroll_offset)
        for surface, rect in rows_to_blit:
            screen.blit(surface, rect)

        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action:
                return ui_action
            button.draw(screen)

        pygame.display.flip()


def story_screen(screen, player_name):

    pygame.mixer.init()
    pygame.mixer.music.load("mainbg.mp3")  # Replace with your actual music file path
    pygame.mixer.music.set_volume(0.5)  # Optional: Set volume to 50%
    pygame.mixer.music.play(-1)


    background = pygame.image.load("New folder/storytime.png")
    screen.blit(background, (0, 0))
    animation = [pygame.image.load(f"New folder/chester ({i}).png") for i in range(1, 5)]

    game_state = GameState.STORY
    title1_font = pygame.font.Font("New folder/JainiPurva-Regular.ttf", 60)  
    tutorial_font = pygame.font.Font("New folder/JainiPurva-Regular.ttf", 30)

    title1_font = pygame.font.Font("New folder/JainiPurva-Regular.ttf",60)  
    title1_text = title1_font.render("WELCOME, GENIUS! ", True, WHITE)
    title1_rect = title1_text.get_rect(center=(400,150))

    title2_font = pygame.font.Font("New folder/JainiPurva-Regular.ttf",20) 
    title2_text = title2_font.render("press anywhere to continue...", True, WHITE)
    title2_rect = title2_text.get_rect(center=(400,550))
    
    tutorial_text_lines = [
        
        "Use the arrow keys or wasd to move.",
        "Select correct weapon type to shoot the\ncorrect type of enemy.",
        "Answer questions by keyboard input\nwhen Eigenvampire chants her ritual.",
        "Good luck, and have fun!"
    ]

    start_time = time.time()
    clock = pygame.time.Clock()

    frame = 0
    frame_delay = 10
    delay_counter = 0
    clock = pygame.time.Clock()


    tutorial_text = []
    for line in tutorial_text_lines:
        tutorial_text.append(tutorial_font.render(line, True, WHITE))
    final_line_font = pygame.font.Font("New folder/JainiPurva-Regular.ttf", 40)  
    final_line = f"Are you ready, {player_name}?"
    final_text = final_line_font.render(final_line, True,  RED)

    tutorial_rects = []
    for i, line in enumerate(tutorial_text):
        rect = line.get_rect(center=(400, 250 + (i * 40)))
        tutorial_rects.append(rect)

    final_text_rect = final_text.get_rect(center=(400, 200 + len(tutorial_text) * 40 + 60))

    while True:
        mouse_up = False
        elapsed_time = time.time() - start_time

        delay_counter += 1
        if delay_counter >= frame_delay:
            frame = (frame + 1) % len(animation)
            delay_counter = 1
        if elapsed_time >= 7:
            return
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.QUIT
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True  

        screen.blit(background, (0, 0))
        screen.blit(title1_text,title1_rect)
        screen.blit(title2_text,title2_rect)
        screen.blit(animation[frame], (0, 0))
        
        for i, line in enumerate(tutorial_text):
            screen.blit(line, tutorial_rects[i])

        screen.blit(final_text, final_text_rect)    
        pygame.display.flip()

        if mouse_up:
            return GameState.TITLE 

def get_player_name_from_database():
    return "John Doe" 

player_name = get_player_name_from_database()

def finish_level(screen):

    background = pygame.image.load("New folder/gameover.png")
    title1_font = pygame.font.Font("New folder/JainiPurva-Regular.ttf", 90) 
    title1_text = title1_font.render("YOU WIN", True, WHITE)
    title1_rect = title1_text.get_rect(center=(400, 300))

    start_btn = UIElement((400, 400), "RETRY", 60, None, WHITE, action=GameState.NEWGAME)
    return_btn = UIElement((110, 70), "MAIN MENU", 30, None, WHITE, action=GameState.TITLE)
    quit_btn = UIElement((690, 70), "QUIT GAME", 30, None, WHITE, action=GameState.QUIT)
    leaderboard_btn = UIElement((400, 450), "LEADERBOARD", 30, None, WHITE, action=GameState.LEADERBOARD)
    buttons = [start_btn, quit_btn, leaderboard_btn,return_btn]

    animation = [pygame.image.load(f"New folder/chesterhappy ({i}).png") for i in range(1,4)]
    clock = pygame.time.Clock()

    frame = 0
    frame_delay = 10
    delay_counter = 0
    clock = pygame.time.Clock()
    start_time = time.time()


    while True:
        mouse_up = False 
        elapsed_time = time.time() - start_time

        delay_counter += 1
        if delay_counter >= frame_delay:
            frame = (frame + 1) % len(animation)
            delay_counter = 1
        if elapsed_time >= 7:
            return
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.QUIT
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        
        screen.blit(animation[frame], (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if confirm_quit(screen):
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True

        screen.blit(background, (0, 0))
        screen.blit(title_text, title_rect)

        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action:
                return ui_action
            button.draw(screen)

        pygame.display.flip()



def game_over(screen):
    background = pygame.image.load("New folder/gameover.png")
    title1_font = pygame.font.Font("New folder/JainiPurva-Regular.ttf", 90) 
    title1_text = title1_font.render("GAME OVER!", True, WHITE)
    title1_rect = title1_text.get_rect(center=(400, 300))

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


def player_name_screen(screen, database: Database):
    global player_name

    background = pygame.image.load("New folder/storytime.png")
    screen.blit(background, (0, 20))

    title_font = pygame.font.Font("New folder/JainiPurva-Regular.ttf", 50)
    title_text = title_font.render("Who's there?", True, WHITE)
    title_rect = title_text.get_rect(center=(400, 250))
    screen.blit(title_text, title_rect)

    input_font = pygame.font.Font("New folder/JainiPurva-Regular.ttf", 32)
    input_box = pygame.Rect(300, 300, 200, 40)
    color_inactive = pygame.Color(WHITE)
    color_active = pygame.Color(BLUE)
    color = color_inactive
    active = False
    text = ''

    # Error message font and settings
    error_font = pygame.font.Font("New folder/JainiPurva-Regular.ttf", 28)
    error_message = ''
    error_message_rect = None

    clock = pygame.time.Clock()

    while True:
        mouse_up = False  # Reset mouse_up at the beginning of each frame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the input box was clicked
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                # Set the input box color based on activity
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:

                        if not text.strip():
                            error_message = "Invalid name"
                            error_message_rect = error_font.render(error_message, True, (255, 0, 0)).get_rect(center=(400, 370))
                        else:
                            player_name = text
                            database.save_player(player_name, kills=0, time_spent=0)
                            return GameState.TITLE
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]  
                    else:
                        text += event.unicode  

        screen.blit(background, (0, 20))
        screen.blit(title_text, title_rect)

        txt_surface = input_font.render(text, True, color)
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)

        if error_message:
            error_text_surface = error_font.render(error_message, True, (255, 0, 0))
            screen.blit(error_text_surface, error_message_rect)

        pygame.display.flip()
        clock.tick(30)



def main():
    database = Database()
    pygame.init()

    screen = pygame.display.set_mode((800, 600))
    game_state = GameState.TITLE

    while True:
        if game_state == GameState.TITLE:
            game_state = title_screen(screen)
        elif game_state == GameState.NEWGAME:
            game_state = loading_screen(screen)
            game_state = player_name_screen(screen, database) 
            game_state = story_screen(screen, player_name)
            if game_state == GameState.TITLE:
                game_state = loading_screen(screen)
                if game_state != GameState.QUIT:
                    game_state = play_level(screen, database)
        elif game_state == GameState.FINISH:
            game_state = finish_level(screen)
        elif game_state == GameState.QUIT: 
            pygame.quit()
            sys.exit()
        elif game_state == GameState.GAMEOVER:
            game_state = game_over(screen)
        elif game_state == GameState.LEADERBOARD:
            game_state = leaderboard(screen, database)
        elif game_state == GameState.STORY:
            game_state = story_screen(screen, player_name)

            
if __name__ == "__main__":
    main()
    

