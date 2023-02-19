import pygame, sys
from pygame.locals import *
import random
from random import randint
import math
import time
pygame.init()
pygame.key.set_repeat(50)

class Player:
    def __init__(self, pos_x, pos_y):
        self.moving_left = False
        self.moving_right = False
        self.moving_down = False
        self.moving_high = False
        self.x = pos_x
        self.y = pos_y
        self.sprites_high = []
        self.sprites_high.append(pygame.image.load('up_0.png'))
        self.sprites_high.append(pygame.image.load('up_1.png'))
        self.sprites_high.append(pygame.image.load('up_2.png'))
        self.sprites_high.append(pygame.image.load('up_3.png'))
        self.sprites_down = []
        self.sprites_down.append(pygame.image.load('down_0.png'))
        self.sprites_down.append(pygame.image.load('down_1.png'))
        self.sprites_down.append(pygame.image.load('down_2.png'))
        self.sprites_down.append(pygame.image.load('down_3.png'))
        self.sprites_right = []
        self.sprites_right.append(pygame.image.load('right_0.png'))
        self.sprites_right.append(pygame.image.load('right_1.png'))
        self.sprites_right.append(pygame.image.load('right_2.png'))
        self.sprites_right.append(pygame.image.load('right_3.png'))
        self.sprites_left = []
        self.sprites_left.append(pygame.image.load('left_0.png'))
        self.sprites_left.append(pygame.image.load('left_1.png'))
        self.sprites_left.append(pygame.image.load('left_2.png'))
        self.sprites_left.append(pygame.image.load('left_3.png'))
        self.current_sprite = 0
        self.image = pygame.image.load('player.png')
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x,self.y]
        self.vie = 50
        self.max_vie = 50
       
        
    def mouvement_haut(self):
        self.moving_high = True

        
    def mouvement_bas(self):
        self.moving_down = True

        
    def mouvement_droite(self):
        self.moving_right = True

        
    def mouvement_gauche(self):
        self.moving_left = True
    
    def draw(self):
        screen.blit(self.image, self.rect)
        
        
        
    def barre_vie(self):
        couleur_barre_vie = (111, 210, 46)
        couleur_fond_barre = (0, 0, 0)
        if self.vie <= 25 and self.vie > 10:
            couleur_barre_vie = (252, 126, 0)
        elif self.vie <= 10:
            couleur_barre_vie = (255, 0, 0)
        
        barre_position = [self.rect[0] + 10, self.rect[1] - 10, self.vie, 6]
        barre_position_fond = [self.rect[0] + 10, self.rect[1] - 10, self.max_vie, 6]
        
        pygame.draw.rect(screen, couleur_fond_barre, barre_position_fond)
        pygame.draw.rect(screen, couleur_barre_vie, barre_position)
   
                
                
                
    

    def update(self, speed):
        if self.moving_high == True:
            self.current_sprite += speed
            if int(self.current_sprite) >= len(self.sprites_high):
                self.current_sprite = 0
                self.moving_high = False
            self.image = self.sprites_high[int(self.current_sprite)]
            
        if self.moving_down == True:
            self.current_sprite += speed
            if int(self.current_sprite) >= len(self.sprites_down):
                self.current_sprite = 0
                self.moving_down = False
            self.image = self.sprites_down[int(self.current_sprite)]
            
            
        if self.moving_left == True:
            self.current_sprite += speed
            if int(self.current_sprite) >= len(self.sprites_left):
                self.current_sprite = 0
                self.moving_left = False
            self.image = self.sprites_left[int(self.current_sprite)]
            
            
        if self.moving_right == True:
            self.current_sprite += speed
            if int(self.current_sprite) >= len(self.sprites_right):
                self.current_sprite = 0
                self.moving_right = False
            self.image = self.sprites_right[int(self.current_sprite)]

        
pygame.init()
clock = pygame.time.Clock()            

screen_width = 1800
screen_height = 1200
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("monster attack")
            
player = Player(screen_width/2, screen_height/2)
BG = pygame.image.load('bg.png').convert_alpha()
position_BG = BG.get_rect()
position_BG.topleft = (-1100, -1300)



class Zombie(pygame.sprite.Sprite):
    def __init__(self, m0, m1, m2, m3, vie, dommage, vitesse, barre):
        super().__init__()
        self.image = pygame.image.load(m0)
        self.rect = self.image.get_rect()
        self.taille = 10
        self.x = randint(10,1500)
        self.y = randint(10,900)
        self.rect.topleft = [self.x,self.y]
        self.vitesse = vitesse
        self.vie = vie
        self.max_vie = vie
        self.dommage = dommage
        self.barre = barre
        self.deplacement = []
        self.deplacement.append(pygame.image.load(m0))
        self.deplacement.append(pygame.image.load(m1))
        self.deplacement.append(pygame.image.load(m2))
        self.deplacement.append(pygame.image.load(m3))
        self.sprite_actuelle = 0
        self.mouvement = False
        
        
    def mouvements(self):
        self.mouvement = True
     
    def update(self, speed):
        if self.mouvement == True:
            self.sprite_actuelle += speed
            if int(self.sprite_actuelle) >= len(self.deplacement):
                self.sprite_actuelle = 0
                self.mouvement = False
            self.image = self.deplacement[int(self.sprite_actuelle)]
            
        
    def distance_joueur(self, target_x, target_y):
        distance_x = target_x  - self.rect[0] 
        distance_y = target_y  - self.rect[1] 
        distance = (distance_x**2 + distance_y**2)**0.5
        
        if distance <= 40:
            player.vie -= self.dommage
        
        if distance < 900:
            if self.rect[0] < player.rect[0]:
                self.rect[0] += self.vitesse
            if self.rect[0] > player.rect[0]:
                self.rect[0] -= self.vitesse
            if self.rect[1] < player.rect[1]:
                self.rect[1] += self.vitesse
            if self.rect[1] > player.rect[1]:
                self.rect[1] -= self.vitesse
                
    def barre_vie(self):
        couleur_barre_vie = (255, 0, 0)
        couleur_fond_barre = (0, 0, 0)
        
        
        barre_position = [self.rect[0] - self.barre, self.rect[1] - 10, self.vie, 6]
        barre_position_fond = [self.rect[0] - self.barre, self.rect[1] - 10, self.max_vie, 6]
        
        pygame.draw.rect(screen, couleur_fond_barre, barre_position_fond)
        pygame.draw.rect(screen, couleur_barre_vie, barre_position)
        
        
    def distance_balle(self, target_x, target_y):
        distance_x = target_x - self.rect[0]
        distance_y = target_y - self.rect[1]
        distance = (distance_x**2 + distance_y**2)**0.5
        
        if distance <= 70:
            self.vie -= 0.8
                
   
                
    
            
            
  
