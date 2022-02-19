from Utility import isDifferent

def AC3(csp, queue=None):

    if queue == None:
        queue = list(csp.binaryConstraints)

    while queue:

        (xi, xj) = queue.pop(0)

        if removeInconsistentValues(csp, xi, xj):

            #If a cell has 0 possibilities the Sudoku is unsolvable
            if len(csp.possibilities[xi]) == 0:
                return False
            
            for Xk in csp.relatedCells[xi]:
                if Xk != xi:
                    queue.append((Xk, xi))
                    
    return True

#Removes inconsistent values and returns true if a value is removed
def removeInconsistentValues(csp, cell_i, cell_j):

    removed = False

    #For every value that is remaining for a cell...
    for value in csp.possibilities[cell_i]:

        #...If that value causes a conflict with its neighbors...
        if not any([isDifferent(value, poss) for poss in csp.possibilities[cell_j]]):
            
            #...Them remove that value as a possibility
            csp.possibilities[cell_i].remove(value)
            removed = True

    #Returns true if we removed a value, false otherwise
    return removed
