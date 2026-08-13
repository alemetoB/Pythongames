import pygame
pygame.init()

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 500

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

running = False
sprinting = False

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                running = True
            if event.type == pygame.K_LSHIFT:
                sprinting = True
                    
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                running = False      
                        

if running == True:
    print('dash')
if sprinting == True:
    print('super dash')
                
                
pygame.quit()


