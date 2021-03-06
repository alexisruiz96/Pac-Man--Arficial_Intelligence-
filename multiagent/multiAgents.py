# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

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
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        
        score = successorGameState.getScore()

        if action == Directions.STOP: # penalize stay in the place
          score -= 100


        """ # We tried to maximize if next pos was food
        if currentGameState.getFood()[newPos[0]][newPos[1]]:
          score += 500

        #We tried to minimize if in next pos there was a ghost
        for g in newGhostStates: 
          if g.getPosition() == newPos:
            score -= 501
        """
        """
        #We tried to maximize as far as it was from the ghost with manhattan distance
        ghost_man_factor = 0.25
        for g in newGhostStates:
          man_dist = manhattanDistance(g.getPosition(), newPos)
          score += ghost_man_factor*man_dist
        
        """
        
        #Manhattan distance between closest food, only if there is no food on the new position
        if not currentGameState.getFood()[newPos[0]][newPos[1]]:
          min_food_man = float("Inf")
          food = newFood.asList()
          for f in food:
            f_man = manhattanDistance(f, newPos)
            min_food_man = min(f_man, min_food_man)
          score -= min_food_man

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

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        def maxval(gameState, depth): #max agent function
          depth += 1 #each time we enter to max function, we are in a new depth level, so we add 1
          if gameState.isWin() or gameState.isLose() or depth == self.depth: #base case, we look if we have win, lose or reached max depth
            return self.evaluationFunction(gameState)
          v = float('-Inf')
          for a in gameState.getLegalActions(0): #get allowed pacman actions
            v = max(v, minval(gameState.generateSuccessor(0, a), depth, 1))
          return v

        def minval(gameState, depth, ghostIndex):
          if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

          v = float('Inf')
          for a in gameState.getLegalActions(ghostIndex): #get allowed ghost actions
            if ghostIndex == (gameState.getNumAgents()-1): #last ghost
              v = min(v, maxval(gameState.generateSuccessor(ghostIndex, a), depth))
            else: #look for other ghosts and choose the minimum value
              v = min(v, minval(gameState.generateSuccessor(ghostIndex, a), depth, ghostIndex+1))
          return v

        vals_of_min =[]
        for a in gameState.getLegalActions(0): #for all possible actions
          depth = 0 #start depth at 0
          vals_of_min.append((minval(gameState.generateSuccessor(0, a), depth, 1), a)) #we store all the values

        return max(vals_of_min,key=lambda item:item[0])[1] #get the action of the tuple containing the maximum value
        
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def maxval(gameState, depth, alpha, beta):
          depth += 1
          #base case, we look if we have win, lose or reached max depth
          if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState)
          v = float('-Inf')
          for a in gameState.getLegalActions(0): #get allowed pacman actions
            v = max(v, minval(gameState.generateSuccessor(0, a), depth, 1, alpha, beta))
            if v > beta: #if we find a v bigger than beta, we can prune
              return v
            alpha = max(alpha, v) #we update alpha with max value between alpha and v
          return v

        def minval(gameState, depth, ghostIndex, alpha, beta):
          if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
          v = float('Inf')
          for a in gameState.getLegalActions(ghostIndex): #get allowed pacman actions
            if ghostIndex == (gameState.getNumAgents()-1): #es el ultimo ghost
              v = min(v, maxval(gameState.generateSuccessor(ghostIndex, a), depth, alpha, beta))
            else: #miramos a los otros ghost i escojemos el minimo valor
              v = min(v, minval(gameState.generateSuccessor(ghostIndex, a), depth, ghostIndex+1, alpha, beta))
            if v < alpha: #if we find a v smaller than beta, we can prune
              return v
            beta = min(beta, v) #we update beta with min value between beta and v
          return v

        
        alpha = float('-Inf')
        beta = float('Inf')
        vals_of_min =[]
        for a in gameState.getLegalActions(0):
          depth = 0
          vals_of_min.append((minval(gameState.generateSuccessor(0, a), depth, 1, alpha, beta), a))
          max_min_val = max(vals_of_min,key=lambda item:item[0])[0]
          max_minaction = max(vals_of_min,key=lambda item:item[0])[1]
          if max_min_val>beta: #we prune idf the maximum minval is bigger than beta and we return the action associated with it
            return max_minaction
          alpha = max(alpha, max_min_val)

        return max(vals_of_min,key=lambda item:item[0])[1]  #get the action of the tuple containing the maximum value

        util.raiseNotDefined()

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
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

