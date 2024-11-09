import pygame
from pygame.locals import *
from Player import *
from Projectile import *
from GameState import *
from Boss import *
from Comet import *
from Enemy import *
from RitualBat import *
from pygame.sprite import Group
import math

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
        self.bats_group = pygame.sprite.Group()  # Group to store the bats

        # Timer to track enemy spawn intervals
        self.last_enemy_spawn_time = pygame.time.get_ticks()

        # Attack cooldown logic
        self.attack_cooldown = 500  # Cooldown in milliseconds
        self.last_attack_time = 0  # Time of the last attack

        # Initialize variables for right-click input
        self.input_active = False
        self.current_input = ""
        self.font = pygame.freetype.SysFont("Blackadder ITC", 36)
        self.input_box = pygame.Rect(20, 1050, 200, 30)  # Text box at the bottom left
        self.current_charge = 0  # Charge variable initialized to 0
        
        self.is_in_ritual = False  # Track if the boss is in ritual state

    def spawn_enemy(self):
        """Spawn an enemy (bat) if enough time has passed."""        
        if self.is_in_ritual:
            return  # Do not spawn enemies during the ritual

        current_time = pygame.time.get_ticks()
        if current_time - self.last_enemy_spawn_time > 2000:  # Spawn every 2 seconds
            enemy = Enemy(self.player)  # Create a new enemy targeting the player
            self.enemies.add(enemy)
            self.last_enemy_spawn_time = current_time

    def kill_all_entities(self):
        """Kill all comets, projectiles, and enemies currently on screen."""
        self.comets.empty()  # Remove all comets
        self.projectiles.empty()  # Remove all projectiles
        self.enemies.empty()  # Remove all enemies

    def spawn_ritual_bats(self):
        """Spawns 6 RitualBats at fixed positions surrounding the player."""
        radius = 150  # Distance from the player at which bats will spawn

        # Specific angles for the 6 positions (in radians)
        angles = [
            math.radians(0),     # Right
            math.radians(60),    # Upper-right
            math.radians(120),   # Upper-left
            math.radians(180),   # Left
            math.radians(240),   # Lower-left
            math.radians(300)    # Lower-right
        ]

        for angle in angles:
            # Calculate the position of each bat based on the angle and radius
            x = self.player.x + radius * math.cos(angle)
            y = self.player.y + radius * math.sin(angle)

            # Create a new RitualBat at the calculated position
            bat = RitualBat(self.player, radius=radius)
            bat.x, bat.y = x, y

            # Add the bat to the bats_group
            self.bats_group.add(bat)

    def check_collisions(self):
        """Check for collisions between projectiles, player, enemies, and comets."""
        # Check for projectile and enemy collisions
        for projectile in self.projectiles:
            hit_enemies = pygame.sprite.spritecollide(projectile, self.enemies, False)  # enemies on collision
            if hit_enemies:
                for enemy in hit_enemies:
                    enemy.die()
                projectile.kill()  # Remove the projectile on collision
                self.kill_count += len(hit_enemies)  # Increment kill count for each enemy hit

        # Check for player and enemy collisions
        for enemy in self.enemies:
            if self.player.rect.colliderect(enemy.rect):  # Use player rect for collision check
                self.player.is_hit = True  # Trigger hit animation for player
                self.player.current_health -= 10  # Example: Decrease health on collision with enemy
                
                # Apply knockback effect based on the enemy position
                self.player.apply_knockback(enemy.x, enemy.y, 2)  # Apply knockback based on enemy position

                enemy.die()
                break  # Break after first collision to avoid checking further enemies

        # Check for player and comet collisions
        for comet in self.comets:
            if self.player.rect.colliderect(comet.rect):  # Check if player collides with comets
                self.player.is_in_hit_animation = True  # Trigger hit animation for player
                self.player.current_health -= 15  # Example: Decrease health on collision with comet
                
                # Apply knockback effect based on the comet position
                self.player.apply_knockback(comet.x, comet.y, 10)  # Apply knockback based on comet position
        
        # Check for projectile and comet collisions
        for projectile in self.projectiles:
            hit_comets = pygame.sprite.spritecollide(projectile, self.comets, False)  # Check if projectile hits a comet
            if hit_comets:
                for comet in hit_comets:
                    comet.state = "explosion"  # Change comet state to explosion
                    comet.animation_index = 0  # Reset the animation frame to start the explosion
                    comet.image_rect.center = (comet.x, comet.y)  # Ensure explosion is centered on comet's position
                projectile.kill()  # Remove the projectile after it hits a comet

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
        # self.comets.draw(self.window)  # Draw the comets on the screen

        # Draw all enemies
        for enemy in self.enemies:
            enemy.draw(self.window)
        for bat in self.bats_group:
            bat.draw(self.window)
        # self.enemies.draw(self.window)

        # Display the "Current Charge" in a box at the upper right
        charge_text = f"Current Charge: {self.current_input if self.input_active else self.current_input}"
        charge_box = pygame.Rect(50, 850, 300, 50)  # Position at upper right corner
        pygame.draw.rect(self.window, (50, 50, 50), charge_box)  # Draw the background box
        pygame.draw.rect(self.window, (255, 255, 255), charge_box, 2)  # Draw the border

        # Render the charge text
        charge_surface, _ = self.font.render(charge_text, (255, 255, 255))
        self.window.blit(charge_surface, (charge_box.x + 10, charge_box.y + 10))

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
                    # Check cooldown before allowing attack
                    current_time = pygame.time.get_ticks()
                    if current_time - self.last_attack_time >= self.attack_cooldown:
                        projectile = self.player.handle_attack(mouse_x, mouse_y)
                        self.projectiles.add(projectile)
                        self.last_attack_time = current_time  # Update last attack time
                
                if event.button == 3:  # Right-click
                    self.input_active = True  # Start accepting input
                    self.current_input = ""  # Clear previous input

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:  # Right-click release
                    self.input_active = False  # Stop accepting input
                    # Update current charge with the input
                    try:
                        self.current_charge = int(self.current_input)  # Change the charge based on input
                    except ValueError:
                        pass
                    print(f"Final charge: {self.current_charge}")  # Print the final charge value

            elif event.type == pygame.KEYDOWN:
                if self.input_active:
                    if event.key == K_BACKSPACE:  # Handle backspace for text input
                        self.current_input = self.current_input[:-1]
                    elif event.key == K_RETURN:  # Accept the input on 'Enter'
                        print(f"Input confirmed: {self.current_input}")
                    else:
                        # Only allow numeric input
                        if event.unicode.isdigit():
                            self.current_input += event.unicode  # Add character to input string

        # Trigger the Ritual at 8 seconds
        if pygame.time.get_ticks() - self.level_time >= 8000 and not self.is_in_ritual:
            self.is_in_ritual = True
            self.player.is_in_ritual = True
            self.boss.is_in_ritual = True
            for enemy in self.enemies:
                if enemy.dying == False:
                    enemy.die()
            
            self.spawn_ritual_bats()
            for comet in self.comets:
                if comet.state != "explosion":
                    comet.state = "explosion"  # Change comet state to explosion
                    comet.animation_index = 0  # Reset the animation frame to start the explosion
                    comet.image_rect.center = (comet.x, comet.y)  # Ensure explosion is centered on comet's position
            
            print("Ritual started!")

        # If we are in ritual state, disable normal actions
        if self.is_in_ritual:
            # Ritual actions: kill entities and spawn bats around the player when at center position

            pass
                # self.kill_all_entities()  # Remove all comets, projectiles, enemies

        else:
            # Handle player input events
            self.player.handle_input()
            
            # Spawn and update enemies
            self.spawn_enemy()  # Spawn new enemies every 2 seconds
            
            # Check for collisions
            self.check_collisions()
        
        # Update game elements
        self.player.update()  # Update player animation and position
        self.projectiles.update()  # Update projectiles (movement, collision checks, etc.)

        # Boss update, passing the shared level_time and player position
        self.boss.update(self.level_time, self.comets, self.player.x)

        # Update comets
        self.comets.update()  # Update comet positions and animations

        self.enemies.update()  # Update enemy movement and animations
        self.bats_group.update()

        # Redraw everything
        self.redraw_game_window()  # Call the redraw function
        
        # Control the frame rate (FPS) to ensure smooth animation
        self.clock.tick(60)  # 60 FPS, adjust if needed

        return GameState.NEWGAME
