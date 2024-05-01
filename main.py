import pygame
import sys
import random

pygame.init()

# Constants
clock = pygame.time.Clock()
width, height = 1080, 1080
screen = pygame.display.set_mode((width, height))
icon = pygame.image.load("img/icon.png")
background = pygame.image.load("img/main.jpg")
play_button = pygame.image.load("img/play.png")
play_button_size = quit_button_size = mode1_button_size = mode2_button_size = (width // 3, height // 8)  # Set the desired size of the button
play_button = pygame.transform.scale(play_button, play_button_size)  # Scale down the button image
play_button_rect = play_button.get_rect(center=(width // 2, height // 2 + 100))
quit_button = pygame.image.load("img/quit.png")
quit_button = pygame.transform.scale(quit_button, quit_button_size)
quit_button_rect = quit_button.get_rect(center=(width // 2, height // 2 + 300))
mode1_button = pygame.image.load("img/mode1.png")
mode1_button = pygame.transform.scale(mode1_button, mode1_button_size)
mode2_button = pygame.image.load("img/mode2.png")
mode2_button = pygame.transform.scale(mode2_button, mode2_button_size)
home_button = pygame.image.load("img/home.png")
home_button_size = (300, 300)
home_button = pygame.transform.scale(home_button, home_button_size)  # Scale down the home button image

# Letter bank settings
letter_bank_font = pygame.font.SysFont(None, 36)
letter_bank_spacing = 20
letter_bank_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Tile settings
tile_size = 90
tile_spacing = 10
tile_font = pygame.font.SysFont(None, 24)
tile_color = (255, 255, 255)
correct_tile_color = (0, 255, 0)  # Green
wrong_position_tile_color = (255, 255, 0)  # Yellow
wrong_letter_tile_color = (255, 0, 0)  # Red

pygame.display.set_caption('WORDWHIZ')
pygame.display.set_icon(icon)

# Function to choose a random word from words.py
def choose_random_word():
    with open("words.py", "r") as file:
        words = file.readlines()
        chosen_word = random.choice(words).strip()
        # Remove any quotation marks from the chosen word
        chosen_word = chosen_word.replace('"', '')
        print("Chosen word:", chosen_word)  
        return chosen_word

# Function to choose a random word from words2.py (Mode 2)
def choose_random_word_mode2():
    with open("words2.py", "r") as file:
        words = file.readlines()
        chosen_word = random.choice(words).strip()
        # Remove any quotation marks from the chosen word
        chosen_word = chosen_word.replace('"', '')
        print("Chosen word (Mode 2):", chosen_word)  
        return chosen_word

def mode1():
    mode1_image = pygame.image.load("img/mode1.jpg")
    screen.blit(mode1_image, mode1_image.get_rect(center=(width // 2, height // 2)))
    if current_screen == "mode1":
        draw_letter_bank()
        draw_tiles()
        # Blit home button on top right corner
        screen.blit(home_button, home_button.get_rect(topright=(width - 30, 10)))
    pygame.display.flip()

def mode2():
    mode2_image = pygame.image.load("img/mode2.jpg")
    screen.blit(mode2_image, mode2_image.get_rect(center=(width // 2, height // 2)))
    if current_screen == "mode2":
        draw_letter_bank()
        draw_tiles()
        # Blit home3 button on top right corner
        screen.blit(home_button, home_button.get_rect(topright=(width - 30, 10)))
    pygame.display.flip()

# Adjust mode screen function
def modescreen():
    screen.blit(background, (0, 0))

    global mode1_button_rect, mode2_button_rect

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
            letter_render = letter_bank_font.render(letter, True, (0, 0, 0))  # Black color for letters
            letter_rect = letter_render.get_rect(center=(box_x + box_size // 2, box_y + box_size // 2))
            screen.blit(letter_render, letter_rect)
             
def check_win_conditions():
    for row in range(5):
        all_correct = True  # Flag to track if all tiles in the row are correct
        for col in range(5):
            if row * 5 + col < len(letters_to_add):  
                if letters_to_add[row * 5 + col].upper() != chosen_word[col].upper():
                    all_correct = False  # If any tile is not green, set the flag to False
                    break  
            else:
                all_correct = False  # If any tile is not filled, set the flag to False
                break   
        if all_correct:
            if current_screen == "mode2":   
                show_popup("img/youwin2.jpg")  
            else:
                show_popup("img/youwin.jpg")   
            return  
    
    # If all tiles are filled and the typed word doesn't match the chosen word
    if all_tiles_filled() and chosen_word.upper() != typed_word.upper():
        if current_screen == "mode2":   
            show_popup("img/youlost2.jpg")  
        else:
            show_popup("img/youlost.jpg") 
        pygame.quit()
        sys.exit()


def draw_tiles():
    # Define starting position for tiles
    start_x = 300
    start_y = 300

    for row in range(5):
        for col in range(5):
            tile_x = start_x + col * (tile_size + tile_spacing)
            tile_y = start_y + row * (tile_size + tile_spacing)

            # Check if the letter exists at this position
            entered_letter = None
            if row * 5 + col < len(letters_to_add):
                entered_letter = letters_to_add[row * 5 + col]

            # Determine the color of the tile
            if entered_letter and entered_letter.upper() == chosen_word[col]:
                color = correct_tile_color  # Green if correct letter in correct position
            elif entered_letter and entered_letter.upper() in chosen_word:
                color = wrong_position_tile_color  # Yellow if correct letter in wrong position
            elif entered_letter:
                color = wrong_letter_tile_color  # Red if incorrect letter
            else:
                color = tile_color  # Default color

            pygame.draw.rect(screen, color, (tile_x, tile_y, tile_size, tile_size))
            pygame.draw.rect(screen, (0, 0, 0), (tile_x, tile_y, tile_size, tile_size), 2)

            # Redraw letter if exists
            if entered_letter:
                letter_render = tile_font.render(entered_letter, True, (0, 0, 0))
                letter_rect = letter_render.get_rect(center=(tile_x + tile_size // 2, tile_y + tile_size // 2))
                screen.blit(letter_render, letter_rect)

    # Check for win conditions after drawing all tiles
    check_win_conditions()
    pygame.display.update()

def show_popup(image_path):
    popup_image = pygame.image.load(image_path)
    screen.blit(popup_image, (width//2 - popup_image.get_width()//2, height//2 - popup_image.get_height()//2))
    pygame.display.update()
    pygame.time.delay(2000)  # Show for 2 seconds
    pygame.quit()
    sys.exit()

def all_tiles_filled():
    return len(letters_to_add) == 25

# Initial state
current_screen = "main"
typed_words = ["", "", "", "", ""]
letters_to_add = []  # letters being added as user types
chosen_word = ""
typed_word = ""

while True:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Button click handling code
            if current_screen == "main" and play_button_rect.collidepoint(event.pos):
                current_screen = "modescreen"
            elif current_screen == "modescreen":
                if mode1_button_rect.collidepoint(event.pos):
                    current_screen = "mode1"
                    chosen_word = choose_random_word()  # Choose word from words.py for mode 1
                elif mode2_button_rect.collidepoint(event.pos):
                    current_screen = "mode2"
                    chosen_word = choose_random_word_mode2()  # Choose word from words2.py for mode 2
            elif current_screen in ["mode1", "mode2"] and home_button.get_rect(topright=(width - 50, 50)).collidepoint(event.pos):  
                current_screen = "main"
                typed_words = ["", "", "", "", ""]  # Reset typed_words to empty list
                letters_to_add = []  # Reset letters_to_add to empty list
                chosen_word = ""  # Reset chosen_word
                typed_word = ""
            elif current_screen == "main" and quit_button_rect.collidepoint(event.pos):
                pygame.quit()
                sys.exit()
        elif event.type == pygame.KEYDOWN:
            # Key press handling code
            #if event.key == pygame.K_BACKSPACE:
               # if len(letters_to_add) > 0:
                   # letters_to_add.pop()
               # draw_letter_bank()
                #draw_tiles()
            if event.unicode.upper() in letter_bank_letters:
                row_index = len(letters_to_add) // 5
                if len(typed_words[row_index]) <= 5:
                    letters_to_add.append(event.unicode.upper())
                    typed_words[row_index] += event.unicode.upper()
                    typed_word = "".join(filter(str.isalpha, typed_words[row_index]))
                    if typed_word.upper() == chosen_word.upper():
                        print("Typed word matches chosen word")
                        chosen_word = choose_random_word() if current_screen == "mode1" else choose_random_word_mode2()
                        show_popup("img/youwin.jpg")
                        print("Chosen word:", chosen_word)  
                    elif len(letters_to_add) % 5 == 0:
                        if row_index < 5 and chosen_word != typed_word:
                            typed_words[row_index] = ""
                            print("Typed word :", typed_word)
                        else:
                            show_popup("img/youlost.jpg")
                            pygame.quit()
                            sys.exit()

    # Drawing code
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

    pygame.display.flip()
