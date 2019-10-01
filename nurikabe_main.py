# Nurikabe Display - Version 2.0 (Object Oriented Programming Version)
# Author : Eric Holzer
# Created : 28 June 2019
# Last Edit : 29 September 2019

# Import modules
import pygame
from pygame import Rect # Import the Rect class
from pygame.locals import *  # Import coftant definitiof (QUIT, keys, etc)
import functions as f # Nurikabe solving functions
import solver as s # Nurikabe solver algorithm
#import numpy as np

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
BLUE  = (0, 0, 255)
GREEN = (0, 255, 0)

# Define table
table = None

table1 = [[0, 1, 0, 0],
                  [0, 0, 0, 2],
                  [1, 0, 2, 0],
                  [0, 0, 0, 0],
                  [0, 0, 0, 0],
                  [2, 0, 2, 0]]

table2 = [[0, 0, 0, 0, 0],
                   [2, 0, 0, 1, 0],
                   [0, 0, 0, 0, 0],
                   [0, 2, 0, 0, 0],
                   [0, 0, 0, 0 ,2]]

table3 = [[0, 0, 0, 0, 0],
                   [0, 0, 0, 1, 0],
                   [0, 0, 3, 0, 0],
                   [1, 0, 0, 0, 0],
                   [0, 0, 4, 0, 0]]

table4 = [[1, 0, 2, 0, 2, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0],
                   [2, 0, 0, 0, 0, 4, 0],
                   [0, 0, 4, 0, 0, 0, 0],
                   [0, 0, 0, 0, 2, 0, 0],
                   [2, 0, 0, 0, 0, 0, 0],
                   [0, 0, 1, 0, 0, 0, 1]]

#table4 =[
#[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#[0, 0, 0, 3, 0, 0, 0, 0, 0, 0],
#[0, 0, 3, 0, 0, 0, 0, 3, 0, 0],
#[0, 0, 0, 2, 0, 0, 4, 0, 1, 0],
#[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#[0, 3, 0, 1, 0, 0, 2, 0, 0, 0],
#[0, 0, 1, 0, 0, 0, 0, 4, 0, 0],
#[0, 1, 0, 0, 0, 0, 4, 0, 0, 0],
#[0, 0, 0, 0, 0, 0, 0, 0, 1, 0]]

