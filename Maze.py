import pygame
from collisions import *
import random

LIGHT_GRAY = (231, 231, 231)
WALL_COLOR = (77, 77, 77)



class Cell:
    def __init__(self, i, j, width, margin_left, margin_top):
        
        self.row = i
        self.col = j
        self.width = width
        
        self.walls_short = 6
        self.walls_long = self.width + self.walls_short


        self.left = True
        self.right = True
        self.top = True
        self.bottom = True

        self.left_rect = pygame.Rect(margin_left + self.width*self.col - self.walls_short//2, margin_top + self.width*self.row - self.walls_short//2, self.walls_short, self.walls_long)
        self.right_rect =  pygame.Rect(margin_left + self.width*(self.col + 1) - self.walls_short//2, margin_top + self.width*self.row - self.walls_short//2, self.walls_short, self.walls_long)
        self.top_rect = pygame.Rect(margin_left + self.width*self.col - self.walls_short//2, margin_top + self.width*self.row - self.walls_short//2,  self.walls_long, self.walls_short)
        self.bottom_rect = pygame.Rect(margin_left + self.width*self.col - self.walls_short//2, margin_top + self.width*(self.row + 1) - self.walls_short//2,  self.walls_long, self.walls_short)
        
        self.walls = [self.left_rect, self.right_rect, self.top_rect, self.bottom_rect]
        self.Update()

        self.visited = False



    def Draw(self, WIN):

        # left wall
        if self.left:
            pygame.draw.rect(WIN, WALL_COLOR, self.left_rect)

        # right wall
        if self.right:
            pygame.draw.rect(WIN, WALL_COLOR, self.right_rect)
        
        # top wall
        if self.top:
            pygame.draw.rect(WIN, WALL_COLOR, self.top_rect)

        # bototm wall
        if self.bottom:
            pygame.draw.rect(WIN, WALL_COLOR, self.bottom_rect)
    
    def Update(self):
        self.walls_true = [self.left, self.right, self.top, self.bottom]
    
    def CheckCollision(self, polygon):
        #check collision with every wall
        for i in range(len(self.walls)):
            if not self.walls_true[i]:
                continue
            wall_corners = [self.walls[i].topleft, self.walls[i].bottomleft, self.walls[i].bottomright, self.walls[i].topright]
            if do_polygons_intersect(wall_corners, polygon):
                #print("Collision, wall", self.row, self.col, i)
                return True
        return False

class Maze:
    def __init__(self, height, width, screen_height, screen_width):
        self.height = height
        self.width = width

        cell_width = 100
        margin_left = (screen_width - width * cell_width)//2
        margin_top = (screen_height - height * cell_width)//2

        self.cells = []
        for i in range(height):
            l = []
            for j in range(width):
                newCell = Cell(i, j, cell_width, margin_left, margin_top)
                l.append(newCell)
            self.cells.append(l)
        #print(len(self.cells))
        #print(len(self.cells[0]))

        self.maze_rect = pygame.Rect(margin_left, margin_top, width* cell_width, height * cell_width)

    def Draw(self, WIN):
        pygame.draw.rect(WIN, LIGHT_GRAY, self.maze_rect)
        for i in range(len(self.cells)):
            for j in range(len(self.cells[i])):
                self.cells[i][j].Draw(WIN)    


    def CarveMazeRecursive(self, row, col):
        #print(row, col)
        # mark as visited
        self.cells[row][col].visited = True
        
        # until all neighbors are visited

        while True:

            neighbors = []
            # gather all non-visited neighbors
            if row != 0 and not self.cells[row-1][col].visited:
                neighbors.append('top')
            
            if row != self.height-1 and not self.cells[row+1][col].visited:
                neighbors.append('bottom')
            
            if col != 0 and not self.cells[row][col-1].visited:
                neighbors.append('left')

            if col != self.width-1 and not self.cells[row][col+1].visited:
                neighbors.append('right')

            if len(neighbors) == 0:
                return
            # pick a neighbor
            pick_index = random.randrange(0, len(neighbors))
            pick = neighbors[pick_index]

            if pick == 'top':
                self.CarveMazeRecursive(row-1, col)
                self.cells[row][col].top = False
                self.cells[row-1][col].bottom = False
            
            if pick == 'bottom':
                self.CarveMazeRecursive(row+1, col)
                self.cells[row][col].bottom = False
                self.cells[row+1][col].top = False
            
            if pick == 'left':
                self.CarveMazeRecursive(row, col-1)
                self.cells[row][col].left = False
                self.cells[row][col-1].right = False
            
            if pick == 'right':
                self.CarveMazeRecursive(row, col+1)
                self.cells[row][col].right = False
                self.cells[row][col+1].left = False

            neighbors.pop(pick_index)



    def CarveMaze(self):
        startingRow = 0
        startingCol = 0

        self.CarveMazeRecursive(startingRow, startingCol)
        for i in range(len(self.cells)):
            for j in range(len(self.cells[i])):
                self.cells[i][j].Update()
    
    def RemoveExtraWalls(self, n):
        # gather candidate walls for removal
        
        for _ in range(n):
            walls = []
            row = random.randrange(self.height)
            col = random.randrange(self.width)

            if row != 0:
                walls.append('top')
            
            if row != self.height - 1:
                walls.append('bottom')
            
            if col != 0:
                walls.append('left')
            
            if col != self.width - 1:
                walls.append('right')
            
            pick_index = random.randrange(0, len(walls))
            pick = walls[pick_index]
            #print(row, col, pick)

            # I don't want there to be a corner of a tile without at least one wall, so we will do some checking before I remove
            if pick == 'top':
                #    left corner check
                if (self.cells[row][col].left or self.cells[row][col-1].top or self.cells[row-1][col-1].right) and  \
                    (self.cells[row][col].right or self.cells[row][col+1].top or self.cells[row-1][col+1].left): # right corner check
                    #print('removing top wall', row, col)
                    self.cells[row][col].top = False
                    self.cells[row-1][col].bottom = False
                
            if pick == 'bottom':
                #   left corner check
                if (self.cells[row][col].left or self.cells[row][col-1].bottom or self.cells[row+1][col-1].right) and \
                    (self.cells[row][col].right or self.cells[row][col+1].bottom or self.cells[row+1][col+1].left): # right corner check
                    #print('removing bottom wall', row, col)
                    self.cells[row][col].bottom = False
                    self.cells[row+1][col].top = False
            
            if pick == 'left':
                #   top corner check
                if (self.cells[row][col].top or self.cells[row][col-1].top or self.cells[row-1][col-1].right) and \
                    (self.cells[row][col].bottom or self.cells[row][col-1].bottom or self.cells[row+1][col-1].right): # bottom corner check
                    #print('removing left wall', row, col)
                    self.cells[row][col].left = False
                    self.cells[row][col-1].right = False
            
            if pick == 'right':
                #   top corner check
                if (self.cells[row][col].top or self.cells[row][col+1].top or self.cells[row-1][col+1].left) and \
                    (self.cells[row][col].bottom or self.cells[row][col+1].bottom or self.cells[row+1][col+1].left): # bottom corner check
                    #print('removing right wall', row, col)
                    self.cells[row][col].right = False
                    self.cells[row][col+1].left = False

        for i in range(len(self.cells)):
            for j in range(len(self.cells[i])):
                self.cells[i][j].Update()

    def CheckCollision(self, polygon):
        for i in range(len(self.cells)):
            for j in range(len(self.cells[i])):
                if self.cells[i][j].CheckCollision(polygon):
                    return True
        return False

        





