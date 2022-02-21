import time

from colors import *
from collections import deque

from ui.cell_grid import getTarget, searchPressed

# Direction vectors
dRow = [ -1, 0, 1, 0]
dCol = [ 0, 1, 0, -1]

def isValid(vis, row, col):
   
    # If cell lies out of bounds
    if (row < 0 or col < 0 or row >= 40 or col >= 80):
        return False
    if (vis[row][col]):
        return False
    return True

def foundTarget(vis, target):
    targetX = target.getX()
    targetY = target.getY()
    return vis[targetY][targetX]

def breadth_first_search(grid, vis, row, col, tickTime):
    searchPressed()
    q = deque([[(row, col)]])
    vis[row][col] = True

    while len(q) > 0:
        path = q.popleft()
        # Target found
        x, y = path[-1]
        # Skip barricade cells
        if grid.coords(x, y).getType() == 3:
            continue
        # Colour in non-start cells
        if grid.coords(x, y).getType() != 2:
            newCell = grid.coords(x, y)
            newCell._switch()
            newCell.draw()
            grid.switched.append(newCell)
        for i in range(4):
            adjx = x + dRow[i]
            adjy = y + dCol[i]
            if (isValid(vis, adjx, adjy)):
                q.append(path + [(adjx, adjy)])
                vis[adjx][adjy] = True
                # Target found
                if foundTarget(vis, getTarget()):
                    grid.drawPath(path)
                    return
        time.sleep(tickTime)

