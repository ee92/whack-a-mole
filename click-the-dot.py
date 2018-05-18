import pygame
import time
from random import randint

# screen size
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400

# colors
GREEN = [73,188,11]
YELLOW = [225, 225, 0]
RED = [255,0,0]

# target position, game points, play time,
x = None
y = None
score = 0
game_time = 10
start_time = 0

# game state: 0 - welcome, 1 - playing, 2 - game over
state = 0

# make game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('click a dot')
pygame.font.init()


# screens for different game states
def welcome_screen():
    screen.fill(GREEN)
    font = pygame.font.Font(None, 30)
    text = font.render("press ENTER to start", False, RED)
    screen.blit(text, [SCREEN_WIDTH / 2 - text.get_width() / 2, 185])

def play_screen():
    screen.fill(GREEN)
    show_score()
    show_timer()
    show_dot()

def end_screen():
    screen.fill(GREEN)
    font = pygame.font.Font(None, 30)
    game_over = font.render("GAME OVER", False, RED)
    font = pygame.font.Font(None, 25)
    points = font.render("score: " + str(score), False, RED)
    font = pygame.font.Font(None, 22)
    restart = font.render("press ENTER to play again", False, RED)
    screen.blit(game_over, [SCREEN_WIDTH / 2 - game_over.get_width() / 2, 100])
    screen.blit(points, [SCREEN_WIDTH / 2 - points.get_width() / 2, 200])
    screen.blit(restart, [SCREEN_WIDTH / 2 - restart.get_width() / 2, 300])


# game play functions
def play():
    global state, score, start_time, time_left
    start_time = time.time()
    score = 0
    state = 1
    new_dot()
    whack()

def whack():
    global score
    cx, cy = pygame.mouse.get_pos()
    if abs(cx - x - 5) <= 5 and abs(cy - y - 5) <= 5:
        score += 1
        new_dot()

def new_dot():
    global state, x, y
    x = randint(0, SCREEN_WIDTH - 10)
    y = randint(30, SCREEN_HEIGHT - 10)

def show_dot():
    pygame.draw.rect(screen, YELLOW, (x, y, 10, 10))

def show_score():
    font = pygame.font.Font(None, 18)
    text = font.render(str(score), False, [255,0,0])
    screen.blit(text, (10, 0))

def show_timer():
    elapsed = time.time() - start_time
    timer = game_time - elapsed
    if timer < 0:
        end()
    font = pygame.font.Font(None, 18)
    text = font.render(str(int(timer)), False, [255,0,0])
    screen.blit(text, (385, 0))

def end():
    global state
    state = 2


# event handlers for different game states
def handle_welcome(e):
    welcome_screen()
    if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
        play()

def handle_play(e):
    if e.type == pygame.MOUSEBUTTONDOWN:
        whack()
    if e.type == pygame.KEYDOWN and e.key == pygame.K_q:
        end()

def handle_end(e):
    if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
        play()


# game event loop
def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #exit button
                running = False
            elif state == 0: # welcome screen
                handle_welcome(event)
            elif state == 1: # game play
                handle_play(event)
            elif state == 2: # game over
                handle_end(event)

        if state == 1:
            play_screen()
        if state == 2:
            end_screen()

        clock.tick(30)
        pygame.display.update()

main()
