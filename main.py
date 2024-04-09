import pygame
import sys

pygame.init()

# Constants
width, height = 1080, 1080
screen = pygame.display.set_mode((width, height))
icon = pygame.image.load("img/icon.png")
background = pygame.image.load("img/main.png")
play_button = pygame.image.load("img/play.png")
play_button_original = play_button.copy()   
play_button_rect = play_button.get_rect(center=(width // 2, height // 2 + 100))
quit_button = pygame.image.load("img/quit.png")   
quit_button_rect = quit_button.get_rect(center=(width // 2, height // 2 + 300))
quit_button_original = quit_button.copy()
home_button = pygame.image.load("img/home2.png")
home_button_original = home_button.copy()
home_button_rect = home_button.get_rect(topright=(width - (-60), -90))   
mode1_button = pygame.image.load("img/mode1bttn.png")
mode2_button = pygame.image.load("img/mode2bttn.png")
mode1_button_original = mode1_button.copy()

# Letter bank settings
letter_bank_font = pygame.font.SysFont(None, 36)
letter_bank_color = (255, 255, 255)
letter_bank_spacing = 20
letter_bank_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Tile settings
tile_size = 90
tile_spacing = 10
tile_margin = 3
tile_font = pygame.font.SysFont(None, 24)
tile_color = (255, 255, 255)

pygame.display.set_caption('WORDWHIZ')
pygame.display.set_icon(icon)

def scale_button(button, factor):
    """Scale the button image by a factor."""
    button_rect = button.get_rect(center=button_rect.center)
    return pygame.transform.scale(button, (int(button_rect.width * factor), int(button_rect.height * factor)))

def mode1():
    mode1_image = pygame.image.load("img/mode1.jpg")
    screen.blit(mode1_image, mode1_image.get_rect(center=(width // 2, height // 2)))
    if current_screen == "mode1" and "mode2":   
        draw_letter_bank()   
        draw_tiles()  
        
def modescreen():
    screen.blit(background, (0, 0))

    global mode1_button_rect

    button_spacing = 50 

    initial_y = height // 2

    mode1_button_rect = mode1_button.get_rect(center=(width // 2, height // 2 + 100))
    mode2_button_rect = mode2_button.get_rect(center=(width // 2, height // 2 + 300))  

    screen.blit(mode1_button, mode1_button_rect)
    screen.blit(mode2_button, mode2_button_rect) 
    pygame.display.update()


def draw_letter_bank():
    box_size = 50
    border_thickness = 2
    x_offset = 215
    y_offset = height - 230 
    
    lines = [
        "ABCDEFGHIJ",
        "KLMNOPQRST",
        "UVWXYZ"
    ]

    for line_index, line_letters in enumerate(lines):
        for col_index, letter in enumerate(line_letters):
            box_x = x_offset + col_index * (box_size + letter_bank_spacing)
            box_y = y_offset + line_index * (box_size + letter_bank_spacing)  
            
            # Draw the box
            pygame.draw.rect(screen, (255, 255, 255), (box_x, box_y, box_size, box_size), border_thickness)
            
            # Draw the letter
            letter_render = letter_bank_font.render(letter, True, letter_bank_color)
            letter_rect = letter_render.get_rect(center=(box_x + box_size // 2, box_y + box_size // 2))
            screen.blit(letter_render, letter_rect)

def draw_tiles():
    # Define starting position for tiles
    start_x = 300
    start_y = 300
    
    for row in range(5):
        for col in range(5):
            tile_x = start_x + col * (tile_size + tile_spacing)
            tile_y = start_y + row * (tile_size + tile_spacing)
            pygame.draw.rect(screen, tile_color, (tile_x, tile_y, tile_size, tile_size))
            pygame.draw.rect(screen, (0, 0, 0), (tile_x, tile_y, tile_size, tile_size), 2)
            pygame.display.update(pygame.Rect(tile_x, tile_y, tile_size, tile_size))

# Initial state
current_screen = "main"

letters_to_add = [] #for letters added 

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if current_screen == "main" and play_button_rect.collidepoint(event.pos):
                current_screen = "modescreen"   
            elif current_screen == "modescreen":
                if mode1_button_rect.collidepoint(event.pos):
                    current_screen = "mode1"   
            elif current_screen == "mode1" and home_button_rect.collidepoint(event.pos):
                current_screen = "main"
            elif current_screen == "main" and quit_button_rect.collidepoint(event.pos):
                pygame.quit()
                sys.exit()
        elif event.type == pygame.KEYDOWN:
            # Check if the pressed key is in the letter bank
            if event.unicode.upper() in letter_bank_letters:
                letters_to_add.append(event.unicode.upper())
            # Check if the pressed key is 'C' to clear the tiles
            elif event.key == pygame.K_c:
                letters_to_add.clear()  # Clear the letters to add
    
    screen.blit(background, (0, 0))  # Draw the background image

    if current_screen == "main":
        screen.blit(play_button, play_button_rect)   
        screen.blit(quit_button, quit_button_rect)   
    elif current_screen == "modescreen":
        modescreen()
    elif current_screen == "mode1":
        mode1()
        draw_tiles() 
        for idx, letter in enumerate(letters_to_add):
            tile_x = 300 + (idx % 5) * (tile_size + tile_spacing)
            tile_y = 300 + (idx // 5) * (tile_size + tile_spacing)
            letter_render = tile_font.render(letter, True, (0, 0, 0))
            letter_rect = letter_render.get_rect(center=(tile_x + tile_size // 2, tile_y + tile_size // 2))
            screen.blit(letter_render, letter_rect)
    
    pygame.display.update()
