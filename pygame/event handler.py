import pygame
pygame.init()

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        if event.type == pygame.KEYDOWN:
            print('a key has been pressed')
            
        if event.type == pygame.KEYUP:
            print('a key has just been released')
            
        if event.type == pygame.MOUSEMOTION:
            print('mouse is in motion')
pygame.quit()
