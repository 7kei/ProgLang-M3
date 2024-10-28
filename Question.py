import pygame
from pygame import Rect

class Question:
    def __init__(self, question, answer):
        self.questionSurface = pygame.font.SysFont('Arial', 12).render(question, True, pygame.Color(0,0,0))
        self.answer = answer
    
    def checkAnswer(self, answerToBeChecked: str):
        return answerToBeChecked.strip().lower() == self.answer
    
    def draw(self, window, x, y):
        # BG
        pygame.draw.rect(window, (255,255,255), Rect(x,y,150,60))

        window.blit(self.questionSurface, (x,y))