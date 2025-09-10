import pygame
from collisions import *
import os
import math
import time

GREEN = (0, 255, 0)
PI = 3.141592653


class Tank:
    def __init__(self, x, y, deg, img):
        self.x = x
        self.y = y
        self.deg = deg

        self.spin_speed = 3
        self.move_speed = 3

        self.width = 29
        self.height = 45

        self.MAXBULLETS = 3
        self.bullets = []

        self.isSpinCounterClockwise = False
        self.isSpinClockwise = False
        self.isMoveForward = False
        self.isMoveBackward = False
        self.fire_key = False
        self.is_alive = True

        #              top-left/bottom-left/bottom-right/top-right
        self.corners = [
            [self.x - self.height / 2 + 10, self.y - self.width / 2],
            [self.x - self.height / 2 + 10, self.y + self.width / 2],
            [self.x + self.height / 2 - 10, self.y + self.width / 2],
            [self.x + self.height / 2 - 10, self.y - self.width / 2],
        ]

        self.corners_offset = self.corners[::]

        self.tank_img = pygame.image.load(os.path.join("Assets", img))
        self.tank_img_copy = pygame.transform.rotate(self.tank_img, 360 - self.deg)
        self.UpdateImage()

    def Draw(self, WIN):
        for i in range(len(self.bullets)):
            self.bullets[i].Draw(WIN)

        if not self.is_alive:
            return

        WIN.blit(self.tank_img_copy, self.rect)
        """for i in range(len(self.corners)):
            rect = pygame.Rect(self.corners_offset[i][0], self.corners_offset[i][1], 2, 2)
            pygame.draw.rect(WIN, (255, 0, 0), rect)"""

    def SpinClockwise(self, maze):
        if not self.is_alive or not self.isSpinClockwise:
            return
        self.deg += self.spin_speed
        self.deg = self.deg % 360
        self.UpdateImage()
        self.RotateCorners()

        if maze.CheckCollision(self.corners_offset):
            self.deg -= self.spin_speed
            self.deg = self.deg % 360
            self.UpdateImage()
            self.RotateCorners()

    def SpinCounterClockwise(self, maze):
        if not self.is_alive or not self.isSpinCounterClockwise:
            return
        self.deg -= self.spin_speed
        self.deg = self.deg % 360
        self.UpdateImage()
        self.RotateCorners()

        if maze.CheckCollision(self.corners_offset):
            self.deg += self.spin_speed
            self.deg = self.deg % 360
            self.UpdateImage()
            self.RotateCorners()

    def MoveForward(self, maze):
        if not self.is_alive or not self.isMoveForward:
            return
        x_pos = self.move_speed * math.cos(self.deg * PI / 180)
        y_pos = self.move_speed * math.sin(self.deg * PI / 180)

        self.x += x_pos
        self.y += y_pos
        self.UpdateImage()
        self.TranslateCorners(x_pos, y_pos)
        self.RotateCorners()

        if maze.CheckCollision(self.corners_offset):
            self.x -= x_pos
            self.y -= y_pos
            self.UpdateImage()
            self.TranslateCorners(-x_pos, -y_pos)
            self.RotateCorners()

    def MoveBackward(self, maze):
        if not self.is_alive or not self.isMoveBackward:
            return
        x_pos = self.move_speed * math.cos(self.deg * PI / 180)
        y_pos = self.move_speed * math.sin(self.deg * PI / 180)

        self.x -= x_pos
        self.y -= y_pos
        self.UpdateImage()
        self.TranslateCorners(-x_pos, -y_pos)
        self.RotateCorners()

        if maze.CheckCollision(self.corners_offset):
            self.x += x_pos
            self.y += y_pos
            self.UpdateImage()
            self.TranslateCorners(x_pos, y_pos)
            self.RotateCorners()

    def TranslateCorners(self, x, y):
        for i in range(len(self.corners)):
            self.corners[i] = [self.corners[i][0] + x, self.corners[i][1] + y]

    def RotateCorners(self):
        for i in range(len(self.corners)):
            ox = self.corners[i][0] - self.x
            oy = self.corners[i][1] - self.y
            nx, ny = RotatePoints(ox, oy, self.deg)
            # print(ox, oy, nx, ny)
            nx += self.x
            ny += self.y
            self.corners_offset[i] = [nx, ny]

    def ShootBullet(self):
        if not self.is_alive:
            return
        if len(self.bullets) < self.MAXBULLETS:
            bullet = Bullet(self.x, self.y, self.deg, self.height)
            self.bullets.append(bullet)

    def UpdateBullets(self, maze, tanks):
        for i in range(len(self.bullets)):
            self.bullets[i].Update(maze)
            self.bullets[i].CheckCollisionTank(tanks)
        self.RemoveOldBullets()

    def RemoveOldBullets(self):
        for i in range(len(self.bullets) - 1, -1, -1):
            if self.bullets[i].IsOld():
                del self.bullets[i]

    def UpdateImage(self):
        self.tank_img_copy = pygame.transform.rotate(self.tank_img, 360 - self.deg)
        self.rect = self.tank_img_copy.get_rect()
        self.rect.center = (self.x, self.y)

    def UpdateMovement(self, gMaze):
        self.SpinCounterClockwise(gMaze)
        self.SpinClockwise(gMaze)
        self.MoveForward(gMaze)
        self.MoveBackward(gMaze)


