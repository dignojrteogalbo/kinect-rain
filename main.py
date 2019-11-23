import random, time, threading, freenect, numpy
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

refreshRate = 16 # per ms to move rain
resolution = 15 # amount of columns and rows
rainWidth = 1
rainAmount = 100
rainLength = 15
gravity = 0.5

threshold = 150 # number between 0-255

drops = []
dropsFallSpeed = []
graph = []
activePlots = []

def draw_graph(): # initialize grid
    global depth
    global d3

    depth,_ = freenect.sync_get_depth() # get frame from kinect
    d3 = numpy.dstack((depth, depth, depth)).astype(numpy.uint8) # stack data of frames into multidimensional array organized like (y, x, depth)

    for col in range(resolution):
        for row in range(resolution):
            box = c.create_rectangle((screen_width/resolution)*row, (screen_height/resolution)*col, (screen_width/resolution)*(row+1), (screen_height/resolution)*(col+1), fill='', outline='black')
            x1 = c.coords(box)[0]
            x2 = c.coords(box)[2]
            y1 = c.coords(box)[1]
            y2 = c.coords(box)[3]
            label = c.create_text(((x1+x2)/2, (y1+y2)/2), text=d3[int((y1+y2)/2)][int((x1+x2)/2)][0])
            graph.append([x1, x2, y1, y2, box, label])

def draw_drops(): #function to create a raindrop
    randomPositionX = random.randint(0, screen_width)
    randomPositionY = random.randint(-screen_height-rainLength*5, 0)
    rainDrop = c.create_line(randomPositionX, randomPositionY, randomPositionX, randomPositionY+rainLength, fill='red', width=rainWidth)
    drops.append(rainDrop)
    dropsFallSpeed.append(1)

for i in range(rainAmount): #draws raindrops
    draw_drops()

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

        for plot in range(len(activePlots)):
            if c.coords(activePlots[plot])[0] <= x1 <= c.coords(activePlots[plot])[2] and c.coords(activePlots[plot])[1] <= y2 <= c.coords(activePlots[plot])[3] and c.itemcget(activePlots[plot], 'fill') != '':
                dropsFallSpeed[drop] = rainSpeed
                c.coords(rainDropObj, x1, randomPositionY, x2, randomPositionY+rainLength) #return raindrop to the top

        if y1 > screen_height+rainLength: #if y2 coord of raindrop is outside of visible canvas
            dropsFallSpeed[drop] = rainSpeed
            c.coords(rainDropObj, x1, randomPositionY, x2, randomPositionY+rainLength) #return raindrop to the top
        else: #move the raindrop fallspeed downward
            c.move(rainDropObj, 0, dropsFallSpeed[drop])

    for speed in range(len(dropsFallSpeed)): #adds factor of gravity to fallspeed
        dropsFallSpeed[speed] += gravity

    for b in range(len(graph)): #update text and color or boxes and labels according to the data from the kinect
        c.itemconfig(graph[b][5], text=d3[int(c.coords(graph[b][5])[1])][int(c.coords(graph[b][5])[0])][0])
        if int(c.itemcget(graph[b][5], 'text')) >= threshold:
            c.itemconfig(graph[b][4], fill='')
        else:
            c.itemconfig(graph[b][4], fill='green')

    main.after(refreshRate, move_drops) #loops move_drops

c.pack()
draw_graph() # init graph
main.after(refreshRate, move_drops) #loops move_drops
main.mainloop()
