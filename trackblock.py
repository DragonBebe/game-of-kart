import pygame
from abc import ABC, abstractmethod
BLOCK_SIZE = 50 # Définition de la taille standard d'un bloc de piste
class TrackBlock(ABC):
    # Constructeur de la classe abstraite TrackBlock.
    def __init__(self, x, y, color):
        # Création d'un rectangle pour représenter la position et la taille du bloc de piste.
        # La taille du bloc est définie par BLOCK_SIZE.
        self.__rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
        # Stockage de la couleur du bloc.
        self.__color = color
    @abstractmethod
    # Méthode abstraite pour dessiner le bloc sur l'écran.
    def draw(self, screen):
        # Utilisation de pygame.draw.rect pour dessiner le bloc.
        # Cette méthode est abstraite et doit être redéfinie dans les sous-classes.
        pygame.draw.rect(screen, self.__color, self.__rect)
