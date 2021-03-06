from tkinter import *

target = None
start = None

targetSelected = False
startSelected = False
drawSelected = False
pressedSearch = False
shortestPath = False

def selectTarget():
    global targetSelected, startSelected, drawSelected, pressedSearch, shortestPath
    targetSelected = True
    startSelected = False
    drawSelected = False
    pressedSearch = False
    shortestPath = False

def selectStart():
    global targetSelected, startSelected, drawSelected, pressedSearch, shortestPath
    targetSelected = False
    startSelected = True
    drawSelected = False
    pressedSearch = False
    shortestPath = False

def selectDraw():
    global targetSelected, startSelected, drawSelected, pressedSearch, shortestPath
    targetSelected = False
    startSelected = False
    drawSelected = True
    pressedSearch = False
    shortestPath = False

def searchPressed():
    global targetSelected, startSelected, drawSelected, pressedSearch, shortestPath
    targetSelected = False
    startSelected = False
    drawSelected = False
    pressedSearch = True
    shortestPath = False

def shortestPathFill():
    global targetSelected, startSelected, drawSelected, pressedSearch, shortestPath
    targetSelected = False
    startSelected = False
    drawSelected = False
    pressedSearch = False
    shortestPath = True

def emptyFill():
    global targetSelected, startSelected, drawSelected, pressedSearch, shortestPath
    targetSelected = False
    startSelected = False
    drawSelected = False
    pressedSearch = False
    shortestPath = False

def getStart():
    global start
    return start

def getTarget():
    global target
    return target

class Cell():
    SEARCH_COLOR_BG = "#c68bf7"
    START_COLOR_BG = "#1f44ff"
    TARGET_COLOR_BG = "#f21b1b"
    FILLED_COLOR_BG = "#20b509"
    EMPTY_COLOR_BG = "white"
    EMPTY_COLOR_BORDER = "black"

    def __init__(self, master, x, y, size, parent=None, position=None):
        """ Constructor of the object called by Cell(...) """
        self.master = master
        self.abs = x
        self.ord = y
        self.size = size
        self.fill = False
        self.type = None
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0
    
    def getType(self):
        return self.type

    def getX(self):
        return self.abs

    def getY(self):
        return self.ord

    def getFill(self):
        return self.fill

    def _switch(self):
        """ Switch if the cell is filled or not. """
        self.fill= not self.fill
    
    def same_pos(self, other):
        return self.position == other.position

    def __hash__(self):               
        return hash(self.position)

    def draw(self):
        global targetSelected, startSelected, drawSelected, pressedSearch
        """ order to the cell to draw its representation on the canvas """
        if self.master != None :
            # Target Node
            if (targetSelected):
                self.type = 1
                fill = Cell.TARGET_COLOR_BG
                outline = Cell.EMPTY_COLOR_BORDER
            elif (startSelected):
                self.type = 2
                fill = Cell.START_COLOR_BG
                outline = Cell.EMPTY_COLOR_BORDER
            elif (drawSelected):
                self.type = 3
                fill = Cell.FILLED_COLOR_BG
                outline = Cell.EMPTY_COLOR_BORDER
            elif (pressedSearch):
                if not self.fill:
                    self._switch()
                self.type = 4
                fill = Cell.SEARCH_COLOR_BG
                outline = Cell.EMPTY_COLOR_BORDER
            elif (shortestPath):
                fill = "#fcba03"
                outline = Cell.EMPTY_COLOR_BORDER

            if not self.fill:
                fill = Cell.EMPTY_COLOR_BG
                outline = Cell.EMPTY_COLOR_BORDER
            
            if self.fill:
                self.master.switched.append(self)

            xmin = self.abs * self.size
            xmax = xmin + self.size
            ymin = self.ord * self.size
            ymax = ymin + self.size

            self.master.create_rectangle(xmin, ymin, xmax, ymax, fill = fill, outline = outline)
            self.master.update_idletasks()

class CellGrid(Canvas):

    def __init__(self, master, rowNumber, columnNumber, cellSize, *args, **kwargs):
        emptyFill()
        
        Canvas.__init__(self, master, width = cellSize * columnNumber , height = cellSize * rowNumber, *args, **kwargs)

        self.cellSize = cellSize

        self.grid = []
        for row in range(rowNumber):

            line = []
            for column in range(columnNumber):
                line.append(Cell(self, column, row, cellSize))

            self.grid.append(line)

        #memorize the cells that have been modified to avoid many switching of state during mouse motion.
        self.switched = []

        #bind click action
        self.bind("<Button-1>", self.handleMouseClick)  
        #bind moving while clicking
        self.bind("<B1-Motion>", self.handleMouseMotion)
        #bind release button action - clear the memory of midified cells.
        # self.bind("<ButtonRelease-1>", lambda event: self.switched.clear())
        
        self.draw()


    def draw(self):
        for row in self.grid:
            for cell in row:
                cell.draw()

    def drawPath(self, path):
        shortestPathFill()
        for coord in path:
            cell = self.coords(coord[0], coord[1])
            if cell == start:
                continue
            if cell == target:
                break
            cell.draw()

    def clear(self):
        global start, target
        for cell in self.switched:
            if cell:
                cell.fill = False
                cell.type = 0
                cell.draw()
        self.switched.clear()
        start = None
        target = None

    def _eventCoords(self, event):
        row = int(event.y / self.cellSize)
        column = int(event.x / self.cellSize)
        return row, column

    def coords(self, row, column):
        return self.grid[row][column]

    # Helper function to ensure single start/target cell
    def singleCell(self, cell):
        cell._switch()
        cell.draw()

    def handleMouseClick(self, event):
        global target, start, targetSelected, startSelected
        row, column = self._eventCoords(event)
        if targetSelected or startSelected:
            if target and targetSelected:
                self.singleCell(target)
            elif start and startSelected:
                self.singleCell(start)
        cell = self.grid[row][column]
        cell._switch()
        cell.draw()
        if targetSelected:
            target = cell
        elif startSelected:
            start = cell
        # add the cell to the list of cell switched during the click
        self.switched.append(cell)

    def handleMouseMotion(self, event):
        if not (targetSelected or startSelected):
            row, column = self._eventCoords(event)
            if row <= 39 and column <= 79:
                cell = self.grid[row][column]
                if cell not in self.switched:
                    cell._switch()
                    cell.draw()
                    self.switched.append(cell)
    