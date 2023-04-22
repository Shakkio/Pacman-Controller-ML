from nodes import *
from vector import Vector2
import sys
import random 
from constants import *

class Algorithm(object):
    
    visitedNodes = []

    #node to direction

    def AStar(self, start, goalNode, nodes):

        if goalNode is None or start.position == goalNode.position:
            return start
        
        print("stars")
        
        open = list()
        closed = list()
        
        start.gScore = 0
        start.fScore = 0

        for node in nodes.nodesLUT.values():
            node.gScore = 0
            node.previousNode = None

        open.append(start)

        while len(open) > 0:

            current = self.Heuristic(open, goalNode)

            if current == goalNode:
                path = list()

                current_node = current
                while current_node is not None:
                    path.append(current_node)
                    current_node = current_node.previousNode

                path.reverse()
                if len(path) >= 2:
                    print("end")
                    self.visitedNodes.append(path[1])
                    print(path[1].fScore)
                    return path[1]
                print("end")
                self.visitedNodes.append(start)
                return start

            connections = current.getAllNodesWithAccess()

            for connection in connections:
                    if connection not in open and connection not in closed:
                        open.append(connection)
                        connection.previousNode = current
                        connection.gScore = current.gScore + 10 
                    else:
                        if connection.gScore > current.gScore + 10:
                            connection.gScore = current.gScore + 10
                            connection.previousNode = current
                            if connection in closed:
                                closed.remove(connection)
                                open.append(connection)

            open.remove(current)
            closed.append(current)

        print('Path X!')
        return None
    
    def Heuristic(self, open, endGoal):

        selectedNode = None
        
        for node in open:
                if selectedNode == None:
                    selectedNode = node
                elif node.fScore + node.gScore  < selectedNode.fScore + selectedNode.gScore:
                    selectedNode = node

        if selectedNode == None:
            for node in open:
                selectedNode = node
                if node.fScore + node.gScore  < selectedNode.fScore + selectedNode.gScore:
                    selectedNode = node
        
        return selectedNode
    
    def defineGoalNode(self, pacmanNode, nodes):
        selectedNode = pacmanNode
        selectedNode.fScore = sys.maxsize

        for node in nodes.nodesLUT.values():

                if node in self.visitedNodes:
                    continue

                if node.position in NODE_POSITIONS_IGNORE:
                    continue
            
                if node.fScore < selectedNode.fScore:
                    selectedNode = node

        if selectedNode.fScore == sys.maxsize:
            for node in nodes.nodesLUT.values():

                if node.position in NODE_POSITIONS_IGNORE:
                    continue
                
                if node.fScore < selectedNode.fScore:
                    selectedNode = node
            
        return selectedNode
       
    
    def getDirection(self, node, next_node):
        for direction, value in node.neighbors.items():
            if value is not None and next_node is not None and value.position == next_node.position:
                return direction
        return STOP



        
       

            
 

        




    