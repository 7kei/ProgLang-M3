import pygame
from Player import *
from Enemy import *
from Question import *
from GameState import *
from Database import *

BLUE = (106, 159, 181)
WHITE = (255, 255, 255)

class Level:
    def __init__(self, window, database: Database):
        self.window = window
        self.player = Player(800 // 2, 600 // 2, 1000, window)
        self.databaseConnection = database
        self.questions_dict = {}
        self.enemyList = []
        self.bullets = []
        self.initQuestions()
        self.initEnemies()
        self.player_answer = ""
        self.enemy_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.GroupSingle()  # Use Single for the player as it's only one
        
        # Ensure player is centered at the start
        # screen_width, screen_height = self.window.get_size()
        # self.player.x, self.player.y = screen_width // 2, screen_height // 2

        
    def initQuestions(self):
        curQues = self.databaseConnection.getQuestions()
        for i in curQues:
            self.questions.append(Question(i[0], i[1]))

    def initEnemies(self):
        num_enemies = 8
        angle_between_enemies = 2 * math.pi / num_enemies
        
        # Window center
        center_x = self.window.get_rect().center[0]
        center_y = self.window.get_rect().center[1]
        
        self.questions = list(self.questions_dict.items()) # Convert question dictionary to list of tuples
        
        for i in range(num_enemies):
            question_text, answer = self.questions.pop(random.randint(0, len(self.questions) - 1))
            
            # Set an initial angle for each enemy
            angle = i * angle_between_enemies
            
            # Create the enemy with the specified starting angle
            enemy = Enemy(self.window, (0, 0, 255), 3, center_x, center_y, 200, angle, 0.05, question=Question(question_text, answer))
            self.enemyList.append(enemy)
            
    def mainloop(self, eventList):
        self.window.fill((106, 159, 181))  # Blue BG
        
        if len(self.enemyList) == 0:  # Check if all enemies are destroyed
            return GameState.FINISH
        
        self.player.update(self.window, self.bullets, eventList, self.questions)
        
        # Update enemies and let them shoot
        curtime = time.time()
        for enemy in self.enemyList:
            enemy.update(curtime, self.bullets)
            
         # Update and draw each bullet
        for bullet in self.bullets[:]:
            bullet.update()  # Update bullet position
            bullet.draw(self.window)  # Draw bullet on the screen
            
            # Remove bullet if it goes off-screen
            if (bullet.pos[0] < 0 or bullet.pos[0] > self.window.get_width() or 
                bullet.pos[1] < 0 or bullet.pos[1] > self.window.get_height()):
                self.bullets.remove(bullet)

        for event in eventList:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.player_answer = self.player_answer[:-1]
                elif event.key == pygame.K_RETURN:
                    self.checkAnswer()
                elif event.unicode.isalnum():  # input as num and letters.
                    self.player_answer += event.unicode

        # Draw each enemy and its question
        for enemy in self.enemyList[:]:
            enemy.update(time.time(), self.bullets)
            enemy.question.draw(self.window, enemy.x, enemy.y - 40)  # Display question above enemy

        # Draw player's answer box
        self.drawAnswerBox()

        pygame.display.flip()
        
    def drawAnswerBox(self):
        # Create a font for displaying the answer
        font = pygame.font.SysFont("Arial", 24)
        
        # Render the player's current answer input
        answer_surf = font.render(f"|{self.player_answer}|", True, (255, 255, 255))
        
        # Get the player's position or rect (assuming self.player has this attribute)
        player_rect = self.player.rect if hasattr(self.player, 'rect') else pygame.Rect(0, 0, 50, 50)
        
        # Position the answer box above the player
        answer_box_x = player_rect.centerx - answer_surf.get_width() // 2
        answer_box_y = player_rect.top - answer_surf.get_height() - 10  # 10 pixels above the player
        
        # Draw the answer box at the calculated position
        self.window.blit(answer_surf, (answer_box_x, answer_box_y))

    def checkAnswer(self):
        for enemy in self.enemyList[:]:  # Copy to allow safe removal
            if enemy.question.checkAnswer(self.player_answer):
                self.enemyList.remove(enemy)  # Remove enemy if answer matches
                self.player_answer = ""  # Clear answer after correct response
                break
