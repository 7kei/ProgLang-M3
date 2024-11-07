import pygame
import os

class Comet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # Initial position and speed of the comet
        self.x = x
        self.y = y
        self.speed = 5

        # Load comet animation frames
        self.frames = self.load_animation_frames(f'proglang proj/assets/boss/comet')
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def load_animation_frames(self, path):
        """Load animation frames from a folder."""
        return [pygame.image.load(os.path.join(path, img)) for img in sorted(os.listdir(path))]

    def update_animation(self):
        """Update the animation frame index to loop the comet animation."""
        # Adjust the speed of the animation
        self.animation_index += 0.1  # Modify this number to adjust animation speed
        if self.animation_index >= len(self.frames):
            self.animation_index = 0  # Loop back to the first frame

        # Update the current image
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        """Update the comet's position and animation as it falls."""
        self.y += self.speed  # Move comet down
        self.rect.y = self.y

        # Update animation
        self.update_animation()

        # Remove the comet if it goes off-screen
        if self.y > 900:  # Assuming 900 is the height of the game screen
            self.kill()

    def draw(self, window):
        """Draw the comet on the game window."""
        window.blit(self.image, self.rect.topleft)
