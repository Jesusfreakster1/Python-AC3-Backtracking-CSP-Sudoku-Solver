from Utility import selectMostConstrainedVariable, orderDomainValues, isConsistent, assign, unassign

#Supposes assignments, and then backtracks and tries again through the possibilities
#Uses recursion to test all possibilities until a solution is found or all possibilities have been tried and none exists
def backtrackRecursion(assignment, sudoku):

    #If the assignment is the same size as the sudoku, we know we have solved it and can return the result
    if len(assignment) == len(sudoku.cells):
        return assignment

    #Decide what variable to work with (MRV)
    cell = selectMostConstrainedVariable(assignment, sudoku)

    #Pick an assignement that causes the least conflicts...
    for value in orderDomainValues(sudoku, cell):

        #...If there are no conflicts with this assignment, then...
        if isConsistent(sudoku, assignment, cell, value):

            #...Add this assignment supposition to our proposed solution...
            assign(sudoku, cell, value, assignment)

            #...and keep going to until we find a solution.
            result = backtrackRecursion(assignment, sudoku)

            #...If continuing forward finds a solution, we return the assignment of that solution
            if result:
                return result

            #...If we find the current assignment does conflict with something, we undo it and try to pick another
            unassign(sudoku, cell, assignment)
   
    #If we made it here, that means we...
    #-went through all possible values for the curent cell
    #-continued through the algorithm to the end of all the possibilities of every cell from then on by calling recursively
    #-and STILL coulnd't find a solution, therefore it doesn't exist, so return failure
    return False