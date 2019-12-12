import random, numpy, freenect
try:
    from tkinter import *
    import tkinter as tk
except ImportError:
    from Tkinter import *
    import Tkinter as tk

main = tk.Tk()
screen_width = 480  #main.winfo_screenwidth() to make fullscreen
screen_height = 480 #main.winfo_screenheight()
c = Canvas(main, bg='blue', width=screen_width, height=screen_height)

refreshRate = 16 # per ms to movInt
resolution = tk.StringVar() # amount of columns and rows
rainWidth = tk.StringVar()
rainAmount = tk.StringVar()
rainLength = tk.StringVar()
gravity = tk.StringVar()

resL = tk.Label(main, text='Resolution')
resolutionEntry = tk.Entry(main, textvariable=resolution)
resolutionEntry.insert(END, '10')

rAmtL = tk.Label(main, text='Rain Amount')
rainAmountEntry = tk.Entry(main, textvariable=rainAmount)
rainAmountEntry.insert(END, '100')

rWidL = tk.Label(main, text='Rain Width')
rainWidthEntry = tk.Entry(main, textvariable=rainWidth)
rainWidthEntry.insert(END, '5')

rLenL = tk.Label(main, text='Rain Length')
rainLengthEntry = tk.Entry(main, textvariable=rainLength)
rainLengthEntry.insert(END, '10')

gravL = tk.Label(main, text='Gravity')
gravityEntry = tk.Entry(main, textvariable=gravity)
gravityEntry.insert(END, '0.5')

threshold = 150 # number between 0-255

boxOutline = '' # set to 'black' or '' to show or hide box outlines
textColor = '' # set to 'black' or '' to show or hide depth values

drops = []
dropsFallSpeed = []
graph = []
activePlots = []

resolution = int(resolutionEntry.get())
rainWidth = int(rainWidthEntry.get())
rainAmount = int(rainAmountEntry.get())
rainLength = int(rainLengthEntry.get())
gravity = float(gravityEntry.get())

def retrieve_input(event):
    global resolution, rainWidth, rainAmount, rainLength, gravity, drops, dropsFallSpeed, graph
    resolution = int(resolutionEntry.get())
    rainWidth = int(rainWidthEntry.get())
    rainAmount = int(rainAmountEntry.get())
    rainLength = int(rainLengthEntry.get())
    gravity = float(gravityEntry.get())
    drops = []
    dropsFallSpeed = []
    graph = []
    c.delete('all')
    draw_graph()

def draw_drops(): #function to create a raindrop
    randomPositionX = random.randint(0, screen_width)
    randomPositionY = random.randint(-screen_height-rainLength*5, 0)
    rainDrop = c.create_line(randomPositionX, randomPositionY, randomPositionX, randomPositionY+rainLength, fill='red', width=rainWidth)
    drops.append(rainDrop)
    dropsFallSpeed.append(1)

def draw_graph(): # initialize grid
    global depth, d3

    depth,_ = freenect.sync_get_depth() # get frame from kinect
    d3 = numpy.dstack((depth, depth, depth)).astype(numpy.uint8) # stack data of frames into multidimensional array organized like (y, x, depth)

    for i in range(rainAmount): #draws raindrops
        draw_drops()

    for col in range(resolution):
        for row in range(resolution):
            box = c.create_rectangle((screen_width/resolution)*row, (screen_height/resolution)*col, (screen_width/resolution)*(row+1), (screen_height/resolution)*(col+1), fill='', outline=boxOutline)
            x1 = c.coords(box)[0]
            x2 = c.coords(box)[2]
            y1 = c.coords(box)[1]
            y2 = c.coords(box)[3]
            label = c.create_text(((x1+x2)/2, (y1+y2)/2), fill=textColor) # text=d3[int((y1+y2)/2)][int((x1+x2)/2)][0], fill=textColor)
            graph.append([x1, x2, y1, y2, box, label])

def move_drops():
    depth,_ = freenect.sync_get_depth() # get new frame from kinect
    d3 = numpy.dstack((depth, depth, depth)).astype(numpy.uint8)

    for drop in range(len(drops)):
        rainSpeed = random.randint(1, 10)
        randomPositionY = random.randint(-screen_height-rainLength*5, 0)

        x1 = c.coords(drops[drop])[0] # establish coordinates for each raindrop
        y1 = c.coords(drops[drop])[1]
        x2 = c.coords(drops[drop])[2]
        y2 = c.coords(drops[drop])[3]
        rainDropObj = drops[drop]

        for b in range(len(graph)):
            if graph[b][0] <= x1 <= graph[b][1] and graph[b][2] <= y2 <= graph[b][3] and c.itemcget(graph[b][4], 'fill') != '':
                dropsFallSpeed[drop] = rainSpeed
                c.coords(rainDropObj, x1, randomPositionY, x2, randomPositionY+rainLength) #return raindrop to the top

        if y1 > screen_height+rainLength: #if y2 coord of raindrop is outside of visible canvas
            dropsFallSpeed[drop] = rainSpeed
            c.coords(rainDropObj, x1, randomPositionY, x2, randomPositionY+rainLength) #return raindrop to the top
        else: #move the raindrop fallspeed downward
            c.move(rainDropObj, 0, dropsFallSpeed[drop])

    for speed in range(len(dropsFallSpeed)): #adds factor of gravity to fallspeed
        dropsFallSpeed[speed] += gravity

    for b in range(len(graph)):
        c.itemconfig(graph[b][5], text=d3[int(c.coords(graph[b][5])[1])][int(c.coords(graph[b][5])[0])][0]) # d3[int(c.coords(graph[b][5])[1])][int(c.coords(graph[b][5])[0])][0]
        if int(c.itemcget(graph[b][5], 'text')) <= threshold:
            c.itemconfig(graph[b][4], fill='green')
            activePlots.append(graph[b][4])
        else:
            if graph[b][4] in activePlots:
                c.itemconfig(graph[b][4], fill='')
                activePlots.remove(graph[b][4])

    main.after(refreshRate, move_drops) #loops move_drops

c.grid(row=0, rowspan=5, column=0)

resL.grid(row=0, column=2)
rWidL.grid(row=1, column=2)
rAmtL.grid(row=2, column=2)
rLenL.grid(row=3, column=2)
gravL.grid(row=4, column=2)

resolutionEntry.grid(row=0, column=3)
rainWidthEntry.grid(row=1, column=3)
rainAmountEntry.grid(row=2, column=3)
rainLengthEntry.grid(row=3, column=3)
gravityEntry.grid(row=4, column=3)

draw_graph() # init graph
main.bind('<Return>', retrieve_input)
main.after(refreshRate, move_drops) #loops move_drops
main.mainloop()
