
import pygame
from globals import *



def getMouseNode(nodes):

    pos = pygame.mouse.get_pos()

    clicked_sprites = [s for s in nodes if s.rect.collidepoint(pos)]

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
