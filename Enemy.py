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
    def __init__(self, window, color, dmgAmt, center_x, center_y, radius, angle, speed):
        self.window = window
        self.dmgAmt = dmgAmt
        self.color = color
        self.center_x = center_x    # Center of circular path (window center)
        self.center_y = center_y    # Center of circular path (window center)
        self.radius = radius        # Radius of circular path
        self.angle = angle          # Starting angle
        self.speed = speed          # Speed of circular motion
        self.last_fired = time.time()

    def update(self, curtime, bullet_list):
        # Update position based on the circular path
        self.x = int(self.center_x + self.radius * math.cos(self.angle))
        self.y = int(self.center_y + self.radius * math.sin(self.angle))

        # Draw the enemy at the calculated position
        pygame.draw.circle(self.window, self.color, (self.x, self.y), 30)

        # Increment the angle to keep moving in a circular path
        self.angle += self.speed

        if curtime - self.last_fired >= 0.5:
            self.shoot(bullet_list)
            self.last_fired = curtime

    def shoot(self, bullet_list):
        dx, dy = self.window.get_rect().center[0] - self.x, self.window.get_rect().center[1] - self.y
        distance = math.sqrt(dx**2 + dy**2)
        direction = (dx / distance, dy / distance)
        bullet_list.append(Bullet([self.x,self.y], direction, self.dmgAmt))