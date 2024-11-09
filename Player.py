import pygame
import os
from Projectile import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, max_health=100):
        super().__init__()

        # Position and physics properties
        self.x = x
        self.y = y
        self.speed = 5
        self.velocity_y = 0
        self.is_jumping = False
        self.jumpCount = 10
        self.facing_right = True  # Default facing direction

        # Health attributes
        self.max_health = max_health
        self.current_health = max_health

        # Load animations
        self.animations = {
            "idle": self.load_animation('assets/wizard/idle'),
            "run": self.load_animation('assets/wizard/run'),
            "jump": self.load_animation('assets/wizard/jump'),
            "attack2": self.load_animation('assets/wizard/attack2'),
            "death": self.load_animation('assets/wizard/death'),
            "hit": self.load_animation('assets/wizard/hit')  # Hit animation
        }

        # Set initial animation
        self.current_animation = "idle"
        self.animation_index = 0
        self.jump_animation_index = 0  # Separate index for jump animation
        self.image = self.animations[self.current_animation][self.animation_index]

        # Set up the hitbox rect and image rect
        self.rect = self.image.get_rect(center=(self.x, self.y))  # Hitbox for collision detection
        self.image_rect = self.rect.copy()  # Separate rect for the image (visual transformation)

        # Resize the rect (e.g., to shrink the player's hitbox during attack)
        self.rect.width = self.image_rect.width // 7  # Adjust width (e.g., reduce width by 7)
        self.rect.height = self.image_rect.height // 4  # Adjust height (e.g., reduce height by 4)

        # Flags to track animation states
        self.in_attack_animation = False
        self.is_hit = False  # Flag to track if the player is hit
        self.knockback_direction = 0  # Flag to track knockback direction (1 or -1)
        self.is_knocked_back = False  # Flag to track if the player is currently in knockback state
        self.knockback_timer = 0  # Timer to track the duration of the knockback
        self.hit_timer = 0  # Timer for how long the player stays in the hit state

        # Ritual state flag
        self.is_in_ritual = False  # Whether the player is in ritual state

    def load_animation(self, path):
        """Load all images in a folder as animation frames."""
        return [pygame.image.load(os.path.join(path, img)) for img in sorted(os.listdir(path))]

    def handle_input(self):
        """Handle player input for movement, jumping, and attacking."""
        if self.is_in_ritual:
            return  # Disable input if the player is in ritual state

        if self.is_knocked_back:
            return  # Prevent movement during knockback

        keys = pygame.key.get_pressed()

        # Trigger attack animation on mouse click if not already attacking
        if pygame.mouse.get_pressed()[0] and not self.in_attack_animation:
            self.in_attack_animation = True
            self.current_animation = "attack2"  # Set to attack animation
            self.animation_index = 0  # Start from the first frame

        # If the attack animation is not active, handle other movements and animations
        if not self.in_attack_animation:
            # Movement and facing direction
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.x -= self.speed
                self.facing_right = False
                if not self.is_jumping:
                    self.current_animation = "run"
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.x += self.speed
                self.facing_right = True
                if not self.is_jumping:
                    self.current_animation = "run"
            else:
                if not self.is_jumping:
                    self.current_animation = "idle"

            # Jumping
            if not self.is_jumping:
                if keys[pygame.K_UP] or keys[pygame.K_w]:
                    self.is_jumping = True
                    self.current_animation = "jump"  # Set to jump animation
                    self.jump_animation_index = 0  # Reset jump animation index

    def enter_ritual(self):
        """Enter the ritual state and play the hit animation in a loop."""
        self.is_in_ritual = True
        self.x = 900  # Move the player to the center of the screen (adjust for your screen size)
        self.y = 600
        self.facing_right = True  # Ensure the player is facing right during the ritual
        self.current_animation = "hit"  # Play the hit animation in a loop

    def update_animation(self):
        """Update animation frame based on current action and direction."""
        if self.is_in_ritual:
            # In ritual, play the hit animation in a loop
            self.animation_index += 0.12
            self.facing_right = True
            if self.animation_index >= len(self.animations["hit"]):
                self.animation_index = 0  # Loop the hit animation
            frame = self.animations["hit"][int(self.animation_index)]
        elif self.is_hit:
            # Trigger hit animation and use the hit timer
            self.current_animation = "hit"
            self.animation_index += 0.12
            if self.animation_index >= len(self.animations["hit"]):
                self.animation_index = 0

            # Flip the hit animation based on knockback direction
            if self.knockback_direction > 1:
                self.facing_right = False  # Flip the direction for knockback to the right
            elif self.knockback_direction < -1:
                self.facing_right = True  # Flip the direction for knockback to the left

            frame = self.animations[self.current_animation][int(self.animation_index)]

        elif self.in_attack_animation:
            # Determine the facing direction during attack based on mouse position
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if mouse_x < self.x:
                self.facing_right = False  # Face left if mouse is to the left
            else:
                self.facing_right = True  # Face right if mouse is to the right

            # Run through the attack animation frames
            self.animation_index += 0.15
            if self.animation_index >= len(self.animations["attack2"]):
                self.animation_index = 0  # Reset the animation after completing
                self.in_attack_animation = False  # End attack animation
                # Resume the jump animation if player is mid-jump
                if self.is_jumping:
                    self.current_animation = "jump"

            # Set the frame for the attack animation
            frame = self.animations["attack2"][int(self.animation_index)]

        else:
            # If in jump animation, continue progressing jump frames
            if self.current_animation == "jump":
                self.jump_animation_index += 0.09
                if self.jump_animation_index >= len(self.animations["jump"]):
                    self.jump_animation_index = 0
                frame = self.animations["jump"][int(self.jump_animation_index)]
            else:
                # Other animations (idle/run)
                self.animation_index += 0.15
                if self.animation_index >= len(self.animations[self.current_animation]):
                    self.animation_index = 0
                frame = self.animations[self.current_animation][int(self.animation_index)]

        # Flip the frame if the player is facing left
        self.image = pygame.transform.flip(frame, True, False) if not self.facing_right else frame

        # Update image_rect to center the player sprite
        self.image_rect = self.image.get_rect(center=(self.x, self.y))

    def update(self):
        """Update player position and animation."""
        if self.is_knocked_back:
            # Apply knockback
            self.x += self.knockback_direction  # Move the player slightly based on knockback direction
            self.knockback_timer -= 1  # Decrease the knockback duration timer

            if self.knockback_timer <= 0:
                self.is_knocked_back = False  # End knockback state when timer expires

        # Update animation (does not depend on input)
        self.update_animation()  # Update the animation frame regardless of input

        # Hit state timer: If the player is hit, start the timer
        if self.is_hit:
            self.hit_timer += 1  # Increment the hit timer
            if self.hit_timer >= 30:  # Assuming the hit animation lasts for 30 frames
                self.is_hit = False  # Reset hit flag
                self.hit_timer = 0  # Reset the hit timer
                self.current_animation = "idle"  # Return to idle state after hit animation completes

        # Update the vertical position during jumping, even if the player is hit
        if self.is_jumping:
            if self.jumpCount >= -10:
                neg = 1
                if self.jumpCount < 0:
                    neg = -1
                self.y -= (self.jumpCount ** 2) * 0.15 * neg  # Applying slower jump arc
                self.jumpCount -= 0.5  # Extended air time
            else:
                self.is_jumping = False
                self.jumpCount = 10
                # Reset to idle or run animation based on movement
                if self.x != 0:  # If moving left or right, play run animation
                    self.current_animation = "run"
                else:
                    self.current_animation = "idle"

        # Prevent the player from falling below the ground level (e.g., 500 is the ground level)
        if self.y >= 790:
            self.y = 790  # Reset position to ground level
            self.is_jumping = False
            self.jumpCount = 10  # Reset jump count

        # Gradually move the player towards the center during ritual
        if self.is_in_ritual:
            target_x, target_y = 750, 400  # Ritual target position (center)
            if abs(self.x - target_x) > self.speed:
                self.x += self.speed if self.x < target_x else -self.speed
            if abs(self.y - target_y) > self.speed:
                self.y += self.speed if self.y < target_y else -self.speed

        # Update the hitbox rect to follow the player's position
        self.rect.center = (self.x, self.y)

    def handle_attack(self, mouse_x, mouse_y):
        """Handle player attack animation and create projectiles."""
        self.current_animation = "attack2"
        self.animation_index = 0  # Reset animation to start from the first frame
        
        # Pass path to the projectile's animation frames
        projectile_path = 'assets/projectile'  # Example path for your projectile animation frames
        return Projectile(self.x, self.y, mouse_x, mouse_y, projectile_path)

    def apply_knockback(self, enemy_x, enemy_y, knockback_strength):
        """Apply knockback based on the position of the enemy."""
        if enemy_x < self.x:
            # Enemy is to the left, apply knockback to the right
            self.knockback_direction = 1 * knockback_strength
        else:
            # Enemy is to the right, apply knockback to the left
            self.knockback_direction = -1 * knockback_strength
        
        self.is_knocked_back = True  # Trigger knockback state
        self.knockback_timer = 25  # Duration of knockback in frames (adjust as needed)
        self.is_hit = True  # Trigger the hit state when knockback happens

    def draw(self, window):
        """Draw the player on the game window and show the rectangle."""
        # Draw the player sprite using image_rect to ensure it's centered
        window.blit(self.image, self.image_rect.topleft)  # Draw the image at the top-left of the rect

        # Optional: Draw the rectangle around the player for visualization
        pygame.draw.rect(window, (255, 0, 0), self.rect, 2)  # Red rectangle with a 2-pixel border
