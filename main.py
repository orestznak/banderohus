import random
from os import listdir

import pygame
from pygame.constants import K_DOWN, K_LEFT, K_RIGHT, K_UP, QUIT

pygame.init()

WHITE = 255,255,255
BLACK = 0,0,0
BLUE=0,0,255
YELLOW=255,255,0
RED= 255,0,0
GREEN=0,255,0

font = pygame.font.SysFont('Verdana', 20)
 
FPS = pygame.time.Clock()

screen= width,height = 800, 600

main_surface = pygame.display.set_mode(screen)

IMGS_PATH = 'goose'

# ball= pygame.Surface((20,20))
# ball.fill((WHITE))

player_images=[pygame.transform.scale(pygame.image.load(IMGS_PATH + '/' + file).convert_alpha(),(40,60)) for file in listdir(IMGS_PATH)]

player = player_images[0]
player_rect = player.get_rect()
player_speed= 5


def creat_enemy():
    enemy = pygame.transform.scale(pygame.image.load('enemy.png').convert_alpha(),(40,40))
    # enemy.fill(RED)
    enemy_rect=pygame.Rect(width,random.randint(0,height), *enemy.get_size())
    enemy_speed = random.randint(2,5)
    return [enemy,enemy_rect, enemy_speed]

bg = pygame.transform.scale(pygame.image.load('background.png').convert(), screen)
bgX=0
bgX2 = bg.get_width()
bg_speed = 10

def creat_bonus():
    bonus = pygame.transform.scale(pygame.image.load('bonus.png').convert_alpha(),(60,60))
    # bonus.fill(GREEN)
    bonus_rect=pygame.Rect(random.randint(0,height),0, *bonus.get_size())
    bonus_speed = random.randint(2,5)
    return [bonus,bonus_rect, bonus_speed]

CREAT_ENEMY=pygame.USEREVENT + 1
pygame.time.set_timer(CREAT_ENEMY, 2500)

CREAT_BONUS=pygame.USEREVENT + 2
pygame.time.set_timer(CREAT_BONUS, 3500)

CHANGE_IMG=pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMG, 125)


enemies= []
bonuses=[]
countBonus=0
img_index=0

is_working=True
while is_working:
    FPS.tick(60)
    for event in pygame.event.get():
        if event.type == QUIT:
            is_working = False
            
        if event.type == CREAT_ENEMY:
            enemies.append(creat_enemy())
        
        if event.type == CREAT_BONUS:
            bonuses.append(creat_bonus())
        
        if event.type == CHANGE_IMG:
            img_index+=1
            
            if img_index == len(player_images):
                img_index = 0
            
            player =  player_images[img_index]
    
    pressed_keys = pygame.key.get_pressed()
        
    # main_surface.fill(bg)
    # main_surface.blit(bg,(0,0))
    bgX -= bg_speed
    bgX2-= bg_speed
    
    # плавний перехід фону
    if bgX < -bg.get_width():
        bgX = bg.get_width()
    if bgX2 < -bg.get_width():
        bgX2 = bg.get_width()
        
    main_surface.blit(bg,(bgX,0))
    main_surface.blit(bg,(bgX2,0))
        
    main_surface.blit(player, player_rect)
    
    main_surface.blit(font.render(str(countBonus),True,BLUE),(width-30,0))
    
    for enemy in enemies:
        enemy[1]=enemy[1].move(-enemy[2],0)
        main_surface.blit(enemy[0], enemy[1])
        
        if enemy[1].left<0:
            enemies.pop(enemies.index(enemy))
            
        if player_rect.colliderect(enemy[1]):
            is_working =False
    
    for bonus in bonuses:
        bonus[1]=bonus[1].move(0,bonus[2])
        main_surface.blit(bonus[0], bonus[1])
        
        if bonus[1].bottom>height:
            bonuses.pop(bonuses.index(bonus))
            
        if player_rect.colliderect(bonus[1]):
            bonuses.pop(bonuses.index(bonus))
            countBonus+=1
                   
    if pressed_keys[K_DOWN] and not (player_rect.bottom>=height):
        player_rect = player_rect.move(0,player_speed)
        
    if pressed_keys[K_UP] and not (player_rect.top<=0):
        player_rect = player_rect.move(0,-player_speed)
            
    if pressed_keys[K_LEFT] and not (player_rect.left <=0):
        player_rect = player_rect.move(-player_speed,0)
            
    if pressed_keys[K_RIGHT] and not (player_rect.right>=width):
        player_rect = player_rect.move(player_speed,0)
      
    pygame.display.flip()
            