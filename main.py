import pygame
import sys
import random

pygame.init()

# Constants
width, height = 1080,1080
screen = pygame.display.set_mode((width, height))
icon = pygame.image.load("img/icon.png")
background = pygame.image.load("img/main.png")
play_button = pygame.image.load("img/play.png")
play_button_original = play_button.copy()
play_button_rect = play_button.get_rect(center=(width // 2, height // 2 + 100))
quit_button = pygame.image.load("img/quit.png")
quit_button_rect = quit_button.get_rect(center=(width // 2, height // 2 + 300))
quit_button_original = quit_button.copy()
mode1_button = pygame.image.load("img/mode1bttn.png")
mode2_button = pygame.image.load("img/mode2bttn.png")
mode1_button_original = mode1_button.copy()
mode2_button_original = mode2_button.copy()
home_button = pygame.image.load("img/home2.png")
home_button_original = home_button.copy()
home_button_size = (300, 300)
home_button = pygame.transform.scale(home_button, home_button_size)  # Scale down the home button image
you_win_image = pygame.image.load("img/youwin.jpg")

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

# Function to choose a random word from words.py
def choose_random_word():
    with open("words.py", "r") as file:
        words = file.readlines()
        return random.choice(words).strip()

# Pop-up message function
def show_popup(message):
    pygame.font.init()
    font = pygame.font.SysFont(None, 100)
    text = font.render(message, True, (255, 0, 0))
    screen.blit(text, (width//2 - text.get_width()//2, height//2 - text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(2000)  # Show for 2 seconds

def scale_button(button, factor):
    button_rect = button.get_rect(center=button_rect.center)
    return pygame.transform.scale(button, (int(button_rect.width * factor), int(button_rect.height * factor)))

def mode1():
    mode1_image = pygame.image.load("img/mode1.jpg")
    screen.blit(mode1_image, mode1_image.get_rect(center=(width // 2, height // 2)))
    if current_screen == "mode1":
        draw_letter_bank()
        draw_tiles()
        # Blit home button on top right corner
        screen.blit(home_button, home_button.get_rect(topright=(width - 50, 50)))

def mode2():
    mode2_image = pygame.image.load("img/mode2.jpg")
    screen.blit(mode2_image, mode2_image.get_rect(center=(width // 2, height // 2)))
    if current_screen == "mode2":
        draw_letter_bank()
        draw_tiles()
        # Blit home button on top right corner
        screen.blit(home_button, home_button.get_rect(topright=(width - 50, 50)))

def modescreen():
    screen.blit(background, (0, 0))

    global mode1_button_rect, mode2_button_rect

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

            # Determine the background color based on whether the letter has been typed
            if letter in letters_to_add:
                box_color = (255, 0, 0)  # red color for typed letters
            else:
                box_color = (255, 255, 255)  # Default white color

            # Draw the box
            pygame.draw.rect(screen, box_color, (box_x, box_y, box_size, box_size), border_thickness)

            # Draw the letter
            letter_render = letter_bank_font.render(letter, True, (0, 0, 0))  # White color for letters
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
            # Draw the letter on the tile if available
            if row * 5 + col < len(letters_to_add):
                letter = letters_to_add[row * 5 + col]
            else:
                letter = ""  # No letter to display
            letter_render = tile_font.render(letter, True, (0, 0, 0))
            letter_rect = letter_render.get_rect(center=(tile_x + tile_size // 2, tile_y + tile_size // 2))
            screen.blit(letter_render, letter_rect)

    pygame.display.flip()  # Update the display

def show_try_again_popup():
    pygame.font.init()
    font = pygame.font.SysFont(None, 50)
    text = font.render("Try again tomorrow", True, (255, 0, 0))
    screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(2000)  # Show for 2 seconds

# Initial state
current_screen = "main"

# Create a list to store typed words for each row
typed_words = ["", "", "", "", ""]

letters_to_add = []  # letters being added as user types

# Choose a random word
chosen_word = choose_random_word()
print("Word:", chosen_word)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check button clicks based on the current screen
            if current_screen == "main" and play_button_rect.collidepoint(event.pos):
                current_screen = "modescreen"
            elif current_screen == "modescreen":
                if mode1_button_rect.collidepoint(event.pos):
                    current_screen = "mode1"
                elif mode2_button_rect.collidepoint(event.pos):
                    current_screen = "mode2"
            elif current_screen in ["mode1", "mode2"] and home_button.get_rect(topright=(width - 50, 50)).collidepoint(
                    event.pos):  # Check if home button is clicked
                current_screen = "main"
            elif current_screen == "main" and quit_button_rect.collidepoint(event.pos):
                pygame.quit()
                sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if len(letters_to_add) > 0:
                    letters_to_add.pop()
                draw_letter_bank()
                draw_tiles()
            elif event.key == pygame.K_c:
                letters_to_add.clear()
            elif event.unicode.upper() in letter_bank_letters:
                row_index = len(letters_to_add) // 5
                if len(letters_to_add) % 5 == 0:
                    if row_index < 5:
                        typed_words[row_index] = ""
                    else:
                        show_try_again_popup()
                        continue
                if len(typed_words[row_index]) < 5:
                    letters_to_add.append(event.unicode.upper())
                    typed_words[row_index] += event.unicode.upper()
                    typed_word = "".join(filter(str.isalpha, typed_words[row_index]))
                    print("Typed word (Row", row_index + 1, "):", typed_word)
                    print("Chosen word:", chosen_word)
                    if typed_word.upper() == chosen_word.upper():
                        print("Typed word matches chosen word")
                        screen.blit(you_win_image, you_win_image.get_rect(center=(width // 2, height // 2)))
                        pygame.display.update()
                        pygame.time.delay(2000)
                        chosen_word = choose_random_word()



    screen.blit(background, (0, 0))  # Draw the background image

    if current_screen == "main":
        screen.blit(play_button, play_button_rect)
        screen.blit(quit_button, quit_button_rect)
    elif current_screen == "modescreen":
        modescreen()
    elif current_screen == "mode1":
        mode1()
    elif current_screen == "mode2":
        mode2()

    pygame.display.update()
