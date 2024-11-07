import pygame
import os
import random
import math

class Enemy(pygame.sprite.Sprite):
    def __init__(self, player, scale=2):
        super().__init__()

        # Determine initial position (off-screen to left, right, or top)
        spawn_side = random.choice(["left", "right", "top"])
        if spawn_side == "left":
            self.x = -50
            self.y = random.randint(0, 650)
        elif spawn_side == "right":
            self.x = 1850
            self.y = random.randint(0, 650)
        elif spawn_side == "top":
            self.x = random.randint(0, 1800)
            self.y = -50

        self.scale = scale  # Keep scale for other uses if necessary
        self.speed = 3
        self.animation_speed = 0.2
        self.flipped = False  # Track whether the sprite is flipped or not

        # Randomly choose enemy type: 0 for positive, 1 for negative
        self.enemy_type = random.choice([0, 1])
        animation_folder = "positive" if self.enemy_type == 0 else "negative"
        self.frames = self.load_animation(f"assets/bat/{animation_folder}")
        
        # Initialize animation state
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(center=(self.x, self.y))

        # Set the player reference to follow dynamically
        self.player = player

    def load_animation(self, path):
        """Load and downsize all images in a folder as animation frames."""
        frames = []
        for img in sorted(os.listdir(path)):
            frame = pygame.image.load(os.path.join(path, img))
            # Downsize the frame to 10% of the original size
            downsized_frame = pygame.transform.scale(frame, (frame.get_width() // 4, frame.get_height() // 4))
            frames.append(downsized_frame)
        return frames

    def update_animation(self):
        """Update the animation frames of the enemy."""
        self.animation_index += self.animation_speed
        if int(self.animation_index) >= len(self.frames):
            self.animation_index = 0  # Loop the animation frames
        self.image = self.frames[int(self.animation_index)]
        
        # Flip the sprite if necessary (based on the player's position)
        if self.flipped:
            self.image = pygame.transform.flip(self.image, True, False)
        
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def move_towards_player(self):
        """Move the enemy towards the player's current position."""
        target_x, target_y = self.player.rect.center
        angle = math.atan2(target_y - self.y, target_x - self.x)
        self.x += self.speed * math.cos(angle)
        self.y += self.speed * math.sin(angle)

        # Flip the sprite based on the player's position
        if target_x < self.x:
            self.flipped = True  # Player is to the left of the enemy
        else:
            self.flipped = False  # Player is to the right of the enemy

    def update(self):
        """Update enemy's position and animation."""
        # Move towards the player's current position
        self.move_towards_player()

        # Update rect and animate
        self.rect.center = (self.x, self.y)
        self.update_animation()

    def draw(self, window):
        """Draw the enemy on the window and show the hitbox."""
        window.blit(self.image, self.rect)  # Draw the enemy sprite at its current position

        # Optional: Draw the hitbox rectangle for visualization
        # Reduce the size of the hitbox by half (you can adjust this factor as needed)
        reduced_width = self.rect.width // 1.125
        reduced_height = self.rect.height // 1.125
        reduced_rect = pygame.Rect(self.rect.centerx - reduced_width // 2, self.rect.centery - reduced_height // 2, reduced_width, reduced_height)

        pygame.draw.rect(window, (0, 255, 0), reduced_rect, 2)  # Green rectangle with a 2-pixel border for hitbox
