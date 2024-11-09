import pygame
import os
from Comet import *

class Boss(pygame.sprite.Sprite):
    def __init__(self, level_time, x, y, scale=2):
        super().__init__()

        # Position
        self.x = x
        self.y = y
        self.scale = scale  # Scaling factor for boss size
        self.health = 500  # Boss health

        # Load animations with scaling
        self.animations = {
            "spawn": self.load_animation("assets/boss/spawn"),
            "idle": self.load_animation("assets/boss/idle"),
            "attack": self.load_animation("assets/boss/attack"),
            "death": self.load_animation("assets/boss/death"),
            "ritual": self.load_animation("assets/boss/ritual")  # Ritual animation
        }

        # Animation settings
        self.current_animation = "spawn"
        self.animation_index = 0
        self.image = self.animations[self.current_animation][self.animation_index]
        self.rect = self.image.get_rect(center=(self.x, self.y))

        # Timers
        self.last_attack_time = level_time  # Shared time reference
        self.attack_interval = 5000  # Attack every 5 seconds
        self.spawned = False  # To track if spawn animation is done
        self.dead = False  # Track if the boss is dead
        self.attack_started = False  # Track if an attack animation is active

        # Animation speed controls
        self.animation_speed = 0.15  # Controls how quickly frames change

        # Ritual state flag
        self.is_in_ritual = False  # Whether the boss is in the ritual state

        # Speed for gradual movement
        self.move_speed = 5  # Boss move speed

    def load_animation(self, path):
        """Load all images in a folder as animation frames and scale them."""
        frames = [pygame.image.load(os.path.join(path, img)) for img in sorted(os.listdir(path))]
        # Scale each frame based on self.scale
        return [pygame.transform.scale(frame, (int(frame.get_width() * self.scale), int(frame.get_height() * self.scale))) for frame in frames]

    def update_animation(self):
        """Update animation frame based on current action."""
        self.animation_index += self.animation_speed

        # If in ritual state, loop the ritual animation indefinitely
        if self.is_in_ritual:
            if int(self.animation_index) >= len(self.animations["ritual"]):
                self.animation_index = 0  # Restart ritual animation loop
            self.image = self.animations["ritual"][int(self.animation_index)]
        else:
            if int(self.animation_index) >= len(self.animations[self.current_animation]):
                if self.current_animation == "spawn":
                    self.current_animation = "idle"
                    self.animation_index = 0
                    self.spawned = True
                elif self.current_animation == "attack":
                    # After attack completes, go back to idle
                    self.current_animation = "idle"
                    self.animation_index = 0
                    self.attack_started = False
                elif self.current_animation == "death":
                    self.dead = True
                elif self.current_animation == "idle":
                    self.animation_index = 0

            self.image = self.animations[self.current_animation][int(self.animation_index)]

        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self, level_time, comet_group, player_x):
        """Handle animation updates and timing for attack."""
        current_time = pygame.time.get_ticks()

        if self.dead:
            return

        # If in ritual state, move the boss gradually towards the center
        if self.is_in_ritual:
            target_y = 350  # Center of the screen vertically (adjust as necessary)
            
            # Gradually move the boss towards the target y position
            if self.y < target_y:
                self.y += self.move_speed  # Move down
            elif self.y > target_y:
                self.y -= self.move_speed  # Move up

            # Update the rect position to reflect new y position
            self.rect.center = (self.x, self.y)

            # Continue looping the ritual animation
            self.update_animation()
            return

        # Trigger attack based on time (outside of ritual state)
        if self.spawned and not self.attack_started and current_time - self.last_attack_time >= self.attack_interval:
            self.current_animation = "attack"
            self.animation_index = 0
            self.attack_started = True
            self.last_attack_time = current_time

            # Spawn a comet after the attack animation is triggered
            self.spawn_comet(player_x, comet_group)

        self.update_animation()

    def spawn_comet(self, player_x, comet_group):
        """Spawn a comet when the boss attacks."""
        comet = Comet(player_x + 50, "assets/boss/comet/fall", "assets/boss/comet/explosion", scale=2)
        comet_group.add(comet)

    def take_damage(self, amount):
        """Handle damage to the boss."""
        self.health -= amount
        if self.health <= 0:
            self.current_animation = "death"
            self.animation_index = 0
            self.dead = True

    def enter_ritual(self):
        """Enter the ritual state."""
        self.is_in_ritual = True
        self.y = 0  # Start from the top of the screen (or adjust starting position)
        self.x = 900  # Adjust to center the boss horizontally
        self.rect.center = (self.x, self.y)  # Update the rect position
        self.current_animation = "ritual"  # Start ritual animation loop
        self.animation_index = 0

    def exit_ritual(self):
        """Exit the ritual state."""
        self.is_in_ritual = False
        self.current_animation = "idle"  # Resume normal idle state after ritual ends

    def draw(self, window):
        """Draw the boss on the window."""
        window.blit(self.image, self.rect)
