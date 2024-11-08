import pygame
import random
import os
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

        self.scale = scale
        self.speed = 3
        self.animation_speed = 0.2
        self.flipped = False
        self.last_frame_update = pygame.time.get_ticks() / 1000.0  # Convert to seconds
        self.last_fired = pygame.time.get_ticks() / 1000.0

        # Randomly choose enemy type: 0 for positive, 1 for negative
        self.enemy_type = random.choice([0, 1])
        animation_folder = "positive" if self.enemy_type == 0 else "negative"
        self.frames = self.load_animation(f"assets/bat/{animation_folder}")
        
        # Initialize animation state
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        
        # Set up the hitbox rect and image rect
        self.rect = self.image.get_rect(center=(self.x, self.y))  # Hitbox for collision detection
        self.image_rect = self.rect.copy()  # Separate rect for the image (visual transformation)

        # Set the player reference and window
        self.player = player
        self.window = None  # Will be set when drawing

    def load_animation(self, path):
        """Load and downsize all images in a folder as animation frames."""
        frames = []
        for img in sorted(os.listdir(path)):
            frame = pygame.image.load(os.path.join(path, img))
            # Downsize the frame to 25% of the original size
            downsized_frame = pygame.transform.scale(frame, (frame.get_width() // 4, frame.get_height() // 4))
            frames.append(downsized_frame)
        return frames

    def update_animation(self):
        """Update the animation frames of the enemy."""
        current_time = pygame.time.get_ticks() / 1000.0
        
        if current_time - self.last_frame_update > 0.1:  # Update every 0.1 seconds
            self.animation_index = (self.animation_index + 1) % len(self.frames)
            self.last_frame_update = current_time
            
        self.image = self.frames[self.animation_index]
        
        if self.flipped:
            self.image = pygame.transform.flip(self.image, True, False)
        
        # Update image_rect based on the flipped image
        self.image_rect = self.image.get_rect(center=(self.x, self.y))

    def move_towards_player(self):
        """Move the enemy towards the player's current position."""
        target_x, target_y = self.player.rect.center
        angle = math.atan2(target_y - self.y, target_x - self.x)
        self.x += self.speed * math.cos(angle)
        self.y += self.speed * math.sin(angle)

        # Update facing direction
        self.flipped = target_x < self.x

    def update(self):
        """Update enemy's position and animation."""
        self.move_towards_player()
        self.rect.center = (self.x, self.y)
        self.update_animation()

    def draw(self, window):
        """Draw the enemy on the window."""
        self.window = window  # Store the window reference
        window.blit(self.image, self.rect)

        # Draw hitbox (optional, for debugging)
        reduced_width = self.rect.width // 1.125
        reduced_height = self.rect.height // 1.125
        reduced_rect = pygame.Rect(
            self.rect.centerx - reduced_width // 2,
            self.rect.centery - reduced_height // 2,
            reduced_width,
            reduced_height
        )
        pygame.draw.rect(window, (255, 0, 0), reduced_rect, 1)  # Red rectangle with 1-pixel border

    # def shoot(self, bullet_list):
    #     """Create a new bullet aimed at the player."""
    #     current_time = pygame.time.get_ticks() / 1000.0
        
    #     if current_time - self.last_fired >= 0.5:  # Shoot every 0.5 seconds
    #         if self.window:  # Check if window reference exists
    #             target_x, target_y = self.window.get_rect().center
    #             dx, dy = target_x - self.x, target_y - self.y
    #             distance = math.sqrt(dx ** 2 + dy ** 2)
    #             direction = (dx / distance, dy / distance)
                
    #             # Create new bullet (implementation depends on your Bullet class)
    #             bullet_list.append(Bullet([self.x, self.y], direction, self.dmg_amt))
    #             self.last_fired = current_time
