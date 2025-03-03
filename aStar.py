

def isvalid(cell, grid):
    if cell[0] >= 0 and cell[0] < len(grid):
        if cell[1] >= 0 and cell[1] < len(grid[0]):
            return True
    return False

def unblocked(cell, grid):
    if grid[cell[0]][cell[1]] == 1:
        return False
    return True

def isDestination(cell, end):
    if cell[0] == end[0] and cell[1] == end[1]:
        return True
    return False

def calculateHValue(cell, end):
    return abs(cell[0] - end[0]) + abs(cell[1] - end[1])

def tracePath(cellDetails, end):
    print("The Path is: ")
    row = end[0]
    col = end[1]

    Path = []
    while not (cellDetails[row][col]["parent_i"] == row and cellDetails[row][col]["parent_j"] == col):
        Path.append([row, col])
        temp_row = cellDetails[row][col]["parent_i"]
        temp_col = cellDetails[row][col]["parent_j"]
        row = temp_row
        col = temp_col

    Path.append([row, col])
    Path.reverse()
    
    return Path[1]

def aStarSearch(grid, start , end):
    if not isvalid(start, grid):
        print("Start is invalid")
        return start
    
    if not isvalid(end, grid):
        print("End is invalid")
        return start
    
    if not unblocked(end, grid):
        print("End is blocked")
        return start
    
    if start == end:
        print("Start and End are same")
        return start
    
    # Initialize the closed list
    closedList = [[False for i in range(len(grid[0]))] for j in range(len(grid))]

    cellDetails = [[{} for i in range(len(grid[0]))] for j in range(len(grid))]
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            cellDetails[i][j]["f"] = float('inf')
            cellDetails[i][j]["g"] = float('inf')
            cellDetails[i][j]["h"] = float('inf')
            cellDetails[i][j]["parent_i"] = -1
            cellDetails[i][j]["parent_j"] = -1

    i = int(start[0])
    j = int(start[1])
    cellDetails[i][j]["f"] = 0.0
    cellDetails[i][j]["g"] = 0.0
    cellDetails[i][j]["h"] = 0.0
    cellDetails[i][j]["parent_i"] = i
    cellDetails[i][j]["parent_j"] = j

    openList = [[0.0, i, j]]

    foundDest = False

    while len(openList) > 0:
        p = openList.pop(0)
        i = p[1]
        j = p[2]
        closedList[i][j] = True

        sNew = [[-1, 0], [0, -1], [1, 0], [0, 1]]
        for k in range(len(sNew)):
            iNew = i + sNew[k][0]
            jNew = j + sNew[k][1]
            if isvalid([iNew, jNew], grid):
                
                if isDestination([iNew, jNew], end):
                    cellDetails[iNew][jNew]["parent_i"] = i
                    cellDetails[iNew][jNew]["parent_j"] = j
                    print("The destination cell is found")
                    foundDest = True
                    return tracePath(cellDetails, end)
                
                elif closedList[iNew][jNew] == False and unblocked([iNew, jNew], grid):
                    
                    gNew = cellDetails[i][j]["g"] + 1.0
                    hNew = calculateHValue([iNew, jNew], end)
                    fNew = gNew + hNew
                    if cellDetails[iNew][jNew]["f"] == float('inf') or cellDetails[iNew][jNew]["f"] > fNew:
                        openList.append([fNew, iNew, jNew])
                        cellDetails[iNew][jNew]["f"] = fNew
                        cellDetails[iNew][jNew]["g"] = gNew
                        cellDetails[iNew][jNew]["h"] = hNew
                        cellDetails[iNew][jNew]["parent_i"] = i
                        cellDetails[iNew][jNew]["parent_j"] = j

    if foundDest == False:
        print("Failed to find the destination cell")
    return start
    



