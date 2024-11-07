import pygame

class HealthBar:
    def __init__(self, max_health=100, initial_health=100, pos=(100, 100), size=(200, 20)):
        self.max_health = max_health
        self.current_health = initial_health
        self.pos = pos
        self.size = size
        self.green_color = (0, 255, 0)
        self.red_color = (255, 0, 0)

    def damage(self, amount):
        self.current_health = max(0, self.current_health - amount)

    def heal(self, amount):
        self.current_health = min(self.max_health, self.current_health + amount)

    def is_dead(self):
        return self.current_health <= 0
    
    def update_position(self, position):
        self.position = position

    def needs_heal(self):
        return self.current_health < self.max_health

    def draw(self, window):  # Accept window as an argument
        # Calculate the width of the green (health) part
        green_width = int((self.current_health / self.max_health) * self.size[0])

        # Draw the red (empty) part
        pygame.draw.rect(window, self.red_color, (*self.pos, *self.size))

        # Draw the green (health) part on top
        pygame.draw.rect(window, self.green_color, (self.pos[0], self.pos[1], green_width, self.size[1]))
