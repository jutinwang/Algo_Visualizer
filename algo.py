import pygame #pygame for window
import tkinter
from tkinter import * #tkinter for popups
from tkinter import ttk
from tkinter.ttk import *
from tkinter import messagebox
import math
from queue import PriorityQueue
import sys

#~~~~~~~~~this is the screen~~~~~~~~~
screen = pygame.display.set_mode((500,500))#(width, height)
width = 500
rows = 50
squaresize = 10 #size of the squares

#colors
white = (200, 200, 200)
green = (0, 255, 0)
purple = (128, 0, 128)
red = (255, 0, 0)
blue = (0,0,255)
gray = (100,100,100)
black = (0,0,0)
yellow = (255,255,0)

#class for all the important functions and creating nodes to track.
class Squares: #by calling this, it creates a unique node for each space you give it
    def __init__(self, row, col, width, total_rows):
        self.row = row 
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = black #controls background color
        self.besides = [] #array for tracking neighbours of current node
        self.width = width
        self.total_rows = total_rows
    
    def get_pos(self):
        return self.row, self.col #get the current position
    
    def is_wall(self):
        return self.color == white #walls are white blocks

    def make_wall(self):
        self.color = white
    
    def make_start(self):
        self.color = green #start is a green block
    
    def make_end(self):
        self.color = red #end block is red
    
    def make_open(self):
        self.color = purple #open nodes are purple

    def make_closed(self):
        self.color = blue #closed nodes not worth checking is blue

    def make_path(self):
        self.color = yellow #reconstruct block is yellow
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.width)) #__init__ function to draw the blocks
    
    def update_neighbors(self, grid):#function that checks if the neighbouring nodes exist
        self.besides = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_wall(): # DOWN
            self.besides.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_wall(): # UP
            self.besides.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_wall(): # RIGHT
            self.besides.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_wall(): # LEFT
            self.besides.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False


def h(p1, p2): #h() function (f(x) = g(x) + h(x))
    #h() = cost from current node to end node
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(prev, current, draw):#function to redraw shortest path
	while current in prev:
		current = prev[current]
		current.make_path()
		draw()

#a* algorithm
#The algorithm (f(x) = g(x) + h(x) where g() is the cost of the start to end node and h() is the cost of the current to end node)
#The algo knows the general direction of the end node and prioritizes checking in that direction instead of a general search

def astar(draw, grid, start, end):
    count = 0 #counter
    openlist = PriorityQueue() #creates a priority queue for which nodes to check next
    openlist.put((0, count, start)) #(f score, counter, start position) if the f() is the same for 2 paths, they will check the counter for the shortest
    prev = {} #list of the previous nodes

    g = {spot: float('inf') for row in grid for spot in row} #gives unique key for each node and sets each one to equal infinity distance
    g[start] = 0 #the g() score, distance from start is 0
    f = {spot: float('inf') for row in grid for spot in row}
    f[start] = h(start.get_pos(), end.get_pos()) #the f() score

    open_hash = {start} #keeps track of whats in the queue

    while not openlist.empty(): #if the list is not empty
        for event in pygame.event.get(): #closes the window if you press the x button
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = openlist.get()[2] #the value of current is the node
        open_hash.remove(current) #removes the current node from queue

        if current == end: #if the current node is the end node
            reconstruct_path(prev, current, draw)
            end.make_end()
            return True

        for neighbor in current.besides: #loops on for each node beside the current value
            temp_g_score = g[current] + 1 
            if temp_g_score < g[neighbor]: #if the current g score is less than the one beside it
                prev[neighbor] = current #adds neighbor value to prev list which is equal to current value
                g[neighbor] = temp_g_score #g() score of neighbor is now temp_g_score
                f[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_hash: 
                    count += 1
                    openlist.put((f[neighbor], count, neighbor))
                    open_hash.add(neighbor)
                    neighbor.make_open()
        draw()

        if current != start:
            current.make_closed()

    return False

#dijkstra's algorithm
#difference between dijkstra's algorithm and a* is that a* has an f(), g() and h() score used to track the shortest path in the direction of the target node         
def dijkstra(draw, grid, start, end):
    count = 0
    distance = {spot: float("inf") for row in grid for spot in row} #set all nodes as infinity distance
    distance[start] = 0 #set start node as 0
    prev = {}#keeps track of previous nodes visited
    
    openlist = PriorityQueue()#queue
    openlist.put((count, start))#puts the counter and start node in queue

    openhash = {start}#keeps track of what's in the queue


    while not openlist.empty(): #quits when you press the X
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        u = openlist.get()[1]#get the best vertex value
        openhash.remove(u)

        if u == end: #if the current node is the end node
            reconstruct_path(prev, end, draw)
            end.make_end()
            return True

        for neighbor in u.besides: # for each neighbor beside the current node
            alt = distance[u] + h(u.get_pos(), neighbor.get_pos()) #find what this do
            if alt < distance[neighbor]:
                distance[neighbor] = alt
                prev[neighbor] = u
                if neighbor not in openhash: 
                    count += 1
                    openlist.put((count, neighbor))
                    openhash.add(neighbor)
                    neighbor.make_open()
        draw()

        if u != start:
            u.make_closed()
    
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
choices = ["", "a*", "dijkstra"] #options for the drop menu
variable = StringVar(root) 
variable.set("") #set the default option for the menu as blank
menu = OptionMenu(root, variable, *choices) #OptionMenu function
menu.grid(column = 3, row = 6) 

#text input
s1 = Label(root, text = "Position of starting node (5-495)")
s2 = Label(root, text = "Position of ending node (5-495)")
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
algo = algochoice()

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
            if event.key == pygame.K_SPACE and start and end and algo == "a*":
                for row in matrix:
                    for spot in row:
                        spot.update_neighbors(matrix)
            
                astar(lambda: draw(screen, matrix, rows, width), matrix, start, end) #lambda allows you to call a function using another function

            elif event.key == pygame.K_SPACE and start and end and algo == "dijkstra":
                for row in matrix:
                    for spot in row:
                        spot.update_neighbors(matrix)
            
                dijkstra(lambda: draw(screen, matrix, rows, width), matrix, start, end)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



