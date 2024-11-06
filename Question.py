import pygame
from pygame import Rect

class Question:
    def __init__(self, question, answer):
        self.font = pygame.font.SysFont('Arial', 12)
        self.questionSurface = self.font.render(question, True, pygame.Color(0, 0, 0))  # Text with no background
        self.answer = answer
    
    def checkAnswer(self, answerToBeChecked: str):
        return answerToBeChecked.strip().lower() == self.answer
    
    def draw(self, window, x, y):
        # display question
        window.blit(self.questionSurface, (x,y))
    
    def draw_question(self, screen):
        question_text = question_font.render(self.question.text, True, (255, 255, 255))  # White text, no background
        text_rect = question_text.get_rect(center=(self.x, self.y - 20))  # Position text slightly above the enemy
        screen.blit(question_text, text_rect)
