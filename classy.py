import pygame
import time
from random import randint

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400

GREEN = [73,188,11]
YELLOW = [225, 225, 0]
RED = [255,0,0]

class Game:

    def __init__(self):
        self.score = 0
        self.game_time = 10
        self.start_time = time.time()
        self.game_over = False

        pygame.init()
        pygame.font.init()
        pygame.display.set_caption('whack-a-mole')
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background()

    def play(self):
        self.mole()
        self.start_time = time.time()

    def whack(self):
        cx, cy = pygame.mouse.get_pos()
        if abs(cx - self.x - 5) <= 5 and abs(cy - self.y - 5) <= 5:
            self.score += 1
            self.background()
            self.mole()

    def mole(self):
        self.x = randint(0, SCREEN_WIDTH - 10)
        self.y = randint(30, SCREEN_HEIGHT - 10)
        pygame.draw.rect(self.screen, YELLOW, (self.x, self.y, 10, 10))

    def background(self):
        self.screen.fill(GREEN)

    def time(self):
        self.game_time = self.game_time + int(self.start_time - time.time())
        if self.game_time == 0:
            self.__init__()
            print("game over")

    def show_score(self):
        font = pygame.font.Font(None, 18)
        text = font.render(str(self.score), False, [255,0,0])
        self.screen.blit(text, (10, 0))

def main():
    game = Game()
    while not game.game_over:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                game.game_over = True
            if e.type == pygame.KEYDOWN:
                game.play()
            if e.type == pygame.MOUSEBUTTONDOWN:
                game.whack()

        game.show_score()
        pygame.display.update()

main()
