import pygame #pygame for window
import tkinter
from tkinter import * #tkinter for popups
from tkinter import ttk
from tkinter.ttk import *
from tkinter import messagebox
import math


#this is the screen
#(width, height)
screen = pygame.display.set_mode((800,800))
width = 1000
height = 800
white = (200, 200, 200)


#~~~~~~~~~creating a grid~~~~~~~~~
def grid():
    #sets the squaresize to 20, with the grid size, it makes a 40x40 grid
    squaresize = 20
    for x in range(0, width, squaresize):
        for y in range (0, height, squaresize):
            rect = pygame.Rect(x, y, squaresize, squaresize)
            pygame.draw.rect(screen, white, rect, 1)
            
def placeblock():
    squaresize = 20
    start = pygame.Rect(1, 1, squaresize, squaresize )
    pygame.draw.rect(screen, green, start, 0)

#~~~~~~~~~Widget~~~~~~~~~
root = Tk() 
label = tkinter.Label(root, text= "hello")
root.geometry('500x500')

#Choice box
choices = ["", "a*", "bruh"] #options for the drop menu
variable = StringVar(root) 
variable.set("") #set the default option for the menu as blank
menu = OptionMenu(root, variable, *choices) #OptionMenu function
menu.pack() 

#Button
def choice(): #function
    selection = variable.get() #selection variable gets the value of the option chosen
button = Button(root, text="OK", command=choice)
button.pack()

#text input
#still doesn't look good but it functionally works
s1 = Label(root, text = "Position of starting node")
s1.pack(side = LEFT)
a1 = Entry(root)
a1.pack(side = RIGHT)

space = Label(root, text = "\n")
space.pack()

s2 = Label(root, text = "Position of end node")
s2.pack(side = LEFT)
a2 = Entry(root)
a2.pack(side = RIGHT)

root.mainloop()

#~~~~~~~~~algo~~~~~~~~~
def astar():
    print ("e") 

#~~~~~~~~~main pygame screen~~~~~~~~~
running = True
# game loop
while running:
    pygame.display.flip() #displays the screen
    grid() #displays the grid
# for loop through the event queue  
    for event in pygame.event.get():
        # Check for QUIT event      
        if event.type == pygame.QUIT:
            running = False