# Define classes
class App:
    """Create the application. This object is a singleton. This object is created first."""
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
        Room() # Create a Room object
               
        title = Text('Nurikabe', size=100) # Create a Text object
        title.rect.center = (self.screen_center[0], self.screen_center[1] - 200)
        
        play = Button('PLAY', size=64, cmd='App.room = App.rooms[1]') # Create a Button object
        play.rect.center = self.screen_center
        
        solve = Button('SOLVE', size=64, cmd='App.room = App.rooms[3]')
        solve.rect.center = (self.screen_center[0], self.screen_center[1] + 100)
        
        option = Button('HELP', size=64, cmd='App.room = App.rooms[5]')
        option.rect.center = (self.screen_center[0], self.screen_center[1] + 200)
        
        credit = Text('Made by Eric Holzer and Jacek Wikiera, 2019')
        credit.rect.bottomright = self.screen_size
        
        # Room 1 (Choosing Playable Level Room)
        Room()
        Button('menu', cmd='App.room = App.rooms[0]', pos=(10, 10), thickness = 2, inf = 10)
        text = Text('Choose a level', size=72)
        text.rect.center = (self.screen_center[0], 30)
        Button('1', pos=(100, self.screen_center[1]), size=72, cmd='App.room = App.rooms[2]; App.grid.set_table(table1); App.grid.playable = True')
        Button('2', pos=(200, self.screen_center[1]), size=72, cmd='App.room = App.rooms[2]; App.grid.set_table(table2); App.grid.playable = True')
        Button('3', pos=(300, self.screen_center[1]), size=72, cmd='App.room = App.rooms[2]; App.grid.set_table(table3); App.grid.playable = True')
        Button('4', pos=(400, self.screen_center[1]), size=72, cmd='App.room = App.rooms[2]; App.grid.set_table(table4); App.grid.playable = True')
        
        # Room 2 (Playable Room)  
        Room()
        Button('menu', cmd='App.reset(App.grid.table); App.room = App.rooms[0]', pos=(10, 10), thickness = 2, inf = 10)
        App.grid = Grid(table1)
        App.grid.playable = True
        mode = Text('Mode: play', size=30)
        mode.rect.center = (self.screen_center[0], 20)
        Button('check_continuity', pos=(600, 100), size=20, cmd='App.checkWallIntegrity(App.grid.table)', inf = 20, thickness = 2)
        Button('2x2 block', pos=(600, 150), size=20, cmd='App.wallBlockCheck(App.grid.table)', inf = 20, thickness = 2)
        Button('island_complete', pos=(600, 200), size=20, cmd='App.allIslCheck(App.grid.table)', inf = 20, thickness = 2)
        Button('undefined', pos=(600, 250), size=20, cmd='App.checkForUndefined(App.grid.table)', inf = 20, thickness = 2)
        Button('fill', pos=(600, 600), size=20, cmd='App.fill(App.grid.table)', inf = 20, thickness = 2, col=GREEN)
        Button('check', pos=(600, 650), size=20, cmd='App.check(App.grid.table)', inf = 20, thickness = 2, col=BLUE)
        Button('reset', pos=(600, 700), size=20, cmd='App.reset(App.grid.table)', inf = 20, thickness = 2, col=RED)
        
        # Room 3 (Choosing Solving Level Room)
        Room()
        Button('menu', cmd='App.room = App.rooms[0]', pos=(10, 10), thickness = 2, inf = 10)
        text = Text('Choose a level', pos=(0, 0), size=72)
        text.rect.center = (self.screen_center[0], 30)
        Button('1', pos=(100, self.screen_center[1]), size=72, cmd='App.room = App.rooms[4]; App.grid2.set_table(table1)')
        Button('2', pos=(200, self.screen_center[1]), size=72, cmd='App.room = App.rooms[4]; App.grid2.set_table(table2)')
        Button('3', pos=(300, self.screen_center[1]), size=72, cmd='App.room = App.rooms[4]; App.grid2.set_table(table3)')
        Button('4', pos=(400, self.screen_center[1]), size=72, cmd='App.room = App.rooms[4]; App.grid2.set_table(table4)')
        
        # Room 4 (Solving Room)
        Room()
        Button('menu', cmd='App.reset(table1); App.room = App.rooms[0]', pos=(10, 10), thickness = 2, inf = 10)
        App.grid2 = Grid(table1)
        App.grid2.playable = False
        mode = Text('Mode: solve', size=30)
        mode.rect.center = (self.screen_center[0], 20)
        Button('around_one', pos=(600, 50), size=20, cmd='f.elimAroundOnes(App.grid2.table)', inf = 20, thickness = 2)
        Button('between_numbers', pos=(600, 100), size=20, cmd='f.elimAdj(App.grid2.table)', inf = 20, thickness = 2)
        Button('diagonal', pos=(600, 150), size=20, cmd='f.diagonal(App.grid2.table)', inf = 20, thickness = 2)
        Button('surrounded', pos=(600, 200), size=20, cmd='f.surround(App.grid2.table)', inf = 20, thickness = 2)
        Button('solve', pos=(600, 300), size=20, cmd='currentState = f.state(App.grid2.table);table = currentState.table;s.solve(table, currentState)', inf = 20, thickness = 2)
        Button('check', pos=(600, 650), size=20, cmd='App.check(App.grid2.table)', inf = 20, thickness = 2, col=BLUE)
        Button('reset', pos=(600, 700), size=20, cmd='App.reset(App.grid2.table)', inf = 20, thickness = 2, col=RED)
        
        # Room 5 (Help Room)
        Room()
        Button('menu', cmd='App.room = App.rooms[0]', pos=(10, 10), thickness = 2, inf = 10)
        Text('In this program you can either play nurikabe or watch our algorithm do the work.', pos=(10, 50))
        Text('This has been made in the context of a school project by Jacek Wikiera and Eric Holzer. 2019', pos=(10, 70))
        Text('', pos=(10, 90))
        
        App.room = App.rooms[0] # Set the first room to Title Screen Room

    def run(self):
        # Run the Event Loop
        # While the user doesn't close the window, the program is running
        self.active = True
        
        while self.active:
            for event in pygame.event.get():
                if event.type == QUIT: # If the window close button is pressed
                    self.active = False
            
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.active = False
                        
                elif event.type == MOUSEBUTTONDOWN:
                    print("")
                    print("mouse position : ", event.pos)
                        
                App.room.do_event(event) # Call the "do_event" function from the current Room object
            
                self.draw()
                            
        pygame.quit()
        exit()
        
    def draw(self):
        """Draw the application window."""
        App.screen.fill(self.background_color)
        App.room.draw() # Call the "draw" function from the current Room object
        pygame.display.update()
        
    # Check Table Functions. Print whether the nurikabe's rules are respected or not
    def checkWallIntegrity(table):
        if f.checkWallIntegrity2(table):
            print("> the wall is continuous")
        elif not f.checkWallIntegrity2(table):
            print("> the wall is not continuous")
        elif f.checkWallIntegrity2(table) == None:
            print("> there is no walls")
            
    def wallBlockCheck(table):
        if f.wallBlockCheck(table) != None:
            print("> there is a 2x2 block at " + str(f.wallBlockCheck(table)))
        else:
            print("> there is no 2x2 block")
            
    def allIslCheck(table):
        if f.allIslCheck(table):
            print("> All the islands are complete")
        else:
            print("> All the islands are not complete")
            
    def checkForUndefined(table):
        if f.checkForUndefined(table):
            print("> undefined tile(s) are remaining")
        else:
            print("> no undefined tiles found")
        
    def check(table):
        # Check if the nurikabe is correct
        if f.checkWallIntegrity2(table):
            print("> the wall is continuous")
        elif not f.checkWallIntegrity2(table):
            print("> the wall is not continuous")
        elif f.checkWallIntegrity2(table) == None:
            print("> there is no walls")
        
        if f.wallBlockCheck(table) != None:
            print("> there is a 2x2 block at " + str(f.wallBlockCheck(table)))
        else:
            print("> there is no 2x2 block")
            
        if f.allIslCheck(table):
            print("> All the islands are complete")
        else:
            print("> All the islands are not complete")
            
        if f.checkForUndefined(table):
            print("> undefined tile(s) are remaining")
        else:
            print("> no undefined tiles found")
                
    def fill(table):
        # Fill the nurikabe with logical moves
        f.wallAroundIslands(table)
        table = f.elimAdj(table)
        table = f.diagonal(table)
        table = f.surround(table)
                        
    def reset_np(table):
        # Reset the table using numpy
        x_len = len(table)
        y_len = len(table[1])
        
        for x in range(x_len):
            for y in range(y_len):
                if (table[x, y] < 0):
                    table[x, y] = 0
    
    def reset(table):
        # Reset the table
        x_len = len(table)
        y_len = len(table[1])
        
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
        
        #Create the surface image of the text
        self.img = font.render(self.text, True, self.col)
        self.rect = self.img.get_rect()
        self.rect.topleft = self.pos
        
    def draw(self):
        App.screen.blit(self.img, self.rect)
        
    def do_event(self, event):
        pass
    
    
