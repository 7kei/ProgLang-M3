import pygame
import math
import os

from Player import *

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y, path_to_frames, projectile_type ,hitbox_width=25, hitbox_height=25):
        super().__init__()
        
        # Set projectile type (1 = negative, 2 = positive)
        self.type = projectile_type

        # Initial position of the projectile (where it is fired from)
        self.x = x
        self.y = y
        self.speed = 10  # Speed of the projectile

        # Load projectile animation frames (a sequence of PNG images)
        self.frames = self.load_animation(path_to_frames)
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        
        # Set the custom hitbox dimensions (these are separate from the image size)
        self.hitbox_width = hitbox_width
        self.hitbox_height = hitbox_height
        
        # Set the hitbox to match the projectile's hitbox (not its image)
        self.rect = pygame.Rect(self.x - self.hitbox_width // 2, self.y - self.hitbox_height // 2, self.hitbox_width, self.hitbox_height)

        # Create a separate rect for the image (this will be rotated)
        self.image_rect = self.image.get_rect(center=(self.x, self.y))

        # Calculate the angle of the projectile relative to the player's position and mouse position
        self.target_x = target_x
        self.target_y = target_y
        self.angle = math.atan2(target_y - y, target_x - x)  # Angle from the player to the mouse

        # Timer for delay
        self.delay_time = 550  # Delay in milliseconds (0.5 seconds)
        self.start_time = pygame.time.get_ticks()  # Get current time when the projectile is created
        self.started = False  # Flag to check if the projectile has started moving

        # Animation speed control
        self.animation_speed = 0.3  # Higher values make the animation loop faster (e.g., 0.3 makes it faster than 0.1)

    def load_animation(self, path, width=100, height=100):
        """Load all images in a folder as animation frames and resize them."""
        frames = []
        for img_name in sorted(os.listdir(path)):
            img_path = os.path.join(path, img_name)
            img = pygame.image.load(img_path)
            img = pygame.transform.scale(img, (width, height))  # Resize the image to the specified width and height
            frames.append(img)
        return frames

    def update(self, enemies_positive, enemies_negative):
        """Update the projectile's position and check for collision with enemies."""
        # Check if the delay time has passed
        if pygame.time.get_ticks() - self.start_time >= self.delay_time:
            if not self.started:
                self.started = True  # Set the flag to True after the delay

        if self.started:
            # Move the projectile toward its target
            self.x += self.speed * math.cos(self.angle)
            self.y += self.speed * math.sin(self.angle)

            # Update the animation frame based on the speed control
            self.animation_index += self.animation_speed  # Increase animation speed
            if self.animation_index >= len(self.frames):
                self.animation_index = 0  # Loop animation

            self.image = self.frames[int(self.animation_index)]  # Get the current frame

            # Rotate the image so that it faces the direction from the player to the mouse
            self.image = pygame.transform.rotate(self.frames[int(self.animation_index)], ((-1)*math.degrees(self.angle)) + 90)
            
            # Recalculate the position of the rect so the rotation happens around the base of the projectile
            self.rect = self.image.get_rect(center=(self.x, self.y))  # Reset the rect to keep the projectile's position
            
            # Collision detection with the correct group based on projectile type
            if self.type == 1:  # Negative Projectile
                for enemy in enemies_positive:
                    if self.rect.colliderect(enemy.rect):
                        enemy.kill()  # Destroy the enemy
                        self.kill()   # Destroy the projectile
            elif self.type == 0:  # Positive Projectile
                for enemy in enemies_negative:
                    if self.rect.colliderect(enemy.rect):
                        enemy.kill()  # Destroy the enemy
                        self.kill()   # Destroy the projectile

            # Add boundary checking (e.g., remove projectile if out of bounds)
            if self.x < 0 or self.x > 1500 or self.y < 0 or self.y > 900:  # Assuming the screen is 1500x900
                self.kill()  # Remove the projectile if out of bounds

    def draw(self, window):
        """Draw the projectile on the window only if it has started moving."""
        if self.started:  # Only draw the projectile after the delay
            window.blit(self.image, self.image_rect)  # Draw the rotated image at the calculated image rect position

            # Draw the custom hitbox (this is a rectangle)
            pygame.draw.rect(window, (0, 255, 0), self.rect, 2)  # Green color for hitbox
