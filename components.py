import pygame
from globals import *
from helperfunctions import *
import random
import time
import uuid

class Map(object):
    def __init__(self):

        self.start = None
        self.end = None
        self.nodes = pygame.sprite.Group()
        self.fillBoard()


    def fillBoard(self):
        #Create Nodes

        #Fill a n by x matrix of nodes in the correct positions
        nodeList = []
        for yStart in range(ROOT_NUM_BOXES):
            nodeList.append([])
            yPos = yStart*boxHeight + (boxHeight / 2)
            for xStart in range(ROOT_NUM_BOXES):

                xPos = xStart*boxWidth + (boxWidth / 2)
                newNode = Node((xPos, yPos))
                nodeList[-1].append(newNode)

        dir = [(-1,-1),( 0,-1),( 1,-1)
              ,(-1, 0),( 0, 0),( 1, 0)
              ,(-1, 1),( 0, 1),( 1, 1)]


        #for every node assign its adjacent nodes
        for row in range(ROOT_NUM_BOXES):
            for col in range(ROOT_NUM_BOXES):

                curNode = nodeList[row][col]
                for direction in range(len(dir)):
                    if (curNode.adj[direction] == None):
                        curNode.adj[direction] = nodeList[row + dir[direction][1]][col + dir[direction][0]]
                    #add the nodes to the group
                    self.nodes.add(nodeList[row][col])

    def removeWalls(self):
        for node in self.nodes:
            if not node.active:
                node.clicked()

    def clearEverything(self):
        self.start = None
        self.end = None

        for node in self.nodes:
            node.active = True
            node.surf.fill(WHITE)


    def update(self, screen):

        screen.fill((255, 255, 255))

        for curNode in self.nodes:
            screen.blit(curNode.surf, curNode.rect)

        #Create Grid
        for i in range(ROOT_NUM_BOXES):
            pygame.draw.line(screen, (0,0,0), (i*boxWidth, 0), (i*boxWidth, SCREEN_HEIGHT), 1)
            pygame.draw.line(screen, (0,0,0), (0, i*boxHeight), (SCREEN_WIDTH, i*boxHeight), 1)

        pygame.display.flip()


    def makeStart(self, sprite):
        if (self.start != None) and (self.start != self.end):
            self.start.surf.fill(WHITE)
            self.start.active = True
        self.start = sprite
        self.start.surf.fill(START_COLOR)
        #self.start.active = False

    def makeEnd(self, sprite):
        if self.end != None:
            self.end.surf.fill(WHITE)
            self.end.active = True
        self.end = sprite
        self.end.surf.fill(END_COLOR)
        #self.end.active = False


    def bfs(self, screen):
        if (self.start == None) or (self.end == None) or (self.end == self.start):
            return()

        queue = [self.start]
        count = 0

        visited = set()

        while (queue):

            item = queue[-1]


            if item == self.end:
                return()

            for adjacent in item.adj:
                if (adjacent != 0) and (adjacent.id not in visited):

                    if adjacent.active:
                        adjacent.surf.fill(getGradColor((52, 140, 235), count))
                        queue.insert(0, adjacent)
                    visited.add(adjacent.id)


            count += 1

            queue.pop()




class Node(pygame.sprite.Sprite):

    def __init__(self, pos):
        super(Node, self).__init__()

        self.surf = pygame.Surface((boxWidth, boxHeight))
        self.surf.fill(WHITE)
        self.rect = self.surf.get_rect(center=pos)

        self.x = pos[0]
        self.y = pos[1]
        self.pos = pos

        self.active = True
        self.adj = [None, None, None,
                    None,    0, None,
                    None, None, None]

        self.id = uuid.uuid1()
        self.visited = False


        for constraint in self.checkEdges():
            self.adj[constraint] = 0


    def clicked(self):

        if self.active:
            self.surf.fill(BLACK)
        else:
            self.surf.fill(WHITE)
        self.active = not self.active

    def checkEdges(self):

        constraints = set()

        if (self.x + boxWidth > SCREEN_WIDTH):
            #if on right wall
            constraints.add(2)
            constraints.add(5)
            constraints.add(8)
        if (self.x - boxWidth < 0):
            #if on left wall
            constraints.add(0)
            constraints.add(3)
            constraints.add(6)
        if (self.y + boxHeight > SCREEN_HEIGHT):
            #if on bottom wall
            constraints.add(6)
            constraints.add(7)
            constraints.add(8)
        elif (self.y - boxHeight <= 0):
            #if on top wall
            constraints.add(0)
            constraints.add(1)
            constraints.add(2)

        return(constraints)
