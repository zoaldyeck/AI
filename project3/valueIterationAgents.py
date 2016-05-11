# valueIterationAgents.py
# -----------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
  """
      * Please read learningAgents.py before reading this.*

      A ValueIterationAgent takes a Markov decision process
      (see mdp.py) on initialization and runs value iteration
      for a given number of iterations using the supplied
      discount factor.
  """
  def __init__(self, mdp, discount = 0.9, iterations = 100):
    """
      Your value iteration agent should take an mdp on
      construction, run the indicated number of iterations
      and then act according to the resulting policy.
    
      Some useful mdp methods you will use:
          mdp.getStates()
          mdp.getPossibleActions(state)
          mdp.getTransitionStatesAndProbs(state, action)
          mdp.getReward(state, action, nextState)
          V(s) = max_{a in actions} Q(s,a)
    """
    self.mdp = mdp
    self.discount = discount
    self.iterations = iterations
    self.values = util.Counter()   # A Counter is a dict with default 0
    "*** YOUR CODE HERE ***"
    self.qValues = util.Counter()  #global v and q for every state, initial = 0
    states = mdp.getStates()
    for i in range(0,iterations):
        new = self.values.copy()
        for state in states:
            actions = mdp.getPossibleActions(state)
            qValues = []
            for action in actions: #for every state, several actions,every has a q value
                qValues.append(self.getQValue(state,action))
            if len(qValues)==0:
                new[state] = 0
            else:
                new[state] = max(qValues) #use get qvalue to get q value,and select the biggest qvalue for every state
        self.values=new.copy()   
        
  def getValue(self, state):
    """
      Return the value of the state (computed in __init__).
    """
    return self.values[state]


  def getQValue(self, state, action):
    """
      The q-value of the state action pair
      (after the indicated number of value iteration
      passes).  Note that value iteration does not
      necessarily create this quantity and you may have
      to derive it on the fly.
      mdp.getStates()
          mdp.getPossibleActions(state)
          mdp.getTransitionStatesAndProbs(state, action)
          mdp.getReward(state, action, nextState)
    """
    "*** YOUR CODE HERE ***"
    trans = self.mdp.getTransitionStatesAndProbs(state,action)
    temp=0.0
    for nextState,prob in trans:
        temp+=prob*(self.mdp.getReward(state,action,nextState)+self.discount*self.getValue(nextState))
    self.qValues[state,action]=temp
    return self.qValues[state,action]
    util.raiseNotDefined()

  def getPolicy(self, state):
    """
      The policy is the best action in the given state
      according to the values computed by value iteration.
      You may break ties any way you see fit.  Note that if
      there are no legal actions, which is the case at the
      terminal state, you should return None.
      policy(s) = arg_max_{a in actions} Q(s,a)
      mdp.getStates()
          mdp.getPossibleActions(state)
          mdp.getTransitionStatesAndProbs(state, action)
          mdp.getReward(state, action, nextState)
    """
    "*** YOUR CODE HERE ***"
    actions = self.mdp.getPossibleActions(state)
    maxAction = []
    maxQ = -999999
    if len(actions)==0:
        return None
    else:
        for action in actions:
            if self.qValues[state,action]>maxQ:
                maxQ = self.qValues[state,action]
                maxAction = action
        return maxAction
    
   

  def getAction(self, state):
    "Returns the policy at the state (no exploration)."
    return self.getPolicy(state)
  
