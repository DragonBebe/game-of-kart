import time
import pygame
from player import Player
class Human(Player):
    # Constructeur pour la classe Human.
    def __init__(self):
        # Initialisation de l'attribut kart à None.
        # Cela signifie que par défaut, il n'y a pas de kart associé à cet objet.
        self.kart = None

    # Méthode pour obtenir l'état actuel des touches du clavier.
    def move(self, string):
        # Pause courte pour contrôler la vitesse de traitement des entrées.
        # 0.02 seconde d'attente assure que cette méthode ne s'exécute pas trop rapidement.
        time.sleep(0.02)
        # Retourne l'état de toutes les touches du clavier.
        # pygame.key.get_pressed() renvoie un tableau indiquant l'état de chaque touche.
        return pygame.key.get_pressed()