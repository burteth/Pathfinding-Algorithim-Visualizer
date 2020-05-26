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
        self.visited = set()
        self.state = "inactive"
        self.stateColors = [getstateColor(HIGHLIGHT,n) for n in range(STATE_UPPER)]

        self.drawingPath = False
        self.pathlist = []

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
                newNode.stateColors = self.stateColors
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

    def setRandomPattern(self):

        count = int( (ROOT_NUM_BOXES ** 2) * (1/4))

        nodes = list(self.nodes)

        while (count > 0):

            randomNum = random.randint(0,len(nodes) - 1)
            if (nodes[randomNum].active):
                nodes[randomNum].clicked()
                count -=1



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
            node.path = []
            node.state = -1
            self.state = "inactive"
            self.drawingPath = False

    def update(self, screen):


        screen.fill((255, 255, 255))

        for curNode in self.nodes:
            screen.blit(curNode.surf, curNode.rect)

        #Create Grid
        for i in range(ROOT_NUM_BOXES):
            pygame.draw.line(screen, (0,0,0), (i*boxWidth, 0), (i*boxWidth, SCREEN_HEIGHT), 1)
            pygame.draw.line(screen, (0,0,0), (0, i*boxHeight), (SCREEN_WIDTH, i*boxHeight), 1)

        pygame.display.flip()

    def updateStates(self):

        visited = False
        for curNode in self.nodes:
            if (curNode.active == True) and (curNode.state > 0):
                visited = True
                curNode.updateState()

        if (not visited) and (self.state == "finish sequence"):
            self.state = "inactive"

    def makeStart(self, sprite):
        if (self.start != None) and (self.start != self.end):
            self.start.surf.fill(WHITE)
            self.start.active = True
            self.start.state = -1
        self.start = sprite
        self.start.surf.fill(START_COLOR)
        self.start.state = -2
        #self.start.active = False

    def makeEnd(self, sprite):
        if self.end != None:
            self.end.surf.fill(WHITE)
            self.end.active = True
            self.start.state = -1
        self.end = sprite
        self.end.surf.fill(END_COLOR)
        self.start.state = -2
        #self.end.active = False


    def bfs(self, queue):

        #Check if the bounds are valid
        if (self.start == None) or (self.end == None) or (self.end == self.start):
            return([])

        #if it is the first iteration
        if len(queue) == 0:
            queue = [self.start]
            self.visited.add(self.start.id)

        i, j = 0, len(queue) - 1

        while( i <= j ):

            item = queue.pop()
            j -= 1

            #Initiate Ending Sequence
            if item == self.end:
                self.drawingPath = True
                self.nextPath = self.end.last

                curNode = self.end
                while (curNode != self.start):
                    curNode = curNode.last
                    curNode.state = -2

                self.reset()
                return([])

            for adjacent in item.adj:
                if (adjacent != 0) and (adjacent.id not in self.visited):

                    if adjacent.active :

                        #update the path list for the adjacent nodes
                        #adjacent.path = item.path + [item]

                        adjacent.last = item
                        if adjacent.state == -1:
                            adjacent.state = STATE_UPPER
                        queue.insert(0, adjacent)
                        i += 1
                        j += 1
                    self.visited.add(adjacent.id)
            i += 1
        return(queue)

    def dfs(self, stack):

            #Check if the bounds are valid
            if (self.start == None) or (self.end == None) or (self.end == self.start):
                self.reset()
                return([])

            #if it is the first iteration
            if len(stack) == 0:
                stack = [self.start]
                self.visited.add(self.start.id)

            item = stack[-1]

            #Initiate Ending Sequence
            if item == self.end:
                self.drawingPath = True
                self.nextPath = self.end.last

                curNode = self.end
                while (curNode != self.start):
                    curNode = curNode.last
                    curNode.state = -2

                self.reset()
                return([])

            visitAny = False
            for adjacent in item.adj:
                if (adjacent != 0) and (adjacent.id not in self.visited):
                    if adjacent.active:

                        visitAny = True

                        adjacent.last = item
                        if adjacent.state == -1:
                            adjacent.state = STATE_UPPER

                        stack.append(adjacent)
                        self.visited.add(adjacent.id)
                        break
                    self.visited.add(adjacent.id)


            if not visitAny:
                stack.pop()

            return(stack)


    def bidirectionBfs(self, queue1, queue2):

        #Check if the bounds are valid
        if (self.start == None) or (self.end == None) or (self.end == self.start):
            return([],[])

        #if it is the first iteration
        if len(queue1) == 0:
            queue1 = [self.start]
            queue2 = [self.end]

            self.visited1 = set()
            self.visited2 = set()

            self.visited1.add(self.start.id)
            self.visited2.add(self.end.id)

            self.last1 = None
            self.last2 = None


        #Next Layer for queue1
        i, j = 0, len(queue1) - 1

        while( i <= j ):

            item = queue1.pop()
            j -= 1


            for adjacent in item.adj:
                if (adjacent != 0) and (adjacent.id not in self.visited1):

                    if adjacent.active:
                        if adjacent.id in self.visited2:

                            self.pathlist = adjacent.path + [adjacent, item] + item.path[::-1]

                            self.drawingPath = True

                            for node in self.pathlist:
                                node.state = -2

                            self.reset()
                            return([],[])


                        adjacent.path = item.path + [item]
                        if adjacent.state == -1:
                            adjacent.state = STATE_UPPER
                        queue1.insert(0, adjacent)
                        i += 1
                        j += 1
                    self.visited1.add(adjacent.id)
            i += 1



        #Next Layer for queue2
        i, j = 0, len(queue2) - 1

        while( i <= j ):

            item = queue2.pop()
            j -= 1

            for adjacent in item.adj:
                if (adjacent != 0) and (adjacent.id not in self.visited2):

                    if adjacent.active:
                        if adjacent.id in self.visited1:

                            self.pathlist =  adjacent.path + [adjacent, item] + item.path[::-1]

                            for node in self.pathlist:
                                node.state = -2

                            self.reset()
                            return([],[])


                        adjacent.path = item.path + [item]
                        if adjacent.state == -1:
                            adjacent.state = STATE_UPPER
                        queue2.insert(0, adjacent)
                        i += 1
                        j += 1
                    self.visited2.add(adjacent.id)
            i += 1

        return(queue1, queue2)



    def reset(self):
        self.visited = set()
        self.state = "finish sequence"

    def drawPath(self, option = None):

        if option == "bidirectionBfs":
            if len(self.pathlist) == 0:
                self.drawingPath = False
            else:
                nextNode = self.pathlist.pop()
                nextNode.surf.fill(PATH_HIGHLIGHT)
            return()

        if self.nextPath == self.start:
            self.drawingPath = False
            return()
        self.nextPath.surf.fill(PATH_HIGHLIGHT)
        self.nextPath = self.nextPath.last



