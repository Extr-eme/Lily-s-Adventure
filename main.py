import pygame

from src.config.constants import FPS, SCREEN_HEIGHT, SCREEN_WIDTH  #import constants from constants.py
from src.Level import level1
from src.Level import level2
from src.Level import level3

pygame.init()



#1. Game Window
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
print("screen blited")
pygame.display.set_caption("Lily's Adventure")

def load_assets():
    level1.preload()

def main():
    clock = pygame.time.Clock()
    
    L1, L2, L3 = False, False, False
    
    level = 1
    load_assets()
    outro_surface = pygame.image.load('Assets/level3/outroscreen.png').convert_alpha()


#2. Game Loop
    run = True
    while run:
        clock.tick(FPS)                 #LIMIT FPS
#3. Game Event Handler

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()               

        match level:
            case 1:
                L1=level1.draw(SCREEN, keys)
                # L1 = True
                if L1:
                    level = 2
                    continue
            case 2:
                SCREEN.blit(outro_surface, (0, 0))
                L2=level2.draw(SCREEN, clock)
                if L2:
                    level = 3
                    continue
            case 3:
                L3 = level3.draw(SCREEN, clock)
                if L3:
                    level = 'end'
                    continue
            
            case 'end':
                print('Over')
                SCREEN.blit(pygame.Rect(0,0,SCREEN_WIDTH, SCREEN_HEIGHT))

    pygame.quit()

if __name__ == '__main__':
    main()
