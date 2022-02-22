import time

from colors import *

from ui.cell_grid import getTarget, searchPressed, getStart

def astar(grid, timeTick):
    searchPressed()
    start_cell = getStart()
    start_cell.position = (start_cell.getX(), start_cell.getY())
    start_cell.parent = None
    start_cell.g = start_cell.h = start_cell.f = 0
    end_cell = getTarget()
    end_cell.position = (end_cell.getX(), end_cell.getY())
    end_cell.parent = None

    # Initialize open and closed list
    open_list = []
    closed_list = []

    # Append starting node
    open_list.append(start_cell)

    while len(open_list) > 0:
        current_cell = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_cell.f:
                current_cell = item
                current_index = index

        open_list.pop(current_index)
        closed_list.append(current_cell)

        if current_cell == end_cell:
            path = []
            current = current_cell
            while current is not None:
                path.append(current.position)
                current = current.parent
            grid.drawPath(path[::-1])
            return

        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            cell_position = (current_cell.position[0] + new_position[0], current_cell.position[1] + new_position[1])
        
            if cell_position[0] > (len(grid.grid) - 1) or cell_position[0] < 0 or cell_position[1] > (len(grid.grid[len(grid.grid)-1]) -1) or cell_position[1] < 0:
                continue

            if grid.coords(cell_position[0], cell_position[1]).getType() == 3:
                continue

            new_cell = grid.coords(cell_position[0], cell_position[1])
            new_cell.position = (cell_position[0], cell_position[1])
            new_cell.parent = current_cell

            if current_cell.parent != None:
                while new_cell == current_cell.parent:
                    if current_cell.parent != None or new_cell != None:
                        break
                    continue

            children.append(new_cell)
            new_cell.draw()

        
        for child in children:
            for closed_child in closed_list:
                if child == closed_child:
                    continue
            children = list(dict.fromkeys(children))
            print("At: " + "("+ str(child.getX()) + ", " + str(child.getY()) + ")")
            
            child.g = current_cell.g + 1
            child.h = ((child.position[0] - end_cell.position[0]) ** 2) + ((child.position[1] - end_cell.position[1]) ** 2)
            child.f = child.g + child.h

            for open_cell in open_list:
                if child == open_cell and child.g > open_cell.g:
                    continue

            open_list.append(child)
        time.sleep(timeTick)