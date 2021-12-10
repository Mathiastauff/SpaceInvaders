import pygame
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
)
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700

class Joueur(pygame.sprite.Sprite) : 
    def __init__(self) -> None:
        super(Joueur, self).__init__()#permet d'initialiser la classe parente. Equivalent à super().__init__(self)
        self._vie = 3
        self.surf = pygame.image.load("joueur.jpg").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(center=(350,600))

    def isAlive(self) :
        return self._vie > 0

    def update(self, pressed_keys):#les touches quand ça joue
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        #ne pas sortir de la map
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT