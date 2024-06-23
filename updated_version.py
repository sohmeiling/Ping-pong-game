# Codes for ping pong game

from pygame import *
import pygame.font
import random

class GameSprite(sprite.Sprite):
    #class constructor
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__() #sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
 
        #every sprite must have the rect property – the rectangle it is fitted in
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    #method drawing the character on the window
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

#child class
class Paddle (GameSprite):
    #method to control the sprite with arrow keys
    def update_right(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 150:
            self.rect.y += self.speed
    def update_left(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - 150:
            self.rect.y += self.speed

#interface
BLUE = (200, 255, 255)
win_width = 600
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Ping Pong")
window.fill(BLUE)

# Create a court background
background = Surface((win_width, win_height))
background.fill((0, 128, 0))  # Set green as background color

# Draw court boundaries
pygame.draw.rect(background, (255, 255, 255), (0, 0, win_width, 10))  # Top boundary
pygame.draw.rect(background, (255, 255, 255), (0, win_height - 10, win_width, 10))  # Bottom boundary

# Draw center line
pygame.draw.line(background, (255, 255, 255), (win_width // 2, 0), (win_width // 2, win_height), 2)


#create sprites (paddle and balls)
paddleA_img = "paddle_blue.png"
paddleB_img = "paddle_red.png"
ball_img = "tennis_ball.png"

paddleLeft = Paddle (paddleA_img, 20, 200, 30, 150, 5)
paddleRight = Paddle (paddleB_img, win_width - 50, 200, 30, 150, 5)
ball = GameSprite(ball_img, 330, 200, 50, 50, 2)


#game loop
game = True
finish = False
clock = time.Clock()
FPS = 60

#fonts
pygame.font.init()
font = pygame.font.Font(None, 35)
lose1 = font.render('BLUE PLAYER LOSE!', True, (180, 0, 0))
lose2 = font.render('RED PLAYER LOSE!', True, (180, 0, 0))

win_blue = font.render('BLUE PLAYER WIN!', True, (180, 0, 0))
win_red = font.render('RED PLAYER WIN!', True, (180, 0, 0))

BLUE_SCORE = 0
RED_SCORE = 0
font_score = pygame.font.Font(None, 18)
blue_board = font_score.render('BLUE: ' + str(BLUE_SCORE), True, (0, 0, 0))
red_board = font_score.render('RED: ' + str(RED_SCORE), True, (0, 0, 0))

# Randomly determine the initial direction and speed of the ball
initial_direction = random.choice([-1, 1])  # Randomly choose -1 (left) or 1 (right)
speed_x = 3 * initial_direction
speed_y = 3 * initial_direction

# Introducing acceleration of the ball
acceleration = 0.0005

while game:
    for e in event.get():
        if e.type ==QUIT:
            game = False

    if finish != True:
        window.fill (BLUE)
        window.blit(background, (0, 0))
        paddleLeft.update_left()
        paddleRight.update_right()

        ball.rect.x += speed_x 
        ball.rect.y += speed_y 

        # Accelerate the ball
        speed_x += acceleration * speed_x
        speed_y += acceleration * speed_y

        # Score board for both players
        window.blit(blue_board, (10, 10))
        window.blit(red_board, (win_width - 80, 10))

        # Ball bounces when hit the paddle
        if sprite.collide_rect(paddleLeft, ball) and speed_x < 0:
            BLUE_SCORE += 1
            blue_board = font_score.render('BLUE: ' + str(BLUE_SCORE), True, (0, 0, 0))
            # Randomize the angle of bounce by adjusting speed_y
            speed_x *= -1
            speed_y *= 1

        if sprite.collide_rect(paddleRight, ball) and speed_x > 0:
            RED_SCORE += 1
            red_board = font_score.render('RED: ' + str(RED_SCORE), True, (0, 0, 0))
            # Randomize the angle of bounce by adjusting speed_y
            speed_x *= -1
            speed_y *= 1

        # Ball bounces when hit the top or bottom wall
        if ball.rect.y <= 10 or ball.rect.y >= win_height - 50:
            speed_y *= -1

        #if ball flies behind this paddle, display loss condition for player left
        if ball.rect.x < 0:
            finish = True
            game_over = True
            window.blit(lose1, (200, 200))

        #if the ball flies behind this paddle, display loss condition for player right
        if ball.rect.x > win_width:
            finish = True
            game_over = True
            window.blit(lose2, (200, 200))

        if BLUE_SCORE >= 11: 
            finish = True
            game_over = True
            window.blit(win_blue, (200, 200))


        if RED_SCORE >= 11: 
            finish = True
            game_over = True
            window.blit(win_red, (200, 200))

        paddleLeft.reset()
        paddleRight.reset()
        ball.reset()

    display.update()
    clock.tick(FPS)
