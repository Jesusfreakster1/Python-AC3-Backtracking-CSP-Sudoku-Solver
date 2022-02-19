import sys

#Returns the variable that has the least possible values remaining
def selectMostConstrainedVariable(assignment, sudoku):

    unassigned = []

    #Add all cells to the assignment that aren't
    for cell in sudoku.cells:
        if cell not in assignment:
            unassigned.append(cell)

    #The least possibliites left is what we are judging by
    criterion = lambda cell: len(sudoku.possibilities[cell])

    #Return the value with the lowest number of possibilities remaining
    return min(unassigned, key=criterion)

#When selecting a value to assign a cell, choose the one that conflicts with the least other possibilities for neighboring cells
def orderDomainValues(sudoku, cell):

    #If we only have one option we return it
    if len(sudoku.possibilities[cell]) == 1:
        return sudoku.possibilities[cell]

    #Otherwise, we find the possible value that has the least number of conflicts with its neighbors
    criterion = lambda value: CountConflicts(sudoku, cell, value)
    return sorted(sudoku.possibilities[cell], key=criterion)

#If two cells are different, return true; otherwise, return false
def isDifferent(cell_i, cell_j):
    result = cell_i != cell_j
    return result

#Count up the number of conflicts cuased by a particular cell assignment, and return that count
def CountConflicts(sudoku, cell, value):

    count = 0

    #For all neighbors...
    for relatedCell in sudoku.relatedCells[cell]:

        #If we don't already know its value, and our value is within the realm of our neighbors possibilities...
        if len(sudoku.possibilities[relatedCell]) > 1 and value in sudoku.possibilities[relatedCell]:
            
            #...Then count the conflict
            count += 1

    return count

#Checks if a particular cell has a valid value
def isConsistent(sudoku, assignment, cell, value):

    isConsistent = True

    #For each cell in assignment...
    for currentCell, currentValue in assignment.items():

        #...If it has a neighbor that has an equal value...
        if currentValue == value and currentCell in sudoku.relatedCells[cell]:

            #...Then cell is not consistent
            isConsistent = False
    
    #...Otherwise is it fine
    return isConsistent

#Adds a cell and its value to the assginment
def assign(sudoku, cell, value, assignment):

    assignment[cell] = value

    if sudoku.possibilities:
        #Forward check based on the new assignment
        forwardCheck(sudoku, cell, value, assignment)

#Remove a supposed assignment
def unassign(sudoku, cell, assignment):

    #If the cell is in assignment
    if cell in assignment:

        #For each coordinate, value pair in the pruned set...
        for (coord, value) in sudoku.pruned[cell]:

            #Add it back to the possibilities
            sudoku.possibilities[coord].append(value)

        #And reset what we have pruned for that cell
        sudoku.pruned[cell] = []

        #And finally delete its assignment
        del assignment[cell]

#Remove conflicting values forward after a cell assignment
def forwardCheck(sudoku, cell, value, assignment):

    #For each neighboring cell
    for relatedCell in sudoku.relatedCells[cell]:

        #If the neighbor is not in the assignment
        if relatedCell not in assignment:

            #And if the value we just assigned to conflicts with this neighbor (e.g. its in the possibilities)
            if value in sudoku.possibilities[relatedCell]:

                #Remove the conflicting value fromthe possibilities
                sudoku.possibilities[relatedCell].remove(value)

                #And add the conflicting cell, value pair to pruned
                sudoku.pruned[cell].append((relatedCell, value))