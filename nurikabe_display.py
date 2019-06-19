# Nurikabe Display - Version 1.??
# Author : Eric Holzer
# Date : 19 June 2019

# Import Modules
import pygame
from pygame.locals import * # Get Input Variables
import nurikabe_solver as ns # Jacek's program
import nurikabe_tables as nt # Nurikabe Tables
import validite # functions that check if the Nurikabe is completed

# Initialize Pygame
pygame.init()

# Initialize Font
pygame.font.init()
font = pygame.font.SysFont("Helvetica", 72)
font_little = pygame.font.SysFont("Helvetica", 24)

# Create Table
""" "W" = white
    "B" = black
    "U" = undefined """

# Table 1
table = [["U", "U", "1", "U", "U", "2"],
         ["1", "U", "U", "U", "U", "U"],
         ["U", "U", "2", "U", "U", "2"],
         ["U", "2", "U", "U", "U", "U"]]

# Set x and y length of the table
x_len = len(table)
y_len = len(table[0])

# Initialize Variables
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
BLUE  = (0, 0, 255)
GREEN = (0, 255, 0)

color1 = WHITE
color2 = BLACK

TOOLBAR_DISTANCE      = 50
DISTANCE_BETWEEN_EDGE = 200
CASE_LENGTH           = 100
SCREEN_DIMENSION      = ((x_len * CASE_LENGTH) + DISTANCE_BETWEEN_EDGE, (y_len * CASE_LENGTH) + TOOLBAR_DISTANCE)
SCREEN_CENTER         = (SCREEN_DIMENSION[0] / 2, SCREEN_DIMENSION[1] / 2)

DISTANCE_BETWEEN_BUTTON = 50

play_button_rectangle   = pygame.Rect(0, 0, 250, 80)
solve_button_rectangle  = pygame.Rect(0, 0, 250, 80)
option_button_rectangle = pygame.Rect(0, 0, 250, 80)

inverse_color_button_rectangle = pygame.Rect(0, 0, 400, 80)

cursor_rectangle        = pygame.Rect(0, 0, CASE_LENGTH, CASE_LENGTH)
white_cell_rectangle    = pygame.Rect(0, 0, 20, 20)
black_cell_rectangle    = pygame.Rect(0, 0, CASE_LENGTH, CASE_LENGTH)

around_one_button_rectangle = pygame.Rect(0, 0, 150, 30)
adj_button_rectangle        = pygame.Rect(0, 0, 150, 30)
diagonal_button_rectangle   = pygame.Rect(0, 0, 150, 30)
reset_button_rectangle      = pygame.Rect(0, 0, 150, 30)
continuity_button_rectangle = pygame.Rect(0, 0, 150, 30)
block_2x2_button_rectangle  = pygame.Rect(0, 0, 150, 30)

return_button_rectangle = pygame.Rect(0, 0, 75, 30)

level1_button_rectangle = pygame.Rect(0, 0, 100, 100)
level2_button_rectangle = pygame.Rect(0, 0, 100, 100)
level3_button_rectangle = pygame.Rect(0, 0, 100, 100)
level4_button_rectangle = pygame.Rect(0, 0, 100, 100)

active = True # Main Loop Variable

room = 1 # The game starts in room 1, corresponding to the title screen

room_mode = "" # Whether "solve" or "play"

# Create Window
window_title = "Nurikabe"
window = pygame.display.set_mode(SCREEN_DIMENSION)
pygame.display.set_caption(window_title)

# Creating Functions
def initialize_debug_table():
    """ Return an empty table that has the same dimension as the initial table """
    tempTable = []
    for x in range(x_len):
        tempTable.append([])
        for y in range(y_len):
            tempTable[x].append(0)
    return tempTable

def clamp(n, smallest, largest):
    """Keep the value between 2 numbers."""
    return max(smallest, min(n, largest))

def draw_button(name, distance_from_top, small_button_rectangle, color):
    """Create a button : text surrounded by a rectangle."""
    
    # Draw Button Text
    button_txt = font_little.render(name, True, color)
    button_txt_rectangle = button_txt.get_rect()
    button_txt_rectangle.center = ((x_len * CASE_LENGTH) + CASE_LENGTH, distance_from_top)
    window.blit(button_txt, button_txt_rectangle)

    # Draw Button Rectangle
    small_button_rectangle.center = button_txt_rectangle.center
    pygame.draw.rect(window, color, small_button_rectangle, 2)
    
