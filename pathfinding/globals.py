import pygame
import math

BLACK = (0,0,0)
WHITE = (255,255,255)
START_COLOR = (230,55,220)
END_COLOR = (60,255,20)
HIGHLIGHT = (91, 141, 189)
PATH_HIGHLIGHT = (252, 252, 3)


from pygame.locals import (
    K_1, #bfs
    K_2, #bidirectionBfs
    K_3, #dfs
    K_4, #A*
    K_5, #dijkstras
    K_6, #Greedy Best First Search
    K_b, #Change thickness of cursor for walls
    K_r, #Generate Random Walls
    K_j,
    K_h,
    K_c, #Clear Everything
    K_w,
    K_a,
    K_s,
    K_d,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

small = 25
med = 120
large = 160


ROOT_NUM_BOXES = 85
BORDER = 0

boxWidth = SCREEN_WIDTH / ROOT_NUM_BOXES
boxHeight = SCREEN_HEIGHT / ROOT_NUM_BOXES

boxHyp = int(math.sqrt(SCREEN_WIDTH**2 + SCREEN_HEIGHT**2))

STATE_UPPER = 10

ONLY_ADJCENT = True