class Node(pygame.sprite.Sprite):

    def __init__(self, pos):
        super(Node, self).__init__()

        #Pygame Sprite Things
        self.surf = pygame.Surface((boxWidth, boxHeight))
        self.surf.fill(WHITE)
        self.rect = self.surf.get_rect(center=pos)

        #Position of the Node
        self.pos = pos

        #is the node a wall
        self.active = True

        #list of adjacent nodes
        self.adj = [None, None, None,
                    None,    0, None,
                    None, None, None]

        #Unique Id for the Node
        self.id = uuid.uuid1()

        #Current State of the node
        #   STATE_UPPER: just visited
        #   STATE_UPPER-1: recently visited
        #   0: visited & no longer phasing out
        #   -1: never visited
        #   -2: part of the path
        self.state = -1

        #List of nodes that were visited along
        #the path to get to this node
        self.path = []
        self.last = 0

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

        if (self.pos[0] + boxWidth > SCREEN_WIDTH):
            #if on right wall
            constraints.add(2)
            constraints.add(5)
            constraints.add(8)
        if (self.pos[0] - boxWidth < 0):
            #if on left wall
            constraints.add(0)
            constraints.add(3)
            constraints.add(6)
        if (self.pos[1] + boxHeight > SCREEN_HEIGHT):
            #if on bottom wall
            constraints.add(6)
            constraints.add(7)
            constraints.add(8)
        elif (self.pos[1] - boxHeight <= 0):
            #if on top wall
            constraints.add(0)
            constraints.add(1)
            constraints.add(2)

        if ONLY_ADJCENT:
            constraints.add(0)
            constraints.add(2)
            constraints.add(6)
            constraints.add(8)

        return(constraints)

    def updateState(self):
        self.state -= 1
        self.surf.fill(self.stateColors[self.state])
