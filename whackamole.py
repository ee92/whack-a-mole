import pygame
import time
from random import randint

# screen size
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400

# colors
GREEN = [73, 188, 11]
YELLOW = [225, 225, 0]
WHITE = [255, 255, 255]

# target position, game points, play time,
x = None
y = None
score = 0
game_time = 20
start_time = 0
mallet_down = False

# game state: 0 - welcome, 1 - playing, 2 - game over
state = 0

# make game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
mole = pygame.image.load('mole.png')
mallet = pygame.image.load('mallet.png')
down_mallet = pygame.image.load('down-mallet.png')
background = pygame.image.load('grass.png')
pygame.mouse.set_visible(False)
pygame.display.set_caption('click a mole')
pygame.font.init()


# screens for different game states
def welcome_screen():
    screen.fill(GREEN)
    font = pygame.font.Font(None, 30)
    text = font.render("press ENTER to start", False, WHITE)
    screen.blit(text, [SCREEN_WIDTH / 2 - text.get_width() / 2, 185])
    screen.blit(mallet, [200, 50])
    screen.blit(mole, [120, 250])

def play_screen():
    screen.blit(background, [0,0])
    show_score()
    show_timer()
    show_mole()
    show_mallet()

def end_screen():
    screen.fill(GREEN)
    font = pygame.font.Font(None, 30)
    game_over = font.render("GAME OVER", False, WHITE)
    font = pygame.font.Font(None, 25)
    points = font.render("score: " + str(score), False, WHITE)
    font = pygame.font.Font(None, 22)
    restart = font.render("press ENTER to play again", False, WHITE)
    screen.blit(game_over, [SCREEN_WIDTH / 2 - game_over.get_width() / 2, 100])
    screen.blit(points, [SCREEN_WIDTH / 2 - points.get_width() / 2, 200])
    screen.blit(restart, [SCREEN_WIDTH / 2 - restart.get_width() / 2, 300])


# game play functions
def play():
    global state, score, start_time
    start_time = time.time()
    score = 0
    state = 1
    new_mole()
    whack()

def whack():
    global score
    mx, my = pygame.mouse.get_pos()

    width, height = mole.get_size()
    if abs(mx - x - width / 2) <= width / 2 and abs(my - y - height / 2) <= height / 2:
        score += 1
        new_mole()

def new_mole():
    global state, x, y
    x = randint(0, SCREEN_WIDTH - mole.get_width())
    y = randint(30, SCREEN_HEIGHT - mole.get_height())

def show_mole():
    screen.blit(mole, [x, y])

def check_mallet_state():
    global mallet_down
    if pygame.mouse.get_pressed()[0]:
        mallet_down = True
    else:
        mallet_down = False

def show_mallet():
    check_mallet_state()
    mallet_position = mallet.get_rect()
    mallet_position.center = pygame.mouse.get_pos()
    if mallet_down:
        screen.blit(down_mallet, mallet_position)
    else:
        screen.blit(mallet, mallet_position)

def show_score():
    font = pygame.font.Font(None, 28)
    text = font.render(str(score), False, WHITE)
    screen.blit(text, (10, 0))

def show_timer():
    elapsed = time.time() - start_time
    timer = game_time - elapsed
    if timer < 0:
        end()
    font = pygame.font.Font(None, 28)
    text = font.render(str(int(timer)), False, WHITE)
    screen.blit(text, (370, 0))

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
