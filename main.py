import pygame
import random
import os

WIN_WIDTH = 500
WIN_HEIGHT = 700
score = 0
hit = 0
# loading the images
BIRDS_IMG = [pygame.transform.scale2x(pygame.image.load(os.path.join('images', "bird1.png"))),
             pygame.transform.scale2x(pygame.image.load(os.path.join('images', "bird2.png"))),
             pygame.transform.scale2x(pygame.image.load(os.path.join('images', "bird3.png")))]

PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join('images', "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join('images', "base.png")))
BG_IMG = pygame.transform.rotate(pygame.transform.scale2x(pygame.image.load(os.path.join('images', "bg.png"))), 180)

bg = 0
bg1 = WIN_WIDTH


class Bird:
    IMGS = BIRDS_IMG
    # the extend to which the bird can rotate
    MAX_ROTATION = 25
    # how fast will the bird move
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self, a):
        self.tick_count += a

        d = self.vel * self.tick_count + 1.5 * self.tick_count ** 2

        if d >= 16:
            d = 16
        if d <= 0:
            d -= 2

        self.y = self.y + d

        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt = self.ROT_VEL

    def draw(self, win):
        self.img_count += 1

        # which image need to be shown
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME * 2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME * 4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME * 4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME * 2

        rotate_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotate_image.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)

        # win.blit(rotate_image, new_rect.topleft)
        win.blit(rotate_image, (self.x, self.y))

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class Pipe:
    GAP = 100
    VEL = 5

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.gap = 100

        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False
        self.set_height()

    def set_height(self):
        # self.height = random.randint(0, 220)
        self.height = int(random.random() * 400)
        self.top = -PIPE_IMG.get_height() + self.height
        self.bottom = self.height + self.GAP

    def draw(self, win, bird, pipe):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))
        if self.x - self.VEL <= 0:
            self.x = random.randint(800, 1000)
            self.set_height()
        else:
            self.x -= self.VEL
        if 100 < pipe.x < 110:
            isCollision(bird, pipe, win)


def isCollision(bird, pipe, win):
    global score, hit
    if pipe.bottom - pipe.GAP < bird.height < pipe.bottom and bird.height < 700 - BASE_IMG.get_height():
        score += 10
        pass
    else:
        score -= 5
        hit += 1
        if hit > 5:
            font_game = pygame.font.Font('freesansbold.ttf', 64)
            text = font_game.render('Game Over', True, (255, 0, 0))
            win.blit(text, (40, 350))
            pygame.time.delay(4000)
            # resetting the position
            bird.x = 100
            bird.y = 200
            hit = 0


def draw_win(win, bird, pipe):
    global bg, bg1, score
    win.blit(BG_IMG, (0, -350))
    bg += -1
    bg1 += -1
    if bg < WIN_WIDTH * -1:
        bg = WIN_WIDTH
    if bg1 < WIN_WIDTH * -1:
        bg1 = WIN_WIDTH

    bird.draw(win)
    pipe.draw(win, bird, pipe)
    font = pygame.font.Font('freesansbold.ttf', 24)
    text = font.render('Score: ' + str(score), True, (0, 0, 0))
    win.blit(text, (350, 20))
    win.blit(BASE_IMG, (bg, WIN_HEIGHT - BASE_IMG.get_height() + 120))
    win.blit(BASE_IMG, (bg1, WIN_HEIGHT - BASE_IMG.get_height() + 120))
    pygame.display.update()


def main():
    pygame.init()
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    bird = Bird(100, 200)
    pipe = Pipe(400)
    run = True
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        key = pygame.key.get_pressed()
        if key[pygame.K_UP]:
            bird.move(1)
        elif key[pygame.K_DOWN]:
            bird.move(-1)
        elif key[pygame.K_SPACE]:
            bird.jump()

        draw_win(win, bird, pipe)

    pygame.quit()
    quit()


main()
