# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"

    startState=problem.getStartState()
    currentLocation = startState 

    #for GSA implementation
    exploredStates = []
    exploredStates.append(startState)
    
    #To transform the graph to stack for better access in DFS
    frontierStack = util.Stack()
    for frontier in problem.getSuccessors(startState):
        frontierRoute = frontier + (frontier[1],)
        frontierStack.push(frontierRoute)

    currentRoute = []

    #start DFS
    while not(frontierStack.isEmpty()):
        currentStage = frontierStack.pop()
        currentState = currentStage[0]
        currentRoute = currentStage[3]

        if problem.isGoalState(currentState):   
            break
        if currentState not in exploredStates:
            for frontier in problem.getSuccessors(currentState):
                if frontier[0] not in exploredStates:
                    nextRoute = currentRoute + "," + frontier[1]
                    frontierRoute = frontier + (nextRoute,)
                    frontierStack.push(frontierRoute)
        exploredStates.append(currentState)
    
    return currentRoute.split(",")

    util.raiseNotDefined()
    

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    "*** YOUR CODE HERE ***"

    startState=problem.getStartState()
    currentLocation = startState

    #for GSA implementation
    exploredStates = []
    exploredStates.append(startState)
    
    #To transform the graph to stack for better access in BFS
    frontierQueue = util.Queue()
    for frontier in problem.getSuccessors(startState):
        frontierRoute = frontier + (frontier[1],)
        frontierQueue.push(frontierRoute)

    currentRoute = []

    #start BFS
    while not(frontierQueue.isEmpty()):
        currentStage = frontierQueue.pop()
        currentState = currentStage[0]
        currentRoute = currentStage[3]      
        
        if problem.isGoalState(currentState):   
            break
        
        if currentState not in exploredStates:
            for frontier in problem.getSuccessors(currentState):
                if frontier[0] not in exploredStates:
                    nextRoute = currentRoute + "," + frontier[1]
                    frontierRoute = frontier + (nextRoute,)
                    frontierQueue.push(frontierRoute)
        
        exploredStates.append(currentState)
    return currentRoute.split(",")

    util.raiseNotDefined()

def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"

    startState=problem.getStartState()
    currentLocation = startState

    #for GSA implementation   
    exploredStates = []
    exploredStates.append(startState)
    
    #To transform the graph to stack for better access in UCS
    frontierPriorityQueue = util.PriorityQueue()
    for frontier in problem.getSuccessors(startState):
        frontierRouteAndSum = frontier + (frontier[1],) + (frontier[2],)
        frontierPriorityQueue.push(frontierRouteAndSum, frontier[2])

    currentRoute = []

    #start UCS
    while not(frontierPriorityQueue.isEmpty()):
        currentStage = frontierPriorityQueue.pop()
        currentState = currentStage[0]
        currentRoute = currentStage[3]
        currentCost = currentStage[4]
    
        if problem.isGoalState(currentState):   
            break

        if currentState not in exploredStates:
            for frontier in problem.getSuccessors(currentState):
                if frontier[0] not in exploredStates:
                    nextCost = currentCost + frontier[2]
                    nextRoute = currentRoute + "," + frontier[1]
                    frontierRouteAndSum = frontier + (nextRoute,) + (nextCost,)
                    frontierPriorityQueue.push(frontierRouteAndSum, nextCost)
        exploredStates.append(currentState)

    return currentRoute.split(",")
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"
    
    startState=problem.getStartState()
    currentLocation = startState

    #for GSA implementation
    exploredStates = []
    exploredStates.append(startState)
    
    #To transform the graph to stack for better access in A*
    frontierPriorityQueue = util.PriorityQueue()
    for frontier in problem.getSuccessors(startState):
        hCost = heuristic(frontier[0], problem)
        totalCost = frontier[2] + hCost
        frontierRouteAndSum = frontier + (frontier[1],) + (frontier[2],) + (hCost,)
        frontierPriorityQueue.push(frontierRouteAndSum, totalCost)

    currentRoute = []

    #start A*
    while not(frontierPriorityQueue.isEmpty()):
        currentStage = frontierPriorityQueue.pop()
        currentState = currentStage[0]
        currentRoute = currentStage[3]
        currentCost = currentStage[4]

        if problem.isGoalState(currentState):   
            break

        if currentState not in exploredStates:
            for frontier in problem.getSuccessors(currentState):
                if frontier[0] not in exploredStates:
                    hCost = heuristic(frontier[0], problem)
                    nextCost = currentCost + frontier[2] 
                    nextRoute = currentRoute + "," + frontier[1]
                    frontierRouteAndSum = frontier + (nextRoute,) + (nextCost,) + (hCost,)
                    frontierPriorityQueue.push(frontierRouteAndSum, nextCost + hCost)
        exploredStates.append(currentState)

    return currentRoute.split(",")
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
