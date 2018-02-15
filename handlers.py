from math import *
import random

def ReviseBinary(bc):
    # The Revise() function from AC-3, which removes elements from var1 domain, if not arc consistent
    # A single BinaryConstraint instance is passed in to this function.
    # copy domains for use with iteration (they might change inside the for loops)
    try:
        bc.var3
        ReviseTrinary(bc)
    except:
        dom1 = list(bc.var1.domain)
        dom2 = list(bc.var2.domain)

    # pepino = False
    # if bc.var1.name == "H10" and bc.var2.name == "J10" or bc.var2.name == "H10" and bc.var1.name == "J10":
    #     pepino = True


        addToQueue = False
        # for each value in the domain of variable 1
        for x in dom1:
            # for each value in the domain of variable 2
            satisfies = False
            for y in dom2:
                if (bc.func(x,y) == True):
                    satisfies = True
                    break;
            if (satisfies == False):
                bc.var1.domain.remove(x)
                addToQueue = True
        return addToQueue
        # if nothing in domain of variable2 satisfies the constraint when variable1==x, remove x

def ReviseTrinary(bc):
    # The Revise() function from AC-3, which removes elements from var1 domain, if not arc consistent
    # A single BinaryConstraint instance is passed in to this function.
    # copy domains for use with iteration (they might change inside the for loops)

    dom1 = list(bc.var1.domain)
    dom2 = list(bc.var2.domain)
    dom3 = list(bc.var3.domain)

    addToQueue = False
    # for each value in the domain of variable 1
    for x in dom1:
        # for each value in the domain of variable 2
        satisfies = False
        for y in dom2:
            for z in dom3:
                if (bc.func(x,y,z) == True):
                    satisfies = True
        if (satisfies == False):
            bc.var1.domain.remove(x)
            addToQueue = True
    return addToQueue
    # if nothing in domain of variable2 satisfies the constraint when variable1==x, remove x


def PrepareQueue(queue, constraints, variables):
    # Append constraints in the queue
    for c in constraints:
        queue.put(c)

    # Append neighbors in the queue
    for variable in variables:
        variables[variable].neighbors = constraints

def RunQueue(queue):
    while not queue.empty():
            constraint = queue.get()
            if ReviseBinary(constraint):
                for c in constraint.var1.neighbors:
                    queue.put(c)

def MRV(board):
    maxDomain = int(sqrt(len(board)))
    domainSize = 0
    mrv = ''
    for var in board:
        domainSize = len(board[var].domain)
        if (domainSize < maxDomain) and (domainSize > 1):
            maxDomain = domainSize
            mrv = var
    return mrv

def RandomVar(vars):
    selectedVar = random.choice(list(vars.keys()))
    while(len(vars[selectedVar].domain) <= 1):
        selectedVar = random.choice(list(vars.keys()))
    return selectedVar

def UpdateVar(constraints, var):
    varName = var[0][0]
    varVal = var[0][1]
    for c in constraints:
            if c.var1.name == varName:
                c.var1.domain = [varVal]
                break

def checkEmptyDomains(board):
    emptyDomain = False
    for var in board:
        domainSize = len(board[var].domain)
        if domainSize == 0:
            emptyDomain = True
            break;
    return emptyDomain

def checkCompleteDomain(board):
    completeDomain = True
    for var in board:
        domainSize = len(board[var].domain)
        if domainSize != 1:
            completeDomain = False
            break;
    return completeDomain

def countDomains(variables):
    count = 0
    for var in variables:
        count = count + len(variables[var].domain)
    return count

def printDomains(vars, n=3):
    count = 0
    for k in sorted(vars.keys()):
        print(k, '{', vars[k].domain, '}, ', end="")
        count = count + 1
        if ( 0 == count % n ):
            print(' ')