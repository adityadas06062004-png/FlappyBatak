import pygame
from sys import exit
import random
import os
import pygame.font

#game variables
GAME_WIDTH = 360
GAME_HEIGHT = 640

bird_x = GAME_WIDTH/8
bird_y = GAME_HEIGHT/2
bird_width = 36
bird_height = 33

class Bird(pygame.Rect):
    def __init__(self, img):
        pygame.Rect.__init__(self, bird_x, bird_y, bird_width, bird_height)
        self.img = img

pipe_x = GAME_WIDTH
pipe_y = 0
pipe_width = 64
pipe_height = 512

class Pipe(pygame.Rect):
    def __init__(self, img, x, y):
        pygame.Rect.__init__(self, x, y, pipe_width, pipe_height)
        self.img = img
        self.passed = False


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

background_image = pygame.image.load(os.path.join(BASE_DIR, "Background.jpg"))
background_image = pygame.transform.scale(background_image, (GAME_WIDTH, GAME_HEIGHT))
bird_image = pygame.image.load(os.path.join(BASE_DIR, "Batak.png.jpeg"))
bird_image = pygame.transform.scale(bird_image, (bird_width, bird_height))
top_pipe_image = pygame.image.load(os.path.join(BASE_DIR, "toppipe.png.jpg"))
top_pipe_image = pygame.transform.scale(top_pipe_image, (pipe_width, pipe_height))
bottom_pipe_image = pygame.image.load(os.path.join(BASE_DIR, "bottompipe.png.jpg"))
bottom_pipe_image = pygame.transform.scale(bottom_pipe_image, (pipe_width, pipe_height))

bird = Bird(bird_image)
pipes = []
velocity_x = -3
velocity_y = 0
gravity = 0.4
score = 0
game_over = False


def draw():
    screen.blit(background_image, (0, 0))
    screen.blit(bird.img, bird)

    for pipe in pipes:
        screen.blit(pipe.img, pipe)

    text_str = str(int(score))
    if game_over:
        text_str = "Game Over: " + text_str

    text_font = pygame.font.SysFont("Comic Sans MS", 45)
    text_render = text_font.render(text_str, True, "white")
    screen.blit(text_render, (5, 0))

def move():

    global velocity_y, score, game_over
    velocity_y += gravity
    bird.y += velocity_y
    bird.y = max(0, bird.y)

    if bird.y >= GAME_HEIGHT - bird.height:
        game_over = True

    for pipe in pipes:
        pipe.x += velocity_x

        if not pipe.passed and bird.x > pipe.x + pipe.width:
            score += 0.5
            pipe.passed = True


        if bird.colliderect(pipe):
            game_over = True
            return

    while len(pipes) > 0 and pipes[0].x + pipes[0].width < 0:
        pipes.pop(0)

def create_pipes():
    random_pipe_y = pipe_y - pipe_height//4 - random.randint(0, pipe_height//2)
    opening_space = GAME_HEIGHT/4

    top_pipe = Pipe(top_pipe_image, GAME_WIDTH, 0)
    top_pipe.y = random_pipe_y
    pipes.append(top_pipe)

    bottom_pipe = Pipe(bottom_pipe_image, GAME_WIDTH, opening_space + 150) 
    bottom_pipe.y = top_pipe.y + top_pipe.height + opening_space
    pipes.append(bottom_pipe)



pygame.init()
screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("Flappy Batak")
clock = pygame.time.Clock()

create_pipe_timer = pygame.USEREVENT + 0
pygame.time.set_timer(create_pipe_timer, 1500)

while True:  #game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == create_pipe_timer and not game_over:
            create_pipes()

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_x, pygame.K_UP):  
                velocity_y = -6


                
                if game_over:
                    bird.y = bird_y
                    pipes.clear()
                    score = 0
                    game_over = False

    if not game_over:
        move()
        draw()
        pygame.display.update()
        clock.tick(60) 
