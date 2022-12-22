import pygame, sys
from pygame.locals import *
from code_temporaire import *
pygame.init()
fenetre = pygame.display.set_mode((1280, 720))






class Bouton():
    def __init__(self, image, pos, text_input, police, couleur_originel):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.police = police
        self.couleur_originel = couleur_originel
        self.text_input = text_input
        self.text = self.police.render(self.text_input, True, self.couleur_originel)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        return position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom)

bg = pygame.image.load("blood.jpg").convert_alpha()


def get_police(size): 
    return pygame.font.Font("police.ttf", size)

def option():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        fenetre.fill("black")

        OPTIONS_TEXT = get_police(45).render("touche : z avancer", True, "white")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(230, 30))
        fenetre.blit(OPTIONS_TEXT, OPTIONS_RECT)
        
        OPTIONS_TEXT_1 = get_police(45).render("s reculer", True, "white")
        OPTIONS_RECT_1 = OPTIONS_TEXT_1.get_rect(center=(340, 80))
        fenetre.blit(OPTIONS_TEXT_1, OPTIONS_RECT_1)
        
        OPTIONS_TEXT_2 = get_police(45).render("q gauche", True, "white")
        OPTIONS_RECT_2 = OPTIONS_TEXT_2.get_rect(center=(330, 130))
        fenetre.blit(OPTIONS_TEXT_2, OPTIONS_RECT_2)
        
        OPTIONS_TEXT_3 = get_police(45).render("d droite", True, "white")
        OPTIONS_RECT_3 = OPTIONS_TEXT_3.get_rect(center=(330, 180))
        fenetre.blit(OPTIONS_TEXT_3, OPTIONS_RECT_3)
        
        OPTIONS_TEXT_4 = get_police(45).render("clic_gauche tirer ", True, "white")
        OPTIONS_RECT_4 = OPTIONS_TEXT_4.get_rect(center=(450, 230))
        fenetre.blit(OPTIONS_TEXT_4, OPTIONS_RECT_4)
        
        

        OPTIONS_BACK = Bouton(None, (550, 460), "BACK", get_police(75), "white")
        OPTIONS_BACK.update(fenetre)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                     menu()

        pygame.display.flip()


def menu():
    while True:
        fenetre.blit(bg, (-100,0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        
        
        MENU_TEXT = get_police(100).render("MENU", True, "#ffffff")
        MENU_RECT = MENU_TEXT.get_rect(center=(600, 80))
        
        start_bouton = Bouton(pygame.image.load("Play Rect.png"), (600, 250), "PLAY", get_police(75), "#000000")
        option_bouton = Bouton(pygame.image.load("Options Rect.png"), (600, 400), "OPTIONS", get_police(75), "#000000")
        leave_bouton = Bouton(pygame.image.load("Quit Rect.png"), (600, 550),"QUIT", get_police(75), "#000000")
        
        
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                if start_bouton.checkForInput(MENU_MOUSE_POS):
                   main_jeux()
                   
                    
                if option_bouton.checkForInput(MENU_MOUSE_POS):
                    option()
                    
                if leave_bouton.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
                    
        
        
        for button in [start_bouton, option_bouton, leave_bouton]:
            button.update(fenetre)
        
        
        fenetre.blit(MENU_TEXT, MENU_RECT)
        pygame.display.flip()
        
        

        
menu()
