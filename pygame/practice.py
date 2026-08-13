import pygame
pygame.init()

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

pause = False

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pause = True
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                pause = False

                
if pause == True:
      print("pausing")
            
        

        
pygame.quit()
