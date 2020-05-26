import pygame
import random
from components import *
from helperfunctions import *
from globals import *



pygame.init()


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

map = Map()


running = True
drag = False


"""queue = [self.start]
count = 0

visited = set()"""

# Main loop
while running:

    # for loop through the event queue
    for event in pygame.event.get():
        # Check for KEYDOWN event
        if event.type == KEYDOWN:

            if event.key == K_ESCAPE:
                running = False

            elif event.key == K_c:
                map.clearEverything()
                #map.removeWalls()

            elif event.key == K_h:
                map.bfs(screen)


        elif event.type == QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:

            if (event.button == 1):

                drag = True
                pastNodes = []

                clicked_sprites = getMouseNode(map.nodes)

                for sprite in clicked_sprites:
                    sprite.clicked()
                    pastNodes.append(sprite)

            elif (event.button == 3):
                for sprite in getMouseNode(map.nodes):
                    if map.start == sprite:
                        map.makeEnd(sprite)
                    else:
                        map.makeStart(sprite)



        elif event.type == pygame.MOUSEBUTTONUP:
            drag = False

        elif event.type == pygame.MOUSEMOTION:

             if drag:
                 pos = pygame.mouse.get_pos()

                 clicked_sprites = [sprite for sprite in getMouseNode(map.nodes) if sprite not in pastNodes]

                 for sprite in clicked_sprites:
                     sprite.clicked()
                     pastNodes.append(sprite)




    map.update(screen)
