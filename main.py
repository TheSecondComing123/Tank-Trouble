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


pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
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

    tank1 = Tank(200, 200, 0, 'green_tank.png')
    tank2 = Tank(500, 500, 0, 'red_tank.png')

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
    
    tankImages = ['green_tank.png', 'red_tank.png']

    # reset player position
    for i in range(len(gTanks)):
        randx = random.randrange(2,MAZE_WIDTH + 1) * 100
        randy = random.randrange(2,MAZE_HEIGHT + 1) * 100

        randdeg = random.randrange(360)

        gTanks[i] = Tank(randx, randy, randdeg, tankImages[i])
        



def main():
    global joysticks
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
                    gTanks[0].fire_key = True
                if event.key == pygame.K_LCTRL:
                    gTanks[1].fire_key = True
        
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_m:
                    gTanks[0].fire_key = False
                if event.key == pygame.K_LCTRL:
                    gTanks[1].fire_key = False
            
            if event.type == pygame.JOYBUTTONDOWN:
                for player in gPlayers:
                    if player.controller_id == event.instance_id:
                        if event.button == 0:
                            gTanks[player.id].ShootBullet()
                        
            if event.type == pygame.JOYBUTTONUP:
                pass
            if event.type == pygame.JOYAXISMOTION:
                for player in gPlayers:
                    if player.controller_id == event.instance_id:
                        
                        if event.axis == 0:
                            if event.value < 0:
                                gTanks[player.id].isSpinCounterClockwise = True
                            else:
                                gTanks[player.id].isSpinClockwise = True
                            if InDeadzone(event.value):
                                gTanks[player.id].isSpinCounterClockwise = False
                                gTanks[player.id].isSpinClockwise = False
                        
                        if event.axis == 5:
                            gTanks[player.id].isMoveForward = True
                            if event.value < 0:
                                gTanks[player.id].isMoveForward = False
                        if event.axis == 4:
                            gTanks[player.id].isMoveBackward = True
                            if event.value < 0:
                                gTanks[player.id].isMoveBackward = False

            if event.type == pygame.JOYHATMOTION: # the d-pad
                print(event)
            if event.type == pygame.JOYDEVICEADDED:
                joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
                print(len(joysticks))
            if event.type == pygame.JOYDEVICEREMOVED:
                joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
                print(len(joysticks))
            
        '''
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_LEFT]:
            gTanks[0].isSpinCounterClockwise = True
        if keys_pressed[pygame.K_RIGHT]:
            gTanks[0].isSpinClockwise = True
        if keys_pressed[pygame.K_UP]:
            gTanks[0].isMoveForward = True
        if keys_pressed[pygame.K_DOWN]:
            gTanks[0].isMoveBackward = True

        if keys_pressed[pygame.K_d]:
            gTanks[1].SpinCounterClockwise(gMaze)
        if keys_pressed[pygame.K_g]:
            gTanks[1].SpinClockwise(gMaze)
        if keys_pressed[pygame.K_r]:
            gTanks[1].MoveForward(gMaze)
        if keys_pressed[pygame.K_f]:
            gTanks[1].MoveBackward(gMaze)
        '''

        
        for i in range(len(gTanks)):
            gTanks[i].UpdateMovement(gMaze)
        update_bullets()
        draw_window()
        game_not_in_play = CheckWin()

        if game_not_in_play:
            ResetPosition()
    
    pygame.quit()

if __name__ == '__main__':
    main()