def draw_title_button(name, distance_from_center, big_button_rectangle, color):
    """Create a title button : text surrounded by a rectangle."""
    
    # Draw Button Text
    button_txt = font.render(name, True, color)
    button_txt_rectangle = button_txt.get_rect()
    button_txt_rectangle.center = (SCREEN_CENTER[0], SCREEN_CENTER[1] + distance_from_center)
    window.blit(button_txt, button_txt_rectangle)

    # Draw Button Rectangle
    big_button_rectangle.center = button_txt_rectangle.center
    pygame.draw.rect(window, color, big_button_rectangle, 5)
    
def draw_return_button(name, x, y, small_button_rectangle, color):
    """Create a button : text surrounded by a rectangle."""
    
    # Draw Button Text
    button_txt = font_little.render(name, True, color)
    button_txt_rectangle = button_txt.get_rect()
    button_txt_rectangle.center = (x, y)
    window.blit(button_txt, button_txt_rectangle)

    # Draw Button Rectangle
    small_button_rectangle.center = button_txt_rectangle.center
    pygame.draw.rect(window, color, small_button_rectangle, 2)
    
def draw_level_button(name, level_button_rectangle, color, number_of_levels):
    """Create a level button : number surrounded by a square."""
    
    """number_of_rows = 1
    actual_row = 1
    
    if number_of_levels > 5:
        number_of_rows = 2
        if int(name) > 5:
            actual_row = 2
    if number_of_levels > 10:
        number_of_rows = 3
        if int(name) > 5:
            actual_row = 3"""
    
    # Draw Button Number
    button_txt = font.render(name, True, color)
    button_txt_rectangle = button_txt.get_rect()
    button_txt_rectangle.center = ((SCREEN_DIMENSION[0] // (number_of_levels + 1))* int(name), SCREEN_CENTER[1])
    window.blit(button_txt, button_txt_rectangle)

    # Draw Button Rectangle
    level_button_rectangle.center = button_txt_rectangle.center
    pygame.draw.rect(window, color, level_button_rectangle, 5)
    
def reset_table(table):
    for x in range(x_len):
        for y in range(y_len):
            if (table[x][y] == "W" or table[x][y] == "B"):
                table[x][y] = "U"

# Room 1 (Title)
def draw_room1():
    """Draws a title and some buttons."""
    
    window.fill(color1)
    
    # Reset table
    reset_table(table)

    # Draw Title
    title_txt = font.render("Nurikabe", True, color2)
    title_txt_rectangle = title_txt.get_rect()
    title_txt_rectangle.center = (SCREEN_CENTER[0], SCREEN_CENTER[1] - 100)
    window.blit(title_txt, title_txt_rectangle)
    
    # Draw Title Buttons
    draw_title_button("PLAY", 0, play_button_rectangle, color2)
    draw_title_button("SOLVE", 100, solve_button_rectangle, color2)
    draw_title_button("OPTION", 200, option_button_rectangle, color2)
    
    # Draw Autor's names Text
    author_name_txt = font_little.render("Made by Eric Holzer and Jacek Wikeira, 2019", True, color2)
    author_name_txt_rectangle = author_name_txt.get_rect()
    author_name_txt_rectangle.bottomright = (SCREEN_DIMENSION[0] - 10, SCREEN_DIMENSION[1] - 10)
    window.blit(author_name_txt, author_name_txt_rectangle)
    
# Room 2 (Play)
def draw_grid(n, m, case_length):
    """Draws n horizontal lines of length m * case_length.
       Draws m vertical lines of length n * case_length."""
    
    # Draw Horizontal Lines
    for i in range(n + 1):
        y = i * case_length
        x = m * case_length
        pygame.draw.line(window, color2, (0, y + TOOLBAR_DISTANCE), (x, y + TOOLBAR_DISTANCE), 5)
        
    # Draw Vertical Lines
    for i in range(m + 1):
        y = n * case_length
        x = i * case_length
        pygame.draw.line(window, color2, (x, TOOLBAR_DISTANCE), (x, y + TOOLBAR_DISTANCE), 5)

def draw_grid_text(table, case_length): # Draw numbers in the grid
    for x in range(x_len):
        for y in range(y_len):
            # If case is a number, print the number
            if (table[x][y] != "U" and table[x][y] != "B" and table[x][y] != "W"):
                number_txt = font.render(str(table[x][y]), True, color2)
                number_txt_rectangle = number_txt.get_rect()
                number_txt_rectangle.center = ((x * case_length) + (case_length / 2), (y * case_length) + (case_length / 2) + TOOLBAR_DISTANCE)
                window.blit(number_txt, number_txt_rectangle)
                
def draw_grid_color(table, case_length):
    """Fill the cell with the according color."""
    for x in range(x_len):
        for y in range(y_len):
            if table[x][y] == "W":
                white_cell_rectangle.center = ((x * case_length) + (case_length / 2), (y * case_length) + (case_length / 2) + TOOLBAR_DISTANCE)
                pygame.draw.rect(window, color2, white_cell_rectangle)
                
            elif table[x][y] == "B":
                black_cell_rectangle.center = ((x * case_length) + (case_length / 2), (y * case_length) + (case_length / 2) + TOOLBAR_DISTANCE)
                pygame.draw.rect(window, color2, black_cell_rectangle)
                
def draw_debug_table(debug_table, case_length):
    """Fill the cell with the according color."""
    for x in range(x_len):
        for y in range(y_len):
            if debug_table[x][y] == "R":
                white_cell_rectangle.center = ((x * case_length) + (case_length / 2), (y * case_length) + (case_length / 2) + TOOLBAR_DISTANCE)
                pygame.draw.rect(window, RED, white_cell_rectangle)
                
def get_index(x, y, case_length): # Get the case index
    """Returns the (i, j) case index."""
    i = x // case_length
    j = (y - TOOLBAR_DISTANCE) // case_length
    
    return (i, j)

def draw_room2(): 
    """Playable room"""
    
    window.fill(color1)
    
    # Draw Grid
    draw_grid(y_len, x_len, CASE_LENGTH)
    draw_grid_text(table, CASE_LENGTH)
    draw_grid_color(table, CASE_LENGTH)
    
    draw_debug_table(debug_table, CASE_LENGTH)
    
    pygame.draw.rect(window, RED, cursor_rectangle, 5)
    
    # Draw Buttons
    draw_button("check_continuity", TOOLBAR_DISTANCE + DISTANCE_BETWEEN_BUTTON, continuity_button_rectangle, color2)
    draw_button("2x2_block", TOOLBAR_DISTANCE + (DISTANCE_BETWEEN_BUTTON * 2), block_2x2_button_rectangle, color2)
    draw_button("reset", SCREEN_DIMENSION[1] - DISTANCE_BETWEEN_BUTTON, reset_button_rectangle, RED)
    draw_return_button("menu", 50, 25, return_button_rectangle, color2)
    
    # Draw Room Mode
    mode_txt = font_little.render("MODE : " + room_mode, True, color2)
    mode_txt_rectangle = mode_txt.get_rect()
    mode_txt_rectangle.center = (SCREEN_CENTER[0], 25)
    window.blit(mode_txt, mode_txt_rectangle)
    
# Room 3 (Solve)
def draw_room3():
    """Solving Room"""
    
    window.fill(color1)
    
    # Draw Grid
    draw_grid(y_len, x_len, CASE_LENGTH)
    draw_grid_text(table, CASE_LENGTH)
    draw_grid_color(table, CASE_LENGTH)
    
    # Draw Buttons
    draw_button("around_one", TOOLBAR_DISTANCE + DISTANCE_BETWEEN_BUTTON, around_one_button_rectangle, color2)
    draw_button("between_numbers", TOOLBAR_DISTANCE + (DISTANCE_BETWEEN_BUTTON * 2), adj_button_rectangle, color2)
    draw_button("diagonal", TOOLBAR_DISTANCE + (DISTANCE_BETWEEN_BUTTON * 3), diagonal_button_rectangle, color2)
    
    draw_button("reset", SCREEN_DIMENSION[1] - DISTANCE_BETWEEN_BUTTON, reset_button_rectangle, RED)
    draw_return_button("menu", 50, 25, return_button_rectangle, color2)
    
    # Draw Room Mode
    mode_txt = font_little.render("MODE : " + room_mode, True, color2)
    mode_txt_rectangle = mode_txt.get_rect()
    mode_txt_rectangle.center = (SCREEN_CENTER[0], 25)
    window.blit(mode_txt, mode_txt_rectangle)

# Room 4 (Option)
def draw_room4():
    window.fill(color1)
    
    draw_title_button("inverse_color", 0, inverse_color_button_rectangle, color2)
    draw_return_button("menu", 50, 25, return_button_rectangle, color2)
    
# Room 5 (Choice of level)
def draw_room5():
    window.fill(color1)
    
    # Draw Title
    title_txt = font.render("Choose a level", True, color2)
    title_txt_rectangle = title_txt.get_rect()
    title_txt_rectangle.center = (SCREEN_CENTER[0], 100)
    window.blit(title_txt, title_txt_rectangle)
    
    # Draw Level Buttons
    draw_level_button("1", level1_button_rectangle, color2, nt.number_of_levels)
    draw_level_button("2", level2_button_rectangle, color2, nt.number_of_levels)
    draw_level_button("3", level3_button_rectangle, color2, nt.number_of_levels)
    draw_level_button("4", level4_button_rectangle, color2, nt.number_of_levels)
    
    draw_return_button("menu", 50, 25, return_button_rectangle, color2)

# Main Loop
while active:
            
    for event in pygame.event.get():
        
        if event.type == QUIT: # If Close The Window
            active = False
            
        elif event.type == KEYDOWN: # If a key is down
            if event.key == K_ESCAPE:
                room = 1
                
            
        elif event.type == MOUSEBUTTONDOWN: # If a mouse button is pressed
            if room == 1:
                if play_button_rectangle.collidepoint(event.pos): # If Play Button is pressed
                    room_mode = "play"
                    room = 5
                    
                if solve_button_rectangle.collidepoint(event.pos):
                    room_mode = "solve"
                    room = 5
                    
                if option_button_rectangle.collidepoint(event.pos):
                    room = 4
                    
            # PLAYABLE ROOM
            elif room == 2:
                # If the mouse is in the nurikabe grid
                if (event.pos[0] < CASE_LENGTH * x_len) and (event.pos[1] < CASE_LENGTH * y_len):
                    # Get the case index
                    (i, j) = get_index(event.pos[0], event.pos[1], CASE_LENGTH)
                    
                    if table[i][j] == "U":
                        table[i][j] = "W"
                        
                    elif table[i][j] == "W":
                        table[i][j] = "B"
                        
                    elif table[i][j] == "B":
                        table[i][j] = "U"
                        
                if continuity_button_rectangle.collidepoint(event.pos):
                    ns.checkWallIntegrity2(table)
                    
                if block_2x2_button_rectangle.collidepoint(event.pos):
                    
                    block_coord = validite.wallBlockCheck(table)
                
                    if block_coord != None:
                        print(block_coord[0])
                        b0 = block_coord[0]
                        b1 = block_coord[1]
                        
                        debug_table[b0][b1] = "R"
                    
                if reset_button_rectangle.collidepoint(event.pos):
                    reset_table(table)
                    
                if return_button_rectangle.collidepoint(event.pos):
                    room = 1
                    
            # SOLVING ROOM
            elif room == 3:
                if around_one_button_rectangle.collidepoint(event.pos):
                    table = ns.elimAroundOnes(table)
                    
                if adj_button_rectangle.collidepoint(event.pos):
                    table = ns.elimAdj(table)
                    
                if diagonal_button_rectangle.collidepoint(event.pos):
                    table = ns.diagonal(table)
                    
                if reset_button_rectangle.collidepoint(event.pos):
                    reset_table(table)
                    
                if return_button_rectangle.collidepoint(event.pos):
                    room = 1
                    
            # OPTION ROOM
            elif room == 4:
                if inverse_color_button_rectangle.collidepoint(event.pos):
                    if color1 == WHITE:
                        color1 = BLACK
                        color2 = WHITE
                        
                    elif color1 == BLACK:
                        color1 = WHITE
                        color2 = BLACK
                        
                if return_button_rectangle.collidepoint(event.pos):
                    room = 1
                    
            # LEVEL CHOOSING ROOM
            elif room == 5:
                if level1_button_rectangle.collidepoint(event.pos): # LEVEL 1
                    
                    table = nt.table1
                    x_len = len(table)
                    y_len = len(table[0])
                    
                    debug_table = initialize_debug_table()
                    
                    if room_mode == "play":
                        room = 2
                    elif room_mode == "solve":
                        room = 3
                    
                    SCREEN_DIMENSION = ((x_len * CASE_LENGTH) + DISTANCE_BETWEEN_EDGE, (y_len * CASE_LENGTH) + TOOLBAR_DISTANCE)
                    SCREEN_CENTER    = (SCREEN_DIMENSION[0] / 2, SCREEN_DIMENSION[1] / 2)
                    window = pygame.display.set_mode(SCREEN_DIMENSION)
                    
                if level2_button_rectangle.collidepoint(event.pos): # LEVEL 2
                    
                    table = nt.table2
                    x_len = len(table)
                    y_len = len(table[0])
                    
                    debug_table = initialize_debug_table()
                    
                    if room_mode == "play":
                        room = 2
                    elif room_mode == "solve":
                        room = 3
                    
                    SCREEN_DIMENSION = ((x_len * CASE_LENGTH) + DISTANCE_BETWEEN_EDGE, (y_len * CASE_LENGTH) + TOOLBAR_DISTANCE)
                    SCREEN_CENTER    = (SCREEN_DIMENSION[0] / 2, SCREEN_DIMENSION[1] / 2)
                    window = pygame.display.set_mode(SCREEN_DIMENSION)
                    
                if level3_button_rectangle.collidepoint(event.pos): # LEVEL 3
                    
                    table = nt.table3
                    x_len = len(table)
                    y_len = len(table[0])
                    
                    debug_table = initialize_debug_table()
                    
                    if room_mode == "play":
                        room = 2
                    elif room_mode == "solve":
                        room = 3
                    
                    SCREEN_DIMENSION = ((x_len * CASE_LENGTH) + DISTANCE_BETWEEN_EDGE, (y_len * CASE_LENGTH) + TOOLBAR_DISTANCE)
                    SCREEN_CENTER    = (SCREEN_DIMENSION[0] / 2, SCREEN_DIMENSION[1] / 2)
                    window = pygame.display.set_mode(SCREEN_DIMENSION)
                    
                if return_button_rectangle.collidepoint(event.pos):
                    room = 1
                    
                if level4_button_rectangle.collidepoint(event.pos): # LEVEL 4
                    
                    table = nt.table4
                    x_len = len(table)
                    y_len = len(table[0])
                    
                    debug_table = initialize_debug_table()
                    
                    if room_mode == "play":
                        room = 2
                    elif room_mode == "solve":
                        room = 3
                    
                    SCREEN_DIMENSION = ((x_len * CASE_LENGTH) + DISTANCE_BETWEEN_EDGE, (y_len * CASE_LENGTH) + TOOLBAR_DISTANCE)
                    SCREEN_CENTER    = (SCREEN_DIMENSION[0] / 2, SCREEN_DIMENSION[1] / 2)
                    window = pygame.display.set_mode(SCREEN_DIMENSION)
                    
                if return_button_rectangle.collidepoint(event.pos):
                    room = 1
        
        elif event.type == MOUSEMOTION: # If the mouse is moving
            if room == 2:
                # Get the case index
                (i, j) = get_index(event.pos[0], event.pos[1], CASE_LENGTH)
                
                cursor_rectangle.x = i * CASE_LENGTH
                cursor_rectangle.y = j * CASE_LENGTH + TOOLBAR_DISTANCE
                
                cursor_rectangle.x = clamp(cursor_rectangle.x, 0, (x_len - 1) * CASE_LENGTH)
                cursor_rectangle.y = clamp(cursor_rectangle.y, TOOLBAR_DISTANCE, ((y_len - 1) * CASE_LENGTH) + TOOLBAR_DISTANCE)
                
        # All drawing is done here
        if room == 1:
            draw_room1()
        elif room == 2:
            draw_room2()
        elif room == 3:
            draw_room3()
        elif room == 4:
            draw_room4()
        elif room == 5:
            draw_room5()
            
        pygame.display.update()

print("quit")
pygame.quit()
exit()
