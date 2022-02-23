import time

from colors import *

from ui.cell_grid import getTarget, searchPressed, getStart

def astar(grid, timeTick):
    searchPressed()
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""
    # Create start and end node
    start_node = getStart()
    start_node.position = (getStart().getX(), getStart().getY())
    start_node.parent = None
    start_node.g = start_node.h = start_node.f = 0
    end_node = getTarget()
    end_node.position = (getTarget().getX(), getTarget().getY())
    end_node.parent = None
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []
    parents = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:
        # Get the current node
        current_node = open_list[0]
        if len(open_list) > 1:
            open_list.pop(0)
        # print(current_node.position)
        current_index = 0
        open_list = list(dict.fromkeys(open_list))
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if (current_node.getX(), current_node.getY() + 1) == end_node.position:
            path = []
            current = current_node
            while current is not None:
                path.append((current.position[1], current.position[0]))
                current = current.parent
            path = path[::-1]
            # Removes extra path node occurring when prev. node has the same X value as the target X
            if path[-2][1] != end_node.position[0]:
                path.pop(-1)
            grid.drawPath(path) # Return reversed path
            return

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[1] > (len(grid.grid) - 1) or node_position[1] < 0 or node_position[0] > (len(grid.grid[len(grid.grid)-1]) -1) or node_position[0] < 0:
                continue

            # Make sure walkable terrain
            if grid.coords(node_position[1],node_position[0]).getType() == 3 or grid.coords(node_position[1],node_position[0]).getType() == 1 or grid.coords(node_position[1], node_position[0]).getType() == 2:
                continue

            # Create new node
            new_node = grid.coords(node_position[1], node_position[0])
            new_node.position = (node_position[0], node_position[1])
            # Ensures parents don't loop into each other
            if new_node.parent not in parents:
                new_node.parent = current_node
                parents.append(current_node)

            # Append
            children.append(new_node)
            new_node.draw()

        # Loop through children
        for child in children:
            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)
        time.sleep(timeTick)