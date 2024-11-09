import pygame
import os
import random
import math

class RitualBat(pygame.sprite.Sprite):
    def __init__(self, player, scale=2, radius=150):
        super().__init__()

        # Reference to the player for movement
        self.player = player

        # Set the radius for the spawn distance from the player
        self.radius = radius
        self.scale = scale
        self.speed = 1  # Speed of the rotation

        # Randomly choose enemy type for animation
        self.enemy_type = random.choice([0, 1])
        animation_folder = "positive" if self.enemy_type == 0 else "negative"
        self.frames = self.load_animation(f"assets/bat/{animation_folder}")

        # Initialize animation state
        self.animation_index = 0
        self.image = self.frames[self.animation_index]

        # Set up the hitbox rect and image rect
        self.rect = self.image.get_rect(center=(self.player.x + self.radius, self.player.y))
        self.image_rect = self.rect.copy()

        # Angle of the bat relative to the player (starting from 0, which is to the right)
        self.angle = 0

        # Initialize flipped state for sprite facing direction
        self.flipped = False

    def load_animation(self, path):
        """Load and downsize all images in a folder as animation frames."""
        frames = []
        for img in sorted(os.listdir(path)):
            frame = pygame.image.load(os.path.join(path, img))
            downsized_frame = pygame.transform.scale(frame, (frame.get_width() // 4, frame.get_height() // 4))
            frames.append(downsized_frame)
        return frames

    def update_animation(self):
        """Update the animation frames of the bat."""
        self.animation_index += 0.2  # Animation speed
        if int(self.animation_index) >= len(self.frames):
            self.animation_index = 0  # Loop the animation frames
        self.image = self.frames[int(self.animation_index)]

        # Update image_rect based on the flipped image
        self.image_rect = self.image.get_rect(center=(self.x, self.y))

    def rotate_around_player(self):
        """Rotate the bat counterclockwise around the player's position."""
        # Increment the angle for rotation
        self.angle -= math.radians(1)  # Rotate counterclockwise by 1 degree each update

        # Calculate the new position based on the angle and radius
        self.x = self.player.x + self.radius * math.cos(self.angle)
        self.y = self.player.y + self.radius * math.sin(self.angle)

        # Update the position of the image's hitbox
        self.rect.center = (self.x, self.y)

    def update(self):
        """Update bat's position and animation."""
        self.rotate_around_player()  # Rotate around the player
        self.update_animation()  # Update animation frames

    def draw(self, window):
        """Draw the bat on the window."""
        window.blit(self.image, self.image_rect.topleft)  # Draw the image at its current position

        # Optionally, draw the hitbox (for debugging)
        pygame.draw.rect(window, (0, 255, 0), self.rect, 2)  # Green hitbox for visualization

    def die(self):
        """Handles the death of the bat (if needed)."""
        self.kill()  # For simplicity, we'll just kill the sprite directly for now


