# Codes for ping pong game

from pygame import *

class GameSprite(sprite.Sprite):
    #class constructor
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        #Call for the class (Sprite) constructor:
        super().__init__() #sprite.Sprite.__init__(self)
 
        #every sprite must store the image property
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
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.y -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.y += self.speed
    def update_left(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.x > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.x < win_width - 80:
            self.rect.y += self.speed

#interface
BLUE = (200, 255, 255)
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))

#create sprites (paddle and balls)
paddleA = "paddle_blue.png"
paddleB = "paddle_red.png"
ball_img = "tennis_ball.png"

paddleLeft = Paddle (paddleA, 30, 200, 4, 50, 150)
paddleRight = Paddle (paddleB, 620, 200, 4, 50, 150)
ball = GameSprite(ball_img, 300, 200, 4, 50, 50)


#game loop
game = True
finish = False
clock = time.Clock()
FPS = 60

while game:
    for e in event.get():
        if e.type ==QUIT:
            game = False

    if finish != True:
        window.fill (BLUE)
        paddleLeft.reset()
        paddleRight.reset()
        ball.reset()

    display.update()
    clock.tick(FPS)
