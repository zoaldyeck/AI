# qlearningAgents.py
# ------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math

class QLearningAgent(ReinforcementAgent):
  """
    Q-Learning Agent

    Functions you should fill in:
      - getQValue
      - getAction
      - getValue
      - getPolicy
      - update

    Instance variables you have access to
      - self.epsilon (exploration prob)
      - self.alpha (learning rate)
      - self.discount (discount rate)

    Functions you should use
      - self.getLegalActions(state)
        which returns legal actions
        for a state
  """
  def __init__(self, **args):
    "You can initialize Q-values here..."
    ReinforcementAgent.__init__(self, **args)

    "*** YOUR CODE HERE ***"
    self.value=util.Counter()
    self.qValue = util.Counter()

  def getQValue(self, state, action):
    """
      Returns Q(state,action)
      Should return 0.0 if we never seen
      a state or (state,action) tuple
    """
    "*** YOUR CODE HERE ***"
  
    return self.qValue[state,action]
    util.raiseNotDefined()


  def getValue(self, state):
    """
      Returns max_action Q(state,action)
      where the max is over legal actions.  Note that if
      there are no legal actions, which is the case at the
      terminal state, you should return a value of 0.0.
    """
    "*** YOUR CODE HERE ***"
    legalActions = self.getLegalActions(state)
    q=[self.getQValue(state, action) for action in legalActions]
    if len(q)==0:
        self.value[state]=0.0
    else:
        self.value[state]=max(q)
    return self.value[state]
    util.raiseNotDefined()

  def getPolicy(self, state):
    """
      Compute the best action to take in a state.  Note that if there
      are no legal actions, which is the case at the terminal state,
      you should return None.
    """
    "*** YOUR CODE HERE ***"
    legalActions = self.getLegalActions(state)
    maxQ = -9999
    maxAction = []
    if len(legalActions)==0:
        return None
    else:
        for action in legalActions:
            if self.qValue[state,action]>maxQ:
                maxQ=self.qValue[state,action]
                maxAction=action
        return maxAction    
    util.raiseNotDefined()

  def getAction(self, state):
    """
      Compute the action to take in the current state.  With
      probability self.epsilon, we should take a random action and
      take the best policy action otherwise.  Note that if there are
      no legal actions, which is the case at the terminal state, you
      should choose None as the action.

      HINT: You might want to use util.flipCoin(prob)
      HINT: To pick randomly from a list, use random.choice(list)
    """
    # Pick Action
    "*** YOUR CODE HERE ***"
    legalActions = self.getLegalActions(state)
    if len(legalActions)==0:
        action = None
    else:
        actionBest = self.getPolicy(state)
        actionRandom = random.choice(legalActions)
        if util.flipCoin(self.epsilon):
            action = actionRandom
        else:
            action = actionBest
    return action

  def update(self, state, action, nextState, reward):
    """
      The parent class calls this to observe a
      state = action => nextState and reward transition.
      You should do your Q-Value update here

      NOTE: You should never call this function,
      it will be called on your behalf
    """
    "*** YOUR CODE HERE ***"
    new=self.qValue.copy()
    new[state,action]=(1-self.alpha)*new[state,action]+self.alpha*(reward+self.discount*self.getValue(nextState))
    self.qValue[state,action]=new[state,action]
   
    
 
 
class PacmanQAgent(QLearningAgent):
  "Exactly the same as QLearningAgent, but with different default parameters"

  def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
    """
    These default parameters can be changed from the pacman.py command line.
    For example, to change the exploration rate, try:
        python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

    alpha    - learning rate
    epsilon  - exploration rate
    gamma    - discount factor
    numTraining - number of training episodes, i.e. no learning after these many episodes
    """
    args['epsilon'] = epsilon
    args['gamma'] = gamma
    args['alpha'] = alpha
    args['numTraining'] = numTraining
    self.index = 0  # This is always Pacman
    QLearningAgent.__init__(self, **args)

  def getAction(self, state):
    """
    Simply calls the getAction method of QLearningAgent and then
    informs parent of action for Pacman.  Do not change or remove this
    method.
    """
    action = QLearningAgent.getAction(self,state)
    self.doAction(state,action)
    return action


class ApproximateQAgent(PacmanQAgent):
  """
     ApproximateQLearningAgent

     You should only have to overwrite getQValue
     and update.  All other QLearningAgent functions
     should work as is.
  """
  def __init__(self, extractor='IdentityExtractor', **args):
    self.featExtractor = util.lookup(extractor, globals())()
    PacmanQAgent.__init__(self, **args)
    # You might want to initialize weights here.
    "*** YOUR CODE HERE ***"
    self.weight=util.Counter()
  
  def getQValue(self, state, action):
    """
      Should return Q(state,action) = w * featureVector
      where * is the dotProduct operator
    """
    "*** YOUR CODE HERE ***"
    #print "get QValue\n"
    #print "state=\n",state,"\naction=",action
   # self.featExtractor = util.lookup('SimpleExtractor',globals())()
    features = self.featExtractor.getFeatures(state,action)
    q=0.0
    for feature in features:
        q+=self.weight[feature]*features[feature]   
    return q


  def update(self, state, action, nextState, reward):
    """
       Should update your weights based on transition
    """
    "*** YOUR CODE HERE ***"
   # self.featExtractor = util.lookup('SimpleExtractor',globals())()
    features = self.featExtractor.getFeatures(state,action)
    #print "round ",self.count
   # print "1.before update\nstate=\n",state,"\naction=",action,"\nnextState=\n",nextState,"\nreward=",reward
    #print "discount=",self.discount,"alpha=",self.alpha   # print "weight=",self.weigh
    sample = reward+self.discount*self.getValue(nextState)
    correction=sample-self.getQValue(state,action)
    
    for feature in features:  
        #print "in update,feature=",features[feature]
        self.weight[feature]=self.weight[feature]+self.alpha*correction*features[feature]
        
    #print "After update,weight=",self.weight
    #return self.weight
    

  def final(self, state):
    "Called at the end of each game."
    # call the super-class final method
    PacmanQAgent.final(self, state)

    # did we finish training?
    if self.episodesSoFar == self.numTraining:
      # you might want to print your weights here for debugging
      "*** YOUR CODE HERE ***"
    #self.count+=1
   # if self.count==100:
        #print yy
    pass
