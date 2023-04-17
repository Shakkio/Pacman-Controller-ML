import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from entity import Entity
from sprites import PacmanSprites
from pathfinder import *
import random
import numpy as np

class State:
    def __init__(self, node):

        self.node = node
        

    def ComputePelletsDictionary(self, pellets):

        #pelletPosition ->  notEaten
        tempDictionary = {}

        for pellet in pellets:
            tempDictionary[pellet.position] = False
        
        return tempDictionary


class Pacman(Entity):
    def __init__(self, node, nodes):
        Entity.__init__(self, node)
        self.name = PACMAN    
        self.color = YELLOW
        self.direction = LEFT
        self.setBetweenNodes(LEFT)
        self.alive = True
        self.sprites = PacmanSprites(self)
        self.nodes = nodes
        self.path = []
        self.ghosts = []
        self.qValues = np.zeros((NROWS, NCOLS, 4))
        self.qLearning()


    def reset(self):
        Entity.reset(self)
        self.direction = LEFT
        self.setBetweenNodes(LEFT)
        self.alive = True
        self.image = self.sprites.getStartImage()
        self.sprites.reset()

    def die(self):
        for node in self.nodes.nodesLUT.values():
            node.fScore = 0
            
        self.alive = False
        self.direction = STOP

    def update(self, dt):	
        self.sprites.update(dt)
        self.position += self.directions[self.direction]*self.speed*dt

        #targetGoal = self.pathfinder.defineGoalNode(self.node, self.nodes)
         
        if self.overshotTarget():

            self.node = self.target
            #nodeToGo = self.pathfinder.AStar(self.node, targetGoal, self.nodes)
            actions = self.GetValidActions(self.node)
            direction = self.getNextAction(actions)
            self.target = self.getNewTarget(direction)
            
            if self.target is not self.node:
                self.direction = direction

            if self.target is self.node:
                self.direction = STOP
            self.setPosition()

    def indexConverter(self, index):
        if index == UP:
            return 0
        elif index == DOWN:
            return 1
        elif index == LEFT:
            return 2
        elif index == RIGHT:
            return 3
        
    def getBestAction(self, actions):

        bestValue = -9999

        for index in actions:
            index = self.indexConverter(index)
            currentValue = self.qValues[self.node.tilePosition.y, self.node.tilePosition.x, index]

            if currentValue > bestValue:
                chosenIndex = index
            else:
                continue

        if chosenIndex == 0:
            return UP
        elif chosenIndex == 1:
            return DOWN
        elif chosenIndex == 2:
            return LEFT
        elif chosenIndex == 3:
            return RIGHT

    def getNextAction(self, actions):

        if(random.uniform(0, 1) > RHO):
            bestValue = -9999

            for index in actions:
                index = self.indexConverter(index)
                currentValue = self.qValues[self.node.tilePosition.y, self.node.tilePosition.x, index]

                if currentValue > bestValue:
                    chosenIndex = index
                    bestValue = currentValue
                else:
                    continue
            
            print(currentValue)

            if chosenIndex == 0:
                return UP
            elif chosenIndex == 1:
                return DOWN
            elif chosenIndex == 2:
                return LEFT
            elif chosenIndex == 3:
                return RIGHT
        else:
            return random.choice(self.validDirections())

    def qLearning(self):

        state = random.choice(list(self.nodes.nodesLUT.values()))

        for episode in range(ITERATIONNUMBER):
            print("Episode: ", episode)
            
            rand_nu = random.uniform(0,1)
            if rand_nu < NU: 
                state = random.choice(list(self.nodes.nodesLUT.values()))

            # Get the list of available actions. 
            actions = self.GetValidActions(state)

            #direction is the action of our case
            direction = self.getNextAction(actions)

            self.target = self.getNewTarget(direction)
            newState = self.target

            convertedDirection = 0

            if(direction == UP):
                convertedDirection = 0
            elif(direction == DOWN):
                convertedDirection = 1
            elif(direction == LEFT):
                convertedDirection = 2
            elif(direction == RIGHT):
                convertedDirection = 3

            #print(self.qValues[state.tilePosition.y, state.tilePosition.x, convertedDirection])

            Q = self.qValues[state.tilePosition.y, state.tilePosition.x, convertedDirection]
            reward = self.nodes.rewards[state.tilePosition.y][state.tilePosition.x] + (100 / 1 + self.distance(state, self.nodes.getNodeFromTiles(1, 26)))
            maxQ = np.max(self.qValues[state.tilePosition.y, state.tilePosition.x])
            Q = (1 - ALPHA) * Q + ALPHA * (reward + GAMMA * maxQ)
            self.qValues[state.tilePosition.y, state.tilePosition.x, convertedDirection] = Q

            state = newState

        self.reset()


    def getValidKey(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_RIGHT]:
            return

    def eatPellets(self, pelletList):
        for pellet in pelletList:
            if self.collideCheck(pellet):
                return pellet
        return None   
    
    def collideGhost(self, ghost):
        return False
        #return self.collideCheck(ghost)

    def collideCheck(self, other):
        d = self.position - other.position
        dSquared = d.magnitudeSquared()
        rSquared = (self.collideRadius + other.collideRadius)**2
        if dSquared <= rSquared:
            return True
        return False
    
    def AddGhost(self, ghost):
        self.ghosts.append(ghost)

    def distance(self, currentNode, endGoal):
        distance = abs(currentNode.position.x - endGoal.position.x) + abs(currentNode.position.y - endGoal.position.y) 

        return distance

    

