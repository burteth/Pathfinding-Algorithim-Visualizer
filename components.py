import pygame
from globals import *
from helperfunctions import *
import random
import time
import uuid
import sys
import math

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
                newNode.row = yStart
                newNode.col = xStart
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

                    #Update unconstrained adjacency list
                    if (curNode.realAdj[direction] == None):
                        curNode.realAdj[direction] = nodeList[row + dir[direction][1]][col + dir[direction][0]]

                    #Update constrained adjacency list
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
            node.touched = True
            node.state = -1
            self.state = "inactive"
            self.drawingPath = False

    def update(self, screen):

        #screen.fill((255, 255, 255))
        rectList = []
        for curNode in self.nodes:
            if curNode.touched:
                rectList.append(screen.blit(curNode.surf, curNode.rect))
                curNode.touched = False


        #Create Grid
        for i in range(ROOT_NUM_BOXES):
            pygame.draw.line(screen, (0,0,0), (i*boxWidth, 0), (i*boxWidth, SCREEN_HEIGHT), 1)
            pygame.draw.line(screen, (0,0,0), (0, i*boxHeight), (SCREEN_WIDTH, i*boxHeight), 1)

        pygame.display.update(rectList)

    def updateStates(self):

        visited = False
        for curNode in self.nodes:
            if (curNode.active == True) and (curNode.state > 0):
                visited = True
                curNode.updateState()
                curNode.touched = True


        if (not visited) and (self.state == "finish sequence"):
            self.state = "inactive"

    def makeStart(self, sprite):
        if (self.start != None) and (self.start != self.end):
            self.start.surf.fill(WHITE)
            self.start.active = True
            self.start.state = -1
            self.start.touched = True
        self.start = sprite
        self.start.surf.fill(START_COLOR)
        self.start.state = -2
        self.start.touched = True

    def makeEnd(self, sprite):
        if self.end != None:
            self.end.surf.fill(WHITE)
            self.end.active = True
            self.end.state = -1
            self.end.touched = True
        self.end = sprite
        self.end.surf.fill(END_COLOR)
        self.end.state = -2
        self.end.touched = True

    def reset(self):
        self.visited = set()
        self.state = "finish sequence"

    def drawPath(self):

        for node in self.pathlist:
            node.touched = True

        if self.pathlist[-1] == self.start:
            self.drawingPath = False
            return()
        else:
            self.pathlist.pop().surf.fill(PATH_HIGHLIGHT)

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


                for node in self.end.path:
                    node.state = -2
                self.pathlist = self.end.path

                self.reset()
                return([])

            for adjacent in item.adj:
                if (adjacent != 0) and (adjacent.id not in self.visited):

                    if adjacent.active :

                        #update the path list for the adjacent nodes

                        adjacent.path = item.path + [item]

                        if adjacent.state == -1:
                            adjacent.state = STATE_UPPER
                            adjacent.touched = True

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
            for node in self.end.path:
                node.state = -2

            self.pathlist = self.end.path

            self.reset()
            return([])

        visitAny = False
        for adjacent in item.adj:
            if (adjacent != 0) and (adjacent.id not in self.visited):
                if adjacent.active:

                    visitAny = True

                    adjacent.path = item.path + [item]

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



        #Next Layer for queue1
        i, j = 0, len(queue1) - 1

        while( i <= j ):

            item = queue1.pop()
            j -= 1


            for adjacent in item.adj:
                if (adjacent != 0) and (adjacent.id not in self.visited1):

                    if adjacent.active:
                        if adjacent.id in self.visited2:

                            self.pathlist = item.path + [item, adjacent] +  adjacent.path[::-1]

                            self.drawingPath = True

                            for node in self.pathlist:
                                node.state = -2
                                node.touched = True

                            self.reset()
                            return([],[])


                        adjacent.path = item.path + [item]
                        if adjacent.state == -1:
                            adjacent.state = STATE_UPPER
                            adjacent.touched = True
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

                            self.pathlist = adjacent.path + [adjacent, item] + item.path[::-1]

                            self.drawingPath = True

                            for node in self.pathlist:
                                node.state = -2
                                node.touched = True

                            self.reset()
                            return([],[])

                        adjacent.path = item.path + [item]
                        if adjacent.state == -1:
                            adjacent.state = STATE_UPPER
                            adjacent.touched = True
                        queue2.insert(0, adjacent)
                        i += 1
                        j += 1
                    self.visited2.add(adjacent.id)
            i += 1

        return(queue1, queue2)

    def aStarSetup(self):

        startX = self.start.col
        startY = self.start.row

        endX = self.end.col
        endY = self.end.row

        for node in self.nodes:
            node.g = calcDist(startX, startY, node.col, node.row)
            node.h = calcDist(endX, endY, node.col, node.row)
            node.cost = int((node.g + node.h) * 10)

    def aStar(self, priorityQueue):

        if (self.start == None) or (self.end == None) or (self.end == self.start):
            self.reset()
            return([])

        #if first iteration
        if priorityQueue.size == 0:
            priorityQueue.insert(self.start)
            self.visited.add(self.start.id)

        #print( [ node.cost for node in priorityQueue.Heap if node != -1 ] )

        item = priorityQueue.remove()

        #Initiate Ending Sequence
        if item == self.end:

            self.drawingPath = True
            for node in self.end.path:
                node.state = -2

            self.pathlist = self.end.path

            self.reset()
            return([])

        if item.state == -1:
            item.state = STATE_UPPER
            item.touched = True


        for adjacent in item.adj:
            if (adjacent != 0):
                if adjacent.active:
                    if (adjacent.id not in self.visited):
                        #update the path list for the adjacent nodes
                        adjacent.path = item.path + [item]

                        priorityQueue.insert(adjacent)
                        self.visited.add(adjacent.id)
                    else:
                        if ( len( adjacent.path ) > len( item.path ) + 1 ):
                            adjacent.path = item.path + [item]
                            #self.visited.remove(adjacent.id)
                            newQueue = [adjacent]
                            while ( newQueue ):
                                node = newQueue.pop()
                                for neighbor in node.adj:
                                    if (neighbor != 0) and (neighbor.active):
                                        if ( len( neighbor.path ) > len( node.path ) + 1 ):
                                            neighbor.path = node.path + [node]
                                            newQueue.insert(0, neighbor)
        priorityQueue.minHeap()
        return(priorityQueue)

    def dijkstras(self, priorityQueue):

        #Check if the bounds are valid
        if (self.start == None) or (self.end == None) or (self.end == self.start):
            return([])

        #if it is the first iteration
        if len(priorityQueue) == 0:
            priorityQueue.insert(self.start)
            self.start.cost = 0
            self.visited.add(self.start.id)

        upper = len(priorityQueue) - 1

        while ( 0 <= upper ):

            item = priorityQueue.remove()
            upper -= 1

            #Initiate Ending Sequence
            if item == self.end:
                self.drawingPath = True


                for node in self.end.path:
                    node.state = -2
                self.pathlist = self.end.path

                self.reset()
                return([])

            for adjacent in item.adj:
                if ( adjacent != 0 ):
                    if ( adjacent.active ):
                        if ( adjacent.id not in self.visited ):

                            #update the path list for the adjacent nodes
                            adjacent.path = item.path + [item]

                            adjacent.cost = item.cost + 1

                            if adjacent.state == -1:
                                adjacent.state = STATE_UPPER
                                adjacent.touched = True

                            priorityQueue.insert(adjacent)

                            self.visited.add(adjacent.id)
        return(priorityQueue)

    def greedyBFSSetup(self):

        endX = self.end.col
        endY = self.end.row

        for node in self.nodes:
            node.cost = int(calcDist(endX, endY, node.col, node.row) * 10)


