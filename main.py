import random, time, threading

try:
    from tkinter import *
    import tkinter as tk
except ImportError:
    from Tkinter import *
    import Tkinter as tk

main = tk.Tk()
c = Canvas(main, bg='blue', width=500, height=500)

rainLength = 15
gravity = 10
drops = []

def draw_drops(): #function to create a raindrop
    randomPositionX = random.randint(0, 500)
    randomPositionY = random.randint(-500, 0)
    rainDrop = c.create_line(randomPositionX, randomPositionY, randomPositionX, randomPositionY+rainLength, fill='red')
    drops.append(rainDrop)

def move_drops():
    for drop in drops:
        x1 = c.coords(drops[drop-1])[0]
        y1 = c.coords(drops[drop-1])[1]
        x2 = c.coords(drops[drop-1])[2]
        y2 = c.coords(drops[drop-1])[3]

        fallSpeed = random.randint(1, 5)
        if y2 > 515: #if y2 coord of raindrop is outside of visible canvas
            c.move(drops[drop-1], 0, -515) #move raindrop to the top
        elif x1 > c.coords(box)[0] and x2 < c.coords(box)[2] and y1 > c.coords(box)[1] and y2 < c.coords(box)[3]: #if x1, x2, y1, and y2 coords are within object
            c.move(drops[drop-1], 0, -515) #return raindrop to the top
        else: #move the raindrop fallspeed downward
            c.move(drops[drop-1], 0, fallSpeed)
    main.after(1, move_drops) #loops move_drops

for i in range(500): #draws raindrops
    draw_drops()

box = c.create_rectangle(125, 125, 250, 250, fill='green') #draws box

def left_callback(self): #functions to move box
    c.move(box, -5, 0)
def right_callback(self):
    c.move(box, 5, 0)
def up_callback(self):
    c.move(box, 0, -5)
def down_callback(self):
    c.move(box, 0, 5)

#print(drops)

main.bind('<Left>', left_callback) #bind functions to key presses
main.bind('<Right>', right_callback)
main.bind('<Up>', up_callback)
main.bind('<Down>', down_callback)

c.pack()
main.after(1, move_drops)
main.mainloop()
