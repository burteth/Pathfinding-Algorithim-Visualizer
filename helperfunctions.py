
import pygame
from globals import *



def getMouseNode(nodes):

    pos = pygame.mouse.get_pos()

    clicked_sprites = [s for s in nodes if s.rect.collidepoint(pos)]

    return(clicked_sprites)

def getGradColor(color,n):
    upper = ROOT_NUM_BOXES**2
    if (n > upper):
        factor = upper
    elif (n < 0):
        factor = 0
    else:
        factor = n
    newColor = []
    for num in color:
        newColor.append(int(num*(1 - factor/upper)))

    return(tuple(newColor))
