import pygame
import sys

pygame.init()

# Constants
width, height = 1080, 1080
screen = pygame.display.set_mode((width, height))
icon = pygame.image.load("img/icon.png")
background = pygame.image.load("img/main.png")
play_button = pygame.image.load("img/play.png")  
play_button_original = play_button.copy()  # Store original size for scaling
play_button_rect = play_button.get_rect(center=(-200, height // 2 + 100))  # Start play button off the left side of the screen
quit_button = pygame.image.load("img/quit.png")  # Load quit button image
quit_button_original = quit_button.copy()
quit_button_rect = quit_button.get_rect(center=(width + 200, height // 2 + 300))  # Start quit button off the right side of the screen
home_button = pygame.image.load("img/home2.png")  
home_button_original = home_button.copy()
home_button_rect = home_button.get_rect(topright=(width - (-60), -90))  # Position home button at the top right corner
mode1_button = pygame.image.load("img/mode1bttn.png") 
mode1_button_original = mode1_button.copy()
mode2_button = pygame.image.load("img/mode2bttn.png") 
mode2_button_original = mode2_button.copy()
home1_button = pygame.image.load("img/home1.png") 
home1_button_original = home1_button.copy()

pygame.display.set_caption('WORDWHIZ')
pygame.display.set_icon(icon)

def scale_button(button, factor):
    """Scale the button image by a factor."""
    button_rect = button.get_rect(center=button_rect.center)
    return pygame.transform.scale(button, (int(button_rect.width * factor), int(button_rect.height * factor)))

def mode1():
    """Function to switch to mode1 image."""
    mode1_image = pygame.image.load("img/mode1.jpg")
    screen.blit(mode1_image, mode1_image.get_rect(center=(width // 2, height // 2)))
    screen.blit(home_button, home_button_rect)  # Blit home button
    pygame.display.update()

def mode2():
    """Function to switch to mode2 image."""
    mode2_image = pygame.image.load("img/mode2.jpg")
    screen.blit(mode2_image, mode2_image.get_rect(center=(width // 2, height // 2)))
    screen.blit(home_button, home_button_rect)  # Blit home button
    pygame.display.update()


def modescreen():
    """Function to display the mode screen."""
    screen.blit(background, (0, 0))

    # Define global variables for rect objects to enable collision detection
    global mode1_button_rect, mode2_button_rect, home1_button_rect

    # Calculate vertical spacing between buttons
    button_spacing = 50 

    # Calculate initial y-coordinate for the first button
    initial_y = height // 2

    # Blit mode1 button
    mode1_button_rect = mode1_button.get_rect(center=(width // 2, initial_y))
    screen.blit(mode1_button, mode1_button_rect)

    # Blit mode2 button
    mode2_button_rect = mode2_button.get_rect(center=(width // 2, initial_y + mode1_button.get_height()//4 + button_spacing))
    screen.blit(mode2_button, mode2_button_rect)
    
    # Blit home1 button
    home1_button_rect = home1_button.get_rect(center=(width // 2, initial_y + mode1_button.get_height()//2 + 2 * button_spacing))
    screen.blit(home1_button, home1_button_rect)

    pygame.display.update()


# Initial state
current_screen = "main"
play_button_speed = 7  # Adjust speed 
quit_button_speed = 7

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if current_screen == "main" and play_button_rect.collidepoint(event.pos):
                current_screen = "modescreen"  # Change current screen to modescreen
            elif current_screen == "modescreen":
                if mode1_button_rect.collidepoint(event.pos):
                    current_screen = "mode1"  # Proceed to mode1
                elif mode2_button_rect.collidepoint(event.pos):
                    current_screen = "mode2"  # Proceed to mode2
                elif home1_button_rect.collidepoint(event.pos):
                    current_screen = "main"  # Go back to main screen
            elif current_screen == "mode1" and home_button_rect.collidepoint(event.pos):
                current_screen = "main"

    screen.blit(background, (0, 0))  # Draw the background image

    if current_screen == "main":
        if play_button_rect.centerx < width // 2:
            play_button_rect.centerx += play_button_speed
        if quit_button_rect.centerx > width // 2:
            quit_button_rect.centerx -= quit_button_speed
        screen.blit(play_button, play_button_rect)  # Blit play button
        screen.blit(quit_button, quit_button_rect)  # Blit quit button
    elif current_screen == "modescreen":
        modescreen()
    elif current_screen == "mode1":
        mode1()
    elif current_screen == "mode2":
        mode2()

    pygame.display.update()
