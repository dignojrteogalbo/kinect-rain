import random, time, threading

try:
    from tkinter import *
    import tkinter as tk
except ImportError:
    from Tkinter import *
    import Tkinter as tk

main = tk.Tk()
screen_width = 500  #main.winfo_screenwidth() to make fullscreen
screen_height = 500 #main.winfo_screenheight()
c = Canvas(main, bg='blue', width=screen_width, height=screen_height)

refreshRate = 16
resolution = 5
rainWidth = 1
rainAmount = 500
rainLength = 15
gravity = 0.5
drops = []
dropsFallSpeed = []
graph = []

def draw_drops(): #function to create a raindrop
    randomPositionX = random.randint(0, screen_width)
    randomPositionY = random.randint(-screen_height-rainLength*5, 0)
    rainDrop = c.create_line(randomPositionX, randomPositionY, randomPositionX, randomPositionY+rainLength, fill='red', width=rainWidth)
    drops.append(rainDrop)
    dropsFallSpeed.append(1)

for i in range(rainAmount): #draws raindrops
    draw_drops()

def move_drops():
    for drop in range(len(drops)):
        rainSpeed = random.randint(1, 10)
        randomPositionY = random.randint(-screen_height-rainLength*5, 0)

        x1 = c.coords(drops[drop])[0] #establish coordinates for each raindrop
        y1 = c.coords(drops[drop])[1]
        x2 = c.coords(drops[drop])[2]
        y2 = c.coords(drops[drop])[3]
        rainDropObj = drops[drop]

        for obj in range(len(graph)):
            if graph[obj][0] <= x1 <= graph[obj][2] and graph[obj][1] <= y2 <= graph[obj][3] and c.itemcget(graph[obj][4], 'fill') != '':
                dropsFallSpeed[drop] = rainSpeed
                c.coords(rainDropObj, x1, randomPositionY, x2, randomPositionY+rainLength) #return raindrop to the top

        if y1 > screen_height+rainLength: #if y2 coord of raindrop is outside of visible canvas
            dropsFallSpeed[drop] = rainSpeed
            c.coords(rainDropObj, x1, randomPositionY, x2, randomPositionY+rainLength) #return raindrop to the top
        else: #move the raindrop fallspeed downward
            c.move(rainDropObj, 0, dropsFallSpeed[drop])

    for speed in range(len(dropsFallSpeed)): #adds factor of gravity to fallspeed
        dropsFallSpeed[speed] += gravity

    main.after(refreshRate, move_drops) #loops move_drops

def draw_graph():
    for row in range(resolution):
        box = c.create_rectangle((screen_width/resolution)*row, 0, (screen_width/resolution)*(row+1), screen_height/resolution, fill='', outline='black')
        graph.append([c.coords(box)[0], c.coords(box)[1], c.coords(box)[2], c.coords(box)[3], box])
        for col in range(resolution):
            box = c.create_rectangle((screen_width/resolution)*row, (screen_height/resolution)*(col), (screen_width/resolution)*(row+1), (screen_height/resolution)*(col+1), fill='', outline='black')
            graph.append([c.coords(box)[0], c.coords(box)[1], c.coords(box)[2], c.coords(box)[3], box])

def movement(event):
    for obj in range(len(graph)):
        if graph[obj][0] <= event.x <= graph[obj][2] and graph[obj][1] <= event.y <= graph[obj][3]:
            c.itemconfig(graph[obj][4], fill='green')
        else:
            c.itemconfig(graph[obj][4], fill='')

def left_callback(self): #functions to move box
    c.move(box, -5, 0)
def right_callback(self):
    c.move(box, 5, 0)
def up_callback(self):
    c.move(box, 0, -5)
def down_callback(self):
    c.move(box, 0, 5)

#print(drops)

main.bind("<Motion>", movement)
main.bind('<Left>', left_callback) #bind functions to key presses
main.bind('<Right>', right_callback)
main.bind('<Up>', up_callback)
main.bind('<Down>', down_callback)

c.pack()
draw_graph()
main.after(refreshRate, move_drops) #loops move_drops
main.mainloop()
