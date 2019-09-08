# Nurikabe Display - Version 3.0 (Object Oriented Programming Version)
# Author : Eric Holzer
# Created : 8 August 2019
# Last Edit : 8 August 2019
# Choose the table of your choice down below

# Import modules
import pygame
from pygame import Rect # Import the Rect class
from pygame.locals import *  # Import constant definitions (QUIT, keys, etc)
import nurikabe_solver as ns # Nurikabe solving functions
import nurikabe_tables as nt # Nurikabe tables
import numpy as np # Import numpy module which is used for tables
#import main_loop as ml

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
BLUE  = (0, 0, 255)
GREEN = (0, 255, 0)

# Define table
table = None

table0 =  [[0, 1, 0, 0],
           [0, 0, 0, 2],
           [1, 0, 2, 0],
           [0, 0, 0, 0],
           [0, 0, 0, 0],
           [2, 0, 2, 0]]

table1 = np.array([[0, 1, 0, 0],
                   [0, 0, 0, 2],
                   [1, 0, 2, 0],
                   [0, 0, 0, 0],
                   [0, 0, 0, 0],
                   [2, 0, 2, 0]])

table2 = np.array([[0, 0, 0, 0, 0],
                   [2, 0, 0, 1, 0],
                   [0, 0, 0, 0, 0],
                   [0, 2, 0, 0, 0],
                   [0, 0, 0, 0 ,2]])

table3 = np.array([[0, 0, 0, 0, 0],
                   [0, 0, 0, 1, 0],
                   [0, 0, 3, 0, 0],
                   [1, 0, 0, 0, 0],
                   [0, 0, 4, 0, 0]])

table4 = np.array([[1, 0, 2, 0, 2, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0],
                   [2, 0, 0, 0, 0, 4, 0],
                   [0, 0, 4, 0, 0, 0, 0],
                   [0, 0, 0, 0, 2, 0, 0],
                   [2, 0, 0, 0, 0, 0, 0],
                   [0, 0, 1, 0, 0, 0, 1]])

table6 = [[0, 0, 0, 0, 0],
           [2, 0, 0, 1, 0],
           [0, 0, 0, 0, 0],
           [0, 2, 0, 0, 0],
           [0, 0, 0, 0 ,2]]

table5 = np.zeros((10, 20), dtype=int)
table5[5, 5] = 1

# The table used
table = table6

# Define classes
class App:
    """Create the application. This object is a singleton. This object is created first"""
    rooms  = [] # All the rooms of the app are stocked here
    room   = None # The current room
    screen = None # The window of the application
    
    def __init__(self):
        # Initialize pygame and font
        pygame.init()
        pygame.font.init()
                
        # Create screen
        self.screen_size      = (750, 750) # Default screen size
        self.screen_center    = (self.screen_size[0] / 2, self.screen_size[1] / 2)
        self.background_color = WHITE
        self.title            = "Nurikabe"
        App.screen            = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption(self.title)
        
        # Initialize Room and Room objects
        Room()
        Text('Nurikabe Solver by Jacek Wikiera and Eric Holzer', size=20)
        Grid(table)
        Button('around_one', pos=(600, 50), size=20, cmd='ns.elimAroundOnes(table)', inf = 20, thickness = 2)
        Button('between_numbers', pos=(600, 100), size=20, cmd='ns.elimAdj(table)', inf = 20, thickness = 2)
        Button('diagonal', pos=(600, 150), size=20, cmd='ns.diagonal(table)', inf = 20, thickness = 2)
        Button('surrounded', pos=(600, 200), size=20, cmd='ns.surround(table)', inf = 20, thickness = 2)
        Button('around_island', pos=(600, 250), size=20, cmd='ns.wallAroundIslands(table)', inf = 20, thickness = 2)
        Button('solve', pos=(600, 300), size=20, cmd='ml.solve(table)', inf = 20, thickness = 2)
        Button('fill', pos=(600, 600), size=20, cmd='App.fill(table)', inf = 20, thickness = 2, col=GREEN)
        Button('check', pos=(600, 650), size=20, cmd='App.check(table)', inf = 20, thickness = 2, col=BLUE)
        Button('reset', pos=(600, 700), size=20, cmd='App.reset(table)', inf = 20, thickness = 2, col=RED)
        
    def run(self):
        # Run the main event loop
        self.active = True
        
        while self.active:
            
            # Logic section
            for event in pygame.event.get():
                if event.type == QUIT: # If the window close button is pressed
                    self.active = False
            
                elif event.type == KEYDOWN: # If a key is pressed
                    if event.key == K_ESCAPE:
                        self.active = False
                        
                elif event.type == MOUSEBUTTONDOWN:
                    print(event.pos)
                        
                App.room.do_event(event)
            
            # Draw section
            self.draw()
                            
        pygame.quit()
        exit()
        
    def draw(self):
        """Draw the application window."""
        App.screen.fill(self.background_color)
        App.room.draw()
        pygame.display.update()
    
    def check(table):
        if ns.checkWallIntegrity2(table):
            print("the wall is continuous")
        elif not ns.checkWallIntegrity2(table):
            print("the wall is not continuous")
        elif ns.checkWallIntegrity2(table) == None:
            print("there is no walls")
        
        if ns.wallBlockCheck(table) != None:
            print("there is a 2x2 block at " + str(ns.wallBlockCheck(table)))
        else:
            print("there is no 2x2 block")
            
        if ns.allIslCheck(table):
            print("All the islands are complete")
        else:
            print("All the islands are not complete")
                
    def fill(table):
        ns.wallAroundIslands(table)
        table = ns.elimAdj(table)
        table = ns.diagonal(table)
        table = ns.surround(table)
                        
    def reset_np(table):
        y_len = len(table)
        x_len = len(table[1])
        
        for x in range(x_len):
            for y in range(y_len):
                if (table[x, y] < 0):
                    table[x, y] = 0
    
    def reset(table):
        y_len = len(table)
        x_len = len(table[1])
        
        for x in range(x_len):
            for y in range(y_len):
                if (table[x][y] < 0):
                    table[x][y] = 0

