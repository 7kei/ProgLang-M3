from Question import Question
import pygame
import math
import random
import time

class Bullet:
    def __init__(self, start_pos, direction, damage, speed=5):
        self.pos = start_pos[:]
        self.direction = direction
        self.speed = speed
        self.damage = damage

    def update(self):
        # Move bullet in the direction vector
        self.pos[0] += self.direction[0] * self.speed
        self.pos[1] += self.direction[1] * self.speed

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (int(self.pos[0]), int(self.pos[1])), 5)


class Enemy:
    # Load animation frames for all enemies
    try: 
        animation = [pygame.image.load(f"Sprites (assets)/bat/fly ({i}).png") for i in range(1, 4)]
    except pygame.error as e:
        print("Error loading animation frames:", e)
        animation = []  # Fallback to empty if loading fails
    def __init__(self, window, color, dmgAmt, center_x, center_y, radius, angle, speed, question):
        self.window = window
        self.dmgAmt = dmgAmt
        self.color = color
        self.center_x = center_x  # Center of circular path (window center)
        self.center_y = center_y  # Center of circular path (window center)
        self.radius = radius      # Radius of circular path
        self.angle = angle        # Starting angle
        self.speed = speed * 0.1  # Speed of circular motion
        self.last_fired = time.time()
        self.question = question
        self.question_font = pygame.font.Font(None, 24)
        
        # Animation frame index and timing
        self.animation_index = 0
        self.last_frame_update = time.time()

    def update(self, curtime, bullet_list):
        # Update position based on the circular path
        self.x = int(self.center_x + self.radius * math.cos(self.angle))
        self.y = int(self.center_y + self.radius * math.sin(self.angle))

        # Update and draw the current animation frame
        if Enemy.animation:
            if curtime - self.last_frame_update > 0.1:  # Adjust time to control frame rate
                self.animation_index = (self.animation_index + 1) % len(Enemy.animation)
                self.last_frame_update = curtime
            # Draw the animation frame at the calculated position
            current_frame = Enemy.animation[self.animation_index]
            frame_rect = current_frame.get_rect(center=(self.x, self.y))
            self.window.blit(current_frame, frame_rect)
        else:
            # Fallback to a circle if no animation frames were loaded
            pygame.draw.circle(self.window, self.color, (self.x, self.y), 30)

        # Increment the angle to keep moving in a circular path
        self.angle += self.speed * 0.5  # Adjust to control speed further if needed

        if curtime - self.last_fired >= 0.5:
            self.shoot(bullet_list)
            self.last_fired = curtime

    def shoot(self, bullet_list):
        dx, dy = self.window.get_rect().center[0] - self.x, self.window.get_rect().center[1] - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        direction = (dx / distance, dy / distance)
        bullet_list.append(Bullet([self.x, self.y], direction, self.dmgAmt))
