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
thickness = 0

currentAlgo = None


map.update(screen)

screen.fill((255, 255, 255))

for i in range(ROOT_NUM_BOXES):
    pygame.draw.line(screen, (0,0,0), (i*boxWidth, 0), (i*boxWidth, SCREEN_HEIGHT), 1)
    pygame.draw.line(screen, (0,0,0), (0, i*boxHeight), (SCREEN_WIDTH, i*boxHeight), 1)

pygame.display.flip()

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

            elif event.key == K_1:
                currentAlgo = "bfs"
                map.state = "active"
                queue = []

            elif event.key == K_2:
                currentAlgo = "bidirectionBfs"
                map.state = "active"
                queue1 = []
                queue2 = []

            elif event.key == K_3:
                currentAlgo = "dfs"
                map.state = "active"
                stack = []

            elif event.key == K_4:
                currentAlgo = "A*"
                map.state = "active"
                map.aStarSetup()

                aFunc = lambda a : a.cost
                aTie = lambda a : a.h
                priorityQueue = MinHeap(func = aFunc, tie = aTie)

            elif event.key == K_5:
                currentAlgo = "dijkstras"
                map.state = "active"

                aFunc = lambda a : a.cost
                priorityQueue = MinHeap(func = aFunc)

            elif event.key == K_6:
                currentAlgo = "A*"
                map.state = "active"
                map.greedyBFSSetup()

                aFunc = lambda a : a.cost
                priorityQueue = MinHeap(func = aFunc)

            elif event.key == K_r:
                map.setRandomPattern()

            elif event.key == K_b:
                if thickness == 2:
                    thickness = 0
                else:
                    thickness += 1

        elif event.type == QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:

            if (event.button == 1):

                drag = True
                pastNodes = set()

                clicked_sprites = getMouseNode(map.nodes)

                for sprite in clicked_sprites:
                    sprite.clicked(thick = thickness, past = pastNodes)
                    pastNodes.add(sprite)

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
                     sprite.clicked(thick = thickness, past = pastNodes)
                     pastNodes.add(sprite)

    if ( currentAlgo == "bfs" ):

        if map.state == "active":
            queue = map.bfs(queue)
            map.updateStates()

        elif (map.state == "inactive") and (not map.drawingPath):
            currentAlgo = None

        if (map.state == "finish sequence") or (map.drawingPath):
            map.updateStates()
            map.drawPath()

    elif (currentAlgo == "bidirectionBfs"):
        if map.state == "active":
            queue1, queue2 = map.bidirectionBfs(queue1, queue2)
            map.updateStates()

        elif (map.state == "inactive") and (not map.drawingPath):
            currentAlgo = None

        if (map.state == "finish sequence") or (map.drawingPath):
            map.updateStates()
            map.drawPath()

    elif (currentAlgo == "dfs"):
        if map.state == "active":
            stack = map.dfs(stack)
            map.updateStates()

        elif (map.state == "inactive") and (not map.drawingPath):
            currentAlgo = None

        if (map.state == "finish sequence") or (map.drawingPath):
            map.updateStates()
            map.drawPath()

    elif (currentAlgo == "A*"):
        if map.state == "active":
            priorityQueue = map.aStar(priorityQueue)
            map.updateStates()

        elif (map.state == "inactive") and (not map.drawingPath):
            currentAlgo = None

        if (map.state == "finish sequence") or (map.drawingPath):
            map.updateStates()
            map.drawPath()

    elif (currentAlgo == "dijkstras"):

        if map.state == "active":
            priorityQueue = map.dijkstras(priorityQueue)
            map.updateStates()

        elif (map.state == "inactive") and (not map.drawingPath):
            currentAlgo = None

        if (map.state == "finish sequence") or (map.drawingPath):
            map.updateStates()
            map.drawPath()


    map.update(screen)