class Text:
    """Create a text object."""
    
    def __init__(self, text, size=24, col=BLACK, pos=(0, 0)):
        self.text = text
        self.size = size
        self.col = col
        self.pos = pos
        self.render()
        
        App.room.objects.append(self) # The object is added to the room object list
        
    def render(self):
        font = pygame.font.SysFont("Helvetica", self.size)
        """Create the surface image of the text."""
        self.img = font.render(self.text, True, self.col)
        self.rect = self.img.get_rect()
        self.rect.topleft = self.pos
        
    def draw(self):
        App.screen.blit(self.img, self.rect)
        
    def do_event(self, event):
        pass
    
    
class Button(Text):
    """Create a button object."""
    
    def __init__(self, text, size=24, col=BLACK, pos=(0, 0), cmd='', thickness=4, inf=40):
        super().__init__(text, size, col, pos)
        self.cmd = cmd
        self.thickness = thickness
        self.inf = inf # inflation of the rectangle around the text
        
    def draw(self):
        r = self.rect.inflate(self.inf, self.inf) # return a new rectangle that is bigger
        pygame.draw.rect(App.screen, self.col, r, self.thickness)
        super().draw()
        
    def do_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            print(self.cmd)
            exec(self.cmd)
    

class Room:
    """Create a room object."""

    def __init__(self):
        App.room = self
        App.rooms.append(self)
        self.objects = []
    
    def draw(self):
        for object in self.objects:
            object.draw()
            
    def do_event(self, event):
        if event.type == MOUSEBUTTONDOWN or event.type == MOUSEMOTION:
            for object in self.objects:
                if object.rect.collidepoint(event.pos):
                    object.do_event(event)
                    if event.type == MOUSEBUTTONDOWN:
                        print('mouse click in', object)
                        
                        

class Grid:
    """Create a grid object."""
    
    def __init__(self, table, pos=(50, 50), col=BLACK):

        App.room.objects.append(self)
        
        #n, m = table.shape
        #self.n = n # Number of rows
        #self.m = m # Number of columns
        
        self.n = len(table)
        self.m = len(table[1])
        self.pos = pos
        self.table = table
        self.col = col
        self.selected_cell_pos = 0, 0
        self.cursor_on_grid = False
        self.playable = False
        
        # Scale the case_length according to the number of rows and columns
        if self.n > self.m:
            self.case_length = 650 // self.n
        else:
            self.case_length = 500 // self.m
            
        self.rect = Rect(*pos, self.m*self.case_length, self.n*self.case_length)
        self.create_cell_text()
        self.thickness = (self.case_length * 4) // 100 # Scaled according to the case_length
        
    
    def create_cell_text(self):
        for i in range(self.n):
            for j in range(self.m):
                current_rect = self.get_cell_rect(i, j)
                
                # Draw the number
                number_size = (self.case_length * 60) // 100 # Scaled according to the case_length
                
                #if self.table[i, j] > 0:
                if self.table[i][j] > 0:
                    #text = Text(str(self.table[i, j]), size = number_size)
                    text = Text(str(self.table[i][j]), size = number_size)
                    text.rect.center = current_rect.center
        
    def draw(self):
        x0, y0 = self.pos
        
        # Horizontal lines
        for i in range(self.n + 1):
            y = y0 + i * self.case_length
            x1 = x0 + self.m * self.case_length
            pygame.draw.line(App.screen, self.col, (x0, y), (x1, y), self.thickness)
        
        # Vertical lines
        for i in range(self.m + 1):
            y1 = y0 + self.n * self.case_length
            x = x0 + i * self.case_length
            pygame.draw.line(App.screen, self.col, (x, y0), (x, y1), self.thickness)
        
        # Draw colors on the grid
        for i in range(self.n):
            for j in range(self.m):
                current_rect = self.get_cell_rect(i, j)
                
                # Draw the cell in black
                #if self.table[i, j] == -1:
                if self.table[i][j] == -1:
                    pygame.draw.rect(App.screen, self.col, current_rect, 0)
                    
                # Draw the cell in white (little black square)
                #elif self.table[i, j] == -2:
                elif self.table[i][j] == -2:
                    inf = (self.case_length * -80) // 100 # Scaled according to the case_length
                    
                    current_rect.inflate_ip(inf, inf) # Shrink the current rectangle
                    pygame.draw.rect(App.screen, self.col, current_rect, 0)
                    
    def get_cell_rect(self, i, j):
        """Get rectangle from index (i, j)."""
        rect = Rect(*self.pos, self.case_length, self.case_length)
        rect.move_ip(j * self.case_length, i* self.case_length)
        return rect
        
    def get_cell_index(self, pos):
        """Get cell index (i, j) from position (x, y)."""
        x0, y0 = self.pos
        x, y = pos
        
        j = (x - x0) // self.case_length
        i = (y - y0) // self.case_length
        
        return i, j
            
    def do_event(self, event):
        pass

# Run the program
if __name__ == '__main__':
    App().run()

