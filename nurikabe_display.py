# Nurikabe Display - Version 1.03
# Author : Eric Holzer
# Date : 26 April 2019

# Import Modules
import pygame
from pygame.locals import * # Get Input Variables
import nurikabe_solver as ns # Jacek's program

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

# Table 2
"""table = [["U", "2", "U", "U", "U"],
         ["U", "U", "U", "2", "U"],
         ["U", "U", "U", "U", "U"],
         ["U", "1", "U", "U", "U"],
         ["U", "U", "U", "U", "2"]]"""

# Table 3
"""table = [["U", "U", "U", "1", "U"],
         ["U", "U", "U", "U", "U"],
         ["U", "U", "3", "U", "4"],
         ["U", "1", "U", "U", "U"],
         ["U", "U", "U", "U", "U"]]"""

# Set x and y length of the table
x_len = len(table)
y_len = len(table[0])

# Initialize Variables
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)

color1 = WHITE
color2 = BLACK

DISTANCE_BETWEEN_EDGE = 200
CASE_LENGTH           = 100
SCREEN_DIMENSION      = ((x_len * CASE_LENGTH) + DISTANCE_BETWEEN_EDGE, (y_len * CASE_LENGTH))
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

active = True # Main Loop Variable

room = 1 # The game starts in room 1

# Create Window
window_title = "Nurikabe"
window = pygame.display.set_mode(SCREEN_DIMENSION)
pygame.display.set_caption(window_title)

# Useful Function
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
    
def reset_table(table):
    for x in range(x_len):
        for y in range(y_len):
            if (table[x][y] == "W" or table[x][y] == "B"):
                table[x][y] = "U"

# Room 1 (Title)
def draw_room1():
    """Draws a title and some buttons (play)."""
    
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
        pygame.draw.line(window, color2, (0, y), (x, y), 5)
        
    # Draw Vertical Lines
    for i in range(m + 1):
        y = n * case_length
        x = i * case_length
        pygame.draw.line(window, color2, (x, 0), (x, y), 5)

def draw_grid_text(table, case_length): # Draw numbers in the grid
    for x in range(x_len):
        for y in range(y_len):
            # If case is a number, print the number
            if (table[x][y] != "U" and table[x][y] != "B" and table[x][y] != "W"):
                number_txt = font.render(str(table[x][y]), True, color2)
                number_txt_rectangle = number_txt.get_rect()
                number_txt_rectangle.center = ((x * case_length) + (case_length / 2), (y * case_length) + (case_length / 2))
                window.blit(number_txt, number_txt_rectangle)
                
def draw_grid_color(table, case_length):
    """Fill the cell with the according color."""
    for x in range(x_len):
        for y in range(y_len):
            if table[x][y] == "W":
                white_cell_rectangle.center = ((x * case_length) + (case_length / 2), (y * case_length) + (case_length / 2))
                pygame.draw.rect(window, color2, white_cell_rectangle)
                
            elif table[x][y] == "B":
                black_cell_rectangle.center = ((x * case_length) + (case_length / 2), (y * case_length) + (case_length / 2))
                pygame.draw.rect(window, color2, black_cell_rectangle)
                
def get_index(x, y, case_length): # Get the case index
    """Returns the (i, j) case index."""
    i = x // case_length
    j = y // case_length
    
    return (i, j)

def draw_room2(): 
    """Playable room"""
    
    window.fill(color1)
    
    # Draw Grid
    draw_grid(y_len, x_len, CASE_LENGTH)
    draw_grid_text(table, CASE_LENGTH)
    draw_grid_color(table, CASE_LENGTH)
    
    pygame.draw.rect(window, RED, cursor_rectangle, 5)
    
    # Draw Buttons
    draw_button("check_continuity", 30, continuity_button_rectangle, color2)
    draw_button("reset", SCREEN_DIMENSION[1] - DISTANCE_BETWEEN_BUTTON, reset_button_rectangle, RED)
    
    
# Room 3 (Solve)
def draw_room3():
    """Solving Room"""
    
    window.fill(color1)
    
    # Draw Grid
    draw_grid(y_len, x_len, CASE_LENGTH)
    draw_grid_text(table, CASE_LENGTH)
    draw_grid_color(table, CASE_LENGTH)
    
    # Draw Buttons
    draw_button("around_one", DISTANCE_BETWEEN_BUTTON, around_one_button_rectangle, color2)
    draw_button("between_numbers", DISTANCE_BETWEEN_BUTTON * 2, adj_button_rectangle, color2)
    draw_button("diagonal", DISTANCE_BETWEEN_BUTTON * 3, diagonal_button_rectangle, color2)
    
    draw_button("reset", SCREEN_DIMENSION[1] - DISTANCE_BETWEEN_BUTTON, reset_button_rectangle, RED)

# Room 4 (Option)
def draw_room4():
    window.fill(color1)
    
    draw_title_button("inverse_color", 0, inverse_color_button_rectangle, color2)
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
                    room = 2
                    
                if solve_button_rectangle.collidepoint(event.pos):
                    room = 3
                    
                if option_button_rectangle.collidepoint(event.pos):
                    room = 4
                    
            # PLAYABLE ROOM
            elif room == 2:
                # If the mouse stay in the nurikabe grid
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
                    
                if reset_button_rectangle.collidepoint(event.pos):
                    reset_table(table)
                    
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
                    
            # OPTION ROOM
            elif room == 4:
                if inverse_color_button_rectangle.collidepoint(event.pos):
                    if color1 == WHITE:
                        color1 = BLACK
                        color2 = WHITE
                        
                    elif color1 == BLACK:
                        color1 = WHITE
                        color2 = BLACK
        
        elif event.type == MOUSEMOTION: # If the mouse is moving
            if room == 2:
                # Get the case index
                (i, j) = get_index(event.pos[0], event.pos[1], CASE_LENGTH)
                
                cursor_rectangle.x = i * CASE_LENGTH
                cursor_rectangle.y = j * CASE_LENGTH
                
                cursor_rectangle.x = clamp(cursor_rectangle.x, 0, (x_len - 1) * CASE_LENGTH)
                
        # All drawing is done here
        if room == 1:
            draw_room1()
        elif room == 2:
            draw_room2()
        elif room == 3:
            draw_room3()
        elif room == 4:
            draw_room4()
            
        pygame.display.update()

print("quit")
pygame.quit()
exit()
