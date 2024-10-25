import pygame
from Player import *
from Enemy import *

BLUE = (106, 159, 181)
WHITE = (255, 255, 255)

class Level:
    def __init__(self, window):
        self.window = window
        self.player = Player(800//2, 600//2, 1000)
        self.ring0 : list[Enemy] = []
        self.bullets : list[Bullet] = []
        self.initEnemies()

    def initEnemies(self):
        num_enemies = 8
        angle_between_enemies = 2 * math.pi / num_enemies

        # Window center
        center_x = self.window.get_rect().center[0]
        center_y = self.window.get_rect().center[1]

        for i in range(num_enemies):
            # Set an initial angle for each enemy
            angle = i * angle_between_enemies

            # Create the enemy with the specified starting angle
            enemy = Enemy(self.window, (0,0,255), 3, center_x, center_y, 200, angle, 0.05)
            self.ring0.append(enemy)

    def mainloop(self):
        self.window.fill(BLUE)

        for bullet in self.bullets:
            bullet.update()
            bullet.draw(self.window)

        self.player.update(self.window, self.bullets)

        curtime = time.time()
        for enemy in self.ring0:
            enemy.update(curtime, self.bullets)
            