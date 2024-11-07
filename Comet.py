import pygame
import os
import random

class Comet(pygame.sprite.Sprite):
    def __init__(self, player_x, path_to_frames, scale=1):
        super().__init__()

        # Comet's initial position (off-screen above the window)
        self.x = random.randint(0, 1500)  # Random X position
        self.y = -50  # Spawn above the screen
        self.scale = scale  # Scaling factor for the comet's size
        self.speed = 5  # Falling speed
        self.animation_speed = 0.2  # Speed of animation frame change

        # Load animation frames and scale them
        self.frames = self.load_animation(path_to_frames)
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(center=(self.x, self.y))

        # Track the player's last X position when the comet spawns
        self.target_x = player_x

    def load_animation(self, path):
        """Load all images in a folder as animation frames and scale them."""
        frames = [pygame.image.load(os.path.join(path, img)) for img in sorted(os.listdir(path))]
        return [pygame.transform.scale(frame, (int(frame.get_width() * self.scale//1.5), int(frame.get_height() * self.scale//1.5))) for frame in frames]

    def update_animation(self):
        """Update the animation frames of the comet."""
        self.animation_index += self.animation_speed
        if int(self.animation_index) >= len(self.frames):
            self.animation_index = 0  # Loop the animation frames
        self.image = self.frames[int(self.animation_index)]
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self):
        """Update comet's position and animation."""
        # Fall towards the player's X position (does not home in, just tracks where it started)
        if self.y < 1500:  # Check if the comet has not hit the bottom of the screen
            self.y += self.speed  # Make it fall down
            self.x = self.target_x  # Track the player's X position at the time of spawn
        else:
            self.kill()  # Remove the comet if it reaches the bottom of the screen

        # Update animation
        self.update_animation()

    def draw(self, window):
        """Draw the comet on the window."""
        # Draw the comet image
        window.blit(self.image, self.rect)

        # Optional: Draw the hitbox for the comet (green color, 2-pixel border)
        reduced_width = self.rect.width // 2
        reduced_height = self.rect.height // 2
        reduced_rect = pygame.Rect(self.rect.centerx - reduced_width // 2, self.rect.centery - reduced_height // 2, reduced_width, reduced_height)

        # Draw the smaller hitbox rectangle
        pygame.draw.rect(window, (0, 255, 0), reduced_rect, 2)  # Green hitbox with 2-pixel border

