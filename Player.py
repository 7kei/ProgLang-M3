import pygame
from pygame import Rect
from Enemy import *
from Question import *

class Player:
    def __init__(self, x, y, maxHealth):
        self.maxHealth = maxHealth
        self.x = x
        self.y = y
        self.currentHealth = maxHealth

        self.hitbox = Rect(0,0,120,120)
        self.hitbox.center = x,y
        self.inputText = ''
        self.inputBox = Rect(self.x-150/2, self.y-150, 150, 60)
        

    def update(self, window, bulletList : list[Bullet], eventList:list[pygame.event.Event], questionList:list[Question]):
        # Check if bullet hit us
        for bullet in bulletList:
            if self.hitbox.collidepoint(bullet.pos):
                bulletList.remove(bullet)
                self.dmg(bullet.damage)

        for event in eventList:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Check input
                    for i in range(len(questionList)):
                        curQues = questionList[i]
                        if curQues.checkAnswer(self.inputText):
                            questionList.remove(curQues)
                    self.inputText = ''

                elif event.key == pygame.K_BACKSPACE:
                    self.inputText = self.inputText[:-1]
                else:
                    self.inputText += event.unicode

        self.draw(window)
    
    def draw(self,window : pygame.display):
        # Player
        pygame.draw.circle(window, (255, 255, 255), (self.x, self.y), 80)
        # Player Hitbox
        pygame.draw.rect(window, (255,0,0), self.hitbox, 5)

        # Health Bar
        pygame.draw.rect(window, (255,0,0), Rect(self.x-self.maxHealth*0.1//2, self.y+120, self.maxHealth*0.1, 20))
        pygame.draw.rect(window, (0,255,0), Rect(self.x-self.maxHealth*0.1//2, self.y+120, self.currentHealth*0.1, 20))

        # Input Rectangle
        pygame.draw.rect(window, (255,255,255), self.inputBox)

        # Input Text
        inputBoxTextSurface = pygame.font.SysFont('Arial', 12).render(self.inputText, True, pygame.Color(0,0,0))
        window.blit(inputBoxTextSurface, (self.inputBox.x, self.inputBox.y))
    
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
        if self.currentHealth + amt >= self.maxHealth:
            self.currentHealth = self.maxHealth
        self.currentHealth += amt