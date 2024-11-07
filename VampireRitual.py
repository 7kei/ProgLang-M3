import pygame

class VampireRitual:
    try:
        animation = [pygame.image.load(f'Sprites/bat/fly ({i}).png') for i in range(1, 4)]
    except pygame.error as e:
        print("Error loading animation frames:", e)
        animation = []

    def __init__(self, window, color, dmgAmt, center_x, center_y, radius, angle, speed, question):
        self.window = window
        self.dmgAmt = dmgAmt
        self.color = color
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius
        self.angle = angle
        self.speed = speed * 0.1
        self.last_fired = time.time()
        self.question = question
        self.question_font = pygame.font.Font(None, 24)

        self.animation_index = 0
        self.last_frame_update = time.time()

        self.enemyList = []
        self.bullets = []
        self.initQuestions()
        self.initEnemies()

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
        
    def initQuestions(self):
        self.questions_dict = {
            "What is 3+4?": "7",
            "What is 5*2?": "10",
            "What is 9-3?": "6",
            "What is 8/2?": "4",
            "What is 1+1?": "2",
            "Color of an apple?" : "red",
            "Color of the sea?" : "blue",
            "Is orange a fruit?" : "yes",
        }

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