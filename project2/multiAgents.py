 # multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
import dis
from _testcapi import INT_MIN, INT_MAX

class ReflexAgent(Agent):
  """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
  """


  def getAction(self, gameState):
    """
    You do not need to change this method, but you're welcome to.

    getAction chooses among the best options according to the evaluation function.

    Just like in the previous project, getAction takes a GameState and returns
    some Directions.X for some X in the set {North, South, West, East, Stop}
    """
    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions()

    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best
    """
    print "choice",legalMoves[chosenIndex]
    print "..............................."
    """

    "Add more of your code here if you want to"
    return legalMoves[chosenIndex]

  def evaluationFunction(self, currentGameState, action):
    """
    Design a better evaluation function here.

    The evaluation function takes in the current and proposed successor
    GameStates (pacman.py) and returns a number, where higher numbers are better.

    The code below extracts some useful information from the state, like the
    remaining food (newFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.

    Print out these variables to see what you're getting, then combine them
    to create a masterful evaluation function.
    """
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    #print "successorGameState",successorGameState
    newPos = successorGameState.getPacmanPosition()
    newFood = successorGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    "*** YOUR CODE HERE ***"
    foods=newFood.asList();  
    score=0  
    if len(foods)==0:
        return 99999          #if there is no food, return 99999
    else:   
        disToClosestFood=min([manhattanDistance(newPos,food)for food in foods]) 
        ghosts=successorGameState.getGhostPositions(); 
        disToClosestGhost=min([manhattanDistance(newPos,ghost)for ghost in ghosts])
        disToAllGhost=0
        
        for ghost in ghosts:
            disToAllGhost+=manhattanDistance(newPos,ghost)
        if disToClosestGhost<3:
            ghostScore1=disToClosestGhost
        else:
            ghostScore1=10
        if disToAllGhost<5:
            ghostScore2=disToAllGhost
        else:
            ghostScore2=10 
         
        score=(ghostScore1/10)*(ghostScore2/10)*(9999-30*len(foods)-3*disToClosestFood/random.randint(1,6))

    return score

def scoreEvaluationFunction(currentGameState):
  """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
  """
  return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
  """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
  """

  def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
    self.index = 0 # Pacman is always agent index 0
    self.evaluationFunction = util.lookup(evalFn, globals())
    self.depth = int(depth)
   

