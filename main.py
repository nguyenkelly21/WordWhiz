import pygame
import sys

pygame.init()

# Constants
width, height = 1080, 1080
screen = pygame.display.set_mode((width, height))
icon = pygame.image.load("img/icon.png")
background = pygame.image.load("img/main.png")
play_button = pygame.image.load("img/play.png")  # Load play button image
play_button_original = play_button.copy()  # Store original size for scaling
play_button_rect = play_button.get_rect(center=(-200, height // 2 + 100))  # Start play button off the left side of the screen
quit_button = pygame.image.load("img/quit.png")  # Load quit button image
quit_button_original = quit_button.copy()
quit_button_rect = quit_button.get_rect(center=(width + 200, height // 2 + 300))  # Start quit button off the right side of the screen
home_button = pygame.image.load("img/home.png")  # Load home button image
home_button_original = home_button.copy()
home_button_rect = home_button.get_rect(topright=(width - 5, 1))  # Position home button at the top right corner

pygame.display.set_caption('WORDWHIZ')
pygame.display.set_icon(icon)

def scale_button(button, factor):
    """Scale the button image by a factor."""
    button_rect = button.get_rect(center=button_rect.center)
    return pygame.transform.scale(button, (int(button_rect.width * factor), int(button_rect.height * factor)))

def mode1():
    """Function to switch to mode1 image."""
    mode1_image = pygame.image.load("img/mode1.png")
    screen.blit(mode1_image, mode1_image.get_rect(center=(width // 2, height // 2)))
    screen.blit(home_button, home_button_rect)  # Blit home button
    pygame.display.update()

# Initial state
current_screen = "main"
play_button_speed = 5  # Adjust speed as needed
quit_button_speed = 5

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if current_screen == "main" and play_button_rect.collidepoint(event.pos):
                current_screen = "mode1"
            elif current_screen == "main" and quit_button_rect.collidepoint(event.pos):
                pygame.quit()
                sys.exit()
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
    elif current_screen == "mode1":
        mode1()

    pygame.display.update()
