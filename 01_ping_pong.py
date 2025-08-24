from pygame import *

# ---------------------- Config ----------------------
init()
win_width, win_height = 800, 500
window = display.set_mode((win_width, win_height))
display.set_caption("Ping Pong")

clock = time.Clock()
FPS = 60

# Colours
BACK  = (16, 120, 16)   # court green
LINES = (240, 240, 240) # court lines + UI
PADD  = (240, 240, 240) # paddles
BALLC = (240, 240, 240) # ball

# Geometry
PAD_W, PAD_H = 14, 120   # thinner paddles
BALL_R = 10              # round ball radius
PAD_GAP = 30             # gap from side wall
BASE_SPEED_PADDLE = 6
BALL_SPEED_X = 4
BALL_SPEED_Y = 3

WIN_SCORE = 6
winner = None

# ---------------------- Sprites ----------------------
class GameSprite(sprite.Sprite):
    def __init__(self, surf, x, y, speed=0):
        super().__init__()
        self.image = surf
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed

    def reset(self):
        window.blit(self.image, self.rect.topleft)

class Player(GameSprite):
    def clamp(self):
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > win_height:
            self.rect.bottom = win_height

    def update_l(self):
        keys = key.get_pressed()
        if keys[K_w]:
            self.rect.y -= self.speed
        if keys[K_s]:
            self.rect.y += self.speed
        self.clamp()

    def update_r(self):
        keys = key.get_pressed()
        if keys[K_UP]:
            self.rect.y -= self.speed
        if keys[K_DOWN]:
            self.rect.y += self.speed
        self.clamp()

class Ball(GameSprite):
    def __init__(self, radius):
        # make a round ball surface with per-pixel alpha
        surf = Surface((radius*2, radius*2), SRCALPHA)
        draw.circle(surf, BALLC, (radius, radius), radius)
        super().__init__(surf, win_width//2 - radius, win_height//2 - radius, 0)
        self.vx = BALL_SPEED_X
        self.vy = BALL_SPEED_Y
        self.radius = radius

    def center_serve(self, direction=1):
        self.rect.center = (win_width // 2, win_height // 2)
        self.vx = BALL_SPEED_X * direction
        self.vy = BALL_SPEED_Y

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        # bounce on top/bottom walls
        if self.rect.top <= 0 or self.rect.bottom >= win_height:
            self.vy *= -1

# ---------------------- Objects ----------------------
# paddles as thin rectangles
paddle_surf = Surface((PAD_W, PAD_H))
paddle_surf.fill(PADD)

racket1 = Player(paddle_surf.copy(), PAD_GAP, (win_height - PAD_H)//2, BASE_SPEED_PADDLE)
racket2 = Player(paddle_surf.copy(), win_width - PAD_GAP - PAD_W, (win_height - PAD_H)//2, BASE_SPEED_PADDLE)
ball = Ball(BALL_R)

# UI
font.init()
score_font = font.Font(None, 56)
hint_font  = font.Font(None, 28)

score1, score2 = 0, 0
paused = False

# ---------------------- Court Drawing ----------------------
def draw_court():
    window.fill(BACK)
    # outer border: baselines & sidelines
    draw.rect(window, LINES, Rect(8, 8, win_width - 16, win_height - 16), width=4)

    # dashed centre line
    dash_h = 18
    gap_h = 14
    x = win_width // 2
    y = 8
    while y < win_height - 8:
        draw.line(window, LINES, (x, y), (x, min(y + dash_h, win_height - 8)), width=4)
        y += dash_h + gap_h

def draw_ui():
    # centred scoreboard at top
    score_text = score_font.render(f"{score1}   :   {score2}", True, LINES)
    window.blit(score_text, (win_width//2 - score_text.get_width()//2, 16))

    if winner is not None:
        win_text = hint_font.render(f"Player {winner} wins! Press R to reset", True, LINES)
        window.blit(win_text, (win_width//2 - win_text.get_width()//2, 60))

# ---------------------- Helpers ----------------------
def handle_paddle_collisions():
    global ball
    # collide with left paddle only when ball moves left
    if sprite.collide_rect(racket1, ball) and ball.vx < 0:
        # separate to avoid sticking
        ball.rect.left = racket1.rect.right
        # reflect X
        ball.vx = abs(ball.vx)
        # add spin: based on contact offset
        offset = (ball.rect.centery - racket1.rect.centery) / (racket1.rect.height / 2)
        ball.vy = max(-7, min(7, ball.vy + 4 * offset))

    # collide with right paddle only when ball moves right
    if sprite.collide_rect(racket2, ball) and ball.vx > 0:
        ball.rect.right = racket2.rect.left
        ball.vx = -abs(ball.vx)
        offset = (ball.rect.centery - racket2.rect.centery) / (racket2.rect.height / 2)
        ball.vy = max(-7, min(7, ball.vy + 4 * offset))

def handle_scoring():
    global score1, score2, winner, paused
    if ball.rect.left <= 0:
        score2 += 1
        ball.center_serve(direction=-1)
    if ball.rect.right >= win_width:
        score1 += 1
        ball.center_serve(direction=1)

    # win condition
    if score1 >= WIN_SCORE or score2 >= WIN_SCORE:
        winner = 1 if score1 >= WIN_SCORE else 2
        paused = True  # stop play

# ---------------------- Main Loop ----------------------
game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                game = False
            if e.key == K_p:
                paused = not paused
            if e.key == K_r:
                score1 = score2 = 0
                winner = None
                racket1.rect.centery = win_height // 2
                racket2.rect.centery = win_height // 2
                ball.center_serve(direction=1)

    if paused:
        draw_court()
        draw_ui()
        pause_text = hint_font.render("Paused (P to resume)  •  R to reset", True, LINES)
        window.blit(pause_text, (win_width//2 - pause_text.get_width()//2, win_height//2 - 14))
        display.update()
        clock.tick(FPS)
        continue

    # updates
    racket1.update_l()
    racket2.update_r()
    ball.update()
    handle_paddle_collisions()
    handle_scoring()

    # draw
    draw_court()
    draw_ui()
    racket1.reset()
    racket2.reset()
    ball.reset()

    display.update()
    clock.tick(FPS)

quit()