class MinimaxAgent(MultiAgentSearchAgent):
  """
    Your minimax agent (question 2)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction.

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    "*** YOUR CODE HERE ***"
    LegalActions=gameState.getLegalActions(0)
    result=[]
    score=-9999
    action=[]
    for action in LegalActions:
        result.append((self.min_value(0,gameState.generateSuccessor(0,action),1),action))
    for score1,action1 in result:
        if score1>score:
            score=score1
            action=action1
    return action
   
  def min_value(self,agent,state,depth):
    depth+=1 #return 3
    if depth>self.depth: 
        return self.evaluationFunction(state)
    else:
        score=99999  
        for gitem in range(1,state.getNumAgents()): #ghost1 2 3 
            LegalActions=state.getLegalActions(gitem)
            if len(LegalActions)==0: 
                return  self.evaluationFunction(state)
            else:
                for action in LegalActions:
                    state1=state.generateSuccessor(gitem,action)
                    score=min(score,self.max_value(gitem,state1,depth))    
    return  score 
    

  def max_value(self,agent,state,depth):
    if depth>self.depth: 
        return self.evaluationFunction(state)
    else: 
        score=-99999
        LegalActions=state.getLegalActions(0) 
        if len(LegalActions)==0: 
            return self.evaluationFunction(state)
        else:  
            for action in LegalActions:  #ghost
                state1=state.generateSuccessor(0,action)
                score=max(score,self.min_value(0,state1,depth))              
    return  score
                    
  
     
class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"
    LegalActions=gameState.getLegalActions(0)
    result=[]
    score=-9999
    action=[]
    for action in LegalActions:
        result.append((self.min_value(0,gameState.generateSuccessor(0,action),1,-9999,9999),action))
    for score1,action1 in result:
        if score1>score:
            score=score1
            action=action1
    return action
   
  def min_value(self,agent,state,depth,alpha,belta):
    depth+=1 #return 3
    if depth>self.depth: 
        return self.evaluationFunction(state)
    else:
        score=99999  
        for gitem in range(1,state.getNumAgents()): #ghost1 2 3 
            LegalActions=state.getLegalActions(gitem)
            if len(LegalActions)==0: 
                return  self.evaluationFunction(state)
            else:
                for action in LegalActions:
                    state1=state.generateSuccessor(gitem,action)
                    score=min(score,self.max_value(gitem,state1,depth,alpha,belta)) 
                    if score<=alpha:
                        return  score
                    belta=min(belta,score)
    return  score 
    

  def max_value(self,agent,state,depth,alpha,belta):
    if depth>self.depth: 
        return self.evaluationFunction(state)
    else: 
        score=-9999
        LegalActions=state.getLegalActions(0) 
        if len(LegalActions)==0: 
            return self.evaluationFunction(state)
        else:  
            for action in LegalActions:  #ghost
                state1=state.generateSuccessor(0,action)
                score=max(score,self.min_value(0,state1,depth,alpha,belta)) 
                if score>=belta:
                    return  score
                alpha=max(alpha,score)
        return score
    

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (question 4)
  """

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """
    "*** YOUR CODE HERE ***"
    LegalActions=gameState.getLegalActions(0)
    result=[]
    score=-9999
    action=[]
    for action in LegalActions:
        result.append((self.min_value(0,gameState.generateSuccessor(0,action),1),action))
    for score1,action1 in result:
        if score1>score:
            score=score1
            action=action1
    return action
   
  def min_value(self,agent,state,depth):
    depth+=1 #return 3
    if depth>self.depth: 
        return self.evaluationFunction(state)
    else:
        score=0  
        for gitem in range(1,state.getNumAgents()): #ghost1 2 3 
            LegalActions=state.getLegalActions(gitem)
            if len(LegalActions)==0: 
                return  self.evaluationFunction(state)
            else:
                for action in LegalActions:
                    state1=state.generateSuccessor(gitem,action)
                    score+=self.max_value(gitem,state1,depth)/len(LegalActions)    
    return  score/state.getNumAgents() 
    

  def max_value(self,agent,state,depth):
    if depth>self.depth: 
        return self.evaluationFunction(state)
    else: 
        score=-99999
        LegalActions=state.getLegalActions(0) 
        if len(LegalActions)==0: 
            return self.evaluationFunction(state)
        else:  
            for action in LegalActions:  #ghost
                state1=state.generateSuccessor(0,action)
                score=max(score,self.min_value(0,state1,depth))              
    return  score
    

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <writing heree someth so we know what you did>
    """
    PacPos = currentGameState.getPacmanPosition()
    FoodPos = currentGameState.getFood().asList()
    GhostPos=currentGameState.getGhostPositions()
    CapPos=currentGameState.getCapsules()
    GhostNum=currentGameState.getNumAgents()-1
    GhostStates = currentGameState.getGhostStates()
    ScaredTimes = [ghostState.scaredTimer for ghostState in GhostStates]
   # print currentGameState,"\nPacman:",PacPos,"\nGhostNum:",GhostNum,"\nGhost:",GhostPos,"\nCapsules:",CapPos,"ScaredTimes",ScaredTimes
    "*** YOUR CODE HERE ***"
    if len(FoodPos)==0:
        return 9999
    else:  
        score=9999-20*len(FoodPos)-100*len(CapPos)
        PacToClosestFood=min([manhattanDistance(PacPos,food)for food in FoodPos])
        if len(CapPos)!=0:
            PacToClosestCap=min([manhattanDistance(PacPos,capsule)for capsule in CapPos])
            score=score+8*pow(0.95,PacToClosestFood)+30*pow(0.95,PacToClosestCap)
        else:
            score=score+10*pow(0.9,PacToClosestFood)
            PacToGhostmin=20 
            PacToAllGhostmin=0
            PacToAllGhost=[manhattanDistance(PacPos,ghost)for ghost in GhostPos]
            for i in range(0,GhostNum):
                if ScaredTimes[i]<2 and PacToAllGhost[i]<4:
                    PacToGhostmin=min(PacToGhostmin,PacToAllGhost[i])
                    PacToAllGhostmin+=PacToGhostmin
                else:
                    PacToAllGhostmin+=10
            
            if PacToAllGhostmin>10:
                PacToAllGhostmin=30
            score=PacToGhostmin/15*PacToAllGhostmin/30*score
 
    return score
  

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

