import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from entity import Entity
from sprites import PacmanSprites
from pathfinder import Algorithm

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
        self.pathfinder = Algorithm()
        self.path = []
        self.ghosts = []

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

        targetGoal = self.pathfinder.defineGoalNode(self.node, self.nodes)
         
        if self.overshotTarget():

            self.node = self.target
            nodeToGo = self.pathfinder.AStar(self.node, targetGoal, self.nodes)
            direction = self.pathfinder.getDirection(self.node, nodeToGo)
            self.target = self.getNewTarget(direction)
            
            if self.target is not self.node:
                self.direction = direction

            if self.target is self.node:
                self.direction = STOP
            self.setPosition()



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
        return self.collideCheck(ghost)

    def collideCheck(self, other):
        d = self.position - other.position
        dSquared = d.magnitudeSquared()
        rSquared = (self.collideRadius + other.collideRadius)**2
        if dSquared <= rSquared:
            return True
        return False
    
    def AddGhost(self, ghost):
        self.ghosts.append(ghost)
    

