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
        
        # Group for projectiles
        self.projectiles = Group()

        # Instantiate the Player object
        self.player = Player(x=100, y=790, max_health=100, projectiles=self.projectiles)
        self.boss = Boss(self.level_time, x=1300, y=200, scale=2)  # Adjust coordinates for upper right placement

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

        # Attack cooldown logic
        self.attack_cooldown = 500  # Cooldown in milliseconds
        self.last_attack_time = 0  # Time of the last attack
        
        self.enemies_positive = pygame.sprite.Group()  # Positive type enemies
        self.enemies_negative = pygame.sprite.Group()  # Negative type enemies

    
    def spawn_enemy(self):
        """Spawn an enemy (bat) if enough time has passed."""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_enemy_spawn_time > 2000:  # Spawn every 2 seconds
            enemy = Enemy(self.player)  # Create a new enemy targeting the player
            self.enemies.add(enemy)
            self.last_enemy_spawn_time = current_time

    def check_collisions(self):
        """Check for collisions between projectiles, player, enemies, and comets."""
        
        # Check for projectile and enemy collisions
        for projectile in self.projectiles:
            if projectile.type == 1:  # Negative Projectile
                hit_enemies = pygame.sprite.spritecollide(projectile, self.enemies_negative, False)  # Check for negative enemies
            elif projectile.type == 0:  # Positive Projectile
                hit_enemies = pygame.sprite.spritecollide(projectile, self.enemies_positive, False)  # Check for positive enemies
            else:
                continue
            
            if hit_enemies:
                for enemy in hit_enemies:
                    # Check if the projectile and enemy type match
                    if (projectile.type == 1 and isinstance(enemy, NegativeEnemy)) or \
                    (projectile.type == 0 and isinstance(enemy, PositiveEnemy)):
                        enemy.kill()  # Destroy enemy if matched type
                        self.kill_count += 1
                    else:
                        projectile.kill()  # Only destroy the projectile if no match

                projectile.kill()  # Always remove the projectile after collision
        
        # Check for player and enemy collisions
        for enemy in self.enemies:
            if self.player.rect.colliderect(enemy.rect):  # Use player rect for collision check
                self.player.is_hit = True  # Trigger hit animation for player
                self.player.current_health -= 10  # Example: Decrease health on collision with enemy
                
                # Apply knockback effect based on the enemy position
                self.player.apply_knockback(enemy.x, enemy.y)  # Apply knockback based on enemy position

                self.enemies.remove(enemy)  # Remove the enemy from the game
                break  # Break after first collision to avoid checking further enemies

        # Check for player and comet collisions
        for comet in self.comets:
            if self.player.rect.colliderect(comet.rect):  # Check if player collides with comets
                self.player.is_in_hit_animation = True  # Trigger hit animation for player
                self.player.current_health -= 15  # Example: Decrease health on collision with comet
                
                # Apply knockback effect based on the comet position
                self.player.apply_knockback(comet.x, comet.y)  # Apply knockback based on comet position

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
            # Call the update method to handle movement and animation
            projectile.update(self.enemies_positive, self.enemies_negative)

            # Call the draw method to display the projectile on screen
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
        mouse_x, mouse_y = pygame.mouse.get_pos()  # Get mouse position for aiming

        # Event Handling
        for event in event_list:
            if event.type == pygame.QUIT:  # Check if player quits
                return GameState.QUIT
            
            # Handling mouse button clicks for attacks
            elif event.type == pygame.MOUSEBUTTONDOWN:
                current_time = pygame.time.get_ticks()
                
                # Check cooldown before allowing attack
                if current_time - self.last_attack_time >= self.attack_cooldown:
                    
                    if self.selected_item == 'item1':  # Negative Projectile (Key 1)
                        new_projectile = self.player.handle_attack(mouse_x, mouse_y, projectile_type=1)
                        if new_projectile:
                            self.projectiles.add(new_projectile)
                        self.last_attack_time = current_time  # Update last attack time

                    elif self.selected_item == 'item2':  # Positive Projectile (Key 2)
                        new_projectile = self.player.handle_attack(mouse_x, mouse_y, projectile_type=0)
                        if new_projectile:
                            self.projectiles.add(new_projectile)
                        self.last_attack_time = current_time  # Update last attack time

            # Handling keyboard input for selecting items
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.selected_item = 'item1'  # Select Negative Projectile
                elif event.key == pygame.K_2:
                    self.selected_item = 'item2'  # Select Positive Projectile
                elif event.key == pygame.K_3:
                    self.selected_item = 'item3'  # Placeholder for other functionality

        # Handle player input events
        self.player.handle_input()

        # Update game elements
        self.player.update()
        self.projectiles.update(self.enemies_positive, self.enemies_negative)

        # Boss and enemy updates
        self.boss.update(self.level_time, self.comets, self.player.x)

        # Update comets
        self.comets.update()  # Update comet positions and animations
        
        # Spawn and update enemies
        self.spawn_enemy()  # Spawn new enemies every 2 seconds
        self.enemies.update()  # Update enemy movement and animations

        # Check for collisions
        self.check_collisions()

        # Redraw everything
        self.redraw_game_window()
        self.clock.tick(60)

        return GameState.NEWGAME