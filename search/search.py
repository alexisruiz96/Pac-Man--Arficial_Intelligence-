# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
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
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    """
    "*** YOUR CODE HERE ***"
    stack = util.Stack() #estructura de datos para dfs 
    first_node = (problem.getStartState(), None, 0, None)
    stack.push(first_node)
    visited = set()
    while not stack.isEmpty(): #mientras pila no sea vacia iteramos

        next_node = stack.pop()
        
        if problem.isGoalState(next_node[0]): #si el nodo es goal devolvemos su path
            actions = [next_node[1]]
            p = next_node[3] #creamos un auxiliar para hacer bactrack
            while p is not None: #backtrack
                actions.append(p[1])
                p = p[3]
            return actions[0:-1][::-1] #retornar actions en orden correcto invirtiendo la lista y sin None
        else:
            if next_node[0] not in visited: #si no ha sido visitado se anade a visited
                visited.add(next_node[0])
                for suc in problem.getSuccessors(next_node[0]): #expandimos los nodos hijos

                    stack.push((suc[0], suc[1], suc[2], next_node))#anadimos nodo a la pila

    
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    El funcionamiento de bfs viene determinado por la 
    estructura de datos que utilizamos por lo que la diferencia 
    con dfs es que utiliza una cola en vez de una pila y 
    por lo tanto su forma de busqueda varia

    """

    queue = util.Queue() #estructura de datos para bfs
    first_node = (problem.getStartState(), None, 0, None)
    queue.push(first_node)
    visited = [] #aqui guardamos los visitados
    while not queue.isEmpty():

        next_node = queue.pop()
        
       
        if problem.isGoalState(next_node[0]):
            actions = [next_node[1]]
            p = next_node[3]
            while p is not None:
                actions.append(p[1])
                p = p[3]
            return actions[0:-1][::-1]
        else:
            if next_node[0] not in visited:
                visited.append(next_node[0])
                for suc in problem.getSuccessors(next_node[0]):
                    queue.push((suc[0], suc[1], suc[2], next_node)) #anadimos nodo a la cola
                    
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    '''
        Para este algoritmo valoramos el coste de cada nodo para 
        llegar al Goal como prioridad en la cola y por lo tanto buscamos
        el camino al Goal menos costoso desde el estado inicial.
    '''
    prio_queue = util.PriorityQueue() #la prio_queue permite dar prioridad en funcion del coste
    first_node = (problem.getStartState(), None, 0, None)
    prio_queue.push(first_node,first_node[2]) #introducimos el primer nodo y el coste como prioridad            
    visited = set()
    while not prio_queue.isEmpty():                         

        next_node = prio_queue.pop()
        
        #si llegamos al goal extraeremos el path del que tiene mayor prioridad
        if problem.isGoalState(next_node[0]):
            actions = [next_node[1]]
            p = next_node[3]
            
            while p is not None:
                actions.append(p[1])
                p = p[3]
            return actions[0:-1][::-1]
        else:
            if next_node[0] not in visited:
                visited.add(next_node[0])
                for suc in problem.getSuccessors(next_node[0]):
                    cost = suc[2] #coste inicial de suc es su propio coste
                    parent = next_node #auxiliar para calcular el coste total del successor
                    while parent is not None: #while de bactrack y suma de costes 
                        cost = cost + parent[2]
                        parent = parent[3]
                                       
                    prio_queue.push((suc[0], suc[1], suc[2], next_node),cost) #anadimos nodo a la prio_queue

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    prio_queue = util.PriorityQueue()
    first_node = (problem.getStartState(), None, 0, None)
    prio_queue.push(first_node,first_node[2])
    visited = []
    while not prio_queue.isEmpty():

        next_node = prio_queue.pop()
        
        
        if problem.isGoalState(next_node[0]): 
            actions = [next_node[1]]
            p = next_node[3]
            
            while p is not None:
                actions.append(p[1])
                p = p[3]
            return actions[0:-1][::-1]
        else:
            if next_node[0] not in visited:
                visited.append(next_node[0])
                for suc in problem.getSuccessors(next_node[0]):
                    cost = suc[2]
                    parent = next_node
                    while parent is not None:
                        cost = cost + parent[2]
                        parent = parent[3]
                    #while de bactrack y suma de costes 
                    #hemos calculado el coste como en ucs pero en este caso le anadimos el 
                    #coste estimado por la heuristica
                    prio_queue.push((suc[0], suc[1], suc[2], next_node),cost + heuristic(suc[0], problem))


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
