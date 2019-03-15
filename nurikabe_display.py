# Nurikabe Display - Version 1
# Author : Eric Holzer
# Date : 10 March 2019

# Import Modules
import pygame
from pygame.locals import * # Get Input Variables

# Initialize Pygame
pygame.init()

# Initialize Font
pygame.font.init()
font = pygame.font.SysFont("Helvetica", 72)

# Initialize Variables
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

CASE_LENGTH = 80
ROWS = 5
COLS = 10

SCREEN_DIMENSION = (COLS * CASE_LENGTH, ROWS * CASE_LENGTH)
SCREEN_CENTER = (SCREEN_DIMENSION[0] // 2, SCREEN_DIMENSION[1] // 2)


active = True # Main Loop Variable

play_button_rectangle = pygame.Rect(0, 0, 200, 80)
    
# Create Window
window_title = "Nurikabe"
window = pygame.display.set_mode(SCREEN_DIMENSION)
pygame.display.set_caption(window_title)

# Create Draw Room Functions
def draw_room1():
    
    window.fill(WHITE)
    
    # Draw Title
    title_txt = font.render("Nurikabe", True, BLACK)
    title_rectangle = title_txt.get_rect()
    title_rectangle.center = (SCREEN_CENTER[0], SCREEN_CENTER[1] - 100)
    window.blit(title_txt, title_rectangle)

    # Draw Play Button Text
    play_button_txt = font.render("PLAY", True, BLACK)
    play_button_txt_rectangle = play_button_txt.get_rect()
    play_button_txt_rectangle.center = SCREEN_CENTER
    window.blit(play_button_txt, play_button_txt_rectangle)

    # Draw Play Button Rectangle
    play_button_rectangle.center = play_button_txt_rectangle.center
    pygame.draw.rect(window, BLACK, play_button_rectangle, 5)


def draw_grid(n, m, case_length):
    """Draws n horizontal lines of length m*case_length.
       Draws m vertical lines of length n*case_length."""
    
    # Draw Horizontal Lines
    for i in range(n):
        y = i * case_length
        x = m * case_length
        pygame.draw.line(window, BLACK, (0, y), (x, y), 5)
        
    # Draw Vertical Lines
    for i in range(m):
        y = n * case_length
        x = i * case_length
        pygame.draw.line(window, BLACK, (x, 0), (x, y), 5)

# Get the case index
def get_index(x, y, case_length):
    """Returns the (row, col) case index."""
    row = y // case_length
    col = x // case_length
    return (row, col)


def draw_room2():
    
    window.fill(WHITE)
    print("room_2")
    
    draw_grid(ROWS, COLS, CASE_LENGTH)
    
# Draw Room 1
draw_room1()

# Main Loop
while active:
    for event in pygame.event.get():
        
        if event.type == QUIT: # If Close The Window
            active = False
            
        elif event.type == KEYDOWN: # If a key is down
            if event.key == K_m:
                draw_room1()
            
        elif event.type == MOUSEBUTTONDOWN: # If a mouse button is pressed
            if play_button_rectangle.collidepoint(event.pos): # If Play Button is pressed
                draw_room2()
            
            # Get the case index
            (row, col) = get_index(event.pos[0], event.pos[1], CASE_LENGTH)
            print(event.pos, row, col)
                        
    pygame.display.update()

print("quit")
pygame.quit()
exit()
