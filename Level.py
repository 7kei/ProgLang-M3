import pygame

from Player import *
from Projectile import *
from GameState import *
from pygame.sprite import Group

class Level:
    # Load and center background image
    bg = pygame.transform.scale(pygame.image.load('D:/Downloads/A.Y 2024 - 2025/1st Term/CS121/proglang proj/assets/bg.jpg'), (1800, 1200))
    floor = pygame.image.load('D:/Downloads/A.Y 2024 - 2025/1st Term/CS121/proglang proj/assets/tile001.png')

    def __init__(self, window):
        self.window = window
        self.kill_count = 0
        self.clock = pygame.time.Clock()  # Initialize the clock to control FPS

        # Instantiate the Player object
        self.player = Player(x=100, y=700, max_health=100)
        
        # Group for projectiles
        self.projectiles = Group()
        
        # Load item images and set up positions
        self.items = {
            'item1': {
                'untoggled': pygame.image.load('D:/Downloads/A.Y 2024 - 2025/1st Term/CS121/proglang proj/assets/weapons/weapon icons (toggled, untoggled)/1.png'),
                'toggled': pygame.image.load('D:/Downloads/A.Y 2024 - 2025/1st Term/CS121/proglang proj/assets/weapons/weapon icons (toggled, untoggled)/2.png')
            },
            'item2': {
                'untoggled': pygame.image.load('D:/Downloads/A.Y 2024 - 2025/1st Term/CS121/proglang proj/assets/weapons/weapon icons (toggled, untoggled)/3.png'),
                'toggled': pygame.image.load('D:/Downloads/A.Y 2024 - 2025/1st Term/CS121/proglang proj/assets/weapons/weapon icons (toggled, untoggled)/4.png')
            },
            'item3': {
                'untoggled': pygame.image.load('D:/Downloads/A.Y 2024 - 2025/1st Term/CS121/proglang proj/assets/weapons/weapon icons (toggled, untoggled)/5.png'),
                'toggled': pygame.image.load('D:/Downloads/A.Y 2024 - 2025/1st Term/CS121/proglang proj/assets/weapons/weapon icons (toggled, untoggled)/6.png')
            }
        }

        # Initial item positions
        self.item_positions = [(650, 800), (750, 800), (850, 800)]
        self.selected_item = None  # Track the currently selected item

    def redraw_game_window(self):
        """Redraw the entire game window."""
        # Redraw background
        self.window.fill((0, 0, 0))  # Clear the screen with black background
        self.window.blit(Level.bg, (-100, -150))  # Draw the background
        
        # Example timer and score rendering (use your own game variables)
        timer = f'Timer: {pygame.time.get_ticks() // 1000} secs'  # Assuming time in seconds
        score = f'Kills: {self.kill_count} eigenbats killed'
        
        FONT_timer = pygame.font.SysFont("Sans", 20)
        self.window.blit(FONT_timer.render(timer, True, (255, 255, 255)), (700, 0))
        self.window.blit(FONT_timer.render(score, True, (255, 255, 255)), (665, 20))

        # Draw the floor tiles
        for i in range(0, 1560, 52):
            self.window.blit(Level.floor, (-5 + i, 804))  # Tile position

        # Draw the player and other game entities
        self.player.draw(self.window)

        # Draw all projectiles
        for projectile in self.projectiles:
            projectile.draw(self.window)
            
        # Draw items at bottom center of screen
        for idx, (item_name, item_data) in enumerate(self.items.items()):      
            if self.selected_item == item_name:
                # Draw the toggled image if selected
                self.window.blit(item_data['toggled'], self.item_positions[idx])
            else:
                # Draw the untoggled image if not selected
                self.window.blit(item_data['untoggled'], self.item_positions[idx])
        
        # Update display
        pygame.display.flip()  # Update the screen with everything drawn

    def mainloop(self):
        # Event Handling
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                return GameState.QUIT
            elif event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:  # Left-click
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    projectile = self.player.handle_attack(mouse_x, mouse_y)
                    self.projectiles.add(projectile)
            elif event.type == pygame.KEYDOWN:
                # Toggle item based on key press
                if event.key == pygame.K_1:
                    self.selected_item = 'item1'
                elif event.key == pygame.K_2:
                    self.selected_item = 'item2'
                elif event.key == pygame.K_3:
                    self.selected_item = 'item3'
                else:
                    self.selected_item = None  # Reset if other keys are pressed
                
        # Handle player input events
        self.player.handle_input()

        # Update game elements
        self.player.update()  # Update player animation and position
        self.projectiles.update()  # Update projectiles (movement, collision checks, etc.)

        # Redraw everything
        self.redraw_game_window()  # Call the redraw function
        
        # Control the frame rate (FPS) to ensure smooth animation
        self.clock.tick(60)  # 60 FPS, adjust if needed

        return GameState.NEWGAME