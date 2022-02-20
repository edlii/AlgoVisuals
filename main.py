from algorithms.BubbleSort import bubble_sort
from algorithms.DFS import depth_first_search
from algorithms.MergeSort import merge_sort
from algorithms.InsertionSort import insertion_sort
from algorithms.SelectionSort import selection_sort
from algorithms.QuickSort import quick_sort
from algorithms.BFS import breadth_first_search

from tkinter import *
from tkinter import ttk
from ui.tkinter_custom_button import TkinterCustomButton
from ui.cell_grid import CellGrid, selectDraw, selectStart, selectTarget, getStart, emptyFill

# Allows for random values
import random
from colors import *

main_window = Tk()
main_window.title("Algorithm Visualizer")
main_window.maxsize(1000, 700)
main_window.config(bg=WHITE)

algorithm_name = StringVar()
sort_algorithm_list = ['Merge Sort', 'Selection Sort', 'Insertion Sort', 'Bubble Sort', 'Quick Sort']
pathfinding_algo_list = ['Breadth First Search', 'Depth First Search']
algo_list = sort_algorithm_list + pathfinding_algo_list

speed_name = StringVar()
speed_list = ["Fast", "Medium", "Slow"]

data = []
grid = None


def renderData(data, color):
    global grid
    global canvas
    global b3, b4, b5
    canvas.delete("all")
    canvas_width = 800
    canvas_height = 400
    if (algo_menu.get() in sort_algorithm_list):
        b1.set_text("Sort!")
        setVisibleDrawMode(False)
        if grid:
            grid.delete("all")
            grid = None
            canvas = Canvas(main_window, width=800, height=400, bg=WHITE)
            canvas.grid(row=1, column=0, padx=10, pady=10)
        x_width = canvas_width / (len(data) + 1)
        offset = 4
        spacing = 1
        normalizedData = [i / max(data) for i in data]

        for i, height in enumerate(normalizedData):
            x0 = i * x_width + offset + spacing
            y0 = canvas_height - height * 390
            x1 = (i + 1) * x_width + offset
            y1 = canvas_height
            canvas.create_rectangle(x0, y0, x1, y1, fill=color[i])
    else:
        b1.set_text("Search!")
        setVisibleDrawMode(True)
        if not grid:
            grid = CellGrid(canvas, int(canvas_height/10), int(canvas_width/10), 10)
            grid.pack()
        else:
            selectDraw()
            for i in range(150):
                x = random.randint(1, 39)
                y = random.randint(1, 79)
                if grid.coords(x,y) not in grid.switched:
                    grid.coords(x, y)._switch()
                    grid.switched.append(grid.coords(x,y)) 
                    grid.coords(x, y).draw()
    main_window.update_idletasks()


def randomize():
    global data 
    data = []
    for i in range(0, 150):
        random_value = random.randint(1, 100)
        data.append(random_value)
    
    renderData(data, [BLUE for x in range(len(data))])

def set_speed():
    if speed_menu.get() == 'Slow':
        return 0.3
    elif speed_menu.get() == 'Medium':
        return 0.1
    else:
        return 0.001

def sort():
    global data, grid
    timeTick = set_speed()
    canvas_width = 800
    canvas_height = 400

    if algo_menu.get() == "Bubble Sort":
        bubble_sort(data, renderData, timeTick)
    elif algo_menu.get() == "Merge Sort":
        merge_sort(data, 0, len(data)-1, renderData, timeTick)
    elif algo_menu.get() == "Insertion Sort":
        insertion_sort(data, renderData, timeTick)
    elif algo_menu.get() == "Selection Sort":
        selection_sort(data, renderData, timeTick)
    elif algo_menu.get() == "Quick Sort":
        quick_sort(data, 0, len(data)-1, renderData, timeTick)
    elif algo_menu.get() == "Breadth First Search":
        vis = [[ False for i in range(int(canvas_width/10))] for i in range(int(canvas_height/10))]
        x = getStart().getX()
        y = getStart().getY()
        breadth_first_search(grid, vis, y, x, timeTick)
    elif algo_menu.get() == "Depth First Search":
        vis = [[ False for i in range(int(canvas_width/10))] for i in range(int(canvas_height/10))]
        x = getStart().getX()
        y = getStart().getY()
        depth_first_search(grid, vis, y, x, timeTick)

def setVisibleDrawMode(on):
    global b3, b4, b5
    if on:
        b3.place(x = 0, y = 0)
        b4.place(x = 0, y = 25)
        b5.place(x = 0, y = 50)
    else:
        b3.place(x = -200)
        b4.place(x = -200)
        b5.place(x = -200)

def getCurrentDrawMode():
    return draw_mode.get()

######## UI ##########
UI_frame = Frame(main_window, width=900, height=300, bg=WHITE)
UI_frame.grid(row=0, column=0, padx=10, pady=5)

# Dropdown to Select Algorithm
l1 = Label(UI_frame, text="Algorithm: ", bg=WHITE, fg=BLACK)
l1.grid(row=0, column=0, padx=10, pady=5, sticky=W)
algo_menu = ttk.Combobox(UI_frame, textvariable=algorithm_name, values=algo_list)
algo_menu.grid(row=0, column=1, padx=5, pady=5)
algo_menu.current(0)

# Dropdown to Change Speed
l2 = Label(UI_frame, text="Speed: ", bg=WHITE, fg=BLACK)
l2.grid(row=1, column=0, padx=10, pady=5, sticky=W)
speed_menu = ttk.Combobox(UI_frame, textvariable=speed_name, values=speed_list) 
speed_menu.grid(row=1, column=1, padx=5, pady=5)
speed_menu.current(0)

# Randomize button
b2 = TkinterCustomButton(master=UI_frame, text="Randomize!", corner_radius=10, command=randomize)
b2.grid(row=2, column=0, padx=10, pady=10)

# Sort Button
b1 = TkinterCustomButton(master=UI_frame, text="Sort!", corner_radius=10, command=sort)
b1.grid(row=2, column=1, padx=10, pady=10)

# Current drawing mode
draw_mode = IntVar()
draw_mode.set(1)

# Toggle target button
b3 = Radiobutton(text="Target Node", bg=WHITE, fg=BLACK, value=1, variable=draw_mode, command=selectTarget)
b3.place(x = -200, y = 0)

# Toggle start button
b4 = Radiobutton(text="Starting Node", bg=WHITE, fg=BLACK, value=2, variable=draw_mode, command=selectStart)
b4.place(x = -200, y = 25)

# Toggle draw button
b5 = Radiobutton(text="Draw", bg=WHITE, fg=BLACK, value=3, variable=draw_mode, command=selectDraw)
b5.place(x = -200, y = 50)

# Canvas to render array
canvas = Canvas(main_window, width=800, height=400, bg=WHITE)
canvas.grid(row=1, column=0, padx=5, pady=10)


main_window.mainloop()

