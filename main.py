from algorithms.BubbleSort import bubble_sort
from algorithms.MergeSort import merge_sort
from algorithms.InsertionSort import insertion_sort

from tkinter import *
from tkinter import ttk

# Allows for random values
import random
from colors import *

main_window = Tk()
main_window.title("Algorithm Visualizer")
main_window.maxsize(1000, 700)
main_window.config(bg=WHITE)

algorithm_name = StringVar()
algorithm_list = ['Merge Sort', 'Selection Sort', 'Insertion Sort', 'Bubble Sort']

speed_name = StringVar()
speed_list = ["Fast", "Medium", "Slow"]

data = []

def renderData(data, color):
    canvas.delete("all")
    canvas_width = 800
    canvas_height = 400
    x_width = canvas_width / (len(data) + 1)
    offset = 4
    spacing = 2
    normalizedData = [i / max(data) for i in data]

    for i, height in enumerate(normalizedData):
        x0 = i * x_width + offset + spacing
        y0 = canvas_height - height * 390
        x1 = (i + 1) * x_width + offset
        y1 = canvas_height
        canvas.create_rectangle(x0, y0, x1, y1, fill=color[i])

    main_window.update_idletasks()

def randomize():
    global data 
    data = []
    for i in range(0, 100):
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
    global data
    timeTick = set_speed()

    if algo_menu.get() == "Bubble Sort":
        bubble_sort(data, renderData, timeTick)
    elif algo_menu.get() == "Merge Sort":
        merge_sort(data, 0, len(data)-1, renderData, timeTick)
    elif algo_menu.get() == "Insertion Sort":
        insertion_sort(data, renderData, timeTick)
        


######## UI ##########
UI_frame = Frame(main_window, width=900, height=300, bg=WHITE)
UI_frame.grid(row=0, column=0, padx=10, pady=5)

# Dropdown to Select Algorithm
l1 = Label(UI_frame, text="Algorithm: ", bg=WHITE, fg=BLACK)
l1.grid(row=0, column=0, padx=10, pady=5, sticky=W)
algo_menu = ttk.Combobox(UI_frame, textvariable=algorithm_name, values=algorithm_list)
algo_menu.grid(row=0, column=1, padx=5, pady=5)
algo_menu.current(0)

# Dropdown to Change Speed
l2 = Label(UI_frame, text="Speed: ", bg=WHITE, fg=BLACK)
l2.grid(row=1, column=0, padx=10, pady=5, sticky=W)
speed_menu = ttk.Combobox(UI_frame, textvariable=speed_name, values=speed_list) 
speed_menu.grid(row=1, column=1, padx=5, pady=5)
speed_menu.current(0)

# Sort Button
b1 = Button(UI_frame, text="Sort!", command=sort, bg=LIGHT_GRAY)
b1.grid(row=2, column=1, padx=5, pady=5)

# Randomize button
b2 = Button(UI_frame, text="Randomize!", command=randomize, bg=LIGHT_GRAY)
b2.grid(row=2, column=0, padx=5, pady=5)

# Canvas to render array
canvas = Canvas(main_window, width=800, height=400, bg=WHITE)
canvas.grid(row=1, column=0, padx=10, pady=5)


main_window.mainloop()