class Playerbullet:
    def __init__(self, x, y, mouse_x, mouse_y):
        self.x = x
        self.y = y
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
        self.speed = 4
        self.angle = math.atan2(mouse_y - self.y, mouse_x - self.x)
        self.x_vel = math.cos(self.angle) * self.speed
        self.y_vel = math.sin(self.angle) * self.speed
        self.taille = 5
    
    def main(self, screen):
        self.x += self.x_vel
        self.y += self.y_vel
        pygame.draw.circle(screen, (0,0,0),(self.x, self.y), self.taille)
        if self.x > screen_width or self.x < 0:
            self.taille = 0
        
        if self.y > screen_height or self.y < 0:
            self.taille = 0
        
        
        


def loose():
    police = pygame.font.SysFont('John Hubbard',120)
    image_texte = police.render("Game Over", 1, (255,0,50))
    screen.blit(image_texte,(700 ,500))
    pygame.display.flip()



player_bullets = []

zombie = pygame.sprite.Group()
for i in range(1):
    monstre = Zombie('0.png', '1.png', '2.png', '3.png', 50, 0.5, 1, -10)
    zombie.add(monstre)

def vague(n):
    for i in range(n):
        monstre = Zombie('0.png', '1.png', '2.png', '3.png', 50, 0.5, 1, -10)
        zombie.add(monstre)            

def main_jeux():
    n = 2
    cooldown = 400
    last_shot = 0
    apparition = True
    apparition_2 = True
    while True:
        
        screen.fill('blue')
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        
        
        if (player.rect.left - 250) < position_BG.left:
            player.vie -= 0.3
            
        if (player.rect.right + 450) > position_BG.right:
            player.vie -= 0.3
            
        if (player.rect.top - 20) < position_BG.top:
            player.vie -= 0.3
    
        if (player.rect.bottom + 400) > position_BG.bottom:
            player.vie -= 0.3
            
        
        if len(zombie) == 0:
            vague(n)
            n += 1
            
        if n == 11  and apparition == True:
            pere = Zombie('00.png', '11.png', '22.png', '33.png', 150, 1, 2, -10)
            zombie.add(pere)
            apparition = False
            
            
        if n == 21 and apparition_2 == True:
            vert = Zombie('g1.png', 'g2.png', 'g3.png', 'g4.png', 250, 1.5, 4, 70)
            zombie.add(vert)
            apparition_2 = False
            
            

       
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and pygame.time.get_ticks() - last_shot > cooldown:
                    player_bullets.append(Playerbullet(player.rect[0], player.rect[1] + 10, mouse_x, mouse_y))
                    last_shot = pygame.time.get_ticks()
                    
                    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    player.mouvement_droite()
                    position_BG[0] -= 25
                    for bullet in  player_bullets:
                        bullet.x -= 25
                    for esprit in zombie:
                        esprit.rect[0] -= 25
                if event.key == pygame.K_z:
                    position_BG[1] += 25
                    for bullet in  player_bullets:
                        bullet.y += 25
                    for esprit in zombie:
                        esprit.rect[1] += 25
                    player.mouvement_haut()
                if event.key == pygame.K_s:
                    for bullet in  player_bullets:
                        bullet.y -= 25
                    for esprit in zombie:
                        esprit.rect[1] -= 25
                    position_BG[1] -= 25
                    player.mouvement_bas()
                if event.key == pygame.K_q:
                    player.mouvement_gauche()
                    position_BG[0] += 25
                    for bullet in  player_bullets:
                        bullet.x += 25
                    for esprit in zombie:
                        esprit.rect[0] += 25
                  
            if event.type == pygame.QUIT:
                sys.exit()
                pygame.quit()


        screen.blit(BG, position_BG)
        zombie.draw(screen)
        zombie.update(0.25)
        for esprit in zombie:
            esprit.mouvements()
            esprit.distance_joueur(player.rect[0], player.rect[1])
            esprit.barre_vie()
            if esprit.vie <=0:
               esprit.kill()
            for bullet in player_bullets:
                esprit.distance_balle(bullet.x, bullet.y)
         
            
        for bullet in player_bullets:
            bullet.main(screen)
        
        
        if player.vie <= 0:
            loose()
            time.sleep(3)
            sys.exit()
            pygame.quit()
             
       
            
            
          
            
        player.barre_vie()
        player.draw()
        player.update(0.25)
        
        pygame.display.flip()
        clock.tick(60)
                
                
main_jeux()



