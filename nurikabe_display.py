# Nurikabe Display - Version 1.02
# Author : Eric Holzer
# Date : 25 April 2019

# Import Modules
import pygame
from pygame.locals import * # Get Input Variables
import numpy as np
import nurikabe

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

sample_table = [["U", "U", "1", "U", "U", "2"],
                ["1", "U", "U", "U", "U", "U"],
                ["U", "U", "2", "U", "U", "2"],
                ["U", "2", "U", "U", "U", "U"]]

table = sample_table

"""table = [["U", "U", "5", "U", "U"],
         ["U", "3", "U", "U", "U"],
         ["U", "U", "U", "U", "U"],
         ["U", "U", "U", "U", "U"],
         ["1", "U", "U", "2", "U"]]"""

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

DISTANCE_BETWEEN_EDGE = 200
CASE_LENGTH           = 100
SCREEN_DIMENSION      = ((x_len * CASE_LENGTH) + DISTANCE_BETWEEN_EDGE, (y_len * CASE_LENGTH))
SCREEN_CENTER         = (SCREEN_DIMENSION[0] / 2, SCREEN_DIMENSION[1] / 2)

play_button_rectangle  = pygame.Rect(0, 0, 200, 80)
solve_button_rectangle = pygame.Rect(0, 0, 200, 80)
cursor_rectangle       = pygame.Rect(0, 0, CASE_LENGTH, CASE_LENGTH)
white_cell_rectangle   = pygame.Rect(0, 0, 20, 20)
black_cell_rectangle   = pygame.Rect(0, 0, CASE_LENGTH, CASE_LENGTH)

around_one_button_rectangle = pygame.Rect(0, 0, 150, 30)
adj_button_rectangle        = pygame.Rect(0, 0, 150, 30)
diagonal_button_rectangle   = pygame.Rect(0, 0, 150, 30)
reset_button_rectangle      = pygame.Rect(0, 0, 150, 30)

active = True # Main Loop Variable

room = 1 # The game starts with room 1

# Create Window
window_title = "Nurikabe"
window = pygame.display.set_mode(SCREEN_DIMENSION)
pygame.display.set_caption(window_title)

# Useful Function
def clamp(n, smallest, largest):
    """Keep the value between 2 numbers."""
    return max(smallest, min(n, largest))

# Room 1
def draw_room1():
    """Draws a title and some buttons (play)."""
    
    window.fill(WHITE)
    
    # Reset table
    table = sample_table
    reset_table(table)

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
    
    
    # Draw Solve Button Text
    solve_button_txt = font.render("SOLVE", True, BLACK)
    solve_button_txt_rectangle = solve_button_txt.get_rect()
    solve_button_txt_rectangle.center = (SCREEN_CENTER[0], SCREEN_CENTER[1] + 100)
    window.blit(solve_button_txt, solve_button_txt_rectangle)
    
    # Draw Solve Button Rectangle
    solve_button_rectangle.center = solve_button_txt_rectangle.center
    pygame.draw.rect(window, BLACK, solve_button_rectangle, 5)
    
    
    # Draw Autor's names Text
    author_name_txt = font_little.render("Made by Eric Holzer and Jacek Wikeira, 2019", True, BLACK)
    author_name_txt_rectangle = author_name_txt.get_rect()
    author_name_txt_rectangle.bottomright = (SCREEN_DIMENSION[0] - 10, SCREEN_DIMENSION[1] - 10)
    window.blit(author_name_txt, author_name_txt_rectangle)

def reset_table(table):
    for x in range(x_len):
        for y in range(y_len):
            if (table[x][y] == "W" or table[x][y] == "B"):
                table[x][y] = "U"
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
    """Playable room"""
    
    window.fill(WHITE)
    draw_grid(y_len, x_len, CASE_LENGTH)
    draw_grid_text(table, CASE_LENGTH)
    draw_grid_color(table, CASE_LENGTH)
    
    pygame.draw.rect(window, RED, cursor_rectangle, 5)
    
