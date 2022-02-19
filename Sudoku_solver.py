import sys
from AC3 import AC3, removeInconsistentValues
from backtrack import backtrackRecursion
import Utility
import re
import itertools

rows = "123456789"
cols = "ABCDEFGHI"

#Set up the Sudoku grid from the string
class Sudoku:
    def __init__(self, grid):
        game = list(grid)

        #Generates all the coordinates to designate each cell in the grid
        self.cells = list()
        self.cells = self.generateCoords()

        #Creates the possibilities 1-9 for every cell, unless its already been given
        self.possibilities = dict()
        self.possibilities = self.generatePossibilities(grid)

        #Generates the constraints for rows, columns, and 3x3 subgrids
        ruleConstraints = self.generateRulesConstraints()

        #Takes the above constraints and createst the binary relations between cells as nodes
        self.binaryConstraints = list()
        self.binaryConstraints = self.GenerateBinaryConstraints(ruleConstraints)

        #Generates the relationship between each node
        self.relatedCells = dict()
        self.relatedCells = self.generateRelatedCells()

        #Generates the list of values that have been pruned out by forward checking
        self.pruned = dict()
        self.pruned = {v: list() if grid[i] == '0' else [int(grid[i])] for i, v in enumerate(self.cells)}

    #Generates the coordinate grid for the all the cells
    def generateCoords(self):

        allCellsCoords = []

        #for A,B,C, ... ,H,I
        for col in cols:

            #for 1,2,3 ,... ,8,9
            for row in rows:
                #A1, A2, A3, ... , H8, H9
                newCoords = col + row
                allCellsCoords.append(newCoords)

        return allCellsCoords

    #Generates the possibilites 1-9 for undetermined cells and slots the given values for given cells at the start
    def generatePossibilities(self, grid):

        gridList = list(grid)

        possibilities = dict()

        for index, coords in enumerate(self.cells):
            #if value is 0, then the cell can have any value in [1, 9]
            if gridList[index] == "0":
                possibilities[coords] = list(range(1, 10))
            #else value is already defined, possibilities is this value
            else:
                possibilities[coords] = [int(gridList[index])]

        return possibilities

    
    #Makes constraints based upon the rules of Sudoku
    def generateRulesConstraints(self):

        rowConstraints = []
        columnConstraints = []
        squareConstraints = []

        #Rows constraints
        for row in rows:
            rowConstraints.append([col + row for col in cols])

        #Columns constraints
        for col in cols:
            columnConstraints.append([col + row for row in rows])

        #3x3 square constraints
        rowsSquareCoords = (cols[i:i + 3] for i in range(0, len(rows), 3))
        rowsSquareCoords = list(rowsSquareCoords)

        colsSquareCoords = (rows[i:i + 3] for i in range(0, len(cols), 3))
        colsSquareCoords = list(colsSquareCoords)

        #Apply the constraints to each cell...
        for row in rowsSquareCoords:
            for col in colsSquareCoords:

                currentSquareConstraints = []

                #...And each value in it
                for x in row:
                    for y in col:
                        currentSquareConstraints.append(x + y)

                squareConstraints.append(currentSquareConstraints)

        #All of the constraints is the sum of the three rules
        return rowConstraints + columnConstraints + squareConstraints

    #Creates the binary constraints from the rule constraints
    def GenerateBinaryConstraints(self, ruleConstraints):
        generatedBinaryConstraints = list()

        #Create binary constraints for each set of constraints based on the rules
        for constraintSet in ruleConstraints:

            binaryConstraints = list()

            #2 because we want binary constraints
            for binaryConstraint in itertools.permutations(constraintSet, 2):
                binaryConstraints.append(binaryConstraint)

            #For every binary constraint...
            for constraint in binaryConstraints:

                #Make sure it is unique/doesn't already exist
                constraintList = list(constraint)
                if (constraintList not in generatedBinaryConstraints):
                    generatedBinaryConstraints.append([constraint[0], constraint[1]])

        return generatedBinaryConstraints

    #Creates what cells are related to one another
    def generateRelatedCells(self):
        relatedCells = dict()

        #for each one of the 81 cells
        for cell in self.cells:

            relatedCells[cell] = list()

            #related cells are the ones that current cell has constraints with
            for constraint in self.binaryConstraints:
                if cell == constraint[0]:
                    relatedCells[cell].append(constraint[1])

        return relatedCells


    #Determines if the Sudoku is solved or not by iterating through each cell and making sure there is only one possibility for it
    def isFinished(self):
        for coords, possibilities in self.possibilities.items():
            if len(possibilities) > 1:
                return False

        return True

    
    #Generates a easy to read string based on a Sudoku
    def __str__(self):

        output = ""
        count = 1

        #For each cell...
        for cell in self.cells:

            #...Print its value
            value = str(self.possibilities[cell])
            if type(self.possibilities[cell]) == list:
                value = str(self.possibilities[cell][0])

            output += "[" + value + "]"

            #Makes a newline at the end of a row
            if count >= 9:
                count = 0
                output += "\n"

            count += 1

        return output

