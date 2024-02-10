import pygame
pygame.init()

#constants 
width, height = 1080, 1080
screen = pygame.display.set_mode((width, height))
background = pygame.image.load("img/tiles.png")
background_rect = background.get_rect(center=(540, 540))
icon = pygame.image.load("img/icon.png")

pygame.display.set_caption('WORDWHIZ')
pygame.display.set_icon(icon)



screen.fill("white")
screen.blit(background, background_rect)
pygame.display.update()

 
 
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    pygame.display.update()