class Bullet:
    def __init__(self, x, y, deg, tank_height):
        scaler = 0.5
        self.x = x + scaler * tank_height * math.cos(deg * PI / 180)
        self.y = y + scaler * tank_height * math.sin(deg * PI / 180)

        self.deg = deg
        self.move_speed = 4
        self.dx = self.move_speed * math.cos(self.deg * PI / 180)
        self.dy = self.move_speed * math.sin(self.deg * PI / 180)

        self.radius = 3
        self.MAXLIFETIME = 10

        self.time_start = time.time()

    def Draw(self, WIN):
        pygame.draw.circle(WIN, (0, 0, 0), (self.x, self.y), self.radius)

    def SetCorners(self, x, y):
        return [
            [x - self.radius, y - self.radius],
            [x - self.radius, y + self.radius],
            [x + self.radius, y + self.radius],
            [x + self.radius, y - self.radius],
        ]

    def Update(self, maze):

        x_only = False
        y_only = False
        both = False

        corners = self.SetCorners(self.x + self.dx, self.y)

        if maze.CheckCollision(corners):
            x_only = True

        corners = self.SetCorners(self.x, self.y + self.dy)

        if maze.CheckCollision(corners):
            y_only = True

        corners = self.SetCorners(self.x + self.dx, self.y + self.dy)

        if maze.CheckCollision(corners):
            both = True

        if x_only and not y_only:
            self.dx *= -1
        elif y_only and not x_only:
            self.dy *= -1
        elif both:
            self.dx *= -1
            self.dy *= -1
        else:
            self.x += self.dx
            self.y += self.dy

    def CheckCollisionTank(self, tanks):
        bullet_corners = self.SetCorners(self.x, self.y)
        for i in range(len(tanks) - 1, -1, -1):
            if not tanks[i].is_alive:
                continue
            if do_polygons_intersect(bullet_corners, tanks[i].corners_offset):
                # print("Hit Tank")
                tanks[i].is_alive = False
                self.time_start -= self.MAXLIFETIME

    def IsOld(self):
        return time.time() - self.time_start >= self.MAXLIFETIME


# will rotate (x, y) about the origin
def RotatePoints(x, y, deg):
    nx = x * math.cos(deg * PI / 180.0) - y * math.sin(deg * PI / 180.0)
    ny = x * math.sin(deg * PI / 180.0) + y * math.cos(deg * PI / 180.0)
    return nx, ny
