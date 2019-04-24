# Nurikabe Display - Version 1.02
# Author : Eric Holzer
# Date : 24 April 2019

# Import Modules
import pygame
from pygame.locals import * # Get Input Variables

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

# Initialize Variables
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)

CASE_LENGTH      = 100
SCREEN_DIMENSION = (x_len * CASE_LENGTH, y_len * CASE_LENGTH)
SCREEN_CENTER    = (SCREEN_DIMENSION[0] / 2, SCREEN_DIMENSION[1] / 2)

play_button_rectangle = pygame.Rect(0, 0, 200, 80)
cursor_rectangle = pygame.Rect(0, 0, CASE_LENGTH, CASE_LENGTH)

active = True # Main Loop Variable

# The game starts with room 1.
room = 1

# Create Window
window_title = "Nurikabe"
window = pygame.display.set_mode(SCREEN_DIMENSION)
pygame.display.set_caption(window_title)

# Room 1
def draw_room1():
    """Draws a title and some buttons (play)."""
    
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

def draw_grid_text(table, CASE_LENGTH): # Draw numbers in the grid
    for x in range(x_len):
        for y in range(y_len):
            # If case is a number, print the number
            if (table[x][y] != "U" and table[x][y] != "B" and table[x][y] != "W"):
                number_txt = font.render(str(table[x][y]), True, BLACK)
                number_txt_rectangle = number_txt.get_rect()
                number_txt_rectangle.center = ((x * CASE_LENGTH) + (CASE_LENGTH / 2), (y * CASE_LENGTH) + (CASE_LENGTH / 2))
                window.blit(number_txt, number_txt_rectangle)
                
def get_index(x, y, case_length): # Get the case index
    """Returns the (row, col) case index."""
    row = y // case_length
    col = x // case_length
    return (row, col)

def draw_room2():
    """Draw the nurikabe game grid."""
    window.fill(WHITE)
    draw_grid(y_len, x_len, CASE_LENGTH)
    draw_grid_text(table, CASE_LENGTH)
    
    pygame.draw.rect(window, RED, cursor_rectangle, 5)

    
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
                (row, col) = get_index(event.pos[0], event.pos[1], CASE_LENGTH)
                print(event.pos, row, col)
        
        elif event.type == MOUSEMOTION:
            if room == 2:
                
                (row, col) = get_index(event.pos[0], event.pos[1], CASE_LENGTH)
                
                cursor_rectangle.y = row * CASE_LENGTH
                cursor_rectangle.x = col * CASE_LENGTH
            
        # All drawing is done here
        if room == 1:
            draw_room1()
        elif room == 2:
            draw_room2()
            
        pygame.display.update()

print("quit")
pygame.quit()
exit()
