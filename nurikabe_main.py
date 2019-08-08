# Nurikabe Display - Version 2.0 (Object Oriented Programming Version)
# Author : Eric Holzer
# Created : 28 June 2019
# Last Edit : 8 August 2019

# Import modules
import pygame
from pygame import Rect # Import the Rect class
from pygame.locals import *  # Import constant definitions (QUIT, keys, etc)
import nurikabe_solver as ns # Nurikabe solving functions
import nurikabe_tables as nt # Nurikabe tables
import numpy as np # Import numpy module which is used for tables

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
BLUE  = (0, 0, 255)
GREEN = (0, 255, 0)

# Define table
table = None

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

tableTest = np.zeros((10, 20), dtype=int)

table = tableTest
table[5, 5] = 1

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
        # Room 0 (Title Screen Room)
        Room()
               
        title = Text('Nurikabe', size=100)
        title.rect.center = (self.screen_center[0], self.screen_center[1] - 200)
        
        play = Button('PLAY', size=72, cmd='App.room = App.rooms[1]')
        play.rect.center = self.screen_center
        
        solve = Button('SOLVE', size=72, cmd='App.room = App.rooms[1]')
        solve.rect.center = (self.screen_center[0], self.screen_center[1] + 100)
        
        option = Button('OPTION', size=72, cmd='print("OPTION ROOM")')
        option.rect.center = (self.screen_center[0], self.screen_center[1] + 200)
        
        credit = Text('Made by Eric Holzer and Jacek Wikiera, 2019')
        credit.rect.bottomright = self.screen_size
        
        # Room 1 (Choosing Level Room)
        Room()
        Button('menu', cmd='App.room = App.rooms[0]', pos=(10, 10), thickness = 2, inf = 10)
        text = Text('Choose a level', pos=(0, 0), size=72)
        text.rect.center = (self.screen_center[0], 30)
        Button('1', pos=(100, self.screen_center[1]), size=72, cmd='App.room = App.rooms[2];App.grid.set_table(table1);App.grid.playable = True')
        Button('2', pos=(200, self.screen_center[1]), size=72, cmd='App.room = App.rooms[2];App.grid.set_table(table2)')
        Button('3', pos=(300, self.screen_center[1]), size=72, cmd='print(3)')
        Button('4', pos=(400, self.screen_center[1]), size=72, cmd='print(4)')
        
        # Room 2 (Playable Room)  
        Room()
        Button('menu', cmd='App.room = App.rooms[0]', pos=(10, 10), thickness = 2, inf = 10)
        App.grid = Grid(table)
        App.grid.playable = True
        mode = Text('Mode: play', size=30)
        mode.rect.center = (self.screen_center[0], 20)
        Button('check_continuity', pos=(600, 100), size=20, cmd='print("check_continuity")', inf = 20, thickness = 2)
        Button('2x2 block', pos=(600, 150), size=20, cmd='print("2x2_block")', inf = 20, thickness = 2)
        Button('island_complete', pos=(600, 200), size=20, cmd='print("island_complete")', inf = 20, thickness = 2)
        
        App.room = App.rooms[0] # Set the first room to Title Screen Room
        
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
            
            #if App.room == App.rooms[0]:
               # print(1)
                            
        pygame.quit()
        exit()
        
    def draw(self):
        """Draw the application window."""
        App.screen.fill(self.background_color)
        App.room.draw()
        pygame.display.update()
        

class Node: # NOT IN USE
    """Create a node for making hierarchies."""
    def __init__(self, parent):
        self.parent = parent
        self.parent.children.append(self)
        self.children = []


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
        self.set_table(table, pos, col)
        App.room.objects.append(self)
        
    def set_table(self, table, pos=(50, 50), col=BLACK):
        n, m = table.shape
        self.n = n # Number of rows
        self.m = m # Number of columns
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
            
        self.rect = Rect(*pos, m*self.case_length, n*self.case_length)
        self.create_cell_text()
        self.thickness = (self.case_length * 4) // 100 # Scaled according to the case_length
        
    
    def create_cell_text(self):
        for i in range(self.n):
            for j in range(self.m):
                current_rect = self.get_cell_rect(i, j)
                
                # Draw the number
                number_size = (self.case_length * 60) // 100 # Scaled according to the case_length
                
                if self.table[i, j] > 0: 
                    text = Text(str(self.table[i, j]), size = number_size)
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
                if self.table[i, j] == -1:
                    pygame.draw.rect(App.screen, self.col, current_rect, 0)
                    
                # Draw the cell in white (little black square)
                elif self.table[i, j] == -2:
                    inf = (self.case_length * -80) // 100 # Scaled according to the case_length
                    
                    current_rect.inflate_ip(inf, inf) # Shrink the current rectangle
                    pygame.draw.rect(App.screen, self.col, current_rect, 0)
        
        # If PLAY Room
        if self.playable:
            # Check if the mouse is colliding the grid
            if pygame.mouse.get_pos()[0] < x0:
                self.cursor_on_grid = False
            elif pygame.mouse.get_pos()[0] > (self.m)*self.case_length+x0:
                self.cursor_on_grid = False
            elif pygame.mouse.get_pos()[1] < y0:
                self.cursor_on_grid = False
            elif pygame.mouse.get_pos()[1] > (self.n)*self.case_length+y0:
                self.cursor_on_grid = False
            else:
                self.cursor_on_grid = True
                        
            # Draw the selected cell
            selected_cell_rect = self.get_cell_rect(*self.selected_cell_pos)
            
            if self.cursor_on_grid:
                pygame.draw.rect(App.screen, RED, selected_cell_rect, self.thickness)
                    
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
        
        # If PLAY Room
        if self.playable:
            i, j = self.get_cell_index(event.pos)
            
            # Move the selected cell (red square)
            self.selected_cell_pos = i, j
            
            if event.type == MOUSEBUTTONDOWN:
                
                print(i, j, self.table[i, j])
                
                if self.table[i, j] == 0: # If the cell is undefined turn it to black
                    self.table[i, j] = -1
                    
                elif self.table[i, j] == -1: # If the cell is black turn it to white
                    self.table[i, j] = -2
                    
                elif self.table[i, j] == -2: # If the cell is white turn it to undefined
                    self.table[i, j] = 0

# Run the program
if __name__ == '__main__':
    App().run()
