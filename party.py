from random import choice
from joueur import Joueur
from ennemi import Ennemi
from pioupiou import PioupiouEnnemi, PioupiouJoueur
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700

def checkPygameInstallation() :
    global pygame
    try : 
        import pygame
    except ImportError :
        print("Erreur le module pygame est requis pour le bon fonctionnement de ce jeu")
        print("Voulez-vous que nous installions automatiquement ce module (Y/n)", end = " ")
        if input("") != "n" :
            print("Installation de pygame en cours...")
            import os
            command = ("python" if os.name == "nt" else "python3") + " -m pip install pygame"
            if not os.system(command) :
                print("Succès ! pygame a bien été installé")
                import pygame
            else : 
                print("Une erreur est survenue veuillez réessayer")
                exit()
        else : exit()
import pygame
pygame.init()
clock = pygame.time.Clock()
clock.tick(30)

class Party :    
    def __init__(self) -> None:
        self.level = 0
        self._joueur = Joueur()
        self._allSprites = pygame.sprite.Group()
        self._allSprites.add(self._joueur)
        self._listEnnemiPioupiou = pygame.sprite.Group()
        self._listJoueurPioupiou = pygame.sprite.Group()
        self.ENNEMIPIOUPIOU = pygame.USEREVENT + 1
        self.screen = pygame.display.set_mode([700, 700])
        
    def playRound(self) :
        #init et création des ennemis
        self._listEnnemis = pygame.sprite.Group()
        for y in range(4) :
            for x in range(6) :
                self._listEnnemis.add(Ennemi(40 + self.level * 5, (100 + 100 * x, 100 + y * 100)))
        self.update()
        pygame.time.set_timer(self.ENNEMIPIOUPIOU, 5000)

        ennemiMoveCounter = 0                        #compteur utilisé pour faire bouger 5 fois les ennemis vers la droite de 10 pixels, puis la même chose vers la gauche et ainsi de suite
        running = True
        while running :
            for event in pygame.event.get():
                if event.type == pygame.QUIT:             #-> l'utilisateur a demandé à fermer la fenêtre
                    running = False

                if event.type == self.ENNEMIPIOUPIOU :
                    choice(self._listEnnemis.sprites()).emitPioupiou()

            pressed_keys = pygame.key.get_pressed()
            self._joueur.update(pressed_keys)

            pariteEnnemiMove = (ennemiMoveCounter//5) % 2
            self._listEnnemis.update("right" if pariteEnnemiMove == 0 else "left")

            #gestion des colisions
            if pygame.sprite.spritecollideany(self._joueur, self._listEnnemiPioupiou) :
                self._joueur.vie -= 1
                running = False
            ennemiCollideDict = pygame.sprite.spritecollide(self._listJoueurPioupiou, self._listEnnemis, False, False)
            if ennemiCollideDict :
                for paire in ennemiCollideDict.items() :
                    paire[0].kill()
                    paire[1].kill()
                    del paire[0], paire[1]
                if len(self._listEnnemis.sprites()) == 0 :
                    self.level += 1
                    running = False

            Party.screen.fill((0, 0, 0))
            self.update()
        
        self._listEnnemis.empty()
        return True if self._joueur.isAlive() else False
        
    def update(self) :
        #actualisation de l'affichage graphique
        for sprite in self._allSprites :
                Party.screen.blit(sprite.surf, sprite.rect)
        pygame.display.flip()


    def terminate(self) :
        pygame.quit()