class Node(pygame.sprite.Sprite):

    def __init__(self, pos):
        super(Node, self).__init__()

        #Pygame Sprite Things
        self.surf = pygame.Surface((boxWidth, boxHeight - BORDER))
        self.surf.fill(WHITE)
        self.rect = self.surf.get_rect(center=pos)

        #Position of the Node
        self.pos = pos

        self.row = None
        self.col = None

        #is the node a wall
        self.active = True

        #list of adjacent nodes avaliable
        #[None, None, None,
        # None,    0, None,
        # None, None, None]
        self.adj = self.generateAdjacency(ONLY_ADJCENT)

        #list of all real adjacent nodes
        self.realAdj = self.generateAdjacency(False)

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

        self.cost = sys.maxsize
        self.g = None
        self.h = None

        self.touched = False


        for constraint in self.checkEdges():
            self.adj[constraint] = 0


    def clicked(self, thick = None, past = None):

        if thick == 1:
            for node in [adj for adj in self.realAdj[5:] if (adj != 0) and (adj not in past)]:
                past.add(node)
                node.clicked()
        elif thick == 2:
            for node in [adj for adj in self.realAdj if (adj != 0) and (adj not in past)]:
                past.add(node)
                node.clicked()

        if self.active:
            self.surf.fill(BLACK)
        else:
            self.surf.fill(WHITE)
        self.active = not self.active
        self.touched = True

    def checkEdges(self, constraint = None):

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

        if constraint:
            constraints.add(0)
            constraints.add(2)
            constraints.add(6)
            constraints.add(8)

        return(constraints)

    def generateAdjacency(self,adjacent):

        start = [None, None, None,
                 None,    0, None,
                 None, None, None]

        for limit in self.checkEdges(constraint = adjacent):
            start[limit] = 0

        return(start)

    def updateState(self):
        self.state -= 1
        self.surf.fill(self.stateColors[self.state])

