import pygame
import os
import random
from Comet import Comet

class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y, health=100):
        super().__init__()

        # Position and health
        self.x = x
        self.y = y
        self.health = health

        # Boss state and timing
        self.spawned = False
        self.is_dead = False
        self.attack_timer = pygame.time.get_ticks()  # Timer for attack intervals
        self.attack_interval = 5000  # Attack every 5 seconds
        self.in_attack_animation = False

        # Load animations
        self.animations = {
            "spawn": self.load_animation('proglang proj/assets/boss/spawn'),
            "idle": self.load_animation('proglang proj/assets/boss/idle'),
            "attack": self.load_animation('proglang proj/assets/boss/attack'),
            "death": self.load_animation('proglang proj/assets/boss/death')
        }

        # Set initial animation state
        self.current_animation = "spawn"
        self.animation_index = 0
        self.image = self.animations[self.current_animation][self.animation_index]
        self.rect = self.image.get_rect(center=(self.x, self.y))

        # Comet tracking
        self.comets = pygame.sprite.Group()

    def load_animation(self, path):
        """Load animation frames from a folder."""
        return [pygame.image.load(os.path.join(path, img)) for img in sorted(os.listdir(path))]

    def update_animation(self):
        """Update the current animation frame."""
        self.animation_index += 0.1  # Adjust speed as necessary

        # Handle transitions after the animation completes
        if self.animation_index >= len(self.animations[self.current_animation]):
            if self.current_animation == "spawn" and not self.spawned:
                self.spawned = True
                self.current_animation = "idle"
            elif self.current_animation == "attack":
                self.current_animation = "idle"
            elif self.current_animation == "death":
                self.kill()  # Remove the boss from the game after death animation

            # Reset animation index after completing each cycle
            self.animation_index = 0

        # Get the current frame
        self.image = self.animations[self.current_animation][int(self.animation_index)]
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def attack(self, player_x):
        """Perform an attack by creating a comet aimed at the player's x position."""
        self.current_animation = "attack"
        comet = Comet(player_x, -50)  # Spawn comet off-screen above the player's x position
        self.comets.add(comet)

    def update(self, player_x):
        """Update the boss's state and animations."""
        if self.is_dead:
            self.current_animation = "death"  # Set to death animation if boss is dead
        else:
            # Check if enough time has passed to perform another attack
            current_time = pygame.time.get_ticks()
            if current_time - self.attack_timer >= self.attack_interval:
                self.attack(player_x)  # Spawn comet every attack interval
                self.attack_timer = current_time  # Reset the attack timer

        # Update boss animation
        self.update_animation()

        # Update comets (falling projectiles) only if the boss is alive
        if not self.is_dead:
            self.comets.update()

    def draw(self, window):
        """Draw the boss and comets on the screen."""
        window.blit(self.image, self.rect.topleft)

        # Draw each comet in the comets group
        for comet in self.comets:
            comet.draw(window)

    def take_damage(self, amount):
        """Reduce health when the boss takes damage."""
        if not self.is_dead:
            self.health -= amount
            if self.health <= 0:
                self.is_dead = True  # Set flag to initiate death sequence
                self.current_animation = "death"  # Switch to death animation
                self.animation_index = 0  # Start death animation from the first frame
