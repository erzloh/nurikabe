# Nurikabe Display - Version 1.02
# Author : Eric Holzer
# Date : 24 April 2019

# Import Modules
import pygame
from pygame.locals import * # Get Input Variables
import numpy as np

# Initialize Pygame
pygame.init()

# Initialize Font
pygame.font.init()
font = pygame.font.SysFont("Helvetica", 72)

# Create Table
""" "W" = white
    "B" = black
    "U" = undefined """

table = [["U", "U", "1", "U", "U", "2"],
         ["1", "U", "U", "U", "U", "U"],
         ["U", "U", "2", "U", "U", "2"],
         ["U", "2", "U", "U", "U", "U"]]

# Set x and y length of the table
x_len = len(table)
y_len = len(table[0])

# Create a player table made out of 0
""" 0 = undefined
    1 = white
    2 = black """

player_table = np.zeros((x_len, y_len), int)

# Initialize Variables
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)

CASE_LENGTH      = 100
SCREEN_DIMENSION = (x_len * CASE_LENGTH, y_len * CASE_LENGTH)
SCREEN_CENTER    = (SCREEN_DIMENSION[0] / 2, SCREEN_DIMENSION[1] / 2)

play_button_rectangle = pygame.Rect(0, 0, 200, 80)
cursor_rectangle = pygame.Rect(0, 0, CASE_LENGTH, CASE_LENGTH)
white_cell_rectangle = pygame.Rect(0, 0, 20, 20)
black_cell_rectangle = pygame.Rect(0, 0, CASE_LENGTH, CASE_LENGTH)

active = True # Main Loop Variable

room = 1 # The game starts with room 1

# Create Window
window_title = "Nurikabe"
window = pygame.display.set_mode(SCREEN_DIMENSION)
pygame.display.set_caption(window_title)

# Room 1
def draw_room1():
    """Draws a title and some buttons (play)."""
    
    room = 1
    
    window.fill(WHITE)
    
    # Draw Title
    title_txt = font.render("Nurikabe", True, BLACK)
    title_txt_rectangle = title_txt.get_rect()
    title_txt_rectangle.center = (SCREEN_CENTER[0], SCREEN_CENTER[1] - 100)
    window.blit(title_txt, title_txt_rectangle)

    # Draw Play Button Text
    play_button_txt = font.render("PLAY", True, BLACK)
    play_button_txt_rectangle = play_button_txt.get_rect()
    play_button_txt_rectangle.center = SCREEN_CENTER
    window.blit(play_button_txt, play_button_txt_rectangle)

    # Draw Play Button Rectangle
    play_button_rectangle.center = play_button_txt_rectangle.center
    pygame.draw.rect(window, BLACK, play_button_rectangle, 5)

# Room 2
def draw_grid(n, m, case_length):
    """Draws n horizontal lines of length m * case_length.
       Draws m vertical lines of length n * case_length."""
    
    # Draw Horizontal Lines
    for i in range(n + 1):
        y = i * case_length
        x = m * case_length
        pygame.draw.line(window, BLACK, (0, y), (x, y), 5)
        
    # Draw Vertical Lines
    for i in range(m + 1):
        y = n * case_length
        x = i * case_length
        pygame.draw.line(window, BLACK, (x, 0), (x, y), 5)

def draw_grid_text(table, case_length): # Draw numbers in the grid
    for x in range(x_len):
        for y in range(y_len):
            # If case is a number, print the number
            if (table[x][y] != "U" and table[x][y] != "B" and table[x][y] != "W"):
                number_txt = font.render(str(table[x][y]), True, BLACK)
                number_txt_rectangle = number_txt.get_rect()
                number_txt_rectangle.center = ((x * case_length) + (case_length / 2), (y * case_length) + (case_length / 2))
                window.blit(number_txt, number_txt_rectangle)
                
def draw_grid_color(table, case_length):
    """Fill the cell with the according color."""
    for x in range(x_len):
        for y in range(y_len):
            if table[x][y] == "W":
                white_cell_rectangle.center = ((x * case_length) + (case_length / 2), (y * case_length) + (case_length / 2))
                pygame.draw.rect(window, BLACK, white_cell_rectangle)
                
            elif table[x][y] == "B":
                black_cell_rectangle.center = ((x * case_length) + (case_length / 2), (y * case_length) + (case_length / 2))
                pygame.draw.rect(window, BLACK, black_cell_rectangle)
    
                
def get_index(x, y, case_length): # Get the case index
    """Returns the (i, j) case index."""
    i = x // case_length
    j = y // case_length
    
    return (i, j)

def draw_room2():
    """Draw the nurikabe game grid."""
    
    room = 2
    
    window.fill(WHITE)
    draw_grid(y_len, x_len, CASE_LENGTH)
    draw_grid_text(table, CASE_LENGTH)
    draw_grid_color(table, CASE_LENGTH)
    
    pygame.draw.rect(window, RED, cursor_rectangle, 5)

draw_room1()
# Main Loop
while active:
            
    for event in pygame.event.get():
        
        if event.type == QUIT: # If Close The Window
            active = False
            
        elif event.type == KEYDOWN: # If a key is down
            if event.key == K_m:
                room = 1
            
        elif event.type == MOUSEBUTTONDOWN: # If a mouse button is pressed
            if room == 1:
                if play_button_rectangle.collidepoint(event.pos): # If Play Button is pressed
                    room = 2
            
            elif room == 2:
                # Get the case index
                (i, j) = get_index(event.pos[0], event.pos[1], CASE_LENGTH)
                
                if table[i][j] == "U":
                    table[i][j] = "W"
                    
                elif table[i][j] == "W":
                    table[i][j] = "B"
                    
                elif table[i][j] == "B":
                    table[i][j] = "U"
                
                
                """player_table[col, row] += 1
                player_table[col, row] %= 3"""
        
        elif event.type == MOUSEMOTION: # If the mouse is moving
            if room == 2:
                (i, j) = get_index(event.pos[0], event.pos[1], CASE_LENGTH)
                
                cursor_rectangle.x = i * CASE_LENGTH
                cursor_rectangle.y = j * CASE_LENGTH
                
        # All drawing is done here
        if room == 1:
            draw_room1()
        elif room == 2:
            draw_room2()
            
        pygame.display.update()

print("quit")
pygame.quit()
exit()
