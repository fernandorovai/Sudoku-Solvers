import re
from enum import Enum

class puzzleClass:
    def __init__(self, puzzle, size, numOfEmpty, unaryDomains):
        self.puzzle = puzzle
        self.size = size
        self.numOfEmpty = numOfEmpty
        self.unaryDomains = unaryDomains

#read in the file with constraints for KenKen puzzles (1 line per puzzle)
def readSudoku():
    lines = open('testSudoku.txt').readlines()
    puzzles = []
    domains = []
    # print(lines)

    for line in lines:
        if not line.__contains__('#'):
            line = line.split("\n")
            # print("OK" + line[0]) #entire line
            rawLine = line[0].split(".")
            size = int(rawLine[0])
            # print("Size: " + rawLine[0]) #entire line
            puzzle = rawLine[1]
            # print("Puzzle: " + puzzle)
            [constraints, emptys] = separatePuzzle(puzzle)
            puzzles.append(puzzleClass(puzzle,size,emptys,constraints))
    return puzzles

def checkHex(element):
    if element == 'A':
        element = 10
    elif element == 'B':
        element = 11
    elif element == 'C':
        element = 12
    elif element == 'D':
        element = 13
    elif element == 'E':
        element = 14
    elif element == 'F':
        element = 15
    elif element == 'G':
        element = 16
    return element

def separatePuzzle(puzzle):
    rows = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T"]
    constraints = []
    emptys = 0
    line = puzzle.split(";")
    for idxRow, puzzleRow in enumerate(line):
        elements = puzzleRow.replace("[","")
        elements = elements.replace("]","")
        rawElements = puzzleRow.split(",")
        for idxElement, element in enumerate(rawElements):
            element = element.replace("[","")
            element = element.replace("]","")
            if element == "-":
                emptys = emptys + 1
            else:
                elementVal = checkHex(element)
                elementName = str(rows[idxRow]) + str(idxElement+1) #create the var name
                constraint = []
                constraint = [elementName, elementVal]
                constraints.append(constraint)
    return [constraints, emptys]

readSudoku()