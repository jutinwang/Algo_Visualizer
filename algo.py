import pygame #pygame for window
import tkinter
from tkinter import * #tkinter for popups
from tkinter import ttk
from tkinter import messagebox
import math

#this is the screen
#(width, height)
screen = pygame.display.set_mode((800,800))
width = 1000
height = 800
white = (200, 200, 200)


#creating a grid
def grid():
    #sets the squaresize to 20, with the grid size, it makes a 40x40 grid
    squaresize = 20
    for x in range(0, width, squaresize):
        for y in range (0, height, squaresize):
            rect = pygame.Rect(x, y, squaresize, squaresize)
            pygame.draw.rect(screen, white, rect, 1)

#opening message
def message():
    messagebox.showinfo("Information","Informative message")
    

running = True
# game loop
while running:
    pygame.display.flip()
    #message()
    grid()
# for loop through the event queue  
    for event in pygame.event.get():
        # Check for QUIT event      
        if event.type == pygame.QUIT:
            running = False
