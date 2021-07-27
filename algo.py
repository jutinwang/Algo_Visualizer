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
rows = 50
squaresize = 10
white = (200, 200, 200)
green = (0, 255, 0)
purple = (128, 0, 128)
red = (255, 0, 0)
blue = (0,0,255)
gray = (100,100,100)
black = (0,0,0)

class Squares:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = black #controls background color
        self.beside = []
        self.width = width
        self.total_rows = total_rows
    
    def get_pos(self):
        return self.row, self.col
    
    def is_wall(self):
        return self.color == white

    def make_wall(self):
        self.color = white
    
    def make_start(self):
        self.color = green
    
    def make_end(self):
        self.color = red
    
    def make_open(self):
        self.color = purple

    def make_closed(self):
        self.color = blue
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.width))
    
    def update_neighbors(self, grid):
        self.beside = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_wall(): # DOWN
            self.beside.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_wall(): # UP
            self.beside.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_wall(): # RIGHT
            self.beside.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_wall(): # LEFT
            self.beside.append(grid[self.row][self.col - 1])
    
    def __lt__(self, other):
	    return False

#the h() score of the algo
def h(pone, ptwo):
    x1, y1 = pone
    x2, y2 = ptwo
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.make_path()
		draw()

def astar(draw, grid, start, end):
    count = 0
    openlist = PriorityQueue()
    openlist.put((0, count, start))
    prev = {}
    g = {spot: float("inf") for row in grid for spot in row}
    g[start] = 0
    f = {spot: float("inf") for row in grid for spot in row}
    f[start] = h(start.get_pos(), end.get_pos())
    print (start.get_pos())
    open_hash = {start}

    while not openlist.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = openlist.get()[2]
        open_hash.remove(current)

        if current == end:
            print ('gamex')
            reconstruct_path(prev, end, draw)
            end.make_end()
            return True
        
        for neighbor in current.beside:
            temp_g = g[current] + 1
            print (g[current])

            if temp_g < g[current]:
                prev[neighbor] = current
                g[neighbor] = temp_g
                f[neighbor] = temp_g + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_hash:
                    print("hu")
                    count += 1
                    openlist.put((f[neighbor], count, neighbor))
                    open_hash.add(neighbor)
                    neighbor.make_open()
        
        draw()

        if current != start:
           current.make_closed()

    return False


#draw the grid
def grid(screen, rows, width):
    space = width // rows
    for row in range(rows):
        pygame.draw.line(screen, gray, (0, row * space), (width, row * space)) #pygame.draw.line(grid, color, start, end, width)
        for columns in range(rows):
            pygame.draw.line(screen, gray, (columns * space, 0), (columns * space, width))

#make spots for algo later on
def make_spots(rows, width):
	matrix = []
	gap = width // rows
	for i in range(rows):
		matrix.append([])
		for j in range(rows):
			spot = Squares(i, j, gap, rows)
			matrix[i].append(spot)

	return matrix

#get usable coor
def placeof(cor, rows, width):
    space = width//rows
    y, x = cor 
    
    row = y // space
    col = x // space

    return row, col

def draw(screen, dis, rows, width):
    screen.fill(black)

    for row in dis:
        for spot in row:
            spot.draw(screen)
    grid(screen, rows, width)
    pygame.display.update()

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
    start = (int(choice1[0]),int(choice1[1]))
    return (start)

def choice2():
    choice2 = a2.get().split(',')
    end = (int(choice2[0]), int(choice2[1]))
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

#~~~~~~~~~main pygame screen~~~~~~~~

matrix = make_spots(rows, width)
running = True
# game loop
destroyed = False
while running:
    while destroyed == False:
        root.destroy()
        destroyed = True
    #pygame.display.flip() #displays the screen
    draw(screen, matrix, rows, width)
    ev = pygame.event.get()
    #placing the start and end blocks
    bruhx, bruhy = placeof(bruh, rows, width)
    bruh2x, bruh2y = placeof(bruh2, rows, width)
    start = matrix[bruhx][bruhy]
    end = matrix[bruh2x][bruh2y]
    start.make_start()
    end.make_end()
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    for event in ev:
        if event.type == pygame.QUIT:
            running = False
            
        if pygame.mouse.get_pressed()[0]: #press mouse
            cor = pygame.mouse.get_pos()#gets the position of click
            row, col = placeof(cor, rows, width)
            place = matrix[row][col]
            place.make_wall()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and start and end:
                for row in matrix:
                    for spot in row:
                        spot.update_neighbors(matrix)

                astar(lambda: draw(screen, matrix, rows, width), matrix, start, end)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

