# On importe ici les modules nécessaire pour faire fonctionner le jeu
import pygame, sys
from pygame.locals import *
from random import randint
import math
import time

# On prépare ensuite tout ce qui sera utile afin de lancer le jeu comme la taille de la fenêtre,
# la carte sur laquelle on joue ...
pygame.display.set_caption("Monster Attack")
pygame.init()
pygame.key.set_repeat(30)

horloge = pygame.time.Clock()            

LARGEUR = 1600
HAUTEUR = 1000

fenetre = pygame.display.set_mode((LARGEUR,HAUTEUR))

carte = pygame.image.load('map.png').convert_alpha()
position_carte = carte.get_rect()
position_carte.topleft = (-1150, -600)

def aide():
    while True:
        fenetre.fill('black')
        police_bouton = pygame.font.SysFont('arial', 50)
        bouton_retour = pygame.Rect(LARGEUR//2 - 250, 3.25 * (HAUTEUR//5), 500, 175)
        texte_retour = police_bouton.render("retour", True, (255,255,255))
        pygame.draw.rect(fenetre, (128, 128, 128), bouton_retour)
        fenetre.blit(texte_retour, (bouton_retour.x + 200, bouton_retour.y + 60))
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                 sys.exit()
                 pygame.quit()
               
            if evenement.type == pygame.MOUSEBUTTONDOWN:
                if bouton_retour.collidepoint(evenement.pos):
                    menu()
                    
                    
        police = pygame.font.SysFont('Arial',60)
        image_texte = police.render("touche", 1, (255,255,255))
        fenetre.blit(image_texte,(750, 10))
        police_2 = pygame.font.SysFont('Arial',50)
        image_avancer = police_2.render("avancer: z", 1, (255,255,255))
        fenetre.blit(image_avancer,(10, 80))
        image_reculer = police_2.render("reculer: s", 1, (255,255,255))
        fenetre.blit(image_reculer,(10, 140))
        
                    
        
        
    
        pygame.display.flip()
    

def menu():
    '''
    Il s'agit du code permettant d'ouvrir le menu post-jeu
    '''
    # On prépare ensuite tout ce qu'il faut pour un menu de jeu :    
    # Définition des boutons (Position : Largeur, Hauteur / Dimensions :épaisseur, hauteur)
    bouton_jouer = pygame.Rect(LARGEUR//2 - 250, 1.25 * (HAUTEUR//5), 500, 175)
    bouton_aide = pygame.Rect(LARGEUR//2 - 250, 2.25 * (HAUTEUR//5), 500, 175)
    bouton_quitter = pygame.Rect(LARGEUR//2 - 250, 3.25 * (HAUTEUR//5), 500, 175)

    # Définition de la police
    police_bouton = pygame.font.SysFont('arial', 30)
    police_titre = pygame.font.SysFont('arial', 95, 50)

    # Définition des couleurs
    BLANC = (255, 255, 255)
    NOIR = (0, 0, 0)
    GRIS = (128, 128, 128)
    SANG = (191, 21, 21)
    
    continuer = True
    monstre_img = pygame.image.load('monstre.img.jpg').convert_alpha()
    position_monstre_img = monstre_img.get_rect()
    position_monstre_img.topleft = (0, 0)
    while continuer:
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                continuer = False

            # On regarde si on appuie sur le bouton
            if evenement.type == pygame.MOUSEBUTTONDOWN:
                if bouton_jouer.collidepoint(evenement.pos):
                    print("Lancement du jeu")
                    jeux()
                elif bouton_aide.collidepoint(evenement.pos):
                    print("Affichage de l'aide")
                    aide()
                elif bouton_quitter.collidepoint(evenement.pos):
                    continuer = False
                    sys.exit()
                    pygame.quit()
                    
        fenetre.blit(monstre_img, position_monstre_img)

        # On dessine les boutons
        pygame.draw.rect(fenetre, GRIS, bouton_jouer) 
        pygame.draw.rect(fenetre, GRIS, bouton_aide)
        pygame.draw.rect(fenetre, GRIS, bouton_quitter)

        # Ce que l'on va écrire sur le menu
        titre_menu = police_titre.render("MONSTER ATTACK ", True, SANG)
        texte_jouer = police_bouton.render("Jouer", True, NOIR)
        texte_aide = police_bouton.render("Aide", True, NOIR)
        texte_quitter = police_bouton.render("Quitter", True, NOIR)

        fenetre.blit(titre_menu, ((LARGEUR//2) - 350, 50))
        fenetre.blit(texte_jouer, (bouton_jouer.x + 225, bouton_jouer.y + 25))
        fenetre.blit(texte_aide, (bouton_aide.x + 225, bouton_aide.y + 25))
        fenetre.blit(texte_quitter, (bouton_quitter.x + 225, bouton_quitter.y + 25))

        # Actualisation de l'écran
        pygame.display.flip()

    pygame.quit()
    
def jeux():
    '''
    Il s'agit du code permettant de faire fonctionner le jeu
    '''
    # On créer la classe de notre personnage
    class Player:
        def __init__(self, position_x, position_y):
            self.deplacement_gauche = False
            self.deplacement_droite = False
            self.deplacement_bas = False
            self.deplacement_haut = False
            
            # On initialise la position du joueur
            self.x = position_x
            self.y = position_y
            
            # On initialise d'autres variables telles que les points de vie
            # ou encore la position par rapport à la carte
            self.image = pygame.image.load('Sprites_NSI/personnage.png')
            self.rect = self.image.get_rect()
            self.rect.topleft = [self.x,self.y]
            self.vie = 50
            self.max_vie = 50
            
            # On créer ensuite des listes qui contiendront unes à unes les sprites,
            # permettant de donner l'illusion d'un mouvement "fluide"
            self.sprites_haut = []
            self.sprites_haut.append(pygame.image.load('Sprites_NSI/perso_haut_0.png'))
            self.sprites_haut.append(pygame.image.load('Sprites_NSI/perso_haut_1.png'))
            self.sprites_haut.append(pygame.image.load('Sprites_NSI/perso_haut_2.png'))
            self.sprites_haut.append(pygame.image.load('Sprites_NSI/perso_haut_3.png'))
            self.sprites_bas = []
            self.sprites_bas.append(pygame.image.load('Sprites_NSI/perso_bas_0.png'))
            self.sprites_bas.append(pygame.image.load('Sprites_NSI/perso_bas_1.png'))
            self.sprites_bas.append(pygame.image.load('Sprites_NSI/perso_bas_2.png'))
            self.sprites_bas.append(pygame.image.load('Sprites_NSI/perso_bas_3.png'))
            self.sprites_droite = []
            self.sprites_droite.append(pygame.image.load('Sprites_NSI/perso_droite_0.png'))
            self.sprites_droite.append(pygame.image.load('Sprites_NSI/perso_droite_1.png'))
            self.sprites_droite.append(pygame.image.load('Sprites_NSI/perso_droite_2.png'))
            self.sprites_droite.append(pygame.image.load('Sprites_NSI/perso_droite_3.png'))
            self.sprites_gauche = []
            self.sprites_gauche.append(pygame.image.load('Sprites_NSI/perso_gauche_0.png'))
            self.sprites_gauche.append(pygame.image.load('Sprites_NSI/perso_gauche_1.png'))
            self.sprites_gauche.append(pygame.image.load('Sprites_NSI/perso_gauche_2.png'))
            self.sprites_gauche.append(pygame.image.load('Sprites_NSI/perso_gauche_3.png'))
            self.sprite_actuel = 0
            
        
        # On créer des méthodes afin d'autoriser ou d'interdire
        # le déplacement du joueur
        def mouvement_haut(self):
            self.deplacement_haut = True

            
        def mouvement_bas(self):
            self.deplacement_bas = True

            
        def mouvement_droite(self):
            self.deplacement_droite = True

            
        def mouvement_gauche(self):
            self.deplacement_gauche = True
        
        def draw(self):
            fenetre.blit(self.image, self.rect)
                
        # Cette méthode sert à afficher la barre de vie du joueur en temps réel
        # ainsi qu'à la modifier si nécessaire (changement de couleur, baisse de points de vie...)
        def barre_vie(self):
            couleur_barre_vie = (111, 210, 46)
            couleur_fond_barre = (0, 0, 0)
            if self.vie <= 25 and self.vie > 10:
                couleur_barre_vie = (252, 126, 0)
            elif self.vie <= 10:
                couleur_barre_vie = (255, 0, 0)
            
            # Ici on positionne la barre de vie au-dessus de la tête du joueur
            barre_position = [self.rect[0] + 10, self.rect[1] - 10, self.vie, 6]
            barre_position_fond = [self.rect[0] + 10, self.rect[1] - 10, self.max_vie, 6]
            
            pygame.draw.rect(fenetre, couleur_fond_barre, barre_position_fond)
            pygame.draw.rect(fenetre, couleur_barre_vie, barre_position)
        
        # Cette méthode sert à actualiser les enchainements de sprites lors des déplacements
        def update(self, vitesse):
            if self.deplacement_haut == True:
                self.sprite_actuel += vitesse
                if int(self.sprite_actuel) >= len(self.sprites_haut):
                    self.sprite_actuel = 0
                    self.deplacement_haut = False
                self.image = self.sprites_haut[int(self.sprite_actuel)]
                
            if self.deplacement_bas == True:
                self.sprite_actuel += vitesse
                if int(self.sprite_actuel) >= len(self.sprites_bas):
                    self.sprite_actuel = 0
                    self.deplacement_bas = False
                self.image = self.sprites_bas[int(self.sprite_actuel)]
                
                
            if self.deplacement_gauche == True:
                self.sprite_actuel += vitesse
                if int(self.sprite_actuel) >= len(self.sprites_gauche):
                    self.sprite_actuel = 0
                    self.deplacement_gauche = False
                self.image = self.sprites_gauche[int(self.sprite_actuel)]
                
                
            if self.deplacement_droite == True:
                self.sprite_actuel += vitesse
                if int(self.sprite_actuel) >= len(self.sprites_droite):
                    self.sprite_actuel = 0
                    self.deplacement_droite = False
                self.image = self.sprites_droite[int(self.sprite_actuel)]
                
                

    # Ici il s'agit de la classe visant à créer les enemies que nous affronterons
    class Monstre(pygame.sprite.Sprite):
        def __init__(self, sprite_1, sprite_2, sprite_3, sprite_4, vie, dommage, vitesse, barre):
            # super().__init__() est fait pour manipuler plus aisément les sprites (supprimer, ajouter ...)
            super().__init__()
            # On initalise les valeurs de bases telles que la taille, le lieu d'apparition (aléatoire dans une fenêtre donnée),
            # la vitesse, les points de vie mais aussi les dommages qu'ils pourront infliger au joueur
            self.image = pygame.image.load(sprite_1)
            self.rect = self.image.get_rect()
            self.taille = 10
            self.x = randint(0,LARGEUR//2)
            self.y = randint(0,HAUTEUR//2)
            self.rect.topleft = [self.x,self.y]
            self.vitesse = vitesse
            self.vie = vie
            self.max_vie = vie
            self.dommage = dommage
            self.barre = barre
            
            # On charge les 4 images (sprites) qui ferons le déplacement de nos enemies 
            self.deplacement = []
            self.deplacement.append(pygame.image.load(sprite_1))
            self.deplacement.append(pygame.image.load(sprite_2))
            self.deplacement.append(pygame.image.load(sprite_3))
            self.deplacement.append(pygame.image.load(sprite_4))
            self.sprite_actuelle = 0
            self.mouvement = False
            
        def mouvements(self):
            self.mouvement = True
        
        # On actualise afin de changer le sprite et donc de donner cette illusion de mouvement
        def update(self, vitesse):
            if self.mouvement == True:
                self.sprite_actuelle += vitesse
                if int(self.sprite_actuelle) >= len(self.deplacement):
                    self.sprite_actuelle = 0
                    self.mouvement = False
                self.image = self.deplacement[int(self.sprite_actuelle)]
        
        # Dans cette méthode, nous calculons la distance entre les monstres et le joueur
        def distance_joueur(self, cible_x, cible_y):
            distance_x = cible_x  - self.rect[0] 
            distance_y = cible_y  - self.rect[1] 
            distance = (distance_x**2 + distance_y**2)**0.5
            
            # Si le joueur est trop proche du monstre, alors il reçoit des dégâts
            if distance <= 40:
                player.vie -= self.dommage
            
            # Cette condition fait en sorte que si le monstre voit le joueur, alors celui-ci est
            # 'attiré', il se déplace vers le joueur
            if distance < 2000:
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
            
            # On place leur barre de vie au-dessus d'eux  
            barre_position = [self.rect[0] - self.barre, self.rect[1] - 10, self.vie, 6]
            barre_position_fond = [self.rect[0] - self.barre, self.rect[1] - 10, self.max_vie, 6]
            
            pygame.draw.rect(fenetre, couleur_fond_barre, barre_position_fond)
            pygame.draw.rect(fenetre, couleur_barre_vie, barre_position)
        
        # Cette méthode elle, calcule la distance entre le monstre et le projectile envoyé par le joueur
        def distance_balle(self, cible_x, cible_y):
            distance_x = cible_x - self.rect[0]
            distance_y = cible_y - self.rect[1]
            distance = (distance_x**2 + distance_y**2)**0.5
            
            # Si ils sont en contact, alors le monstres perd de la vie
            if distance <= 50:
                self.vie -= 2
                
                
    # On créer une autre classe pour les projectiles que le joueur utilise pour se défendre           
    class Playerbullet:
        def __init__(self, x, y, souris_x, souris_y):
            self.x = x
            self.y = y
            # On vise l'enemie avec la souris de bureau, et on calcule l'angle pour que le projectile
            # parte vers le lieux appuyer
            self.souris_x = souris_x
            self.souris_y = souris_y
            self.vitesse = 10
            self.angle = math.atan2(souris_y - self.y, souris_x - self.x)
            # On s'occupe de la vitesse de déplacement des projectiles
            self.x_vel = math.cos(self.angle) * self.vitesse
            self.y_vel = math.sin(self.angle) * self.vitesse
            self.taille = 5
        
        # Cette méthode gère le déplacement linéaire du projectile
        def main(self, fenetre):
            self.x += self.x_vel
            self.y += self.y_vel
            pygame.draw.circle(fenetre, (0,0,0),(self.x, self.y), self.taille)
            
            # Si le projectile sors de la surface visible il est supprimé
            if self.x > LARGEUR or self.x < 0:
                self.taille = 0
            if self.y > HAUTEUR or self.y < 0:
                self.taille = 0
            
            

    # La fonction défaite qui permet, d'afficher le 'Game Over' et le retour au menu
    def defaite():
        police = pygame.font.SysFont('John Hubbard',120)
        image_texte = police.render("Game Over", 1, (255,0,50))
        fenetre.blit(image_texte,(LARGEUR/2, HAUTEUR/2))
        pygame.display.flip()
    
    # Une fonction pour le score du joueur   
    def score(n):
        font = pygame.font.SysFont("Pixelade", 55)
        text = font.render("Score: " + str(n), True, "white")
        fenetre.blit(text, (20, 20))

    # On créer notre personnage, une liste contenant les projectiles ainsi qu'un groupe de sprite qui
    # contiendra tous nos enemies
    player = Player(LARGEUR/2, 800)
    player_bullets = []
    lst_monstres = pygame.sprite.Group()

    # On place notre premier enemie à éliminer dans la liste pour le faire apparaître dans le jeu
    lst_monstres.add(Monstre('Sprites_NSI/monstre_0.png', 'Sprites_NSI/monstre_1.png', 'Sprites_NSI/monstre_2.png', 'Sprites_NSI/monstre_3.png', 50, 0.5, 3, -10))

    # On a ici un système de 'vague' c'est-à-dire que les monstres arriveront de plus en plus nombreux
    def vague(nombre_enemie):
        for i in range(nombre_enemie):
            lst_monstres.add(Monstre('Sprites_NSI/monstre_0.png', 'Sprites_NSI/monstre_1.png', 'Sprites_NSI/monstre_2.png', 'Sprites_NSI/monstre_3.png', 50, 0.5, 3, -10))            

    # Queleques variables que l'on pourra modifier pour faire évoluer le jeu
    nombre_enemie = 2
    attente = 400
    dernier_tir = 0
    # Pour afficher le nombres d'enemies tués
    nb_mort = 0
    # Afin de faire apparaître les boss à un moment précis
    entree_boss = 0
    while True:
        fenetre.fill('blue')
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        if len(lst_monstres) == 0:
            entree_boss += 1
        
        # Si le joueur s'aventure trop loin (dans les eaux profondes) alors il perdra des points de vie 
        if (player.rect.left - 250) < position_carte.left:
            player.vie -= 0.3
        if (player.rect.right + 450) > position_carte.right:
            player.vie -= 0.3  
        if (player.rect.top - 20) < position_carte.top:
            player.vie -= 0.3
        if (player.rect.bottom + 400) > position_carte.bottom:
            player.vie -= 0.3

        # De même pour les enemies   
        for monstre in lst_monstres:
            if (monstre.rect.left - 250) < position_carte.left:
                monstre.vie -= 0.3
            if (monstre.rect.right + 450) > position_carte.right:
                monstre.vie -= 0.3  
            if (monstre.rect.top - 20) < position_carte.top:
                monstre.vie -= 0.3
            if (monstre.rect.bottom + 400) > position_carte.bottom:
                monstre.vie -= 0.3
        
            
        # Nous avons un système de 'Mini-Boss', ils apparaitront à partir d'un certain palier (un certains nombre de vagues survécues)
        if len(lst_monstres) == 0 and entree_boss == 4:
            lst_monstres.add(Monstre('Sprites_NSI/boss_1_0.png', 'Sprites_NSI/boss_1_1.png', 'Sprites_NSI/boss_1_2.png', 'Sprites_NSI/boss_1_3.png', 150, 1.5, 6, -10))
        if len(lst_monstres) == 0 and entree_boss == 6:
            lst_monstres.add(Monstre('Sprites_NSI/boss_2_0.png', 'Sprites_NSI/boss_2_1.png', 'Sprites_NSI/boss_2_2.png', 'Sprites_NSI/boss_2_3.png', 250, 2, 13, 70))
        # Si tous les monstres sur la carte sont morts, alors de nouveaux apparaissent, plus nombreux
        if len(lst_monstres) == 0:
            vague(nombre_enemie)
            nombre_enemie += 1 
        # Cette partie gère les interractions clavier/souris, c'est-à-dire que le joueur et déplaçable et peut 'tirer'
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and pygame.time.get_ticks() - dernier_tir > attente:
                    player_bullets.append(Playerbullet(player.rect[0], player.rect[1] + 10, mouse_x, mouse_y))
                    dernier_tir = pygame.time.get_ticks()
                    
            
            # Ici on s'occupe des déplacements, en effet on a l'illusion que c'est la carte qui se déplace
            # ces conditions font en sorte que lorsque la carte bouge elle n'emporte pas tout,
            # c'est-à-dire que seule la carte est impactée, les autres objets (monstres) ne le sont pas
            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_d:
                    player.mouvement_droite()
                    position_carte[0] -= 25
                    for bullet in  player_bullets:
                        bullet.x -= 25
                    for esprit in lst_monstres:
                        esprit.rect[0] -= 25
                        
                if event.key == pygame.K_z:
                    position_carte[1] += 25
                    for bullet in  player_bullets:
                        bullet.y += 25
                    for esprit in lst_monstres:
                        esprit.rect[1] += 25    
                    player.mouvement_haut()
                    
                if event.key == pygame.K_s:
                    for bullet in  player_bullets:
                        bullet.y -= 25
                    for esprit in lst_monstres:
                        esprit.rect[1] -= 25
                    position_carte[1] -= 25
                    player.mouvement_bas()
                    
                if event.key == pygame.K_q:
                    player.mouvement_gauche()
                    position_carte[0] += 25
                    for bullet in  player_bullets:
                        bullet.x += 25
                    for esprit in lst_monstres:
                        esprit.rect[0] += 25
            
            # Fermer le jeu proprement
            if event.type == pygame.QUIT:
                sys.exit()
                pygame.quit()

        # Ici on fait appraître les monstres et les projectiles, on fait ensuite appelle à leurs méthodes
        # pour qu'ils fonctionnent correctement
        fenetre.blit(carte, position_carte)
        lst_monstres.draw(fenetre)
        lst_monstres.update(0.25)
        
        # On fait appraître les monstres/boss et leurs attributs
        for esprit in lst_monstres:
            esprit.mouvements()
            esprit.distance_joueur(player.rect[0], player.rect[1])
            esprit.barre_vie()
            # Lorsque l'enemie n'a plus de vie, il disparaît
            if esprit.vie <= 0:
                esprit.kill()
                nb_mort += 1
            
            for bullet in player_bullets:
                esprit.distance_balle(bullet.x, bullet.y)
        
        for bullet in player_bullets:
            bullet.main(fenetre)
            
        # Lorsque le joueur n'a plus de points de vie, c'est perdu ! Il faut réessayer
        if player.vie <= 0:
            score(nb_mort)
            defaite()
            time.sleep(2)
            menu()
        
        # Notre personnage et ses attributs
        player.barre_vie()
        player.draw()
        player.update(0.25)
        score(nb_mort)
        
        # Pour gérer les FPS
        pygame.display.flip()
        horloge.tick(60)
                
                
menu()



