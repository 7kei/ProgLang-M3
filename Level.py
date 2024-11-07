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
    bg = pygame.transform.scale(pygame.image.load('assets/bg.jpg'), (1800, 1200))
    floor = pygame.image.load('assets/tile001.png')

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
        self.boss.draw(self.window)  # Draw the boss

        # Draw all projectiles
        for projectile in self.projectiles:
            projectile.draw(self.window)
        
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

        # Handle player input events
        self.player.handle_input()

        # Update game elements
        self.player.update()  # Update player animation and position
        self.projectiles.update()  # Update projectiles (movement, collision checks, etc.)

        # Boss update, passing the shared level_time and player position
        self.boss.update(self.level_time, self.comets, self.player.x)

        # Update comets
        self.comets.update()  # Update comet positions and animations
        

        # Spawn and update enemies
        self.spawn_enemy()  # Spawn new enemies every 2 seconds
        self.enemies.update()  # Update enemy movement and animations

        # Redraw everything
        self.redraw_game_window()  # Call the redraw function
        
        # Control the frame rate (FPS) to ensure smooth animation
        self.clock.tick(60)  # 60 FPS, adjust if needed

        return GameState.NEWGAME