# Room 3
def draw_buttons():
    # Draw around_one Button Text
    around_one_button_txt = font_little.render("around_one", True, BLACK)
    around_one_button_txt_rectangle = around_one_button_txt.get_rect()
    around_one_button_txt_rectangle.center = ((x_len * CASE_LENGTH) + CASE_LENGTH, 30)
    window.blit(around_one_button_txt, around_one_button_txt_rectangle)

    # Draw around_one Button Rectangle
    around_one_button_rectangle.center = around_one_button_txt_rectangle.center
    pygame.draw.rect(window, BLACK, around_one_button_rectangle, 2)
    
    
    # Draw between_numbers Button Text
    adj_button_txt = font_little.render("between_numbers", True, BLACK)
    adj_button_txt_rectangle = adj_button_txt.get_rect()
    adj_button_txt_rectangle.center = ((x_len * CASE_LENGTH) + CASE_LENGTH, 80)
    window.blit(adj_button_txt, adj_button_txt_rectangle)

    # Draw between_numbers Button Rectangle
    adj_button_rectangle.center = adj_button_txt_rectangle.center
    pygame.draw.rect(window, BLACK, adj_button_rectangle, 2)
    
    
    # Draw diagonal Button Text
    diagonal_button_txt = font_little.render("diagonal", True, BLACK)
    diagonal_button_txt_rectangle = diagonal_button_txt.get_rect()
    diagonal_button_txt_rectangle.center = ((x_len * CASE_LENGTH) + CASE_LENGTH, 130)
    window.blit(diagonal_button_txt, diagonal_button_txt_rectangle)

    # Draw diagonal Button Rectangle
    diagonal_button_rectangle.center = diagonal_button_txt_rectangle.center
    pygame.draw.rect(window, BLACK, diagonal_button_rectangle, 2)
    
    
    # Draw reset Button Text
    reset_button_txt = font_little.render("reset", True, RED)
    reset_button_txt_rectangle = reset_button_txt.get_rect()
    reset_button_txt_rectangle.center = ((x_len * CASE_LENGTH) + CASE_LENGTH, SCREEN_DIMENSION[1] - 30)
    window.blit(reset_button_txt, reset_button_txt_rectangle)

    # Draw reset Button Rectangle
    reset_button_rectangle.center = reset_button_txt_rectangle.center
    pygame.draw.rect(window, BLACK, reset_button_rectangle, 2)

def draw_room3():
    """Solving room"""
    
    window.fill(WHITE)
    draw_grid(y_len, x_len, CASE_LENGTH)
    draw_grid_text(table, CASE_LENGTH)
    draw_grid_color(table, CASE_LENGTH)
    
    draw_buttons()
    
# Main Loop
while active:
            
    for event in pygame.event.get():
        
        if event.type == QUIT: # If Close The Window
            active = False
            
        elif event.type == KEYDOWN: # If a key is down
            if event.key == K_ESCAPE:
                room = 1
                table = sample_table
            
        elif event.type == MOUSEBUTTONDOWN: # If a mouse button is pressed
            if room == 1:
                if play_button_rectangle.collidepoint(event.pos): # If Play Button is pressed
                    room = 2
                    
                if solve_button_rectangle.collidepoint(event.pos):
                    room = 3
            
            elif room == 2:
                if (event.pos[0] < CASE_LENGTH * x_len) and (event.pos[1] < CASE_LENGTH * y_len):
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
                    
            elif room == 3:
                if around_one_button_rectangle.collidepoint(event.pos):
                    table = nurikabe.elimAroundOnes(table)
                    
                if adj_button_rectangle.collidepoint(event.pos):
                    table = nurikabe.elimAdj(table)
                    
                if diagonal_button_rectangle.collidepoint(event.pos):
                    table = nurikabe.diagonal(table)
                    
                if reset_button_rectangle.collidepoint(event.pos):
                    reset_table(table)
        
        elif event.type == MOUSEMOTION: # If the mouse is moving
            if room == 2:
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
            
        pygame.display.update()

print("quit")
pygame.quit()
exit()
