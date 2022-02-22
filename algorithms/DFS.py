import time

from colors import *
from collections import deque as queue

from ui.cell_grid import getTarget, searchPressed

# Directional vectors
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

def depth_first_search(grid, vis, row, col, tickTime):
    searchPressed()

    # Stack variable
    st = [[]]
    st.append([(row, col)])

    while len(st) > 0:
        firstPath = st[-1]
        st.remove(st[-1])
        x, y = firstPath[-1]

        vis[x][y] = True
        if foundTarget(vis, getTarget()):
            grid.drawPath(firstPath)
            return

        # Skip barricade cells
        if grid.coords(x, y).getType() == 3:
            continue

        # # Target found
        # if foundTarget(vis, getTarget()):
        #     break
        # Colour in non-start cells
        if grid.coords(x, y).getType() != 2:
            newCell = grid.coords(x, y)
            newCell._switch()
            newCell.draw()
            grid.switched.append(newCell)

        # Push all the adjacent cells
        for i in range(4):
            adjx = x + dRow[i]
            adjy = y + dCol[i]
            if (isValid(vis, adjx, adjy)):
                st.append(firstPath + [(adjx, adjy)])
        time.sleep(tickTime)
