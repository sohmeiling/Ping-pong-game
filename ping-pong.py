# Codes for ping pong game

from pygame import *

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
window.fill(BLUE)

#create sprites (paddle and balls)
paddleA_img = "paddle_blue.png"
paddleB_img = "paddle_red.png"
ball_img = "tennis_ball.png"

paddleLeft = Paddle (paddleA_img, 20, 200, 30, 150, 50)
paddleRight = Paddle (paddleB_img, 520, 200, 30, 150, 50)
ball = GameSprite(ball_img, 330, 200, 50, 50, 50)


#game loop
game = True
finish = False
clock = time.Clock()
FPS = 60

#fonts
font.init()
font = font.Font(None, 35)
lose1 = font.render('BLUE PLAYER LOSE!', True, (180, 0, 0))
lose2 = font.render('RED PLAYER LOSE!', True, (180, 0, 0))

speed_x = 3
speed_y = 3

while game:
    for e in event.get():
        if e.type ==QUIT:
            game = False

    if finish != True:
        window.fill (BLUE)
        paddleLeft.update_left()
        paddleRight.update_right()

        ball.rect.x += speed_x
        ball.rect.y += speed_y

        if sprite.collide_rect(paddleLeft, ball) or sprite.collide_rect(paddleRight, ball):
            speed_x *= -1
            speed_y *= 1

        #ball bounces when hit the up or bottom wall
        if ball.rect.y > win_height-50 or ball.rect.y < 0:
            speed_y *= -1

        #if ball flies behind this paddle, display loss condition for player left
        if ball.rect.x < 0:
            finish = False
            window.blit(lose1, (200, 200))

        #if the ball flies behind this paddle, display loss condition for player right
        if ball.rect.x > win_width:
            finish = False
            window.blit(lose2, (200, 200))

        paddleLeft.reset()
        paddleRight.reset()
        ball.reset()

    display.update()
    clock.tick(FPS)
