import pygame

from Player import *
from Projectile import *
from GameState import *
from Boss import *
from Comet import *
from Enemy import *
from pygame.sprite import Group

class Level:
    # Load and center background image
    bg = pygame.transform.scale(pygame.image.load('D:/Downloads/A.Y 2024 - 2025/1st Term/CS121/proglang proj/assets/bg.jpg'), (1800, 1200))
    floor = pygame.image.load('D:/Downloads/A.Y 2024 - 2025/1st Term/CS121/proglang proj/assets/tile001.png')

    def __init__(self, window):
        self.window = window
        self.kill_count = 0
        self.clock = pygame.time.Clock()  # Initialize the clock to control FPS
        self.level_time = pygame.time.get_ticks()  # Track the level time (shared timer)


        # Instantiate the Player object
        self.player = Player(x=100, y=790, max_health=100)
        self.boss = Boss(self.level_time, x=1300, y=200, scale=2)  # Adjust coordinates for upper right placement
        
        # Group for projectiles
        self.projectiles = Group()

        # Group for comets
        self.comets = pygame.sprite.Group()  

        # Group for enemies
        self.enemies = Group()

        # Timer to track enemy spawn intervals
        self.last_enemy_spawn_time = pygame.time.get_ticks()
        
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

        # Group for comets
        self.comets = pygame.sprite.Group()  

        # Group for enemies
        self.enemies = Group()

        # Timer to track enemy spawn intervals
        self.last_enemy_spawn_time = pygame.time.get_ticks()
    
    def spawn_enemy(self):
        """Spawn an enemy (bat) if enough time has passed."""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_enemy_spawn_time > 2000:  # Spawn every 2 seconds
            enemy = Enemy(self.player)  # Create a new enemy targeting the player
            self.enemies.add(enemy)
            self.last_enemy_spawn_time = current_time

    def redraw_game_window(self):
        """Redraw the entire game window."""
        # Redraw background
        self.window.fill((0, 0, 0))  # Clear the screen with black background
        self.window.blit(Level.bg, (-100, -150))  # Draw the background
        
        # Example timer and score rendering (use your own game variables)
        timer = f'Timer: {pygame.time.get_ticks() // 1000} secs'  # To get time in seconds
        score = f'Kills: {self.kill_count} eigenbats killed'
        
        FONT_timer = pygame.font.SysFont("Sans", 20)
        self.window.blit(FONT_timer.render(timer, True, (255, 255, 255)), (700, 0))
        self.window.blit(FONT_timer.render(score, True, (255, 255, 255)), (665, 20))

        # Draw the floor tiles
        for i in range(0, 1560, 52):
            self.window.blit(Level.floor, (-5 + i, 804))  # Tile position

        # Draw the player and other game entities
        self.player.draw(self.window)
        self.boss.draw(self.window)  # Draw the boss

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
        
         # Draw all comets
        for comet in self.comets:
            comet.draw(self.window)
        self.comets.draw(self.window)  # Draw the comets on the screen

        # Draw all enemies
        for enemy in self.enemies:
            enemy.draw(self.window)
        self.enemies.draw(self.window)

        # Update display
        pygame.display.flip()  # Update the screen with everything drawn

    def mainloop(self, event_list):

        # Event Handling
        for event in event_list:
            if event.type == pygame.QUIT: # Check if player quits
                return GameState.QUIT
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:  # Item 1 - Negative Projectile
                        new_projectile = Projectile(player.x, player.y, target_x, target_y, 'assets/projectile_negative', 1)
                        self.projectiles.add(new_projectile)
                    elif event.key == pygame.K_2:  # Item 2 - Positive Projectile
                        new_projectile = Projectile(player.x, player.y, target_x, target_y, 'assets/projectile_positive', 2)
                        self.projectiles.add(new_projectile)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.selected_item = 'item1'
                elif event.key == pygame.K_2:
                    self.selected_item = 'item2'
                elif event.key == pygame.K_3:
                    self.selected_item = 'item3'
                    
        # Handle player input events
        self.player.handle_input()

        # Update game elements
        self.player.update()
        self.projectiles.update()

        # Boss and enemy updates
        self.boss.update(self.level_time, self.comets, self.player.x)
        self.spawn_enemy()
        self.enemies.update()
        self.comets.update()

        # Redraw everything
        self.redraw_game_window()
        self.clock.tick(60)

        return GameState.NEWGAME