class Button(Text):
    """Create a button object (text surrounded by a rectangle). Clicking the button calls a callback function 'cmd'. """
    """This object inherit from the Text object."""
    
    def __init__(self, text, size=24, col=BLACK, pos=(0, 0), cmd='', thickness=4, inf=40):
        super().__init__(text, size, col, pos)
        self.cmd = cmd
        self.thickness = thickness # Thickness of the surrounding rectangle
        self.inf = inf # inflation of the surrounding rectangle
        self.rect = self.rect.inflate(self.inf, self.inf) # return a new rectangle that is bigger
        self.rect.move_ip(self.inf//2, self.inf//2) # move the rect by half the inflation
        
    def draw(self):
        pygame.draw.rect(App.screen, self.col, self.rect, self.thickness)
        # text rectangle must be moved by half of button inflate (inf//2)
        App.screen.blit(self.img, self.rect.move(self.inf//2, self.inf//2))
        
    def do_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            print("the button execute : ", self.cmd)
            exec(self.cmd)
    

class Room:
    """Create a room object. The room object contains all the objects (texts, buttons, grid)."""

    def __init__(self):
        App.room = self # Set the room to be the current room
        App.rooms.append(self) # Append the room to the list of all the rooms of the App
        self.objects = [] # Room objects List
    
    def draw(self):
        for object in self.objects:
            object.draw()
            
    def do_event(self, event):
        if event.type == MOUSEBUTTONDOWN or event.type == MOUSEMOTION:
            for object in self.objects:
                if object.rect.collidepoint(event.pos):
                    object.do_event(event)
                    if event.type == MOUSEBUTTONDOWN:
                        print('mouse click in : ', object)
                        
                        

class Grid:
    """Create a grid object."""
    
    def __init__(self, table, pos=(50, 50), col=BLACK):
        self.set_table(table, pos, col)
        App.room.objects.append(self)
        
    def set_table(self, table, pos=(50, 50), col=BLACK):
        #n, m = table.shape
        self.remove_numbers() # Remove numbers of previous table (used to fix a bug)
        self.n = len(table) # Number of rows
        self.m = len(table[1]) # Number of columns
        self.pos = pos
        self.table = table
        self.col = col
        self.selected_cell_pos = 0, 0
        self.cursor_on_grid = False
        self.playable = False
        self.text_number_len = 0
        self.cell_text_list = []
        
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
                
                if self.table[i][j] > 0: # if the cell is a number
                    text = Text(str(self.table[i][j]), size = number_size)
                    text.rect.center = current_rect.center
                    self.cell_text_list.append(text)
                    
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
                if self.table[i][j] == -1:
                    pygame.draw.rect(App.screen, self.col, current_rect, 0)
                    
                # Draw the cell in white (little black square)
                elif self.table[i][j] == -2:
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
                
                
                print("cell index : " + "[" + str(i) + "]" + "[" + str(j) + "]" + " | " + "cell state : ", self.table[i][j])
                
                if self.table[i][j] == 0: # If the cell is undefined turn it to black
                    self.table[i][j] = -1
                    
                elif self.table[i][j] == -1: # If the cell is black turn it to white
                    self.table[i][j] = -2
                    
                elif self.table[i][j] == -2: # If the cell is white turn it to undefined
                    self.table[i][j] = 0
                    
    def remove_numbers(self):
        """Removes all numbers (actually all 1-character Text)."""

        remove_list = []
        for x in App.room.objects:
            if isinstance(x, Text) and len(x.text) == 1:
                remove_list.append(x)
                    
        for x in remove_list:
            App.room.objects.remove(x) # remove an object from a list


# Run the program
if __name__ == '__main__':
    App().run()