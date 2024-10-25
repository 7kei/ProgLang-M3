import pygame
from pygame import Rect
from Enemy import *

class Player:
    def __init__(self, x, y, maxHealth):
        self.maxHealth = maxHealth
        self.x = x
        self.y = y
        self.currentHealth = maxHealth
        self.hitbox = Rect(0,0,120,120)
        self.hitbox.center = x,y

    def update(self, window, bulletList:list[Bullet]):
        # Check if bullet hit us
        for bullet in bulletList:
            if self.hitbox.collidepoint(bullet.pos):
                bulletList.remove(bullet)
                self.dmg(bullet.damage)

        self.draw(window)
    
    def draw(self,window):
        pygame.draw.circle(window, (255, 255, 255), (self.x, self.y), 80)
        pygame.draw.rect(window, (255,0,0), self.hitbox, 5)
        pygame.draw.rect(window, (255,0,0), Rect(self.x-self.maxHealth*0.1//2, self.y+120, self.maxHealth*0.1, 20))
        pygame.draw.rect(window, (0,255,0), Rect(self.x-self.maxHealth*0.1//2, self.y+120, self.currentHealth*0.1, 20))
    
    def dmg(self, amt):
        if self.currentHealth <= 0:
            return
        if self.currentHealth - amt < 0:
            self.currentHealth = 0
        else:
            self.currentHealth -= amt
    
    def heal(self, amt):
        if self.currentHealth >= self.maxHealth:
            return
        self.currentHealth += amt