class MinHeap(object):

    def __init__(self, func = None, tie = None):

        #Initial MaxSize of heap
        self.maxsize = 15

        #Create the heap array
        self.Heap = [-1]*(self.maxsize + 1)

        #Set unused first value
        self.Heap[0] = - 1

        self.FRONT = 1
        self.size = 0


        #set tiebreaker and attribute functions
        if tie != None:
            self.tie = self.setAttFunc(tie)
        else:
            self.tie = None

        if func != None:
            self.attFunc = self.setAttFunc(func)
        else:
            self.attFunc = lambda a : a

    def setAttFunc(self, attributeFunc):
        def newFunc(node):
            if (node == -1) or (node == 0):
                return(-1)
            else:
                return(attributeFunc(node))
        return(newFunc)

    def parent(self,pos):
        return( pos // 2)

    def leftChild(self, pos):
        return( 2 * pos )

    def rightChild(self, pos):
        return( (2 * pos) + 1 )

    def isLeaf(self, pos):
        if (pos >= self.size // 2) and (pos <= self.size):
            return(True)
        else:
            return(False)

    def swap(self, fpos, spos):
        self.Heap[fpos], self.Heap[spos] = self.Heap[spos], self.Heap[fpos]

    def minHeapify(self, pos):

        if not self.isLeaf(pos):

            if (self.isGreaterThan( pos, self.leftChild(pos) )) or (self.isGreaterThan( pos, self.rightChild(pos) )):
            #if (self.attFunc(self.Heap[pos]) > self.attFunc(self.Heap[self.leftChild(pos)])) or (self.attFunc(self.Heap[pos]) > self.attFunc(self.Heap[self.rightChild(pos)])):

                #if (self.attFunc(self.Heap[self.leftChild(pos)]) < self.attFunc(self.Heap[self.rightChild(pos)])):
                if ( self.isGreaterThan( self.rightChild(pos) , self.leftChild(pos) ) ):
                    self.swap(pos, self.leftChild(pos))
                    self.minHeapify(self.leftChild(pos))
                else:
                    self.swap(pos, self.rightChild(pos))
                    self.minHeapify(self.rightChild(pos))

    def insert(self, element):
        if (self.size >= self.maxsize):
            self.resize()

        self.size += 1
        self.Heap[self.size] = element

        current = self.size

        while (self.isGreaterThan(self.parent(current), current)):

            self.swap(current, self.parent(current))
            current = self.parent(current)

    def resize(self):
        for i in range(self.maxsize + 1):
            self.Heap.append(-1)
            self.maxsize += 1

    def heap_disp(self):

        heap = [self.attFunc(obj) for obj in self.Heap][1:]

        heap_len = len(heap)
        num_heaps = math.ceil(math.log(heap_len,2))

        count = 0
        spaces = 2**(num_heaps - 1)

        for i in range(num_heaps):

            heap_items = 2**i
            temp_spaces = spaces - heap_items
            side_spaces = math.floor(temp_spaces / heap_items*2)



            for j in heap[count:count + heap_items]:
                print( " "*(side_spaces + (count % 2)), end=" " )
                print(j, end=" ")
                print( " "*(side_spaces), end=" " )
                count += 1
            print()

    def Print(self):
        for i in range(1, (self.size//2)+1):
            print(" PARENT : "+ str(self.attFunc(self.Heap[i]))+" LEFT CHILD : "+
                                str(self.attFunc(self.Heap[2 * i]))+" RIGHT CHILD : "+
                                str(self.attFunc(self.Heap[2 * i + 1])))

    def minHeap(self):

        for pos in range(self.size//2, 0, -1):
            self.minHeapify(pos)

    def remove(self):

        popped = self.Heap[self.FRONT]
        self.Heap[self.FRONT] = self.Heap[self.size]
        self.Heap[self.size] = -1
        self.size -= 1
        self.minHeapify(self.FRONT)

        return(popped)

    def isGreaterThan(self, first, second):
        """ Compares two positions within the heap based
            on the attribute function and the tiebreaker
            function
        """
        firstVal = self.attFunc(self.Heap[first])
        secondVal = self.attFunc(self.Heap[second])

        if firstVal == secondVal:
            if self.tie != None:
                firstTie = self.tie(self.Heap[first])
                secondTie = self.tie(self.Heap[second])
                if firstTie > secondTie:
                    return(True)
                return(False)
        else:
            if firstVal > secondVal:
                return(True)
            return(False)

    def __len__(self):
        return(self.size)
