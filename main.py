from operator import gt
import pygame
import time

from Maze import *
from Tank import *
from Player import *

WIDTH, HEIGHT = 1100, 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF)

WHITE = (200, 200, 200)
LIGHT_BLACK = (0, 0, 0)
FPS = 60

DEADZONERANGE = 0.5

MAZE_HEIGHT = 8
MAZE_WIDTH = 8

gMaze = Maze(MAZE_HEIGHT, MAZE_WIDTH, HEIGHT, WIDTH)
gTanks = []
gPlayers = []


def draw_window():
    WIN.fill(WHITE)
    gMaze.Draw(WIN)
    for i in range(len(gTanks)):
        gTanks[i].Draw(WIN)
    pygame.display.flip()


def initialize_my_stuff():
    gMaze.CarveMaze()
    gMaze.RemoveExtraWalls(10)

    player1 = Player(0, 0)
    player2 = Player(1, 1)

    gPlayers.append(player1)
    gPlayers.append(player2)

    tank1 = Tank(200, 200, 0, "green_tank.png")
    tank2 = Tank(500, 500, 0, "red_tank.png")

    gTanks.append(tank1)
    gTanks.append(tank2)


def update_bullets():
    for i in range(len(gTanks)):
        gTanks[i].UpdateBullets(gMaze, gTanks)


def InDeadzone(num):
    return abs(num) < DEADZONERANGE


def CheckWin():
    for tank in gTanks:
        if not tank.is_alive:
            return True
    return False


def ResetPosition():
    global gMaze
    gMaze = Maze(MAZE_HEIGHT, MAZE_WIDTH, HEIGHT, WIDTH)
    gMaze.CarveMaze()
    gMaze.RemoveExtraWalls(10)
    for tank in gTanks:
        tank.is_alive = True

    tankImages = ["green_tank.png", "red_tank.png"]

    for i in range(len(gTanks)):
        randx = random.randrange(2, MAZE_WIDTH + 1) * 100
        randy = random.randrange(2, MAZE_HEIGHT + 1) * 100

        randdeg = random.randrange(360)

        gTanks[i] = Tank(randx, randy, randdeg, tankImages[i])


def main():
    initialize_my_stuff()

    clock = pygame.time.Clock()

    run = True
    while run:
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    gTanks[0].ShootBullet()
                if event.key == pygame.K_LCTRL:
                    gTanks[1].ShootBullet()

        keys_pressed = pygame.key.get_pressed()

        gTanks[0].isSpinCounterClockwise = keys_pressed[pygame.K_LEFT]
        gTanks[0].isSpinClockwise = keys_pressed[pygame.K_RIGHT]
        gTanks[0].isMoveForward = keys_pressed[pygame.K_UP]
        gTanks[0].isMoveBackward = keys_pressed[pygame.K_DOWN]

        gTanks[1].isSpinCounterClockwise = keys_pressed[pygame.K_a]
        gTanks[1].isSpinClockwise = keys_pressed[pygame.K_d]
        gTanks[1].isMoveForward = keys_pressed[pygame.K_w]
        gTanks[1].isMoveBackward = keys_pressed[pygame.K_s]

        for i in range(len(gTanks)):
            gTanks[i].UpdateMovement(gMaze)
        update_bullets()
        draw_window()
        game_not_in_play = CheckWin()

        if game_not_in_play:
            ResetPosition()

    pygame.quit()


if __name__ == "__main__":
    main()
