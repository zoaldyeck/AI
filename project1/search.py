# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html
from mhlib import PATH



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
    [2nd Edition: p 75, 3rd Edition: p 87]

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm
    [2nd Edition: Fig. 3.18, 3rd Edition: Fig 3.7].

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    
    visited=[]             #already visitedkk
    stack=util.Stack()     #queue push and pop out
    start=problem.getStartState() #begin
    stack.push((start,[],0))  
    visited.append(start)
    result=[]
    
 
    while not stack.isEmpty():
        father=stack.pop()            #[(5,5),' ',0]
        if problem.isGoalState(father[0]):
            return father[1]
        for cord,action,cost in problem.getSuccessors(father[0]): #all child
            result=list(father[1])
            if not cord in visited:
                visited.append(cord)  #(5,4),(4,5) #'south'
                result.append(action)
                stack.push((cord,result,cost+1))

    util.raiseNotDefined()
    
    
         
        

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    [2nd Edition: p 73, 3rd Edition: p 82]
    """
    "*** YOUR CODE HERE ***"
    visited=[]             #already visited
    queue=util.Queue()     #queue push and pop out
    start=problem.getStartState() #begin
    queue.push((start,[],0))  
    visited.append(start)
    result=[]
    

    while not queue.isEmpty():
        father=queue.pop()            #[(5,5),' ',0]
        if problem.isGoalState(father[0]):
            return father[1]
        for cord,action,cost in problem.getSuccessors(father[0]): #all child
            result=list(father[1])
            if not cord in visited:
                visited.append(cord)  #(5,4),(4,5) #'south'
                result.append(action)
                queue.push((cord,result,cost+1))
    util.raiseNotDefined()

def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"
    """
    visited=[]             #already visited   

    priorityqueue=util.PriorityQueue()     #queue push and pop out
    start=problem.getStartState() #begin
    priorityqueue.push((start,[]),0)  
    visited.append(start)
    result=[]
    
  
    while not priorityqueue.isEmpty():
        father=priorityqueue.pop()            #[(5,5),' ',0]
        if problem.isGoalState(father[0]):
            print father[1]
            return father[1]
        for cord,action,cost in problem.getSuccessors(father[0]): #all child
            result=list(father[1])
            if not cord in visited:
                visited.append(cord)  #(5,4),(4,5) #'south'
                result.append(action)
                priorityqueue.push((cord,result),problem.getCostOfActions(result))
    util.raiseNotDefined()
    """
    PQueue=util.PriorityQueue()
    PQueue.push((problem.getStartState(),[]),0)
    explored=[]
    result=[]
    record=[]
    explored.append(problem.getStartState())
    while not PQueue.isEmpty():
        node=PQueue.pop()
        result=node[1]
        if problem.isGoalState(node[0]):
            return result
        explored.append(node[0])
        
        for i in problem.getSuccessors(node[0]):
            succesor=i[0]
            step=i[1]
            record=list(result)
            if not i[0] in explored:
                record.append(step)
                PQueue.push((succesor,record),problem.getCostOfActions(record))
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
    """
    visited=[]             #already visited 
    
    priorityqueue=util.PriorityQueue()     #queue push and pop out
    start=problem.getStartState() #begin 
    g=0
    h=heuristic(start,problem)
    priorityqueue.push((start,[]),g+h)  
    visited.append(start)
    result=[]
    
 
    while not priorityqueue.isEmpty():
        father=priorityqueue.pop()            #[(5,5),' ',0]
        if problem.isGoalState(father[0]):
            return father[1]
        for cord,action,cost in problem.getSuccessors(father[0]): #all child
            result=list(father[1])
            if not cord in visited:
                visited.append(cord)  #(5,4),(4,5) #'south'
                result.append(action)
                g=problem.getCostOfActions(result)
                h=heuristic(cord,problem)
                priorityqueue.push((cord,result,g),g+h)        
    util.raiseNotDefined()
    """
    PQueue=util.PriorityQueue()
    PQueue.push((problem.getStartState(),[]),heuristic(problem.getStartState(),problem))
    explored=[]
    result=[]
    record=[]
    explored.append(problem.getStartState())
    
    while not PQueue.isEmpty():
        node=PQueue.pop()
        result=node[1]
        if problem.isGoalState(node[0]):
            return result
        explored.append(node[0])
        
        for i in problem.getSuccessors(node[0]):
            succesor=i[0]
            step=i[1]
            record=list(result)
            if not i[0] in explored:
                record.append(step)
                PQueue.push((succesor,record),problem.getCostOfActions(record)+heuristic(succesor,problem))
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
