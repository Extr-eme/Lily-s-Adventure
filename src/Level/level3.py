import pygame
from sys import exit
from random import randint, choice
from ..config.animations import walk_frames  

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = walk_frames[0][0]
        player_walk_2 = walk_frames[0][1]
        player_walk_3 = walk_frames[0][2]
        player_walk_4 = walk_frames[0][3]
        player_walk_5 = walk_frames[0][4]
        player_walk_6 = walk_frames[0][5]

        self.player_walk = [
            player_walk_1,
            player_walk_2,
            player_walk_3,
            player_walk_4,
            player_walk_5,
            player_walk_6,
        ]
        self.player_index = 0
        self.player_jump = walk_frames[0][4]

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80, 850))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('Assets/level3/audio/jump.mp3')
        self.jump_sound.set_volume(0.5)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 850:
            self.gravity = -17
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 850:
            self.rect.bottom = 850

    def animation_state(self):
        if self.rect.bottom < 850:
            self.image = self.player_jump
        else:
            self.player_index += 0.18
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def reset(self):
        self.rect.midbottom = (80, 850)
        self.gravity = 0

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()
        if self.rect.x <= 1350:
            self.rect.x += 1.2

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == 'fly':
            fly_1 = pygame.image.load('Assets/level3/graphics/fly/Fly1.png').convert_alpha()
            fly_2 = pygame.image.load('Assets/level3/graphics/fly/Fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 720
        else:
            snail_1 = pygame.image.load('Assets/level3/graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('Assets/level3/graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 850

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(1500, 1600), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

def display_score(start_time):
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    return current_time

def collision_sprite(player, obstacle_group):
    global failed_attempt, game_active
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        player.sprite.reset()
        game_active = False
        failed_attempt = True
        return False
    else:
        return True

pygame.init()
screen = pygame.display.set_mode((1400, 900))
pygame.display.set_caption('Run Muna Run')
clock = pygame.time.Clock()

def preload():
    bg_music = pygame.mixer.Sound('Assets/level3/audio/music.wav')
    bg_music.play(loops=-1)




def draw(SCREEN, clock):
    test_font = pygame.font.Font('Assets/level3/font/Pixeltype.ttf', 50)
    game_active = False
    start_time = 0
    score = 0
    level_completed = False
    failed_attempt = False

    # Timer
    obstacle_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(obstacle_timer, 1500)

    # Groups
    player = pygame.sprite.GroupSingle()
    player.add(Player())
    obstacle_group = pygame.sprite.Group()

    sky_surface = pygame.image.load('Assets/level3/mountain.png').convert()
    ground_surface = pygame.image.load('Assets/level3/groundblack.png').convert()
    intro_surface = pygame.image.load('Assets/level3/introscreen.png').convert_alpha()
    outro_surface = pygame.image.load('Assets/level3/outroscreen.png').convert_alpha()

    first_line = test_font.render('Now, the final test remains.', False, (111, 196, 169))
    first_line_rect = first_line.get_rect(center=(700, 100))
    second_line = test_font.render('Can Muna escape with her fortune?', False, (111, 196, 169))
    second_line_rect = second_line.get_rect(center=(700, 150))
    third_line = test_font.render('The evil Snails and evil Flies are coming!', False, (111, 196, 169))
    third_line_rect = third_line.get_rect(center=(700, 200))

    game_message = test_font.render('Press space to run', False, (111, 196, 169))
    game_message_rect = game_message.get_rect(center=(700, 700))

    # preload()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if game_active and not level_completed:
                if event.type == obstacle_timer and player.sprite.rect.x <= 1100:
                    obstacle_group.add(Obstacle(choice(['fly', 'fly', 'snail', 'snail', 'snail'])))
            elif not game_active and failed_attempt:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    failed_attempt = False
                    obstacle_group.empty()
                    player.sprite.reset()
                    score = 0
                    game_active = True
                    start_time = int(pygame.time.get_ticks() / 1000)
            elif not game_active and not failed_attempt:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    level_completed = False
                    obstacle_group.empty()
                    player.sprite.reset()
                    score = 0
                    game_active = True
                    start_time = int(pygame.time.get_ticks() / 1000)

        if game_active and not level_completed:
            SCREEN.blit(sky_surface, (0, 0))
            SCREEN.blit(ground_surface, (0, 850))
            score = display_score(start_time)

            player.draw(SCREEN)
            player.update()

            obstacle_group.draw(SCREEN)
            obstacle_group.update()

            game_active = collision_sprite(player, obstacle_group)

            if player.sprite.rect.x >= 300:
                level_completed = True

        elif level_completed:
            SCREEN.blit(outro_surface, (0, 0))
            level_complete_text = test_font.render('Level Completed', False, (111, 196, 169))
            level_complete_rect = level_complete_text.get_rect(center=(700, 450))
            SCREEN.blit(level_complete_text, level_complete_rect)
            return True

        elif failed_attempt:
            SCREEN.blit(intro_surface, (0, 0))
            try_again_text = test_font.render('TRY AGAIN!', False, (111, 196, 169))
            try_again_rect = try_again_text.get_rect(center=(700, 400))
            SCREEN.blit(first_line, first_line_rect)
            SCREEN.blit(second_line, second_line_rect)
            SCREEN.blit(third_line, third_line_rect)
            SCREEN.blit(try_again_text, try_again_rect)

        else:
            SCREEN.blit(intro_surface, (0, 0))
            score_message = test_font.render('TRY AGAIN!', False, (111, 196, 169))
            score_message_rect = score_message.get_rect(center=(700, 400))
            SCREEN.blit(first_line, first_line_rect)
            SCREEN.blit(second_line, second_line_rect)
            SCREEN.blit(third_line, third_line_rect)

            if score == 0:
                SCREEN.blit(game_message, game_message_rect)
            else:
                SCREEN.blit(score_message, score_message_rect)

        pygame.display.update()
        clock.tick(60)
