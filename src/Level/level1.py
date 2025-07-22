import pygame
import os
import math
import random
from ..config.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from ..config.movements import Character_state
from ..config.map import load_map
from ..config import map_sketch
from ..config.animations import shoot, idle

pygame.font.init()
font1= pygame.font.SysFont("Times New Roman", 32, bold=False)
font2= pygame.font.SysFont("Times New Roman", 80, bold=True)

SKELETONS= []
SKELETONS_X= []
SKELETONS_Y= []
SKELETONSX_CHANGE= []
SKELETONSY_CHANGE= []
NO_of_SKELETONS= 10
BORDER_POS = 300
TOTAL_SKELETONS= 25
COLLIDED_SKELETONS=0
SKELETONS_CROSSED= 5

# text= font.render("Collided Skeletons: " + str(COLLIDED_SKELETONS), True, (255,255,255))
# text_rect = text.get_rect(center=(150, 20))

BULLETS= pygame.transform.scale((pygame.image.load(os.path.join('Assets', 'Background', 'bullet.png'))), (20,20))
BULLETS_X= 0
BULLETS_Y= 0
BULLETS_STATE= "ready"
BULLETS_X_CHANGE= 10
BULLETS_Y_CHANGE= 0

BORDER= pygame.Rect(BORDER_POS, 0, 5, SCREEN_HEIGHT)
BLACK= (0,0,0)

BOUND, TILE = load_map(map_sketch.map_level1)

character_state=Character_state(BORDER_POS-50, SCREEN_HEIGHT/2 - 50, BOUND)

     

def preload():
    global LEVEL1_BG_IMAGE, BUFFER
    
    LEVEL1_BG= pygame.image.load(os.path.join('Assets','Background','level1-bg.png')).convert()
    LEVEL1_BG_IMAGE= pygame.transform.scale(LEVEL1_BG, (SCREEN_WIDTH, SCREEN_HEIGHT))

    ROCK_BG = pygame.image.load(os.path.join('Assets','Background','Rock.png'))
    
    for skeletons in range(NO_of_SKELETONS):
        SKELETONS.append(pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Background' ,'skeletons.png')).convert_alpha(), (50,70)))
        SKELETONS_X.append(random.randint(1100,1350))
        SKELETONS_Y.append(random.randint(50,850))
        SKELETONSX_CHANGE.append(300)
        SKELETONSY_CHANGE.append(1)

    ROCK = pygame.Surface((50, len(TILE)* 50))
    for i, rock in enumerate(TILE):
        ROCK.blit(ROCK_BG, (0, i* 50))

    
    BUFFER = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    BUFFER.blit(LEVEL1_BG_IMAGE, (0, 0))
    # pygame.draw.rect(BUFFER, BLACK, (BORDER_POS, 0, 5, SCREEN_HEIGHT))
    BUFFER.blit(ROCK, (TILE[0].left,TILE[0].top + 15))
    
def fire_bullets(SCREEN,x,y):
    global BULLETS_STATE
    BULLETS_STATE= "fire"
    SCREEN.blit(BULLETS, (x+16,y+10))
    if x>SCREEN_WIDTH:
        BULLETS_STATE= "ready"
        BULLETS_X= BORDER_POS-50
    
def bullet_control(SCREEN, keys, POS_X, POS_Y):
    global BULLETS_STATE, BULLETS_X, BULLETS_Y
    if keys[pygame.K_SPACE]:
        if BULLETS_STATE == "ready":
            character_state.frame_type = shoot
            BULLETS_X= POS_X
            BULLETS_Y= POS_Y
            fire_bullets(SCREEN, BULLETS_X, BULLETS_Y)
            

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow((enemyX-bulletX),2)+ math.pow((enemyY-bulletY),2))
    if distance < 40:
        print("collided")
        return True
    else:
        return False
    


    

def draw(SCREEN, keys):
     
    if character_state.frame_type != shoot:
        character_state.character_movement(keys)
    else:  
        if shoot.timer == 59:
            shoot.timer = 0
            character_state.frame_type = idle[character_state.direction]
        
    POS_X= character_state.x
    POS_Y= character_state.y
    global BULLETS_X, BULLETS_STATE, COLLIDED_SKELETONS, SKELETONS_CROSSED

    COLLIDED_TEXT= font1.render("Collided Skeletons: " + str(COLLIDED_SKELETONS), True, (255,255,255))
    CROSSED_TEXT= font1.render("Skeletons Crossed: " + str(SKELETONS_CROSSED), True, (0,0,0))
    GAME_OVER_TEXT= font2.render("GAME OVER!", True, (0,0,0))
    LEVEL_COMPLETE_TEXT= font2.render("LEVEL COMPLETED!", True, (0,0,0))
    
    SCREEN.blit(BUFFER, (0,0))
    for i in range(NO_of_SKELETONS):
        SCREEN.blit(SKELETONS[i], (SKELETONS_X[i], SKELETONS_Y[i]))
        
        SKELETONS_Y[i] += SKELETONSY_CHANGE[i]
        
        if SKELETONS_Y[i] > 850:
            SKELETONSY_CHANGE[i]= -1
            SKELETONS_X[i] -= SKELETONSX_CHANGE[i]
            
        elif SKELETONS_Y[i] < 0:
            SKELETONSY_CHANGE[i]= 1
            SKELETONS_X[i] -= SKELETONSX_CHANGE[i]
            
        collision=isCollision(SKELETONS_X[i], SKELETONS_Y[i], BULLETS_X, BULLETS_Y)
        if collision:
            BULLETS_X= BORDER_POS-50
            BULLETS_STATE= "ready"
            SKELETONS_X[i]= random.randint(1100,1350)
            SKELETONS_Y[i]= random.randint(50,850)
            COLLIDED_SKELETONS += 1
            print(COLLIDED_SKELETONS)
            
            
            
            if COLLIDED_SKELETONS >= TOTAL_SKELETONS:
                SCREEN.blit(LEVEL_COMPLETE_TEXT, (330,400))
                pygame.display.update()
                pygame.time.delay(5000)
                SKELETONS_X[i]= 2000
                return True
            
        SCREEN.blit(COLLIDED_TEXT, (0,0))
            
        if SKELETONS_X[i]<BORDER_POS:
            SKELETONS_CROSSED -= 1
            SKELETONS_X[i]= random.randint(1100,1350)
            SKELETONS_Y[i]= random.randint(50,850)
            print(SKELETONS_CROSSED)

        SCREEN.blit(CROSSED_TEXT, (1100,0))
            
        if SKELETONS_CROSSED == 0:
            SCREEN.blit(GAME_OVER_TEXT, (450, 400))
            pygame.display.update()
            pygame.time.delay(5000)
            
            return True  # Yo false garda hang hunxa haryo vane.... ahile next level janxa hare pani
            
            
    bullet_control(SCREEN, keys, POS_X, POS_Y)
    
    
    if BULLETS_STATE == "fire":
        
        BULLETS_X += BULLETS_X_CHANGE
        fire_bullets(SCREEN, BULLETS_X, BULLETS_Y)
    
    
    
    SCREEN.blit(character_state.frame_type.animate(),(character_state.x,character_state.y))

    pygame.display.update()

    return False