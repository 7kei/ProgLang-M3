import pygame
import os
import random

class Comet(pygame.sprite.Sprite):
    def __init__(self, player_x, falling_path, explosion_path, scale=1):
        super().__init__()

        # Comet's initial position (off-screen above the window)
        self.x = random.randint(0, 1500)  # Random X position
        self.y = -50  # Spawn above the screen
        self.scale = scale  # Default scaling factor for the comet's size
        self.speed = 2 # Falling speed
        self.animation_speed = 0.15 # Speed of animation frame change

        # Track the player's last X position when the comet spawns
        self.target_x = player_x

        # Load the falling and explosion animation frames
        self.animations = {
            "falling": self.load_animation(falling_path, scale=2),  # Smaller scale during falling
            "explosion": self.load_animation(explosion_path, scale=5)  # Bigger scale during explosion
        }

        # Initial state is falling
        self.state = "falling"
        self.animation_index = 0
        self.image = self.animations[self.state][self.animation_index]
        self.rect = self.image.get_rect(center=(self.x, self.y))  # Hitbox for collision detection
        self.image_rect = self.rect.copy()  # Separate rect for the image (visual transformation)

        # Resize the rect (e.g., to shrink the comet's hitbox during attack)
        self.rect.width = self.image_rect.width // 2 # Adjust width (e.g., reduce width by 4)
        self.rect.height = self.image_rect.height // 2 # Adjust height (e.g., reduce height by 3)

    def load_animation(self, path, scale=1):
        """Load all images in a folder as animation frames and scale them."""
        frames = [pygame.image.load(os.path.join(path, img)) for img in sorted(os.listdir(path))]
        # Scale each frame based on the provided scale factor
        return [pygame.transform.scale(frame, (int(frame.get_width() * scale), int(frame.get_height() * scale))) for frame in frames]

    def update_animation(self):
        """Update the animation frame based on current state."""
        self.animation_index += self.animation_speed

        if int(self.animation_index) >= len(self.animations[self.state]):
            if self.state == "falling":
                # Reset to beginning of falling animation or transition to explosion
                self.animation_index = 0
                self.image_rect.center = (self.x, self.y)  # Ensure explosion is centered on the comet's position
            elif self.state == "explosion":
                # End the comet's existence after explosion animation finishes
                self.kill()
                return

        self.image = self.animations[self.state][int(self.animation_index)]
        self.image_rect = self.image.get_rect(center=(self.x, self.y))

        # # Resize the rect (collision box) based on the image's new dimensions
        # self.rect.width = self.image_rect.width // 2  # Example: Make the collision box half the width of the sprite
        # self.rect.height = self.image_rect.height // 2  # Example: Make the collision box half the height of the sprite

    def update(self):
        """Update comet's position and animation based on its state."""
        if self.state == "falling":
            # Fall towards the player's X position (does not home in, just tracks where it started)
            self.y += self.speed  # Make it fall down
            self.x = self.target_x  # Track the player's X position at the time of spawn
            
            if self.y >= 725:  # Check if the comet has reached 7 pixels above the ground (790 - 7)
                self.state = "explosion"  # Trigger the explosion when it reaches 7 pixels from the ground
                self.animation_index = 0
                self.image_rect.center = (self.x, self.y)  # Ensure explosion is centered on the comet's position

        # Update the hitbox (rect) position to follow the comet's position
        self.rect.center = (self.x, self.y)
                
        # Update animation based on the state
        self.update_animation()

        

    def draw(self, window):
        """Draw the comet or explosion on the window."""
        # Draw the comet or explosion image
        window.blit(self.image, self.image_rect.topleft)
        
        # Draw the green hitbox for debugging (optional)
        # pygame.draw.rect(window, (0, 255, 0), self.rect, 2)  # Green hitbox with 2-pixel border

        # Only draw the oval and text during the 'falling' state
        if self.state == "falling":
            # Calculate the center of the comet
            center_x, center_y = self.rect.center

            # Set the size of the oval (width and height)
            oval_width = 75  # Width of the oval
            oval_height = 100  # Height of the oval
            border_width = oval_width + 10  # Slightly larger width for the oval border
            border_height = oval_height + 10  # Slightly larger height for the oval border

            # Draw a red oval border
            pygame.draw.ellipse(window, (255, 0, 0), 
                                (center_x - border_width // 2, center_y+20 - border_height // 2, 
                                border_width, border_height))  # Red border

            # Draw the white oval in the center
            pygame.draw.ellipse(window, (255, 255, 255), 
                                (center_x - oval_width // 2, center_y+20 - oval_height // 2, 
                                oval_width, oval_height))  # White oval

            # Render the text inside the oval
            font = pygame.font.SysFont("Arial", 24)  # Set font and size
            text = font.render("1+1 = ?", True, (0, 0, 0))  # Create text (black color)
            text_rect = text.get_rect(center=(center_x, center_y+20))  # Center the text in the oval

            # Draw the text on the window
            window.blit(text, text_rect)






