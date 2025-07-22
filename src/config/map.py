import pygame
from .constants import TILE_HEIGHT, TILE_WIDTH
# from .background import temple_tile

class Tile:
    def __init__(self, x, y):
        self.place = pygame.Rect(x, y, TILE_WIDTH, TILE_HEIGHT)
        self.bound = False
        # self.type = temple_tile

class Boundary(Tile):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.bound = True

    def checkCollision(self, hitbox):
        if self.place.colliderect(hitbox):
            return True

def load_map(map):
    tiles = []
    bound = []

    for i in range(len(map)):
        for j in range(len(map[0])):
            # if(map[i][j]=='x'):
                # tiles.append(Tile(j*TILE_WIDTH, i*TILE_HEIGHT))
            if(map[i][j]=='b' or map[i][j]=='r'):
                # tiles.append(Boundary(j*TILE_WIDTH, i*TILE_HEIGHT))
                bound.append(Boundary(j*TILE_WIDTH, i*TILE_HEIGHT).place)
                if map[i][j] == 'r':
                    tiles.append(Boundary(j*TILE_WIDTH, i*TILE_HEIGHT).place)
    
    return bound, tiles
            