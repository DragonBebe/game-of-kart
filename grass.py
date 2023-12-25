from trackblock import TrackBlock
class Grass(TrackBlock):
    # Constructeur pour la classe Grass.
    def __init__(self, x, y):
        # Appel du constructeur de la classe parent avec des paramètres spécifiques.
        # La couleur (0, 255, 0) correspond à la couleur verte pour l'herbe.
        super().__init__(x, y, (0, 255, 0))

    # Méthode pour dessiner le bloc d'herbe à l'écran.
    def draw(self, screen):
        # Appel de la méthode draw de la classe parent pour effectuer le dessin.
        super().draw(screen)