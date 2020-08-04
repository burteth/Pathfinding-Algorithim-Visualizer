
import pygame
from globals import *



def getMouseNode(nodes):

    pos = pygame.mouse.get_pos()

    clicked_sprites = [s for s in nodes if s.rect.collidepoint(pygame.mouse.get_pos())]

    return(clicked_sprites)

def getstateColor(color,n):
    upper = STATE_UPPER
    if (n > upper):
        factor = upper
    elif (n == 0):
        return(HIGHLIGHT)
    elif (n < 0):
        return(WHITE)
    else:
        factor = n
    newColor = []
    for num in color:
        newColor.append(int(num*(1 - factor/upper)))

    return(tuple(newColor))

def calcDist(goalX, goalY, curX, curY):

    difX = abs(goalX - curX)
    difY = abs(goalY - curY)

    pyth = min(difX, difY)
    straight = max(difX, difY) - pyth

    return((pyth * 1.414214) + straight)
