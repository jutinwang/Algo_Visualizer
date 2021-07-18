import pygame #pygame for window
import tkinter
from tkinter import * #tkinter for popups
from tkinter import ttk
from tkinter.ttk import *
from tkinter import messagebox
import math

#~~~~~~~~~this is the screen~~~~~~~~~
#(width, height)
screen = pygame.display.set_mode((500,500))
width = 500
height = 500
squaresize = 10
white = (200, 200, 200)
green = (0, 128, 0)
red = (255, 0, 0)

#~~~~~~~~~creating a grid~~~~~~~~~~~
#creating a 2d array for each spot on the grid
rect_map = {}
rect_matrix = []

for rows in range(50):
    twodgrid = []
    for columns in range(50):
        twodgrid.append(pygame.Rect((columns * squaresize, rows * squaresize), (squaresize, squaresize)))
        rect_map[(columns, rows)] = 1
    rect_matrix.append(twodgrid)
    

#~~~~~~~~~Blocks~~~~~~~~~
def placeblock():
    start = (0,0) #custom cooridnates use () brackets
    rect_map[start] = 0

def placeend(): 
    end = (10, 10)
    rect_map[end] = 0

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
    placeblock() #places green block
    placeend() # places red block
    ev = pygame.event.get()
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    for event in ev:
        if event.type == pygame.MOUSEBUTTONUP: #press mouse
            pos = pygame.mouse.get_pos()#gets the position of click
            gridpos = pos[0] // squaresize, pos[1] // squaresize
            if rect_map[gridpos] == 1:
                rect_map[gridpos] = 0
            else:
                rect_map[gridpos] = 1

        if event.type == pygame.QUIT:
            running = False

    screen.fill((0,0,0))

    for i, ii in zip(rect_matrix, range(len(rect_matrix))):
        for j, jj  in zip(i, range(len(i))):
            pygame.draw.rect(screen, (100,100,100), j, rect_map[(jj, ii)])

    pygame.display.update()
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
