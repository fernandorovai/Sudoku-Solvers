import copy
from queue import *
from copy import deepcopy
from time import *
import tracemalloc

import handlers
import memoryTracker


"""This is where the problem is defined. Initial state, goal state and
 other information that can be got from the problem"""


class Problem(object):
    def __init__(self, initial=None, timeRunning=None):
        """This is the constructor for the Problem class. It specifies the initial state,
        and possibly a goal state, if there is a unique goal.  You can add other arguments if the need arises"""

        self.initial = initial
        self.ac3Time = timeRunning

    def actions(self, vars):
            """Return the actions that can be executed in the given
            state. The result would typically be a list, but if there are
            many actions, consider yielding them one at a time in an
            iterator, rather than building them all at once."""
            actions = []
            mrv = handlers.MRV(vars)
            # mrv = handlers.RandomVar(vars)

            if mrv != '':
                numDomains = len(vars[mrv].domain)
                print("Using MRV - Size of Domain: " + str(numDomains))
                print("Using MRV - Var Name: " + str(mrv))
                for num in range(0, numDomains):
                    var = mrv
                    val = vars[mrv].domain[num]
                    # check which number is allowed in each empty square using pruning and append it to the actions list
                    # pruning: check empty square, check the row, check the column and check the small square
                    # action array gives the row, the column and the possible number
                    actions.append([(var, val)])
            return actions

    def result(self, action, state):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions"""
        newState = deepcopy(state)

        handlers.UpdateVar(newState.constraints, action)
        queue = Queue()

        # Arrange the queue with all constraints and run Revise
        handlers.PrepareQueue(queue, newState.constraints, newState.variables)
        handlers.RunQueue(queue)

        return newState

    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal, as specified in the constructor. Override this
        method if checking against a single self.goal is not enough.
        This must be written by students"""
        if handlers.checkCompleteDomain(state):
            return True
        return False

class Node:
    """A node in a search tree. Contains a pointer to the parent (the node
    that this is a successor of) and to the actual state for this node. Note
    that if a state is arrived at by two paths, then there are two nodes with
    the same state.  Also includes the action that got us to this state"""

    def __init__(self, state, parent=None, action=None):
        """Create a search tree Node, derived from a parent by an action.
        Update the node parameters based on constructor values"""
        self.state = state
        self.action = action
        self.depth = 0

        if parent:
            self.depth = parent.depth + 1

    def expand(self, problem):
        childNodes = []

        # Check new Actions
        actions = problem.actions(self.state.variables)

        for x in range(0, len(actions)):
            childNodes.append(self.child_node(problem, actions[x]))
        return childNodes

    def child_node(self, problem, action):
        thisState = copy.deepcopy(self) #deepcopy
        newState = problem.result(action, self.state)
        return Node(newState, thisState, action)


def AC3_BFS(problem):
    print("WORKING...")
    tracemalloc.start()

    # Get actual time to calculate the algorithm time when its done.
    start = time()

    # Count the nodes
    childNumber = 0

    # Start from first node of the problem Tree
    node = Node(problem.initial)

    # Check if current node meets Goal_Test criteria
    if problem.goal_test(node.state.variables):
        return node

    # Create a Queue to store all nodes of a particular level.
    frontier = Queue() #FIFO
    frontier.put(node)

    # Loop until all nodes are explored(frontier queue is empty) or Goal_Test criteria are met
    while frontier:
        # Remove from frontier, for analysis
        node = frontier.get()
        # Loop over all children of the current node
        # Note: We consider the fact that a node can have multiple child nodes here
        for child in node.expand(problem):
            childNumber += 1

            # If child node meets Goal_Test criteria
            if problem.goal_test(child.state.variables):
                end = time()
                # snapshot = tracemalloc.take_snapshot()
                # memoryTracker.display_top(snapshot)
                timeRunning = (end - start)
                print("\033[91mTime running BFS: " + str(round(timeRunning,2)) + 's \033[0m')
                print("\033[91mTime running AC3 + MRV + BFS: " + str(round(timeRunning + problem.ac3Time,2)) + 's \033[0m')
                print("# of Visited Nodes: " + str(childNumber))
                print("WELL DONE!")
                print("Here you are the solution")
                handlers.printDomains(child.state.variables, child.state.size)
                return child
            frontier.put(child)
    return None

