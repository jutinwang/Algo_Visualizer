import pygame #pygame for window
import tkinter
from tkinter import * #tkinter for popups
from tkinter import ttk
from tkinter.ttk import *
from tkinter import messagebox
import math
from queue import PriorityQueue

#~~~~~~~~~this is the screen~~~~~~~~~
#(width, height)
screen = pygame.display.set_mode((500,500))
width = 500
height = 500
squaresize = 10
white = (200, 200, 200)
green = (0, 255, 0)
red = (255, 0, 0)
start = (0,0)
end = (0,0)

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
def placeblock(x, y):
    start = (x,y) #custom cooridnates use () brackets
    rect_map[start] = 0

def placeend(x2, y2): 
    end = (x2, y2)
    rect_map[end] = 0

#~~~~~~~~~Widget~~~~~~~~~
root = Tk() 
label = tkinter.Label(root, text= "hello")
root.geometry('400x400')

#Choice box
choices = ["", "a*", "bruh"] #options for the drop menu
variable = StringVar(root) 
variable.set("") #set the default option for the menu as blank
menu = OptionMenu(root, variable, *choices) #OptionMenu function
menu.grid(column = 3, row = 6) 

#text input
s1 = Label(root, text = "Position of starting node (0-49)")
s2 = Label(root, text = "Position of ending node (0-49)")
s1.grid(column = 0, row = 0)
s2.grid(column = 0, row = 1)

#stores answers 
a1 = Entry(root)
a2 = Entry(root)
a1.grid(column = 5, row = 0)
a2.grid(column = 5, row = 1)

def choice(): #function
    choice1 = a1.get().split(',')
    print (choice1[1])
    start = (int(choice1[0]),int(choice1[1]))
    #root.quit()
    return (start)

def choice2():
    choice2 = a2.get().split(',')
    print (choice2[0])
    end = (int(choice2[0]), int(choice2[1]))
    #root.quit()
    return (end)

def algochoice():
   selection = variable.get() #selection variable gets the value of the option chosen
   root.quit()
   return (selection)

button = Button(root, text="START", command=choice)
button.grid(column = 3, row = 5)

button2 = Button(root, text="END", command = choice2)
button2.grid(column = 5, row = 5)

button3 = Button(root, text="OK", command = algochoice)
button3.grid(column = 4, row = 7)

root.mainloop()
bruh = choice() #takes the variable from the function
bruh2 = choice2()
if bruh[0] == bruh2[0] and bruh[1] == bruh2[1]:
    bruht = list(bruh2)
    if bruht[0] > 39:
        bruht[0] -= 10
        bruh2 = tuple(bruht)
    elif bruht[1] > 39:
        bruht[1] -= 10
        bruh2 = tuple(bruht)
    else:
        bruht[0] += 10
        bruht[1] += 10
        bruh2 = tuple(bruht)
#~~~~~~~~~Widget 2~~~~~~~~~


#~~~~~~~~~algo~~~~~~~~~
openlist = []
closedlist = []
#openlist = openlist.head

def astar():
    while len(openlist) > 0:
        smallestindex = bruh
        

#~~~~~~~~~main pygame screen~~~~~~~~~
running = True
# game loop
destroyed = False
while running:
    while destroyed == False:
        root.destroy()
        destroyed = True
    pygame.display.flip() #displays the screen
    placeblock(bruh[0], bruh[1]) #places start block
    placeend(bruh2[0], bruh2[1]) # places end block
    ev = pygame.event.get()
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    for event in ev:
        if event.type == pygame.QUIT:
            running = False
            
        if pygame.mouse.get_pressed()[0]: #press mouse
            pos = pygame.mouse.get_pos()#gets the position of click
            gridpos = pos[0] // squaresize, pos[1] // squaresize
            if rect_map[gridpos] == 1:
                rect_map[gridpos] = 0
            else:
                rect_map[gridpos] = 1


    screen.fill((0,0,0))

    for i, ii in zip(rect_matrix, range(len(rect_matrix))):
        for j, jj  in zip(i, range(len(i))):
            if jj == bruh[0] and ii == bruh[1]:
                pygame.draw.rect(screen, green, j, rect_map[(jj, ii)]) #sets colour of start block to green
            elif jj == bruh2[0] and ii == bruh2[1]:
                pygame.draw.rect(screen, red, j, rect_map[(jj, ii)]) #sets colour of end block to red
            else:     
                pygame.draw.rect(screen, (100,100,100), j, rect_map[(jj, ii)]) #sets colours of blocks to gray

    pygame.display.update()
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
