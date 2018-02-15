from queue import *

# import testRead
import handlers
import BFS
import DFS
from time import *
import math
import testRead


# This is demonstrating a "class" implementation of AC3. You can accomplish the same with lists. For the project, you can choose either.

# The primary problem set-up consists of "variables" and "constraints":
# "variables" are a dictionary of constraint variables (of type ConstraintVar), example variables['A1']
#   "constraints" are a set of binary constraints (of type BinaryConstraint)

# First, Node Consistency is achieved by passing each UnaryConstraint of each variable to nodeConsistent().
# Arc Consistency is achieved by passing "constraints" to Revise().
# AC3 is not fully implemented, Revise() needs to be repeatedly called until all domains are reduced to a single value

class ConstraintVar:
    # instantiation example: ConstraintVar( [1,2,3],'A1' )
    # MISSING filling in neighbors to make it easy to determine what to add to queue when revise() modifies domain

    def __init__(self, d, n):
        self.domain = []

        if len(d) > 0:
            self.domain = [v for v in d]

        self.name = n
        self.neighbors = []


class UnaryConstraint:
    # v1 is of class ConstraintVar
    # fn is the lambda expression for the constraint
    # instantiation example: UnaryConstraint( variables['A1'], lambda x: x <= 2 )
    def __init__(self, v, fn):
        self.var = v
        self.func = fn


class BinaryConstraint:
    # v1 and v2 should be of class ConstraintVar
    # fn is the lambda expression for the constraint
    # instantiate example: BinaryConstraint( A1, A2, lambda x,y: x != y )
    def __init__(self, v1, v2, fn):
        self.var1 = v1
        self.var2 = v2
        self.func = fn


class TrinaryConstraint:
    # v1 and v2 should be of class ConstraintVar
    # fn is the lambda expression for the constraint
    # instantiate example: BinaryConstraint( A1, A2, lambda x,y: x != y )
    def __init__(self, v1, v2, v3, fn):
        self.var1 = v1
        self.var2 = v2
        self.var3 = v3
        self.func = fn


def allDiff(constraints, v):
    # generate a list of constraints that implement the allDiff constraint for all variable combinations in v
    # constraints is a preconstructed list. v is a list of ConstraintVar instances.
    # call example: allDiff( constraints, [A1,A2,A3] ) will generate BinaryConstraint instances for [[A1,A2],[A2,A1],[A1,A3] ...
    fun = lambda x, y: x != y
    for i in range(len(v)):
        for j in range(len(v)):
            if ( i != j ):
                constraints.append(BinaryConstraint(v[i], v[j], fun))


def setUpKenKen(size, variables, constraints):
    # This setup is applicable to KenKen and Sudoku. For this example, it is a 3x3 board with each domain initialized to {1,2,3}
    # The VarNames list can then be used as an index or key into the dictionary, ex. variables['A1'] will return the ConstraintVar object

    # Note that I could accomplish the same by hard coding the variables, for example ...
    # A1 = ConstraintVar( [1,2,3],'A1' )
    # A2 = ConstraintVar( [1,2,3],'A2' ) ...
    # constraints.append( BinaryConstraint( A1, A2, lambda x,y: x != y ) )
    # constraints.append( BinaryConstraint( A2, A1, lambda x,y: x != y ) ) ...
    #   but you can see how tedious this would be.

   #SUDOKU 9x9
    if size == 6:
        domains = [1, 2, 3, 4, 5, 6]
        rows = ['A', 'B', 'C', 'D', 'E', 'F']
        cols = ['1', '2', '3', '4', '5', '6']
    elif size == 9:
        domains = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
        cols = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    elif size == 10:
        domains = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        cols = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    elif size == 12:
        domains = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']
        cols = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
    elif size == 16:
        domains = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
        rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P']
        cols = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16']

    varNames = [x + y for x in rows for y in cols]
    for var in varNames:
        variables[var] = ConstraintVar(domains, var)

    # establish the allDiff constraint for each column and each row
    # for AC3, all constraints would be added to the queue 

    # for example, for rows A,B,C, generate constraints A1!=A2!=A3, B1!=B2...   
    for r in rows:
        aRow = []
        for k in variables.keys():
            if ( str(k).startswith(r) ):
                #accumulate all ConstraintVars contained in row 'r'
                aRow.append(variables[k])
        #add the allDiff constraints among those row elements
        allDiff(constraints, aRow)

    # for example, for cols 1,2,3 (with keys A1,B1,C1 ...) generate A1!=B1!=C1, A2!=B2 ...
    for c in cols:
        aCol = []
        for k in variables.keys():
            key = str(k)
            # the column is indicated in the 2nd character of the key string
            if ( key[1] == c ):
                # accumulate all ConstraintVars contained in column 'c'
                aCol.append(variables[k])
        allDiff(constraints, aCol)


    #add the allDiff constraints to all boxes
    stepRow = 0
    stepCol = 0

    if size == 9:
        stepRow = 3
        stepCol = 3
    elif size == 6:
        stepRow = 2
        stepCol = 3
    elif size == 10:
        stepRow = 2
        stepCol = 5
    elif size == 12:
        stepRow = 3
        stepCol = 4
    elif size == 16:
        stepRow = 4
        stepCol = 4

    for square in range(0, size, int(size/stepCol)):
        for numCol in range(0, size, stepCol):
            boxVarNames = [x + y for x in rows[square:square + stepRow] for y in cols[numCol:numCol + stepCol]]
            boxConstraint = []
            for x in boxVarNames:
                for var in variables.keys():
                    if var == x:
                        boxConstraint.append(variables[var])
                        break
            allDiff(constraints, boxConstraint)

