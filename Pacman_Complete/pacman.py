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
    def __init__(self, node, pelletDirection):

        self.node = node
        self.pelletDirection = pelletDirection

    
    def GetKey(self):

        key = str(self.node.position.x) + str(self.node.position.y) + str(self.pelletDirection)
        #print(f"key: {key}")
        return key 


class Pacman(Entity):
    def __init__(self, node, nodes, pellets):
        Entity.__init__(self, node)
        self.name = PACMAN    
        self.color = YELLOW
        self.direction = LEFT
        self.setBetweenNodes(LEFT)
        self.alive = True
        self.sprites = PacmanSprites(self)
        self.nodes = nodes
        self.pellets = pellets
        self.path = []
        self.ghosts = []
        self.qValues = {}
        self.qLearning()

    def UpdatePacmanFromState(self, state):
        self.node = state.node


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

        actions = self.validDirections()
        closestPellet = self.FindClosestPellet(self.node)
        closestPelletDirection = self.FindPelletDirection(self.node, closestPellet)
        state = State(self.node, closestPelletDirection)
        direction = self.GetBestAction(actions, state)

        if self.overshotTarget():
            self.node = self.target
            #to make bestAction work
            actions = self.validDirections()
            closestPellet = self.FindClosestPellet(self.node)
            closestPelletDirection = self.FindPelletDirection(self.node, closestPellet)
            state = State(self.node, closestPelletDirection)
            direction = self.GetBestAction(actions, state)

            if self.node.neighbors[PORTAL] is not None:
                self.node = self.node.neighbors[PORTAL]
            self.target = self.getNewTarget(direction)
            if self.target is not self.node:
                self.direction = direction
            else:
                self.target = self.getNewTarget(self.direction)

            if self.target is self.node:
                self.direction = STOP
            self.setPosition()
        else: 
            if self.oppositeDirection(direction):
                self.reverseDirection()

    def indexConverter(self, index):
        if index == UP:
            return 0
        elif index == DOWN:
            return 1
        elif index == LEFT:
            return 2
        elif index == RIGHT:
            return 3
        
    def GetBestAction(self, actions, state):

            bestValue = -9999
            for action in actions:
                key = state.GetKey() + str(action)
                if key not in self.qValues:
                    self.qValues[key] = 0
                currentValue = self.qValues[key]

                if currentValue > bestValue:
                    chosenAction = action
                    bestValue = currentValue
                else:
                    continue
            #print(f"BestValue: {bestValue}")
            #print(f"ChosenAction:: {chosenAction}")
            return chosenAction

    def GetOneOfTheAction(self, actions):
        
        direction = random.choice(actions)
        return direction
    
    def ComputeReward(self, state, action):

        if state.pelletDirection == action:
            reward = 1
        else:
            reward = -1

        return reward


    def TakeAction(self, state, action):
        
        #print(f"currentNode: {state.node}")
        self.target = self.getNewTarget(action)
        #print(f"targetNode: {self.target}")

        newState = State(self.target, random.choice(self.GetValidActions(self.target))) 
        
        reward = self.ComputeReward(state, action)
        return reward, newState

    def GetRandomState(self):

        node = random.choice(list(self.nodes.nodesLUT.values()))
        #print(node.position.x)
        pelletDirection = random.choice(self.GetValidActions(node))
        state = State(node, pelletDirection)
        return state
        
    def qLearning(self):

        state = self.GetRandomState()

        for episode in range(ITERATIONNUMBER):
            if episode % 1000:
                print("Episode: ", episode)
            
                rand_nu = random.uniform(0,1)
                if rand_nu < NU: 
                    state = self.GetRandomState()
                    self.UpdatePacmanFromState(state)

                # Get the list of available actions. 
                actions = self.validDirections()
                print(f"actions: {actions}")

                if random.uniform(0, 1) < RHO:
                    action = self.GetOneOfTheAction(actions)
                else:
                    action = self.GetBestAction(actions, state)

                reward, newState = self.TakeAction(state, action)
                

                # Get the current q from the store.
                key = state.GetKey() + str(action)
                if key not in self.qValues.keys():
                    self.qValues[key] = 0
                Q = self.qValues[key]


                self.UpdatePacmanFromState(newState)
                # Get the q of the best action from the new state.
                newActions = self.validDirections()
                newAction = self.GetBestAction(newActions, state)
                newKey = newState.GetKey() + str(newAction)
                if newKey not in self.qValues.keys():
                    self.qValues[newKey] = 0
                maxQ = self.qValues[newKey]

                # Perform the q learning.
                Q = (1 - ALPHA) * Q + ALPHA * (reward + GAMMA * maxQ)

                # Store the new Q-value.
                self.qValues[key] = Q

                # And update the state.
                state = newState
        
        # for keys,values in self.qValues.items():
        #     print(keys)
        #     print(values)
        self.reset()
        #print(self.position)

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
    
    def FindPelletDirection(self, node, pellet):

        yDistance = abs(pellet.truePosition.x - node.position.y)
        xDistance = abs(pellet.truePosition.y - node.position.x)
        print(f"xDistance: {xDistance}")
        print(f"yDistance: {yDistance}")


        if(xDistance < yDistance):
            if(node.position.x > pellet.truePosition.x):
                direction = LEFT
            else:
                direction = RIGHT   
        else:
            if(node.position.y > pellet.truePosition.y):
                direction = UP
            else:
                direction = DOWN

        #print(direction)
        return direction
    
    def FindClosestPellet(self, node):
        minDistance = sys.maxsize
        chosenPellet = None

        for pellet in self.pellets.pelletList:
            distance = self.distance(pellet, node)

            if distance < minDistance:
                minDistance = distance
                chosenPellet = pellet

        #print(f"key: {key}")
        #print(f"chosenPellet Position: {chosenPellet.position}")
        chosenPellet.color = RED
        for pellet in self.pellets.pelletList:
            if pellet == chosenPellet:
                continue

            pellet.color = WHITE

        return chosenPellet

    
    def AddGhost(self, ghost):
        self.ghosts.append(ghost)

    def distance(self, currentNode, endGoal):
        distance = abs(currentNode.position.x - endGoal.position.x) + abs(currentNode.position.y - endGoal.position.y) 

        return distance
    
        

    