#Solves a Sudoku via AC3 and returns true if complete, and false if impossible
def solveAC3(grid):

    print("AC3 starting")
    #Make the Sudoku based on the provided input grid
    sudoku = Sudoku(grid)

    #Launch AC-3 algorithm of the Sudoku
    AC3SolutionExists = AC3(sudoku)

    #Sudoku has no solution
    if not AC3SolutionExists:
        print("this Sudoku has no solution")

    else:
        
        #If AC3 worked print the solution
        if sudoku.isFinished():

            print("Solution complete.")
            print("Result: \n{}".format(sudoku))

        #If AC3 didn't work, we need to backtrack
        else:

            print("Backtracking to find solution...")

            assignment = {}

            #Set the values we already know
            for cell in sudoku.cells:

                if len(sudoku.possibilities[cell]) == 1:
                    assignment[cell] = sudoku.possibilities[cell][0]
            
            #Then start backtraing
            assignment = backtrackRecursion(assignment, sudoku)
            
            #merge the computed values for the cells at one place
            for cell in sudoku.possibilities:
                sudoku.possibilities[cell] = assignment[cell] if len(cell) > 1 else sudoku.possibilities[cell]
            
            if assignment:
                print("Result: \n{}".format(sudoku))

            else:
                print("No solution exists")


if __name__ == "__main__":

    selection = 0
    selection = int(input("Please input a 1 to input the Sudoku manually, or input a 2 to read it from a .txt file\n"))
    sudoku = ""
    while selection != 1 and selection != 2:
        selection = int(input("Input not recognized, please input a 1 or a 2\n"))

    if selection == 1:
        sudoku = str(input("Type the Sudoku as a 81 character string that goes across each row, use a 0 as a blank cell\n"))
        if len(sudoku)  != 81 or not sudoku.isdecimal():
            print("Sudoku is of improper form, exiting")
            exit(1)

    if selection == 2:
        filename = str(input("Type the filename without the file extension\n"))
        filename = filename + ".txt"
        file = open(filename, "r")
        with open(filename, "r") as file:
            while True:
                fileChar = file.read()
                sudoku = sudoku + fileChar
                if fileChar == '':
                    #Debug: print("EOF")
                    break

            #Debug: print(sudoku)
            sudoku = sudoku.replace(" ", "")
            sudoku = sudoku.replace('\n', "")
            sudoku = sudoku.replace('\r', "")
            sudoku = sudoku.replace('\r\n', "")
            sudoku = sudoku.replace(',', "")
            sudoku = sudoku.replace('[', "")
            sudoku = sudoku.replace(']', "")
            #Debug: print(sudoku)

            if len(sudoku)  != 81 or not sudoku.isdecimal():
                print("Sudoku is of improper form, exiting")
                exit(1)

    selection = int(input("Please input a 1 to solve via AC3, or input a 2 to solve via forward checking\n"))
    while selection != 1 and selection != 2:
        selection = int(input("Input not recognized, please input a 1 or a 2\n"))

    if selection == 1:
        solveAC3(sudoku)

    if selection == 2:
        solveForwardChecking(sudoku)