def nodeConsistent(uc):
    domain = list(uc.var.domain)
    for x in domain:
        if ( False == uc.func(x) ):
            uc.var.domain.remove(x)

class CSP():
    def __init__(self, size, variables, constraints):
        self.variables = variables
        self.constraints = constraints
        self.size = size

def tryAC3():
    # create a dictionary of ConstraintVars keyed by names in VarNames.
    startTimer = time()
    variables = dict()
    constraints = []
    queue = Queue()  #instance of a FIFO Queue
    puzzles = testRead.readSudoku()
    puzzle = puzzles[2]
    puzzleSizeFile = puzzle.size

    setUpKenKen(puzzleSizeFile, variables, constraints)  #set All Diff constraints

    for unary in puzzle.unaryDomains:
        nodeConsistent(UnaryConstraint(variables[str(unary[0])], lambda x: x == int(unary[1])))

    print("INITIAL DOMAINS")
    handlers.printDomains(variables, puzzleSizeFile)
    numDomainsBefore = handlers.countDomains(variables)
    print("NUM OF DOMAINS BEFORE AC3: " + str(numDomainsBefore))
    # Arrange the queue with all constraints and run Revise
    handlers.PrepareQueue(queue, constraints, variables)
    handlers.RunQueue(queue)

    if handlers.checkCompleteDomain(variables):
        endTimer = time()
        timeRunning = endTimer - startTimer

        print("Solution using AC-3 Only!")
        handlers.printDomains(variables, puzzleSizeFile)
        print("\033[91mTime running AC-3: " + str(round(timeRunning,2)) + 's \033[0m')
    else:
        endTimer = time()
        print("-------------------------------------------------")
        print("IT WAS NOT POSSIBLE TO SOLVE USING THE AC-3 ONLY.")
        handlers.printDomains(variables, puzzleSizeFile)
        numDomainsAfter = handlers.countDomains(variables)
        gain = (1-(numDomainsAfter / numDomainsBefore)) * 100
        timeRunning = endTimer - startTimer
        print("NUM OF DOMAINS AFTER AC3: " + str(numDomainsAfter))
        print("REDUCTION OF: " + str(round(gain, 2)) + "%")
        print("\033[91mTime running AC-3: " + str(round(timeRunning,2)) + 's \033[0m')
        csp = CSP(puzzleSizeFile, variables, constraints)

        #Here you can choose which search technique you want to use
        searchTechnique = "BFS";
        if(searchTechnique == "BFS"):
            print("CALLING BFS..." + '\n')
            BFS.AC3_BFS(BFS.Problem(csp, timeRunning))
        elif(searchTechnique == "DFS"):
            print("CALLING DFS..." + '\n')
            DFS.AC3_DFS(DFS.Problem(csp, timeRunning))
tryAC3()





