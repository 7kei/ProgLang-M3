import pygame
import random
import os
import math

class Enemy(pygame.sprite.Sprite):
    def __init__(self, player, scale=2):
        super().__init__()

        # Initial position logic
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

        self.scale = scale
        self.speed = 3
        self.animation_speed = 0.2
        self.flipped = False  # Track sprite flipping

        # Randomly choose enemy type for animation
        self.enemy_type = random.choice([0, 1])
        animation_folder = "positive" if self.enemy_type == 0 else "negative"
        self.frames = self.load_animation(f"assets/bat/{animation_folder}")
        
        # Initialize animation state
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        
        # Set up the hitbox rect and image rect
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.image_rect = self.rect.copy()

        # Reference to the player for movement
        self.player = player
        self.window = None  # Will be set when drawing

        # Death animation state
        self.dying = False
        self.dying_time = 0
        self.death_duration = 500  # Death animation duration in ms
        self.max_scale = 2  # Max size for the death animation
        self.opacity = 255  # Fully opaque for the initial image
        self.initial_image = self.frames[0]  # First frame for death animation

    def load_animation(self, path):
        """Load and downsize all images in a folder as animation frames."""
        frames = []
        for img in sorted(os.listdir(path)):
            frame = pygame.image.load(os.path.join(path, img))
            downsized_frame = pygame.transform.scale(frame, (frame.get_width() // 4, frame.get_height() // 4))
            frames.append(downsized_frame)
        return frames

    def update_animation(self):
        """Update the animation frames of the enemy."""
        if not self.dying:
            self.animation_index += self.animation_speed
            if int(self.animation_index) >= len(self.frames):
                self.animation_index = 0  # Loop the animation frames
            self.image = self.frames[int(self.animation_index)]
        else:
            self.death_animation()

        # Flip the sprite if necessary (based on the player's position)
        if self.flipped:
            self.image = pygame.transform.flip(self.image, True, False)
        
        # Update image_rect based on the flipped image
        self.image_rect = self.image.get_rect(center=(self.x, self.y))

    def death_animation(self):
        """Handles the death animation (expansion and fade)."""
        self.dying_time += 16  # 16ms per frame at 60fps

        # Scale the image gradually (expand to twice the original size)
        scale_factor = 1 + (self.dying_time / self.death_duration)
        scale_factor = min(scale_factor, self.max_scale)  # Ensure we don't go beyond max scale
        self.image = pygame.transform.scale(self.initial_image, (int(self.initial_image.get_width() * scale_factor),
                                                                  int(self.initial_image.get_height() * scale_factor)))

        # Fade out the image
        fade_factor = 1 - (self.dying_time / self.death_duration)
        fade_factor = max(fade_factor, 0)  # Ensure opacity doesn't go negative
        self.image.set_alpha(int(255 * fade_factor))

        # Once the animation finishes, kill the enemy
        if self.dying_time >= self.death_duration:
            self.kill()

    def move_towards_player(self):
        """Move the enemy towards the player's current position."""
        if self.dying:
            return  # Don't move if dying

        target_x, target_y = self.player.rect.center
        angle = math.atan2(target_y - self.y, target_x - self.x)
        self.x += self.speed * math.cos(angle)
        self.y += self.speed * math.sin(angle)

        # Flip the sprite based on the player's position
        if target_x < self.x:
            self.flipped = True
        else:
            self.flipped = False

    def update(self):
        """Update enemy's position and animation."""
        if not self.dying:
            self.move_towards_player()  # Move only if not dying

        # Update the hitbox position and animation
        self.rect.center = (self.x, self.y)
        self.update_animation()

    def draw(self, window):
        """Draw the enemy on the window."""
        self.window = window  # Store the window reference
        window.blit(self.image, self.rect)

        # Optionally, draw the hitbox (for debugging)
        pygame.draw.rect(window, (0, 255, 0), self.rect, 2)  # Green hitbox for visualization

    def die(self):
        """Start the death animation."""
        self.dying = True
        self.dying_time = 0  # Reset dying time to start the animation
        self.initial_image = self.frames[0]  # First frame for death animation
